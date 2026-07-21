import networkx as nx
import random
import hashlib
import numpy as np
import actual_data as project_data 
import matplotlib as plt

#==================================================================
# CONSTANTS (PARAMETERS)
#==================================================================
# stages of projects
STAGES = ["definition", "approval", "construction"]
STAGES4 = ["definition", "approval", "construction", "commissioning"]

# fraction split
FRAC_SPLIT = (0.4, 0.6)

# seed for shuffling before frac_split
SEED = 42

# attrition
BASE_RATE = 0.05
MAX_RATE = 0.2
CAPTURE_TOLERANCE = 48

# hammock node
HAMMOCK_THRESHOLD = 0.5

#==================================================================
# STOCHASTIC DURATION SAMPLING
#==================================================================

# note, cv is coefficient of variation, taken as sd/mean
CV_BY_TYPE = {
    "NGCC": {"definition": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}, 
                "approval": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"},
                "construction": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}},
    "ethanol": {"definition": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}, 
                "approval": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"},
                "construction": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}},
    "gas_processing": {"definition": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}, 
                "approval": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"},
                "construction": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}}, 

    "DAC": {"definition": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}, 
                "approval": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"},
                "construction": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}},
    "CHP": {"definition": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}, 
                "approval": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"},
                "construction": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}},
    "legacy_biomass": {"definition": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}, 
                "approval": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"},
                "construction": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}},
    "refinery": {"definition": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}, 
                "approval": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"},
                "construction": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}},
    "biomass_gasification": {"definition": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}, 
                "approval": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"},
                "construction": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}},
    "hydrogen": {"definition": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}, 
                "approval": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"},
                "construction": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}},
    "cement": {"definition": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}, 
                "approval": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"},
                "construction": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}},
    "other_industrial": {"definition": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}, 
                "approval": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"},
                "construction": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}},

    "transport": {"definition": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}, 
                "approval": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"},
                "construction": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}},
    "storage": {"definition": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}, 
                "approval": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"},
                "construction": {"cv": 0.2, "min": 1, "max": 100, "dist": "lognormal"}}
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

def sample_duration(mean, project, stage, replication_seed, sampling, dist_override="lognormal"):
    '''
    Sample one stage duration, centered on `mean` (the fixed duration).
    Returns a positive integer (months).
    '''
    # fixed guard — this allows us to fall back to default durations when we are not sampling
    if not sampling or mean <= 0:
        return mean

    # create the random number generator -> hash gives seed number, which seeds a random number generator
    rng = np.random.default_rng(stable_seed(project, stage, replication_seed)) 

    project_type = project_data.PROJECT_TYPE[project]
    cv = CV_BY_TYPE[project_type][stage]["cv"]
    minimum = CV_BY_TYPE[project_type][stage]["min"]
    maximum = CV_BY_TYPE[project_type][stage]["max"]

    std = cv * mean
    dist = dist_override if dist_override is not None else CV_BY_TYPE[project_type][stage]["dist"]
    
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
# DAG CONSTRUCTION
#==================================================================

def get_tech(G: nx.DiGraph, project):
    return G.nodes[(project, "definition")]["tech"]

def immediate_upstream_project(project, pipe_downstream = project_data.PIPE_DOWNSTREAM, capture_pipe = project_data.CAPTURE_PIPE):
    # Returns a list of projects that link directly into the given project
    direct_pipes = []
    direct_captures = []
    for upstream, downstream in pipe_downstream.items():
        if downstream == project:
            direct_pipes.append(upstream)
    
    for capture, transport in capture_pipe.items():
        if transport == project:
            direct_captures.append(capture)
    
    return direct_captures, direct_pipes

def everything_upstream(project, pipe_downstream = project_data.PIPE_DOWNSTREAM, capture_pipe = project_data.CAPTURE_PIPE):
    upstream_pipes = []
    upstream_captures = []

    direct_captures, direct_pipes = immediate_upstream_project(project, pipe_downstream, capture_pipe)
    upstream_captures.extend(direct_captures)

    for pipe in direct_pipes:
        upstream_pipes.append(pipe)
        caps, pipes = everything_upstream(pipe, pipe_downstream, capture_pipe)
        upstream_captures.extend(caps)
        upstream_pipes.extend(pipes)
    
    return upstream_captures, upstream_pipes

