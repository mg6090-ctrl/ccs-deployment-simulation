import networkx as nx
import random
import hashlib
import numpy as np

#==================================================================
# CONSTANTS (INPUT DATA AND PARAMETERS)
#==================================================================

# stages of projects
STAGES = ["definition", "approval", "construction"]
STAGES4 = ["definition", "approval", "construction", "commissioning"]

# dictionary for capture projects
CAPTURE = {
    "projC1":  {"definition": 12, "approval": 24, "construction": 48},
    "projC2":  {"definition": 30, "approval": 48, "construction": 60},
    "projC3":  {"definition": 24, "approval": 24, "construction": 36},
    "projC4":  {"definition": 50, "approval": 40, "construction": 80},
    "projC5":  {"definition": 46, "approval": 34, "construction": 62},
    "projC6":  {"definition": 10, "approval": 18, "construction": 30},
    "projC7":  {"definition": 20, "approval": 30, "construction": 44},
    "projC8":  {"definition": 36, "approval": 30, "construction": 54},
    "projC9":  {"definition": 14, "approval": 20, "construction": 34},
    "projC10": {"definition": 60, "approval": 44, "construction": 90},
    "projC11": {"definition": 28, "approval": 36, "construction": 50},
    "projC12": {"definition": 18, "approval": 22, "construction": 40},
}

# capture volumes
CAPTURE_VOLUMES = {
    "projC1": 300, "projC2": 300, "projC3": 250,    # projS1 cluster — clears (oversubscribes T1)
    "projC4": 120, "projC5": 110, "projC6": 80, "projC7": 80,   # projS2 — T3 fails, S2 fails (cascade)
    "projC8": 400, "projC9": 200, "projC10": 250,   # projS3 cluster — clears
    "projC11": 45, "projC12": 50,                    # projS4 — starved, fails
}

# dictionary for storage projects
STORAGE = {
    "projS1":  {"definition": 48, "approval": 36, "construction": 72},  
    "projS2":  {"definition": 30, "approval": 50, "construction": 64},  
    "projS3":  {"definition": 48, "approval": 24, "construction": 60},   
    "projS4":  {"definition": 14, "approval": 20, "construction": 40},   
}

# capture volumes
STORAGE_VOLUMES = {
    "projS1": 1000, "projS2": 2500, "projS3": 1500, "projS4": 3000,
}

# dictionary for transport projects
TRANSPORT = {
    "projT1":  {"definition": 24, "approval": 12, "construction": 72},  
    "projT2":  {"definition": 32, "approval": 18, "construction": 64},  
    "projT3":  {"definition": 46, "approval": 25, "construction": 60},   
    "projT4":  {"definition": 18, "approval": 18, "construction": 40},   
    "projT5":  {"definition": 12, "approval": 42, "construction": 60},   
    "projT6":  {"definition": 64, "approval": 36, "construction": 110}, 
    "projT7":  {"definition": 48, "approval": 24, "construction": 56},   
}

# transport volumes
TRANSPORT_VOLUMES = {
    "projT1": 500, "projT2": 400, "projT3": 550, "projT4": 200,
    "projT5": 600, "projT6": 600, "projT7": 250,
}

# NOTE: THE CLUSTER LOGIC HAS CHANGED HERE! NEED TO ENSURE THE FUTURE CODE ALIGNS WITH THE NEW 
# DATA STRUCTURE HERE!
CLUSTERS = {
    "projS1":  {
        "projT1": ["projC1", "projC2"], 
        "projT2": ["projC3"]
        },    
    "projS2":  {
        "projT3": ["projC4", "projC5"], 
        "projT4": ["projC6", "projC7"],
    },   
    "projS3":  {
        "projT5": ["projC8"],
        "projT6": ["projC9", "projC10"]
    },    
    "projS4":  {
        "projT7":  ["projC11", "projC12"]
    }
}

# fraction split
FRAC_SPLIT = (0.2, 0.8)

# seed for shuffling before frac_split
SEED = 42

# attrition
BASE_RATE = 0.05

#==================================================================
# STOCHASTIC DURATION SAMPLING
#==================================================================

DURATION_SAMPLING = {
    "dist": "lognormal",    # "lognormal" | "normal" | "uniform"
    "cv": 0.20,             # coefficient of variation: std = cv * mean (spread knob)
    "min_months": 1,        # floor after sampling
}

def stable_seed(project, stage, replication_seed=0):
    '''
    Deterministic per-(project, stage) seed via blake2b (Python's hash() is
    randomized per process, so we can't use it for reproducibility).
    Mixing in replication_seed lets a multi-run sweep get different draws.
    '''
    key = f"{project}|{stage}|{replication_seed}" # we use the | dividers to separate out components cleanly
    digest = hashlib.blake2b(key.encode(), digest_size=8).digest() 
    return int.from_bytes(digest, "big") # interpets 8 bytes as an integer; "big" means read bytes from most significant digit

