import networkx as nx
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import hashlib
import project_data as project_data

#==================================================================
# CONSTANTS (INPUT DATA AND PARAMETERS)
#==================================================================
# stages of projects
STAGES = ["definition", "approval", "construction"]
STAGES4 = ["definition", "approval", "construction", "commissioning"]

# seed for shuffling before frac_split 
SEED = 42

# constants for the abandonment function
THRESHOLD_FRAC = 0.5
BASE_RATE = 0.05
MAX_RATE = 0.4
CAPTURE_TOLERANCE = 36
STORAGE_TOLERANCE = 36
TRANSPORT_TOLERANCE = 36
LATE_PENALTY = 0.15

#==================================================================
# PROJECT DATA
#==================================================================

# stores the pipe/storage every single transport flows into next
PIPE_DOWNSTREAM = {"projT1": "projS1"}

# stores the transport every single capture flows into next
CAPTURE_PIPE = {"projC1": "projT1", 
                "projC2": "projT1",
                "projC3": "projT1",
                "projC4": "projT1",
                "projC5": "projT1",
                "projC6": "projT1",
                "projC7": "projT1",
                "projC8": "projT1"}

#==================================================================
# STOCHASTIC DURATION SAMPLING
#==================================================================

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

def _stable_seed(project, stage, replication_seed=0):
    '''
    Deterministic per-(project, stage) seed via blake2b (Python's hash() is
    randomized per process, so we can't use it for reproducibility).
    Mixing in replication_seed lets a multi-run sweep get different draws.
    '''
    key = f"{project}|{stage}|{replication_seed}"
    digest = hashlib.blake2b(key.encode(), digest_size=8).digest()
    return int.from_bytes(digest, "big")

def sample_duration(mean, project, stage, tech, replication_seed=0, sampling = False):
    '''
    Sample one stage duration, centered on `mean` (the fixed duration).
    Returns a positive integer (months).
    '''
    # if 
    if not sampling or mean <= 0:
        return mean

    rng = np.random.default_rng(_stable_seed(project, stage, replication_seed))

    cv = CV_BY_TECH[tech][stage]["cv"]
    minimum = CV_BY_TECH[tech][stage]["min"]
    maximum = CV_BY_TECH[tech][stage]["max"]

    std = cv * mean
    dist = DURATION_SAMPLING["dist"]

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

def joint_naming(stage):
    '''
    Description: naming the joint nodes
    Args: stage
    Returns: name of the joint node
    '''
    if stage == "definition":
        joint_name = stage + " joint node"
    elif stage == "approval":
        joint_name = "FID joint node"
    else:
        raise ValueError(f"No joint stage for {stage}") 
    
    return joint_name

def cluster_naming(cluster):
    return cluster + " cluster"

def upstream_project(project, pipe_downstream = PIPE_DOWNSTREAM, capture_pipe = CAPTURE_PIPE):
    # Returns a list of projects that link directly into the given project
    direct_upstream = []
    for upstream, downstream in pipe_downstream.items():
        if downstream == project:
            direct_upstream.append(upstream)
    
    for capture, transport in capture_pipe.items():
        if transport == project:
            direct_upstream.append(capture)
    
    return direct_upstream

def capture_storage(capture, pipe_downstream=PIPE_DOWNSTREAM, capture_pipe=CAPTURE_PIPE):
    # Trace from a capture down through the pipe tree to the storage it feeds.
    current = capture_pipe[capture]
    while current in pipe_downstream:      
        current = pipe_downstream[current] 
    return current                         

