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

CAPTURE = {
    "projC1":  {"definition": 12, "approval": 24, "construction": 36},
    "projC2":  {"definition": 12, "approval": 24, "construction": 36},
    "projC3":  {"definition": 12, "approval": 24, "construction": 36},
    "projC4":  {"definition": 12, "approval": 24, "construction": 36},
    "projC5":  {"definition": 6, "approval": 9, "construction": 12},
    "projC6":  {"definition": 6, "approval": 9, "construction": 12},
    "projC7":  {"definition": 6, "approval": 6, "construction": 6},
    "projC8":  {"definition": 6, "approval": 6, "construction": 6},
}

CAPTURE_VOLUMES = {
    "projC1": 1.469847, "projC2": 1.112612, "projC3": 0.823186, "projC4": 0.241809, 
    "projC5": 0.060437, "projC6": 0.114565, 
    "projC7": 1.011104, "projC8": 0.059286                  
}

# dictionary for storage projects
STORAGE = {
    "projS1":  {"definition": 24, "approval": 30, "construction": 24}   
}

# capture volumes
STORAGE_VOLUMES = {
    "projS1": 6
}

# dictionary for transport projects
TRANSPORT = {
    "projT1":  {"definition": 9, "approval": 36, "construction": 30}
}

# transport volumes
TRANSPORT_VOLUMES = {
    "projT1": 6
}

CLUSTERS = {
    "projS1":  {
        "projT1": ["projC1", "projC2", "projC3", "projC4", "projC5", "projC6", "projC7", "projC8"]
        }
}

# fraction split
FRAC_SPLIT = (0.2, 0.8)

# seed for shuffling before frac_split
SEED = 42

# attrition
BASE_RATE = 0.05
MAX_RATE = 0.4
CAPTURE_TOLERANCE = 48

#==================================================================
# STOCHASTIC DURATION SAMPLING
#==================================================================

# note, cv is coefficient of variation, taken as sd/mean
CV_BY_TECH = {
    "capture": {"definition": {"cv": 0.2, "min": 1, "max": 100}, 
                "approval": {"cv": 0.2, "min": 1, "max": 100},
                "construction": {"cv": 0.2, "min": 1, "max": 100}},
    
    "transport": {"definition": {"cv": 0.2, "min": 1, "max": 100}, 
                "approval": {"cv": 0.2, "min": 1, "max": 100},
                "construction": {"cv": 0.2, "min": 1, "max": 100}},
    
    "storage": {"definition": {"cv": 0.2, "min": 1, "max": 100}, 
                "approval": {"cv": 0.2, "min": 1, "max": 100},
                "construction": {"cv": 0.2, "min": 1, "max": 100}}
}