def sample_duration(mean, project, stage, replication_seed=0, sampling = False):
    '''
    Sample one stage duration, centered on `mean` (the fixed duration).
    Returns a positive integer (months).
    '''
    # fixed guard — this allows us to fall back to default durations when we are not sampling
    if not sampling or mean <= 0:
        return mean

    # create the random number generator -> hash gives seed number, which seeds a random number generator
    rng = np.random.default_rng(stable_seed(project, stage, replication_seed)) 
    cv = DURATION_SAMPLING["cv"]
    std = cv * mean
    dist = DURATION_SAMPLING["dist"]
    
    # conversions for the different distributions
    if dist == "normal":
        sample = rng.normal(mean, std)
    elif dist == "lognormal":
        # convert desired mean/std into lognormal's underlying mu/sigma
        sigma = np.sqrt(np.log(1 + (std / mean) ** 2))
        mu = np.log(mean) - 0.5 * sigma ** 2
        sample = rng.lognormal(mu, sigma)
    elif dist == "uniform":
        sample = rng.uniform(mean - std, mean + std)
    else:
        raise ValueError(f"unknown dist {dist}")

    # cleans up — ensures an integer number of months above minimum is returned
    return int(max(DURATION_SAMPLING["min_months"], round(sample)))

#==================================================================
# BUILDING THE BASE GRAPH (NO INTERDEPENDENCIES)
#==================================================================

def make_base_graph(replication_seed=0, sampling=False):
    '''
    Description: builds intra-project DAG without joint nodes
    Returns: G_indep
    '''
    # helper method for drawing project nodes only (no joint nodes)

    def intra_nodes():
        # make one large graph
        G = nx.DiGraph()

        for storage, transport_clusters in CLUSTERS.items():
            # layer 1: storage nodes
            storage_cluster = storage + " cluster" # naming the overarching storage cluster

            for stage, dur in STORAGE[storage].items():
                G.add_node(
                    (storage, stage),
                    duration = sample_duration(dur, storage, stage, replication_seed, sampling),
                    stage = stage,
                    tech = "storage",
                    ES = 0.0,
                    EF = 0.0,
                    volume = STORAGE_VOLUMES[storage],
                    s_cluster = storage_cluster,
                    t_cluster = None,
                    abandoned = None
                )
            
            # add storage commissioning node
            G.add_node(
                (storage, "commissioning"),
                duration = 0.0,
                stage = "commissioning",
                tech = "storage",
                ES = 0.0,
                EF = 0.0,
                volume = STORAGE_VOLUMES[storage],
                s_cluster = storage_cluster,
                t_cluster = None,
                abandoned = None
            )

            for transport, captures in transport_clusters.items():
                # cluster number is determined by ts project
                transport_cluster =  transport + " cluster"

                # add transport nodes
                for stage, dur in TRANSPORT[transport].items():
                    G.add_node(
                        (transport, stage),
                        duration = sample_duration(dur, transport, stage, replication_seed, sampling),
                        stage = stage,
                        tech = "transport",
                        ES = 0.0,
                        EF = 0.0,
                        volume = TRANSPORT_VOLUMES[transport],
                        t_cluster = transport_cluster,
                        s_cluster = storage_cluster,
                        abandoned = None
                    )

                # add transport commissioning node
                G.add_node(
                    (transport, "commissioning"),
                    duration = 0.0,
                    stage = "commissioning",
                    tech = "transport",
                    ES = 0.0,
                    EF = 0.0,
                    volume = TRANSPORT_VOLUMES[transport],
                    t_cluster = transport_cluster,
                    s_cluster = storage_cluster,
                    abandoned = None
                )

                for capture in captures:
                    # add capture nodes
                    for stage, dur in CAPTURE[capture].items():
                        G.add_node(
                            (capture, stage),
                            duration = sample_duration(dur, capture, stage, replication_seed, sampling),
                            stage = stage,
                            tech = "capture",
                            ES = 0.0,
                            EF = 0.0,
                            volume = CAPTURE_VOLUMES[capture],
                            t_cluster = transport_cluster,
                            s_cluster = storage_cluster,
                            abandoned = None
                        )
            
                    # add capture commissioning node
                    G.add_node(
                        (capture, "commissioning"),
                        duration = 0.0,
                        stage = "commissioning",
                        tech = "capture",
                        ES = 0.0,
                        EF = 0.0,
                        volume = CAPTURE_VOLUMES[capture],
                        t_cluster = transport_cluster,
                        s_cluster = storage_cluster,
                        abandoned = None
                    )

        return G

    # helper method for drawing intra-project edges only
    # this method works for 1:multiple already
    def intra_edges(G: nx.DiGraph):
        def graphEdges(G, pid):
            for a, b in zip(STAGES4[:-1], STAGES4[1:]):
                G.add_edge((pid, a), (pid, b))
        
        for storage, transport_clusters in CLUSTERS.items():
            graphEdges(G, storage)
            for transport, captures in transport_clusters.items():
                graphEdges(G, transport)
                for capture in captures:
                    graphEdges(G, capture)

    # make a NEW graph without interdependent edges to evaluate baseline ES/EF
    G_indep = intra_nodes()
    intra_edges(G_indep)

    return G_indep