def projGraph(replication_seed=0, 
              sampling=False,
              pipe_downstream = project_data.PIPE_DOWNSTREAM,
              capture_pipe = project_data.CAPTURE_PIPE,
              capture_durations=project_data.CAPTURE, 
              capture_volumes=project_data.CAPTURE_VOLUMES,
              storage_durations=project_data.STORAGE, 
              storage_volumes=project_data.STORAGE_VOLUMES,
              transport_durations=project_data.TRANSPORT, 
              transport_volumes=project_data.TRANSPORT_VOLUMES):
    '''
    Description: creating graph and adding nodes
    Returns: directed acyclic graph G
    '''
    # make one large graph
    G = nx.DiGraph()

    # Step 1: build all the storage nodes
    for storage in storage_volumes:
        # name of storage cluster
        storage_cluster = cluster_naming(storage)

        # create nodes for storage definition, approval, construction
        for stage, dur in storage_durations[storage].items():
            G.add_node(
                (storage, stage),
                duration = sample_duration(dur, storage, stage, "storage", replication_seed, sampling),
                stage = stage,
                tech = "storage",
                ES = 0.0,
                EF = 0.0,
                volume = storage_volumes[storage],
                actual_volume = 0.0,
                committed_volume = 0.0,
                s_cluster = storage_cluster,
                abandoned = None
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
            actual_volume = 0.0,
            committed_volume = 0.0,
            s_cluster = storage_cluster,
            abandoned = None
        )
        # create storage joint FID node
        G.add_node(
            (storage_cluster, "FID joint node"),
            duration = 0.0,
            stage = "FID joint node",
            tech = "joint",
            ES = 0.0,
            EF = 0.0,
            volume = storage_volumes[storage],
            actual_volume = 0.0,
            committed_volume = 0.0,
            s_cluster = storage_cluster,
            below_threshold = None,
            abandoned = None
        )
    
    # Step 2: build all the transport nodes
    for transport in transport_volumes:
        # give a successor attribute to each transport project
        succ = pipe_downstream[transport]

        # give a predecessor attribute to each transport project
        preds = upstream_project(transport, pipe_downstream, capture_pipe)
        
        transport_cluster = cluster_naming(transport)

        # create nodes for transport definition, approval, construction
        for stage, dur in transport_durations[transport].items():
            G.add_node(
                (transport, stage),
                duration = sample_duration(dur, transport, stage, "transport", replication_seed, sampling),
                stage = stage,
                tech = "transport",
                ES = 0.0,
                EF = 0.0,
                volume = transport_volumes[transport],
                actual_volume = 0.0,
                committed_volume = 0.0,
                successor = succ,
                predecessor = preds,
                abandoned = None
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
            successor = succ,
            predecessor = preds,
            t_cluster = transport_cluster,
            abandoned = None
        )
        # built transport joint definition and joint FID nodes
        for stage in ["definition", "approval"]:
            G.add_node(
                (transport_cluster, joint_naming(stage)),
                duration = 0.0,
                stage = "FID joint node",
                tech = "joint",
                ES = 0.0,
                EF = 0.0,
                volume = transport_volumes[transport],
                actual_volume = 0.0,
                committed_volume = 0.0,
                t_cluster = transport_cluster,
                successor = succ,
                predecessor = preds,
                below_threshold = None,
                abandoned = None
            )

    # Step 3: build all the capture nodes
    for capture in capture_volumes:
        immediate_transport = capture_pipe[capture]
        for stage, dur in capture_durations[capture].items():
            G.add_node(
                (capture, stage),
                duration = sample_duration(dur, capture, stage, "capture", replication_seed, sampling),
                stage = stage,
                tech = "capture",
                ES = 0.0,
                EF = 0.0,
                volume = capture_volumes[capture],
                actual_volume = 0.0,
                committed_volume = 0.0,
                immediate_transport = immediate_transport,
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
            volume = capture_volumes[capture],
            actual_volume = 0.0,
            committed_volume = 0.0,
            abandoned = None
        )
    
    return G