def project_storage(project, tech, pipe_downstream=project_data.PIPE_DOWNSTREAM, capture_pipe=project_data.CAPTURE_PIPE):
    # Trace from a project down through the pipe tree to the storage it feeds
    if tech == "capture":
        current = capture_pipe[project]
        while current in pipe_downstream:      
            current = pipe_downstream[current] 
        return current    
    elif tech == "transport":
        current = project
        while current in pipe_downstream:
            current = pipe_downstream[current]
        return current 
    else:
        return project                   

def projGraph(replication_seed=0, 
              sampling=False,
              pipe_downstream = project_data.PIPE_DOWNSTREAM,
              capture_pipe = project_data.CAPTURE_PIPE,
              capture_durations=project_data.CAPTURE, 
              capture_volumes=project_data.CAPTURE_VOLUMES,
              storage_durations=project_data.STORAGE, 
              storage_volumes=project_data.STORAGE_VOLUMES,
              transport_durations=project_data.TRANSPORT, 
              transport_volumes=project_data.TRANSPORT_VOLUMES,
              dist_override="lognormal"):
    '''
    Description: creating graph and adding nodes
    Returns: directed acyclic graph G
    '''
    # make one large graph
    G = nx.DiGraph()

    # Step 1: build all the storage nodes
    for storage in storage_volumes:

        # create nodes for storage definition, approval, construction
        for stage, dur in storage_durations[storage].items():
            G.add_node(
                (storage, stage),
                duration = sample_duration(dur, storage, stage, replication_seed, sampling, dist_override),
                stage = stage,
                tech = "storage",
                ES = 0.0,
                EF = 0.0,
                volume = storage_volumes[storage],
                project_type = project_data.PROJECT_TYPE[storage],
                actual_volume = 0.0,
                committed_volume = 0.0,
                abandoned = None,
                delay = 0.0
                )
        # create storage commissioning node
        G.add_node(
            (storage, "commissioning"),
            duration = 0.0,
            stage = "commissioning",
            tech = "storage",
            ES = 0.0,
            EF = 0.0,
            volume = storage_volumes[storage],
            project_type = project_data.PROJECT_TYPE[storage],
            actual_volume = 0.0,
            committed_volume = 0.0,
            abandoned = None,
            delay = 0.0
        )
    
    # Step 2: build all the transport nodes
    for transport in transport_volumes:
        # give a successor attribute to each transport project
        succ = pipe_downstream[transport]

        # give a predecessor attribute to each transport project
        preds = immediate_upstream_project(transport, pipe_downstream, capture_pipe)

        # create nodes for transport definition, approval, construction
        for stage, dur in transport_durations[transport].items():
            G.add_node(
                (transport, stage),
                duration = sample_duration(dur, transport, stage, replication_seed, sampling, dist_override),
                stage = stage,
                tech = "transport",
                ES = 0.0,
                EF = 0.0,
                volume = transport_volumes[transport],
                actual_volume = 0.0,
                committed_volume = 0.0,
                project_type = project_data.PROJECT_TYPE[transport],
                successor = succ,
                predecessor = preds,
                abandoned = None,
                delay = 0.0
            )
        # create transport commissioning node
        G.add_node(
            (transport, "commissioning"),
            duration = 0.0,
            stage = "commissioning",
            tech = "transport",
            ES = 0.0,
            EF = 0.0,
            volume = transport_volumes[transport],
            actual_volume = 0.0,
            committed_volume = 0.0,
            project_type = project_data.PROJECT_TYPE[transport],
            successor = succ,
            predecessor = preds,
            abandoned = None,
            delay = 0.0
        )

    # Step 3: build all the capture nodes
    for capture in capture_volumes:
        immediate_transport = capture_pipe[capture]
        for stage, dur in capture_durations[capture].items():
            G.add_node(
                (capture, stage),
                duration = sample_duration(dur, capture, stage, replication_seed, sampling, dist_override),
                stage = stage,
                tech = "capture",
                ES = 0.0,
                EF = 0.0,
                volume = capture_volumes[capture],
                project_type = project_data.PROJECT_TYPE[capture],
                actual_volume = 0.0,
                committed_volume = 0.0,
                immediate_transport = immediate_transport,
                abandoned = None,
                delay = 0.0
            )
        
        # add capture commissioning node
        G.add_node(
            (capture, "commissioning"),
            duration = 0.0,
            stage = "commissioning",
            tech = "capture",
            ES = 0.0,
            EF = 0.0,
            volume = capture_volumes[capture],
            project_type = project_data.PROJECT_TYPE[capture],
            actual_volume = 0.0,
            committed_volume = 0.0,
            abandoned = None,
            delay = 0.0
        )
    
    return G