#==================================================================
# BUILDING THE DAG WITH INTERDEPENDENCIES
#==================================================================

def fracSplit(captures):
        '''
        Description: helper method that splits capture into two batches based on risk aversion level
        Returns: tuple of ([approval pids], [construction pids])
        '''
        # seeding and introducing randomness
        rng = random.Random(SEED)
        shuffled = list(captures)
        rng.shuffle(shuffled)

        # number of capture projects in approval batch (risk-tolerant)
        approv_num = round(len(shuffled)*FRAC_SPLIT[0])

        # cuts the list of pids in two for the two sets (go ahead at approval and construction)
        return shuffled[:approv_num], shuffled[approv_num:]

def get_storage(G, capture):
    for storage, t_clusters in CLUSTERS.items():
        for transport, captures in t_clusters.items():
            for cap in captures:
                if cap == capture:
                    return storage

def get_transport(G, capture):
    for storage, t_clusters in CLUSTERS.items():
        for transport, captures in t_clusters.items():
            for cap in captures:
                if cap == capture:
                    return transport

def projGraph(replication_seed=0, sampling=False):
    # building the base graph with intra-project edges
    G = make_base_graph(replication_seed, sampling)

    for storage, t_cluster in CLUSTERS.items():
        cluster_captures = [c for caps in t_cluster.values() for c in caps]
        approval, construction = fracSplit(cluster_captures)

        for capture in approval:
            G.add_edge(
                (get_storage(G, capture), "approval"), 
                (capture, "construction")
            )

            G.add_edge(
                (get_transport(G, capture), "approval"),
                (capture, "construction")
            )

        for capture in construction:
            G.add_edge(
                (get_storage(G, capture), "construction"), 
                (capture, "construction")
            )

            G.add_edge(
                (get_transport(G, capture), "construction"),
                (capture, "construction")
            )
    
    # commissioning cascade: storage -> transport -> capture
    for storage, t_cluster in CLUSTERS.items():
        for transport, captures in t_cluster.items():
            G.add_edge((storage, "commissioning"), (transport, "commissioning"))
            for capture in captures:
                G.add_edge((transport, "commissioning"), (capture, "commissioning"))

    return G

#==================================================================
# RUNNING THE CPM
#==================================================================

def CPM(G: nx.DiGraph):
    '''
    Description: runs critical path method (CPM), updating ES and EF 
    Args: G
    '''
    
    for node in nx.topological_sort(G):
        preds = list(G.predecessors(node))

        # the new ES is the max of the EF of the preceeding node(s) and the original ES
        max_preds = max((G.nodes[p]["EF"] for p in preds), default = 0.0)

        updated_ES = max(max_preds, G.nodes[node].get("ES", 0.0))
        
        # update the ES and EF of each node
        G.nodes[node]["ES"] = updated_ES
        G.nodes[node]["EF"] = updated_ES + G.nodes[node]["duration"] 

#==================================================================
# PROJECT ABANDONMENT 
#==================================================================

def mark_capture_abandoned(G: nx.DiGraph, capture, stage):
    G.nodes[(capture, stage)]["abandoned"] = True

def apply_attrition (G: nx.DiGraph, replication_seed = 0):

    # NOTE: here we only roll abandonment for the first two stages so we are consistent with 
    # the base roll for S2
    ROLL_STAGES = ["definition", "approval"]

    # a generator for the whole pass — does not hash per item, just one stream.
    # this is because the order is fixed
    rng = random.Random(SEED + replication_seed)
    abandoned_c = {}
    for storage, t_clusters in CLUSTERS.items():
        for transport, captures in t_clusters.items():
            for capture in captures:
                for stage in ROLL_STAGES:
                    if rng.random() < BASE_RATE:
                        mark_capture_abandoned(G, capture, stage)
                        abandoned_c[capture] = stage
                        break # once a project dies, don't need to roll future stage
    
    return abandoned_c

#==================================================================
# MONTE CARLO
#==================================================================

def monte_carlo(n_reps, sampling = True):
    results = []
    for rep in range(n_reps):
        G = projGraph(replication_seed = rep, sampling = sampling)
        CPM(G)
        abandoned = apply_attrition(G, replication_seed = rep)
        results.append({
                "rep": rep,
                "n_abandoned": len(abandoned),
                "completion": max(G.nodes[n]["EF"] for n in G.nodes)
            }
        )
    return results

def analyze_monte_carlo(results):
    cum_abandoned = 0.0
    cum_time = 0.0

    for rep in results:
        cum_abandoned += rep["n_abandoned"]
        cum_time += rep["completion"]

    avg_abandoned = cum_abandoned/len(results)
    avg_time = cum_time/len(results)

    return ("average no. abandoned: ", avg_abandoned, "average completion time: ", avg_time)

#==================================================================
# MAIN (EXECUTION)
#==================================================================

if __name__ == "__main__":
    results = monte_carlo(300)
    print(analyze_monte_carlo(results))