DURATION_SAMPLING = {
    "dist": "lognormal"    # "lognormal" | "normal" | "uniform"
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

def sample_duration(mean, project, stage, tech, replication_seed, sampling):
    '''
    Sample one stage duration, centered on `mean` (the fixed duration).
    Returns a positive integer (months).
    '''
    # fixed guard — this allows us to fall back to default durations when we are not sampling
    if not sampling or mean <= 0:
        return mean

    # create the random number generator -> hash gives seed number, which seeds a random number generator
    rng = np.random.default_rng(stable_seed(project, stage, replication_seed)) 

    cv = CV_BY_TECH[tech][stage]["cv"]
    minimum = CV_BY_TECH[tech][stage]["min"]
    maximum = CV_BY_TECH[tech][stage]["max"]

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

    # check that it is within bounds
    if round(sample) >= maximum:
        return maximum
    elif round(sample) <= minimum:
        return minimum
    else:
        return round(sample)

#==================================================================
# BUILDING THE BASE GRAPH (NO INTERDEPENDENCIES)
#==================================================================

def make_base_graph(
        replication_seed=0, 
        clusters = CLUSTERS, 
        caps = CAPTURE,
        caps_vol = CAPTURE_VOLUMES,
        trans = TRANSPORT,
        trans_vol = TRANSPORT_VOLUMES,
        stor = STORAGE,
        stor_vol = STORAGE_VOLUMES,
        sampling=False
        ):
    '''
    Description: builds intra-project DAG without joint nodes
    Returns: G_indep
    '''
    # helper method for drawing project nodes only (no joint nodes)

    def intra_nodes():
        # make one large graph
        G = nx.DiGraph()

        for storage, transport_clusters in clusters.items():
            # layer 1: storage nodes
            storage_cluster = storage + " cluster" # naming the overarching storage cluster

            for stage, dur in stor[storage].items():
                G.add_node(
                    (storage, stage),
                    duration = sample_duration(dur, storage, stage, "storage", replication_seed, sampling),
                    stage = stage,
                    tech = "storage",
                    ES = 0.0,
                    EF = 0.0,
                    volume = stor_vol[storage],
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
                volume = stor_vol[storage],
                s_cluster = storage_cluster,
                t_cluster = None,
                abandoned = None
            )

            for transport, captures in transport_clusters.items():
                # cluster number is determined by ts project
                transport_cluster =  transport + " cluster"

                # add transport nodes
                for stage, dur in trans[transport].items():
                    G.add_node(
                        (transport, stage),
                        duration = sample_duration(dur, transport, stage, "transport", replication_seed, sampling),
                        stage = stage,
                        tech = "transport",
                        ES = 0.0,
                        EF = 0.0,
                        volume = trans_vol[transport],
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
                    volume = trans_vol[transport],
                    t_cluster = transport_cluster,
                    s_cluster = storage_cluster,
                    abandoned = None
                )

                for capture in captures:
                    # add capture nodes
                    for stage, dur in caps[capture].items():
                        G.add_node(
                            (capture, stage),
                            duration = sample_duration(dur, capture, stage, "capture", replication_seed, sampling),
                            stage = stage,
                            tech = "capture",
                            ES = 0.0,
                            EF = 0.0,
                            volume = caps_vol[capture],
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
                        volume = caps_vol[capture],
                        t_cluster = transport_cluster,
                        s_cluster = storage_cluster,
                        abandoned = None
                    )

        return G

    # helper method for drawing intra-project edges only
    # this method works for 1:multiple already
    def intra_edges(G: nx.DiGraph, clusters):
        def graphEdges(G, pid):
            for a, b in zip(STAGES4[:-1], STAGES4[1:]):
                G.add_edge((pid, a), (pid, b))
        
        for storage, transport_clusters in clusters.items():
            graphEdges(G, storage)
            for transport, captures in transport_clusters.items():
                graphEdges(G, transport)
                for capture in captures:
                    graphEdges(G, capture)

    # make a NEW graph without interdependent edges to evaluate baseline ES/EF
    G_indep = intra_nodes()
    intra_edges(G_indep, clusters)

    return G_indep

#==================================================================
# BUILDING THE DAG WITH INTERDEPENDENCIES
#==================================================================

def fracSplit(captures, frac_split = FRAC_SPLIT):
        '''
        Description: helper method that splits capture into two batches based on risk aversion level
        Returns: tuple of ([approval pids], [construction pids])
        '''
        # seeding and introducing randomness
        rng = random.Random(SEED)
        shuffled = list(captures)
        rng.shuffle(shuffled)

        # number of capture projects in approval batch (risk-tolerant)
        approv_num = round(len(shuffled)*frac_split[0])

        # cuts the list of pids in two for the two sets (go ahead at approval and construction)
        return shuffled[:approv_num], shuffled[approv_num:]

def get_storage(G, capture, clusters):
    for storage, t_clusters in clusters.items():
        for transport, captures in t_clusters.items():
            for cap in captures:
                if cap == capture:
                    return storage

def get_transport(G, capture, clusters):
    for storage, t_clusters in clusters.items():
        for transport, captures in t_clusters.items():
            for cap in captures:
                if cap == capture:
                    return transport

def projGraph(
        replication_seed=0, 
        clusters = CLUSTERS, 
        caps = CAPTURE,
        caps_vol = CAPTURE_VOLUMES,
        trans = TRANSPORT,
        trans_vol = TRANSPORT_VOLUMES,
        stor = STORAGE,
        stor_vol = STORAGE_VOLUMES,
        frac_split = FRAC_SPLIT,
        sampling = False
        ):
    
    # building the base graph with intra-project edges
    G = make_base_graph(
        replication_seed, 
        clusters, 
        caps,
        caps_vol,
        trans,
        trans_vol,
        stor,
        stor_vol,
        sampling
        )

    for storage, t_cluster in clusters.items():
        cluster_captures = [c for caps in t_cluster.values() for c in caps]
        approval, construction = fracSplit(cluster_captures, frac_split)

        for capture in approval:
            G.add_edge(
                (get_storage(G, capture, clusters), "approval"), 
                (capture, "approval")
            )

            G.add_edge(
                (get_transport(G, capture, clusters), "approval"),
                (capture, "approval")
            )

        for capture in construction:
            G.add_edge(
                (get_storage(G, capture, clusters), "construction"), 
                (capture, "approval")
            )

            G.add_edge(
                (get_transport(G, capture, clusters), "construction"),
                (capture, "approval")
            )
    
    # commissioning cascade: storage -> transport -> capture
    for storage, t_cluster in clusters.items():
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
# CALCULATING PROJECT DELAYS
#==================================================================

def calculate_delay(G: nx.DiGraph, project, stage):
    # actual EF of the node - (EF of last node + duration) 
    # this function only happens at approval for capture because that's the only stage
    # at which capture is waiting for other parties 
    if stage == "approval":
        actual_EF = G.nodes[(project, stage)]["EF"]
        EF_of_predecessor = G.nodes[(project, "definition")]["EF"]
        own_duration = G.nodes[(project, stage)]["duration"]

        original_EF = EF_of_predecessor + own_duration
        delay = actual_EF - original_EF

        return delay
    
    else:
        return 0

#==================================================================
# PROJECT ABANDONMENT 
#==================================================================

def calculate_attrition_probability(
        G: nx.DiGraph, project, stage, base_rate = BASE_RATE, 
        max_rate = MAX_RATE, 
        capture_tolerance = CAPTURE_TOLERANCE
        ):
    '''
    Description: returns attrition probability based on delay
    Principle: slip past partner wait baseline
    Args: delay (calculated from stage_delay) and tech
    Returns: probability
    '''

    delay = calculate_delay(G, project, stage)

    delay_factor = delay / capture_tolerance
    return min(max_rate, base_rate * np.exp(delay_factor))

def mark_capture_abandoned(G: nx.DiGraph, capture, stage):
    for stage in STAGES4:
        G.nodes[(capture, stage)]["abandoned"] = True

def apply_attrition(
        G: nx.DiGraph, 
        base_rate = BASE_RATE,
        clusters = CLUSTERS, 
        replication_seed = 0,
        max_rate = MAX_RATE,
        cap_tolerance = CAPTURE_TOLERANCE
        ):

    # NOTE: here we only roll abandonment for the first two stages so we are consistent with 
    # the base roll for S2
    ROLL_STAGES = ["definition", "approval"]

    # a generator for the whole pass — does not hash per item, just one stream.
    # this is because the order is fixed
    rng = random.Random(SEED + replication_seed)
    abandoned_c = {}
    for storage, t_clusters in clusters.items():
        for transport, captures in t_clusters.items():
            for capture in captures:
                for stage in ROLL_STAGES:
                    if rng.random() < calculate_attrition_probability(G, capture, stage, base_rate, max_rate, cap_tolerance):
                        mark_capture_abandoned(G, capture, stage)
                        abandoned_c[capture] = stage
                        break # once a project dies, don't need to roll future stage
    
    return abandoned_c

#==================================================================
# METRICS
#==================================================================


#==================================================================
# MONTE CARLO
#==================================================================

def monte_carlo(
        n_reps, 
        base_rate = BASE_RATE, 
        max_rate = MAX_RATE,
        cap_tolerance = CAPTURE_TOLERANCE,
        replication_seed=0, 
        clusters = CLUSTERS, 
        caps = CAPTURE,
        caps_vol = CAPTURE_VOLUMES,
        trans = TRANSPORT,
        trans_vol = TRANSPORT_VOLUMES,
        stor = STORAGE,
        stor_vol = STORAGE_VOLUMES,
        frac_split = FRAC_SPLIT,
        sampling = True,
    ):
    
    results = []

    num_cap = len(caps)

    for rep in range(n_reps):

        G = projGraph(
            rep, 
            clusters, 
            caps,
            caps_vol,
            trans,
            trans_vol,
            stor,
            stor_vol,
            frac_split,
            sampling
        )

        CPM(G)

        abandoned = apply_attrition(
                        G, 
                        base_rate = base_rate, 
                        clusters = clusters, 
                        replication_seed = rep,
                        max_rate = max_rate,
                        cap_tolerance = cap_tolerance
                    )

        final_vol = 0
        for storage, t_clusters in clusters.items():
            for transport, captures in t_clusters.items():
                for capture in captures:
                    if not G.nodes[(capture, "commissioning")]["abandoned"]:
                        final_vol += G.nodes[(capture, "commissioning")]['volume']

        results.append({
                "rep": rep,
                "num_cap": num_cap,
                "n_c_abandoned": len(abandoned),
                "completion": max((G.nodes[n]["EF"] for n in G.nodes if G.nodes[n]['abandoned'] is None), default = 0),
                "final volume": final_vol
            }
        )
    return results

def analyze_monte_carlo(results):
    cum_abandoned = 0.0
    cum_time = 0.0
    cum_vol = 0.0
    cap_abandon_rate = []
    cum_c_rate = 0.0

    for rep in results:
        cum_abandoned += rep["n_c_abandoned"]
        cum_time += rep["completion"]
        cum_vol += rep["final volume"]
        cap_abandon_rate.append(rep["n_c_abandoned"]/rep["num_cap"])
        cum_c_rate += rep["n_c_abandoned"]/rep["num_cap"]
    
    avg_abandoned = cum_abandoned/len(results)
    avg_c_abandon_rate = cum_c_rate/len(results)
    avg_time = cum_time/len(results)
    avg_vol = cum_vol/len(results)

    return {"average no. capture abandoned": avg_abandoned, 
            "average capture abandonment rate": avg_c_abandon_rate,
            "average completion time": avg_time,
            "average final volume": avg_vol}

#==================================================================
# MAIN (EXECUTION)
#==================================================================

if __name__ == "__main__":
    print("default:", analyze_monte_carlo(monte_carlo(300)))
    print("high base_rate:", analyze_monte_carlo(monte_carlo(300, base_rate=0.3)))