def fracSplit(captures, frac_split = FRAC_SPLIT, replication_seed = 0):
        '''
        Description: helper method that splits capture into two batches based on risk aversion level
        Returns: tuple of ([approval pids], [construction pids])
        '''
        # seeding and introducing randomness
        rng = random.Random(SEED + replication_seed)
        shuffled = list(captures)
        rng.shuffle(shuffled)

        # number of capture projects in approval batch (risk-tolerant)
        approv_num = round(len(shuffled)*frac_split[0])

        # cuts the list of pids in two for the two sets (go ahead at approval and construction)
        return shuffled[:approv_num], shuffled[approv_num:]

def projEdges(G: nx.DiGraph, 
              pipe_downstream = project_data.PIPE_DOWNSTREAM, 
              capture_pipe = project_data.CAPTURE_PIPE,
              capture_volumes=project_data.CAPTURE_VOLUMES,
              storage_volumes=project_data.STORAGE_VOLUMES,
              transport_volumes=project_data.TRANSPORT_VOLUMES,
              frac_split=FRAC_SPLIT,
              replication_seed=0):
    '''
    Description: adds edges to G
    Args: G
    '''
    
    # Step 1: add intra-project edges (def -> app -> cons -> comm)
    for storage in storage_volumes:
        s1 = STAGES4[:-1]
        s2 = STAGES4[1:]
        for stage1, stage2 in zip(s1, s2):
            G.add_edge(
                (storage, stage1),
                (storage, stage2)
            )
    for transport in transport_volumes:
        s1 = STAGES4[:-1]
        s2 = STAGES4[1:]
        for stage1, stage2 in zip(s1, s2):
            G.add_edge(
                (transport, stage1),
                (transport, stage2)
            )
    for capture in capture_volumes:
        s1 = STAGES4[:-1]
        s2 = STAGES4[1:]
        for stage1, stage2 in zip(s1, s2):
            G.add_edge(
                (capture, stage1),
                (capture, stage2)
            )

    # Step 2: add inter-project dependencies for capture app/ cons
    cluster_captures = list(capture_volumes)
    approval, construction = fracSplit(cluster_captures, frac_split, replication_seed)
    
    for capture in approval:
        dep_trans = capture_pipe[capture]
        dep_stor = project_storage(capture, "capture", pipe_downstream, capture_pipe)
        G.add_edge(
            (dep_stor, "approval"),
            (capture, "approval")
        )
        G.add_edge(
            (dep_trans, "approval"),
            (capture, "approval")
        )

    for capture in construction:
        dep_trans = capture_pipe[capture]
        dep_stor = project_storage(capture, "capture", pipe_downstream, capture_pipe)
        G.add_edge(
            (dep_stor, "construction"),
            (capture, "approval")
        )
        G.add_edge(
            (dep_trans, "construction"),
            (capture, "approval")
        )
    
    # Step 3: add edges for cons -> comm for trans/cap, gating edges for commissioning
    for capture in capture_volumes:
        # add edges from each capture's construction to its commissioning
        G.add_edge(
            (capture, "construction"),
            (capture, "commissioning")
        )
        # add edges from transport commissioning to the dependent capture commissioning 
        G.add_edge(
            (capture_pipe[capture], "commissioning"),
            (capture, "commissioning")
        )
    
    for transport in transport_volumes:
        # add edges from each transport's construction to its commissioning
        G.add_edge(
            (transport, "construction"),
            (transport, "commissioning")
        )
        # add edges from primary transports' commissioning to secondary transports' commissioning
        downstream = pipe_downstream[transport]
        if downstream in transport_volumes:
            G.add_edge(
                (downstream, "commissioning"),
                (transport, "commissioning")
            )

    for storage in storage_volumes:
        # adding edges from storage commissioning to trunk lines' commissioning
        _, transports = immediate_upstream_project(storage, pipe_downstream, capture_pipe)
        for trans in transports:
            G.add_edge(
                (storage, "commissioning"),
                (trans, "commissioning")
            )