def projEdges(G: nx.DiGraph, 
              pipe_downstream = project_data.PIPE_DOWNSTREAM, 
              capture_pipe = project_data.CAPTURE_PIPE,
              capture_volumes=project_data.CAPTURE_VOLUMES,
              storage_volumes=project_data.STORAGE_VOLUMES,
              transport_volumes=project_data.TRANSPORT_VOLUMES):
    '''
    Description: adds intra-project edges to G
    Args: G
    '''
    # add edges between storage nodes
    for storage in storage_volumes:
        # edge from storage def to storage app
        G.add_edge(
            (storage, "definition"),
            (storage, "approval")
        )

        # edge from storage app to storage cluster FID joint node
        G.add_edge(
            (storage, "approval"),
            (cluster_naming(storage), "FID joint node")
        )

        # edge from storage FID to storage construction
        G.add_edge(
            (cluster_naming(storage), "FID joint node"),
            (storage, "construction")
        )

        # edge from storage construction to storage commissioning
        G.add_edge(
            (storage, "construction"),
            (storage, "commissioning")
        )
    
    # add edges from storage to 


    for storage, transport_clusters in clusters.items():
       
        for transport, captures in transport_clusters.items():

            # edge from transport app joint node to ts app
            G.add_edge(
                (transport, "approval joint node"),
                (transport, "approval")
            )

            # edge from transport app to transport cluster FID joint node
            G.add_edge(
                (transport, "approval"),
                (cluster_naming(transport), joint_naming("approval"))
            )

            # edge from storage cluster FID joint node to transport construction
            G.add_edge(
                (cluster_naming(storage), joint_naming("approval")),
                (transport, "construction")
            )

            # edge from ts construction to ts commissioning
            G.add_edge(
                (transport, "construction"),
                (transport, "commissioning")
            )

            # edge from storage commissioning to transport commissioning
            G.add_edge(
                (storage, "commissioning"),
                (transport, "commissioning")
            )

            for capture in captures:
                # edge from ts def to joint def
                G.add_edge(
                    (transport, "definition"),
                    (capture, joint_naming("definition"))
                )

                # edge from cap def to joint def
                G.add_edge(
                    (capture, "definition"),
                    (capture, joint_naming("definition"))
                )
                # edge from joint def to ts app joint node
                G.add_edge(
                    (capture, joint_naming("definition")),
                    (transport, "approval joint node")
                )

                # edge from joint def to cap app
                G.add_edge(
                    (capture, joint_naming("definition")),
                    (capture, "approval")
                )

                # edge from cap app to transport cluster joint FID
                G.add_edge(
                    (capture, "approval"),
                    (cluster_naming(transport), joint_naming("approval"))
                )

                # edge from transport cluster joint FID to storage cluster joint FID
                G.add_edge(
                    (cluster_naming(transport), joint_naming("approval")),
                    (cluster_naming(storage), "FID joint node")
                )

                # edge from storage cluster joint FID to capture cons
                G.add_edge(
                    (cluster_naming(storage), joint_naming("approval")),
                    (capture, "construction")
                )

                # edge from capture construction to capture commissioning
                G.add_edge(
                    (capture, "construction"),
                    (capture, "commissioning")
                )
                
                # edge from ts construction to capture commissioning
                G.add_edge(
                    (transport, "construction"),
                    (capture, "commissioning")
                )
            
#==================================================================
# RUNNING THE CPM
#==================================================================

def is_threshold_joint(G: nx.DiGraph, node):
    '''
    Description: checks if a given node is a joint node requiring volumetric control 
    Args: G, node
    Returns: True or False
    '''
    return G.nodes[node].get("tech") == "joint" and (
        G.nodes[node].get("stage") == "FID joint node" 
        or G.nodes[node].get("stage") == "approval joint node")

def gather_input_specs(G: nx.DiGraph, joint):
    '''
    Description: gathers (volume, arrival_time) specs for predecessors of joint node 
    Args: G, joint node
    Returns a list of (volume, arrival_time) to feed into the volumetric gating method
    '''
    if not is_threshold_joint(G, joint):
        raise ValueError(f"{joint} is not a joint node")
    
    arrivals = []

    for node in G.predecessors(joint):
        # skip nodes marked as abandoned
        if G.nodes[node]["abandoned"] is not None:
            continue

        # this handles inputs from capture projects
        elif G.nodes[node]["tech"] == "capture":
            volume = G.nodes[node]["volume"]
            arrival_time = G.nodes[node]["EF"]
            arrivals.append((volume, arrival_time))
        
        # this handles actual inputs from the transport cluster FID joint node
        elif G.nodes[node]["tech"] == "joint":
            volume = G.nodes[node]["actual_volume"]
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

def CPM(G: nx.DiGraph, threshold_frac=THRESHOLD_FRAC):
    '''
    Description: runs critical path method (CPM), updating ES and EF and checking thresholds
    Args: G
    '''

    for node in nx.topological_sort(G):
        # case where it is a volumetric control gate (FID joint nodes)
        if G.nodes[node].get("abandoned") is not None:
            continue # abandoned nodes do not participate in scheduling
        if is_threshold_joint(G, node):
            arrivals = gather_input_specs(G, node)
            capacity = G.nodes[node]["volume"]
            fire_time = threshold_gating(arrivals, capacity, threshold_frac)
            if fire_time is None:
                G.nodes[node]["ES"] = float("inf")
                G.nodes[node]["EF"] = float("inf")
                G.nodes[node]["below_threshold"] = True
                G.nodes[node]["actual_volume"] = 0.0
            else:
                G.nodes[node]["ES"] = fire_time
                G.nodes[node]["EF"] = fire_time
                G.nodes[node]["below_threshold"] = False
                G.nodes[node]["committed_volume"] = sum(v for v,t in arrivals) # realized throughput
                G.nodes[node]["actual_volume"] = min(
                    G.nodes[node].get("committed_volume"), G.nodes[node].get("volume"))
        
        else:
            preds = list(G.predecessors(node))

            # the new ES is the max of the EF of the preceeding node(s) and the original ES
            # we make sure to only read the EF of preceding nodes that have not been marked abandoned
            max_preds = max((G.nodes[p]["EF"] for p in preds if G.nodes[p].get("abandoned") is None), default = 0.0)

            updated_ES = max(max_preds, G.nodes[node].get("ES", 0.0))
            
            # update the ES and EF of each node
            G.nodes[node]["ES"] = updated_ES
            G.nodes[node]["EF"] = updated_ES + G.nodes[node]["duration"]

            # update the actual volume passing through each node 

#==================================================================
# CALCULATING PROJECT DELAYS
#==================================================================

def transport_captures(G: nx.DiGraph, transport, clusters=project_data.CLUSTERS):
    for storage, t_cluster in clusters.items():
        if transport in t_cluster:
            return t_cluster[transport]

def target_node(G: nx.DiGraph, project, stage):
    tech = G.nodes[(project, stage)].get("tech")
    t_cluster = G.nodes[(project, stage)].get("t_cluster")
    s_cluster = G.nodes[(project, stage)].get("s_cluster")

    if stage == "construction":
        return [(project, "commissioning")]

    if tech == "capture":
        if stage == "definition":
            return [(project, "definition joint node")]
        elif stage == "approval":
            return [(t_cluster, "FID joint node")]

    elif tech == "transport":
        if stage == "definition":
            return [(project, "approval joint node")]
        elif stage == "approval":
            return [(t_cluster, "FID joint node")]

    elif tech == "storage":
        # no sync partner until the storage FID joint
        return [(s_cluster, "FID joint node")]

    raise ValueError(f"no target for tech={tech}, stage={stage}")

def storage_coordination_delay(G: nx.DiGraph, project):
    '''
    Slip for a party waiting at the STORAGE FID joint (the shared coordination node).
    Works for storage and for transports (both wait here for the cluster to commit).
    Slip = (storage FID fire time) - (party's own ready time at this gate).
    '''
    s_cluster = G.nodes[(project, "definition")]["s_cluster"]
    storage_fid = (s_cluster, "FID joint node")
    gate_ef = G.nodes[storage_fid]["EF"]

    tech = G.nodes[(project, "definition")]["tech"]
    if tech == "storage":
        own_ef = G.nodes[(project, "approval")]["EF"]
    else:
        t_cluster = G.nodes[(project, "definition")]["t_cluster"]
        own_ef = G.nodes[(t_cluster, "FID joint node")]["EF"]
    
    delay = gate_ef - own_ef

    return delay if delay > 0 else 0

def stage_delay(G: nx.DiGraph, node):
    '''
    Description: calculates delay at a specific stage
    This code works because joint nodes have duration 0
    Args: constrained graph with interdepencies, node
    Returns: the stage delay at that specific node 
    '''
    # Looks up target node via target_node(), allows it to accommodate multiple successors
    project, stage = node[0], node[1]
    targets = target_node(G, project, stage)
    max_delay = 0
    for target in targets:
        delay = G.nodes[target]["EF"] - G.nodes[(project, stage)]["EF"]
        if delay > max_delay:
            max_delay = delay
    
    return max_delay

#==================================================================
# PROJECT ABANDONMENT NOTE: EDIT THE ATTRITION PROB FUNCTION
#==================================================================