def add_hammock_node(G:nx.DiGraph, 
                    capture_volumes=project_data.CAPTURE_VOLUMES,
                    transport_volumes=project_data.TRANSPORT_VOLUMES):
    # create the hammock node (duration = 0)
    G.add_node(
        ("hammock node", "hammock node"), # need to think about the naming of the node
        duration = 0,
        stage = "hammock node",
        tech = "hammock node",
        ES = 0.0,
        EF = 0.0,
        actual_volume = 0.0,
        committed_volume = 0.0,
        abandoned = None
    )
    # add outwards edge from construction stage of all transports
    for transport in transport_volumes:
        G.add_edge(
            (transport, "construction"),
            ("hammock node", "hammock node")
        )

    # add edge linking hammock to def stage of all captures 
    for capture in capture_volumes:
        G.add_edge(
            ("hammock node", "hammock node"),
            (capture, "definition")
        )

#==================================================================
# RUNNING THE CPM
#==================================================================

def gather_input_specs(G: nx.DiGraph, hammock_node):
    '''
    Description: gathers (volume, arrival_time) specs for predecessors of hammock node 
    Args: G, hammock_node
    Returns a list of (volume, arrival_time) to feed into the volumetric gating method
    '''
    arrivals = []

    for node in G.predecessors(hammock_node):
        # skip nodes marked as abandoned — not necessary here because trans/stor don't abandon
        # but we'll keep it
        if G.nodes[node]["abandoned"] is not None:
            continue

        # this handles inputs from transport projects
        elif G.nodes[node]["tech"] == "transport":
            volume = G.nodes[node]["volume"]
            arrival_time = G.nodes[node]["EF"]
            arrivals.append((volume, arrival_time))
    
    return arrivals

def threshold_gating(arrivals, capacity, fraction):
    '''
    arrivals: list of (volume, arrival_time) for each committed party
    capacity: the downstream capacity (e.g. pipeline volume)
    fraction: fraction that must be filled to fire (e.g. 0.75)
    Returns: the time the gate fires, or None if threshold never reached
    '''
    needed = capacity*fraction
    ordered = sorted(arrivals, key = lambda x: x[1]) #lambda returns second tuple element (arrival time)
    cumulative_volume = 0.0
    for volume, arrival_time in ordered:
        cumulative_volume += volume
        if cumulative_volume >= needed:
            return arrival_time
    return None # if the capacity is never filled, then the gate won't fire

def CPM(G: nx.DiGraph, capacity=project_data.PLANNED_CAP_VOLUME, hammock_threshold=HAMMOCK_THRESHOLD):
    '''
    Description: runs critical path method (CPM), updating ES and EF 
    Args: G
    '''
    for node in nx.topological_sort(G):

        # if we are at the hammock node
        if G.nodes[node]["stage"] == "hammock node":
            arrivals = gather_input_specs(G, node)
            fire_time = threshold_gating(arrivals, capacity, hammock_threshold)
            if fire_time is None:
                raise ValueError("Threshold never reached — check for code issues")
            G.nodes[node]["ES"] = fire_time
            G.nodes[node]["EF"] = fire_time
        
        else:
            preds = list(G.predecessors(node))

            # the new ES is the max of the EF of the preceeding node(s) and the original ES
            max_preds = max((G.nodes[p]["EF"] for p in preds if G.nodes[p]["abandoned"] is None), default = 0.0)

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

        G.nodes[(project, "approval")]["delay"] = delay

        return delay
    
    else:
        return 0 # this is what is returned for the definition stage - a flat abandonment rate

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

def mark_capture_abandoned(G: nx.DiGraph, capture):
    for stage in STAGES4:
        G.nodes[(capture, stage)]["abandoned"] = True