def calculate_attrition_probability(delay, tech, base_rate=BASE_RATE, 
                                    max_rate=MAX_RATE,
                                    capture_tolerance=CAPTURE_TOLERANCE,
                                    transport_tolerance=TRANSPORT_TOLERANCE,
                                    storage_tolerance=STORAGE_TOLERANCE,
                                    late_penalty=LATE_PENALTY):
    '''
    Description: returns attrition probability based on delay and tech
    Principle: slip past partner wait baseline
    Args: delay (calculated from stage_delay) and tech
    Returns: probability
    '''
    if tech == "capture":
        tolerance = capture_tolerance
    elif tech == "transport":
        tolerance = transport_tolerance
    else:
        tolerance = storage_tolerance

    if delay < 0:
        return late_penalty

    else:
        delay_factor = delay / tolerance
        return min(max_rate, base_rate * (np.exp(delay_factor)))

def mark_abandonment(G: nx.DiGraph, project, stage):
    '''
    Description: marks all nodes of all projects in related cluster as abandoned (annotates stage of 
    abandonment)
    Args: Graph, storage_cluster, transport_cluster, project, stage
    Returns: marks nodes as abandoned
    '''
    tech = G.nodes[(project, stage)].get("tech")
    transport_cluster = G.nodes[(project, stage)].get("t_cluster") 
    storage_cluster = G.nodes[(project, stage)].get("s_cluster")

    # if it is a capture project -> mark all stages of the capture project as abandoned
    if tech == "capture":
        for s in ["definition", "approval", "construction", "commissioning"]:
            G.nodes[(project, s)]["abandoned"] = True
    
    # if it is a transport project -> mark every node in the transport cluster as abandoned
    elif tech == "transport":
        for node in G.nodes():
            if G.nodes[node]["t_cluster"] == transport_cluster:
                G.nodes[node]["abandoned"] = True

    # if it is a storage project -> mark every node in the storage cluster as abandoned
    elif tech == "storage":
        for node in G.nodes():
            if G.nodes[node]["s_cluster"] == storage_cluster:
                G.nodes[node]["abandoned"] = True

def already_abandoned(G: nx.DiGraph, project):
    '''
    checks if a project has already been abandoned
    Returns True if project has been abandoned
    '''
    return G.nodes[(project, "definition")]["abandoned"] is not None

def record_abandonment(project, tech, stage, abandoned_t, abandoned_s, abandoned_c, clusters=project_data.CLUSTERS):
    '''
    records the project as abandoned (include stage of abandonment)
    '''
    if tech == "transport":
        abandoned_t[project] = stage
        # record the captures projects in the cluster as abandoned
        for s, t_clusters in clusters.items():
            for transport, captures in t_clusters.items():
                if transport == project:
                    for capture in captures:
                        if capture not in abandoned_c:
                            abandoned_c[capture] = stage

    elif tech == "storage":
        abandoned_s[project] = stage
        # record all dependent transport and capture as abandoned
        for storage, t_clusters in clusters.items():
            for transport, captures in t_clusters.items():
                if storage == project:
                    if transport not in abandoned_t:
                        abandoned_t[transport] = stage
                    for capture in captures:
                        if capture not in abandoned_c:
                            abandoned_c[capture] = stage

    elif tech == "capture":
        abandoned_c[project] = stage

def threshold_failed(G, joint_node):
    return G.nodes[joint_node]["below_threshold"] == True

def time_slip_at_gate(G: nx.DiGraph, rng, parties, stage, abandoned_t, abandoned_s, abandoned_c,
                      base_rate=BASE_RATE, max_rate=MAX_RATE,
                      capture_tolerance=CAPTURE_TOLERANCE, transport_tolerance=TRANSPORT_TOLERANCE,
                      storage_tolerance=STORAGE_TOLERANCE, late_penalty = LATE_PENALTY, clusters=project_data.CLUSTERS):
    '''
    For each tech in parties, calculates delays and rolls abandonment at this stage
    parties comes in [(project, tech)] format for each project
    '''

    for (project, tech) in parties:
        if already_abandoned(G, project):
            continue
        delay = stage_delay(G, (project, stage))
        prob = calculate_attrition_probability(delay, tech, base_rate, max_rate,
                                               capture_tolerance, transport_tolerance, storage_tolerance, late_penalty)
        if rng.random() < prob:
            mark_abandonment(G, project, stage)
            record_abandonment(project, tech, stage, abandoned_t, abandoned_s, abandoned_c, clusters)

def time_slip_at_storage_gate(G: nx.DiGraph, rng, parties, abandoned_t, abandoned_s, abandoned_c,
                               base_rate=BASE_RATE, max_rate=MAX_RATE,
                               capture_tolerance=CAPTURE_TOLERANCE, transport_tolerance=TRANSPORT_TOLERANCE,
                               storage_tolerance=STORAGE_TOLERANCE, late_penalty=LATE_PENALTY, clusters=project_data.CLUSTERS):
    '''
    time slip specifically at the storage cluster FID joint node
    '''
    for (project, tech) in parties:
        if already_abandoned(G, project):
            continue
        delay = storage_coordination_delay(G, project)
        prob = calculate_attrition_probability(delay, tech, base_rate, max_rate,
                                               capture_tolerance, transport_tolerance, storage_tolerance, late_penalty)
        if rng.random() < prob:
            mark_abandonment(G, project, "approval")
            record_abandonment(project, tech, "approval", abandoned_t, abandoned_s, abandoned_c, clusters)

def threshold_test_at_gate(G: nx.DiGraph, joint_node, owner, stage, abandoned_t, abandoned_s, abandoned_c, clusters=project_data.CLUSTERS):
    '''
    If threshold test is not met, return True and collapse the owner of the joint_node
    Otherwise, return False
    '''
    if threshold_failed(G, joint_node):
        mark_abandonment(G, owner, stage)
        record_abandonment(owner, get_tech(G, owner), stage, abandoned_t, abandoned_s, abandoned_c, clusters)
        return True

    return False

def get_tech(G: nx.DiGraph, project):
    return G.nodes[(project, "definition")]["tech"] # this isn't very elegant (I hard-coded for def) but I think it works

def apply_attrition(G: nx.DiGraph, base_rate=BASE_RATE, threshold_frac=THRESHOLD_FRAC,
                    max_rate=MAX_RATE, capture_tolerance=CAPTURE_TOLERANCE,
                    transport_tolerance=TRANSPORT_TOLERANCE, storage_tolerance=STORAGE_TOLERANCE,
                    clusters=project_data.CLUSTERS, late_penalty=LATE_PENALTY, replication_seed = 0):
    '''
    Apply attrition to the graph
    '''
    rng = random.Random(SEED + replication_seed)
    abandoned_t, abandoned_s, abandoned_c = {}, {}, {}

    for storage in clusters:
        if storage in abandoned_s:
            continue

        for transport in clusters[storage]:
            if transport in abandoned_t:
                continue
            captures = clusters[storage][transport]

            #-------- Definition joint nodes ----------

            # 1. time-slip abandonment at joint def nodes
            captures = clusters[storage][transport]
            parties = [(c, "capture") for c in captures] + [(transport, "transport")]
            time_slip_at_gate(G, rng, parties, "definition", abandoned_t, abandoned_s, abandoned_c,
                              base_rate, max_rate, capture_tolerance, transport_tolerance, storage_tolerance, late_penalty, clusters)

            # 2. re-run the CPM
            CPM(G, threshold_frac)

            # 3. threshold check for the joint app node
            if threshold_test_at_gate(G, (transport, "approval joint node"), transport, "definition", abandoned_t, abandoned_s, abandoned_c, clusters):
                continue # transport has collapsed

            #-------- Transport cluster FID joint nodes ----------

            # 4. time-slip abandonment at t_cluster joint FID node
            time_slip_at_gate(G, rng, parties, "approval", abandoned_t, abandoned_s, abandoned_c,
                              base_rate, max_rate, capture_tolerance, transport_tolerance, storage_tolerance, late_penalty, clusters)

            # 5. re-reun the CPM
            CPM(G, threshold_frac)

            # 6. threshold check for the t_cluster joint FID node
            if threshold_test_at_gate(G, (cluster_naming(transport), "FID joint node"), transport, "approval", abandoned_t, abandoned_s, abandoned_c, clusters):
                continue # transport cluster has collapsed

        #-------- Storage cluster FID joint node ----------

        # 7. re-run the CPM
        CPM(G, threshold_frac)

        # 8. time-slip abandonment at s_cluster joint FID node
        survivors = [(t, "transport") for t in clusters[storage] if t not in abandoned_t]
        parties = parties = [(storage, "storage")] + survivors
        time_slip_at_storage_gate(G, rng, parties, abandoned_t, abandoned_s, abandoned_c,
                                  base_rate, max_rate, capture_tolerance, transport_tolerance, storage_tolerance, late_penalty, clusters)

        # 9. re-run the CPM
        CPM(G, threshold_frac)

        # 10. threshold check for the s_cluster joint FID node
        if threshold_test_at_gate(G, (cluster_naming(storage), "FID joint node"), storage, "approval", abandoned_t, abandoned_s, abandoned_c, clusters):
            continue # storage cluster has collapsed

    return abandoned_s, abandoned_t, abandoned_c