def apply_attrition(G, captures=project_data.CAPTURE_VOLUMES, base_rate=BASE_RATE, replication_seed=0, max_rate=MAX_RATE, cap_tolerance=CAPTURE_TOLERANCE):
    ROLL_STAGES = ["definition", "approval"]
    rng = random.Random(SEED + replication_seed)
    abandoned_c = {}
    for capture in captures:
        for stage in ROLL_STAGES:
            p = calculate_attrition_probability(G, capture, stage, base_rate, max_rate, cap_tolerance)
            if rng.random() < p:
                mark_capture_abandoned(G, capture)
                abandoned_c[capture] = stage
                break
    return abandoned_c

#==================================================================
# BUILD MODEL
#==================================================================

def build_model(replication_seed=0, sampling=False,
               pipe_downstream = project_data.PIPE_DOWNSTREAM, capture_pipe = project_data.CAPTURE_PIPE, 
               capture_durations=project_data.CAPTURE, capture_volumes=project_data.CAPTURE_VOLUMES,
               storage_durations=project_data.STORAGE, storage_volumes=project_data.STORAGE_VOLUMES,
               transport_durations=project_data.TRANSPORT, transport_volumes=project_data.TRANSPORT_VOLUMES,
               frac_split=FRAC_SPLIT,
               dist_override="lognormal"):
    G = projGraph(replication_seed, sampling, pipe_downstream, capture_pipe,
                  capture_durations, capture_volumes, 
                  storage_durations, storage_volumes,
                  transport_durations, transport_volumes,
                  dist_override)
    projEdges(G, pipe_downstream, capture_pipe, capture_volumes, storage_volumes, transport_volumes, frac_split, replication_seed)
    add_hammock_node(G, capture_volumes, transport_volumes)
    return G

#==================================================================
# MONTE CARLO
#==================================================================

def monte_carlo(
        n_reps, 
        base_rate = BASE_RATE, 
        max_rate = MAX_RATE,
        pipe_downstream = project_data.PIPE_DOWNSTREAM,
        capture_pipe = project_data.CAPTURE_PIPE,
        cap_tolerance = CAPTURE_TOLERANCE,
        replication_seed=0, 
        caps = project_data.CAPTURE,
        caps_vol = project_data.CAPTURE_VOLUMES,
        trans = project_data.TRANSPORT,
        trans_vol = project_data.TRANSPORT_VOLUMES,
        stor = project_data.STORAGE,
        stor_vol = project_data.STORAGE_VOLUMES,
        frac_split = FRAC_SPLIT,
        sampling = True,
        hammock_threshold = HAMMOCK_THRESHOLD,
        dist_override = "lognormal"
    ):
    
    results = []

    num_cap = len(caps)

    for rep in range(n_reps):

        G = build_model(
            rep, 
            sampling,
            pipe_downstream, 
            capture_pipe, 
            caps, caps_vol,
            stor, stor_vol,
            trans, trans_vol, 
            frac_split,
            dist_override
        )

        CPM(G, hammock_threshold=hammock_threshold)

        abandoned = apply_attrition(
                        G, 
                        captures=caps_vol,
                        base_rate = base_rate,  
                        replication_seed = rep,
                        max_rate = max_rate,
                        cap_tolerance = cap_tolerance
                    )

        CPM(G, hammock_threshold=hammock_threshold)

        final_vol = 0
        
        for capture in caps:
            if not G.nodes[(capture, "commissioning")]["abandoned"]:
                final_vol += G.nodes[(capture, "commissioning")]['volume']

        results.append({
                "c_abandon": abandoned,
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
    print("high base_rate:", analyze_monte_carlo(monte_carlo(300, base_rate=0.05)))

    r = monte_carlo(50, sampling=True, base_rate=0.05)
    comps = [x["completion"] for x in r]
    print("distinct completions:", len(set(comps)), "of", len(comps))

    r1 = monte_carlo(30, base_rate=0.1)
    r2 = monte_carlo(30, base_rate=0.1)
    print("reproducible:", [x["completion"] for x in r1] == [y["completion"] for y in r2])
    
    