#==================================================================
# RUNNING THE MODEL
#==================================================================

def buildmodel(replication_seed=0, sampling=False,
               clusters=project_data.CLUSTERS, capture_durations=project_data.CAPTURE, capture_volumes=project_data.CAPTURE_VOLUMES,
               storage_durations=project_data.STORAGE, storage_volumes=project_data.STORAGE_VOLUMES,
               transport_durations=project_data.TRANSPORT, transport_volumes=project_data.TRANSPORT_VOLUMES):
    '''
    Description: runs the process 1) building graph and add nodes
    -> 2) add intra-project edges
    -> 3) add inter-project edges
    Returns: G
    '''

    G = projGraph(replication_seed, sampling,
                  clusters, capture_durations, capture_volumes,
                  storage_durations, storage_volumes,
                  transport_durations, transport_volumes)
    projEdges(G, clusters)

    return G

#==================================================================
# MONTE CARLO
#==================================================================

def monte_carlo(n_reps, 
                sampling=True, 
                base_rate=BASE_RATE, 
                threshold_frac=THRESHOLD_FRAC,
                max_rate=MAX_RATE, 
                capture_tolerance=CAPTURE_TOLERANCE,
                transport_tolerance=TRANSPORT_TOLERANCE, 
                storage_tolerance=STORAGE_TOLERANCE,
                clusters=project_data.CLUSTERS, 
                capture_durations=project_data.CAPTURE, 
                capture_volumes=project_data.CAPTURE_VOLUMES,
                storage_durations=project_data.STORAGE, 
                storage_volumes=project_data.STORAGE_VOLUMES,
                transport_durations=project_data.TRANSPORT, 
                transport_volumes=project_data.TRANSPORT_VOLUMES,
                late_penalty = LATE_PENALTY):
    results = []

    num_cap = len(capture_volumes)
    num_trans = len(transport_volumes)
    num_stor = len(storage_volumes)

    for rep in range(n_reps):
        G = buildmodel(replication_seed=rep, sampling=sampling,
                       clusters=clusters, capture_durations=capture_durations,
                       capture_volumes=capture_volumes, storage_durations=storage_durations,
                       storage_volumes=storage_volumes, transport_durations=transport_durations,
                       transport_volumes=transport_volumes)

        CPM(G, threshold_frac)

        a_s, a_t, a_c = apply_attrition(G, base_rate, threshold_frac,
                                         max_rate, capture_tolerance, transport_tolerance, storage_tolerance,
                                         clusters, late_penalty, replication_seed = rep)

        finite = [G.nodes[n]["EF"] for n in G.nodes
                if G.nodes[n]["EF"] != float("inf") and G.nodes[n]["abandoned"] is None]

        # getting the final survived volume from unabandoned storage FID joint nodes
        final_vol = 0
        for storage, t_clusters in clusters.items():
            fid = (cluster_naming(storage), "FID joint node")
            if not G.nodes[fid]["below_threshold"] and G.nodes[fid]["abandoned"] is None:
                final_vol += G.nodes[fid]["actual_volume"]
        
        results.append({
                "a_c": a_c,
                "a_t": a_t,
                "a_s": a_s,
                "rep": rep,
                "num_stor": num_stor,
                "storage abandoned": len(a_s),
                "num_trans": num_trans,
                "transport abandoned": len(a_t),
                "num_cap": num_cap,
                "capture abandoned": len(a_c),
                "completion": max(finite) if finite else 0,
                "final volume": final_vol
            }
        )
    return results

def analyze_monte_carlo(results):
    cum_s_abandoned = 0.0
    cum_t_abandoned = 0.0
    cum_c_abandoned = 0.0
    cum_vol = 0.0
    cum_time = 0.0
    cap_abandon_rate = []
    trans_abandon_rate = []
    stor_abandon_rate = []
    cum_c_rate = 0.0
    cum_t_rate = 0.0
    cum_s_rate = 0.0
    all_abandoned = 0.0
    c_abandon_at_app = []
    t_abandon_at_app = []

    for rep in results:
        cum_s_abandoned += rep["storage abandoned"]
        cum_t_abandoned += rep["transport abandoned"]
        cum_c_abandoned += rep["capture abandoned"]

        cum_time += rep["completion"]
        if rep["completion"] == 0:
            all_abandoned += 1

        cum_vol += rep["final volume"]

        a_c = rep["a_c"]
        a_t = rep["a_t"]
        a_s = rep["a_s"]

        c_def = 0
        c_app = 0
        for captures, stages in a_c.items():
            if stages == "definition":
                c_def += 1
            elif stages == "approval":
                c_app += 1
        
        t_def = 0
        t_app = 0
        for captures, stages in a_t.items():
            if stages == "definition":
                t_def += 1
            elif stages == "approval":
                t_app += 1

        if len(a_c) != 0:
            c_abandon_at_app.append(c_app/len(a_c))
        if len(a_t) != 0:
            t_abandon_at_app.append(t_app/len(a_t))
        
        cap_abandon_rate.append(rep["capture abandoned"]/rep["num_cap"])
        cum_c_rate += rep["capture abandoned"]/rep["num_cap"]
        trans_abandon_rate.append(rep["transport abandoned"]/rep["num_trans"])
        cum_t_rate += rep["transport abandoned"]/rep["num_trans"]
        stor_abandon_rate.append(rep["storage abandoned"]/rep["num_stor"])
        cum_s_rate += rep["storage abandoned"]/rep["num_stor"]

    avg_s_abandoned = cum_s_abandoned/len(results)
    avg_t_abandoned = cum_t_abandoned/len(results)
    avg_c_abandoned = cum_c_abandoned/len(results)
    avg_vol = cum_vol/len(results)

    collapse_rate = all_abandoned/len(results)

    # abandonment rates
    avg_c_abandon_rate = cum_c_rate/len(results)
    avg_t_abandon_rate = cum_t_rate/len(results)
    avg_s_abandon_rate = cum_s_rate/len(results)

    # average time taken for completed projects — so denom can only include completed ones
    surviving = len(results) - all_abandoned
    if surviving > 0:
        avg_time = cum_time/surviving 
    else:
        avg_time = -1
    
    # average abandonment stage ratios
    cum_c_abandon_at_app = 0
    for rate in c_abandon_at_app:
        cum_c_abandon_at_app += rate
    avg_c_abandon_at_app = cum_c_abandon_at_app/len(c_abandon_at_app)

    cum_t_abandon_at_app = 0
    for rate in t_abandon_at_app:
        cum_t_abandon_at_app += rate
    avg_t_abandon_at_app = cum_t_abandon_at_app/len(t_abandon_at_app)
    
    return {"average no. capture abandoned": avg_c_abandoned,
            "average capture abandonment rate": avg_c_abandon_rate,
            "average no. transport abandoned": avg_t_abandoned,
            "average transport abandonment rate": avg_t_abandon_rate,
            "average no. storage abandoned": avg_s_abandoned, 
            "average storage abandonment rate": avg_s_abandon_rate,
            "all abandoned": all_abandoned,
            "all abandoned rate": collapse_rate,
            "average completion time of survived": avg_time,
            "average final vol of capture": avg_vol,
            "avg percent of capture abandoning at approval": avg_c_abandon_at_app,
            "avg percent of transport abandoning at approval": avg_t_abandon_at_app,
            }

# NOTE: can also return the list of abandonment rates for data analysis

#==================================================================
# MAIN (EXECUTION)
#==================================================================

if __name__ == "__main__":
    results2 = monte_carlo(100, sampling = True, base_rate=0.10)
    print(analyze_monte_carlo(results2))
