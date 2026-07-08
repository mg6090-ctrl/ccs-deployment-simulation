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

TRUNKS = ["projT1"]

#==================================================================
# STOCHASTIC DURATION SAMPLING
#==================================================================

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

def _stable_seed(project, stage, replication_seed=0):
    '''
    Deterministic per-(project, stage) seed via blake2b (Python's hash() is
    randomized per process, so we can't use it for reproducibility).
    Mixing in replication_seed lets a multi-run sweep get different draws.
    '''
    key = f"{project}|{stage}|{replication_seed}"
    digest = hashlib.blake2b(key.encode(), digest_size=8).digest()
    return int.from_bytes(digest, "big")

def sample_duration(mean, project, stage, replication_seed=0, sampling = False, dist_override="lognormal"):
    '''
    Sample one stage duration, centered on `mean` (the fixed duration).
    Returns a positive integer (months).
    '''
    # if 
    if not sampling or mean <= 0:
        return mean

    rng = np.random.default_rng(_stable_seed(project, stage, replication_seed))

    project_type = project_data.PROJECT_TYPE[project]
    cv = CV_BY_TYPE[project_type][stage]["cv"]
    minimum = CV_BY_TYPE[project_type][stage]["min"]
    maximum = CV_BY_TYPE[project_type][stage]["max"]

    std = cv * mean

    dist = dist_override if dist_override is not None else CV_BY_TYPE[project_type][stage]["dist"]

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
        # name of storage cluster
        storage_cluster = cluster_naming(storage)

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
                actual_volume = 0.0,
                committed_volume = 0.0,
                project_type = "storage",
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
            project_type = "storage",
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
            project_type = "storage",
            below_threshold = None,
            abandoned = None
        )
    
    # Step 2: build all the transport nodes
    for transport in transport_volumes:
        # give a successor attribute to each transport project
        succ = pipe_downstream[transport]

        # give a predecessor attribute to each transport project
        preds = immediate_upstream_project(transport, pipe_downstream, capture_pipe)
        
        transport_cluster = cluster_naming(transport)

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
                successor = succ,
                predecessor = preds,
                t_cluster = transport_cluster,
                project_type = "transport",
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
            project_type = "transport",
            abandoned = None
        )
        # built transport joint definition and joint FID nodes
        for stage in ["definition", "approval"]:
            G.add_node(
                (transport_cluster, joint_naming(stage)),
                duration = 0.0,
                stage = joint_naming(stage),
                tech = "joint",
                ES = 0.0,
                EF = 0.0,
                volume = transport_volumes[transport],
                actual_volume = 0.0,
                committed_volume = 0.0,
                t_cluster = transport_cluster,
                project_type = "transport",
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
            project_type = project_data.PROJECT_TYPE[capture],
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
              transport_volumes=project_data.TRANSPORT_VOLUMES,
              trunks=project_data.TRUNKS):
    '''
    Description: adds edges to G
    Args: G
    '''

    # Step 1: add edges between storage nodes, from stor cluster joint FID to construction of individual dependent projects
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

        # add edges from stor cluster joint FID to construction of individual dependent projects
        captures, pipes = everything_upstream(storage)
        for capture in captures:
            G.add_edge(
                (cluster_naming(storage), joint_naming("approval")),
                (capture, "construction")
            )
        for pipe in pipes:
            G.add_edge(
                (cluster_naming(storage), joint_naming("approval")),
                (pipe, "construction")
            )

    # Step 2: add edges in definition and approval stages for transport and capture
    for stage in ["definition", "approval"]:
        for transport in transport_volumes:
            joint_node = (cluster_naming(transport), joint_naming(stage))
            # add edge from transport def/app to transport def/app joint
            G.add_edge(
                (transport, stage),
                joint_node
            )
            
            d_caps, d_pipes = immediate_upstream_project(transport, pipe_downstream, capture_pipe)
            # for each upstream capture, add an edge from cap def/app to the trans def/app joint 
            for cap in d_caps:
                G.add_edge(
                    (cap, stage),
                    joint_node
                )
            # for each upstream transport, add an edge from that transport's joint def to this joint def
            for pipe in d_pipes:
                G.add_edge(
                    (cluster_naming(pipe), joint_naming(stage)),
                    joint_node
                )

    # Step 3: add trunk edges  
    for trunk in trunks:
        # add edge from trunk def joint to trunk app
        G.add_edge(
            (cluster_naming(trunk), joint_naming("definition")),
            (trunk, "approval")
        )

        # add edge from trunk def joint to app of every cap/trans project dependency
        caps, pipes = everything_upstream(trunk, pipe_downstream, capture_pipe)
        for cap in caps:
            G.add_edge(
                (cluster_naming(trunk), joint_naming("definition")),
                (cap, "approval")
            )
        for pipe in pipes:
            G.add_edge(
                (cluster_naming(trunk), joint_naming("definition")),
                (pipe, "approval")
            )
        # add edge from trunk FID joint to storage cluster FID joint
        stor = project_storage(trunk, "transport", pipe_downstream, capture_pipe)
        G.add_edge(
            (cluster_naming(trunk), joint_naming("approval")),
            (cluster_naming(stor), joint_naming("approval"))
        )

    # Step 4: add edges for cons -> comm for trans/cap, gating edges for commissioning
    for capture in capture_volumes:
        G.add_edge(
            (capture, "construction"),
            (capture, "commissioning")
        )
        G.add_edge(
            (capture_pipe[capture], "commissioning"),
            (capture, "commissioning")
        )
    
    for transport in transport_volumes:
        G.add_edge(
            (transport, "construction"),
            (transport, "commissioning")
        )
        G.add_edge(
            (pipe_downstream[transport], "commissioning"),
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
        or G.nodes[node].get("stage") == "definition joint node")

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
        
        # this handles actual inputs from the joint nodes
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
        
        if G.nodes[node].get("abandoned") is not None:
            continue # abandoned nodes do not participate in scheduling

        # if we encounter a joint node 
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

#==================================================================
# CALCULATING PROJECT DELAYS AND HELPER METHODS
#==================================================================

def delay_at_joint(G: nx.DiGraph, joint, party_node):
    return G.nodes[joint]["EF"] - G.nodes[party_node]["EF"]

def cluster_owner(child_joint_node):
    '''
    Args: joint node
    Returns: name of transport/storage project defining the joint node
    '''
    cluster_name = child_joint_node[0]
    owner_name = cluster_name.replace(" cluster", "")
    return owner_name

def get_tech(G: nx.DiGraph, project):
    return G.nodes[(project, "definition")]["tech"] # this isn't very elegant (I hard-coded for def) but I think it works

#==================================================================
# PROJECT ABANDONMENT 
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

def already_abandoned(G: nx.DiGraph, node):
    '''
    checks if a project has already been abandoned
    Returns True if project has been abandoned
    '''
    return G.nodes[node]["abandoned"] is not None

def mark_own_abandonment(G:nx.DiGraph, owning_proj):
    # capture case
    if get_tech(G, owning_proj) == "capture":
        for s in ["definition", "approval", "construction", "commissioning"]:
                G.nodes[(owning_proj, s)]["abandoned"] = True
    # transport case
    elif get_tech(G, owning_proj) == "transport":
        # mark its own nodes with abandoned = True
        for s in ["definition", "approval", "construction", "commissioning"]:
            G.nodes[(owning_proj, s)]["abandoned"] = True 
        # separate case for joint nodes because of different naming
        for s in [joint_naming("definition"), joint_naming("approval")]:
            G.nodes[(cluster_naming(owning_proj), s)]["abandoned"] = True
    elif get_tech(G, owning_proj) == "storage":
        for s in ["definition", "approval", "construction", "commissioning"]:
            G.nodes[(owning_proj, s)]["abandoned"] = True 
            G.nodes[(cluster_naming(owning_proj), "FID joint node")]["abandoned"] = True

def mark_all_abandonment(G: nx.DiGraph, owning_proj, pipe_downstream=project_data.PIPE_DOWNSTREAM, capture_pipe=project_data.CAPTURE_PIPE):
    '''
    Description: sets "abandoned" = True on graph nodes so they are skipped by the CPM
    Args: Graph, storage_cluster, transport_cluster, project, stage
    Returns: marks nodes as abandoned
    '''
    mark_own_abandonment(G, owning_proj)
    if get_tech(G, owning_proj) != "capture":
        caps, pipes = everything_upstream(owning_proj, pipe_downstream, capture_pipe)
        for proj in caps + pipes:
            mark_own_abandonment(G, proj)

def record_abandonment(project, tech, stage, abandoned_t, abandoned_s, abandoned_c, pipe_downstream=project_data.PIPE_DOWNSTREAM, capture_pipe=project_data.CAPTURE_PIPE):
    '''
    records the project as abandoned (include stage of abandonment) in dictionaries (book-keeping)
    '''
    if tech == "capture":
        abandoned_c[project] = stage
    
    elif tech == "transport":
        abandoned_t[project] = stage
        # record all dependent transport and capture as abandoned
        caps, pipes = everything_upstream(project, pipe_downstream, capture_pipe)
        for cap in caps:
            if cap not in abandoned_c:
                abandoned_c[cap] = stage
        for pipe in pipes:
            if pipe not in abandoned_t:
                abandoned_t[pipe] = stage

    elif tech == "storage":
        abandoned_s[project] = stage
        # record all dependent transport and capture as abandoned
        caps, pipes = everything_upstream(project, pipe_downstream, capture_pipe)
        for cap in caps:
            if cap not in abandoned_c:
                abandoned_c[cap] = stage
        for pipe in pipes:
            if pipe not in abandoned_t:
                abandoned_t[pipe] = stage

def time_slip_at_gate(G: nx.DiGraph, 
                      rng, 
                      joint_node,
                      abandoned_t, abandoned_s, abandoned_c,
                      base_rate = BASE_RATE, 
                      max_rate = MAX_RATE,
                      capture_tolerance = CAPTURE_TOLERANCE, 
                      transport_tolerance = TRANSPORT_TOLERANCE,
                      storage_tolerance = STORAGE_TOLERANCE, 
                      late_penalty = LATE_PENALTY, 
                      pipe_downstream = project_data.PIPE_DOWNSTREAM,
                      capture_pipe = project_data.CAPTURE_PIPE
                      ):
    '''
    Calculates time-delays and rolls abandonment at this joint node
    '''
    # iterate through all the predecessors of the joint node
    for node in G.predecessors(joint_node):
        # if the node has already been marked abandoned, we skip it
        if already_abandoned(G, node):
            continue
        
        # get the stage
        stage = G.nodes[joint_node]["stage"]

        # get the delay of each predecessor at the joint node
        delay = delay_at_joint(G, joint_node, node)

        # get tech to calculate attrition probability
        if G.nodes[node]["tech"] == "joint":
            owning_project = cluster_owner(node)
            tech = "transport"
        
        else:
            tech = G.nodes[node]["tech"]
            owning_project = node[0]
        
        prob = calculate_attrition_probability(delay, tech, base_rate, max_rate,
                                               capture_tolerance, transport_tolerance, storage_tolerance, late_penalty)
        
        if rng.random() < prob:
            mark_all_abandonment(G, owning_project, pipe_downstream, capture_pipe)
            record_abandonment(owning_project, tech, stage, abandoned_t, abandoned_s, abandoned_c, pipe_downstream, capture_pipe)

def threshold_failed(G, joint_node):
    return G.nodes[joint_node]["below_threshold"] == True

def threshold_test_at_gate(G: nx.DiGraph, joint_node, owner, stage, abandoned_t, abandoned_s, abandoned_c, pipe_downstream, capture_pipe):
    '''
    If threshold test is not met, return True and collapse the owner of the joint_node
    Otherwise, return False
    '''
    if threshold_failed(G, joint_node):
        mark_all_abandonment(G, owner, pipe_downstream, capture_pipe)
        record_abandonment(owner, get_tech(G, owner), stage, abandoned_t, abandoned_s, abandoned_c, pipe_downstream, capture_pipe)
        return True

    return False

def traversal_order(G):
    '''
    Produces an ordered list of pipes (and storage) in leaf-to-root order 
    Helper method for apply attrition
    '''
    traverse = []
    for node in nx.topological_sort(G):
        if G.nodes[node]["stage"] == "FID joint node":
            project = cluster_owner(node)
            traverse.append(project)

    return traverse

def apply_attrition(G: nx.DiGraph, 
                    pipe_downstream=project_data.PIPE_DOWNSTREAM, 
                    capture_pipe = project_data.CAPTURE_PIPE,
                    base_rate=BASE_RATE, 
                    threshold_frac=THRESHOLD_FRAC,
                    max_rate=MAX_RATE, 
                    capture_tolerance=CAPTURE_TOLERANCE,
                    transport_tolerance=TRANSPORT_TOLERANCE, 
                    storage_tolerance=STORAGE_TOLERANCE,
                    late_penalty=LATE_PENALTY, 
                    replication_seed = 0):
    '''
    Apply attrition to the graph
    '''
    rng = random.Random(SEED + replication_seed)
    abandoned_t, abandoned_s, abandoned_c = {}, {}, {}

    order = traversal_order(G)
    
    #-------- Definition joint nodes ----------
    for project in order:
        if project in abandoned_t or project in abandoned_s:
            continue
        if get_tech(G, project) == "storage":
            continue # because storage projects don't get their own def joint node
        def_joint_node = (cluster_naming(project), "definition joint node")
        time_slip_at_gate(G, rng, def_joint_node, abandoned_t, abandoned_s, abandoned_c, 
                          base_rate, max_rate, capture_tolerance, transport_tolerance, 
                          storage_tolerance, late_penalty, pipe_downstream, capture_pipe)
        CPM(G, threshold_frac)
        if threshold_test_at_gate(G, def_joint_node, project, "definition joint node", 
                                  abandoned_t, abandoned_s, abandoned_c, pipe_downstream, capture_pipe):
            continue # if we fail the threshold test, the entire cluster collapses

    #-------- FID joint nodes ----------
    for project in order:
        if project in abandoned_t or project in abandoned_s:
            continue
        FID_joint_node = (cluster_naming(project), "FID joint node")
        time_slip_at_gate(G, rng, FID_joint_node, abandoned_t, abandoned_s, abandoned_c, 
                          base_rate, max_rate, capture_tolerance, transport_tolerance, 
                          storage_tolerance, late_penalty, pipe_downstream, capture_pipe)
        CPM(G, threshold_frac)
        if threshold_test_at_gate(G, FID_joint_node, project, "FID joint node", 
                                  abandoned_t, abandoned_s, abandoned_c, pipe_downstream, capture_pipe):
            continue

    return abandoned_s, abandoned_t, abandoned_c

#==================================================================
# RUNNING THE MODEL
#==================================================================

def buildmodel(replication_seed=0, sampling=False, trunks = project_data.TRUNKS,
               pipe_downstream = project_data.PIPE_DOWNSTREAM, capture_pipe = project_data.CAPTURE_PIPE, 
               capture_durations=project_data.CAPTURE, capture_volumes=project_data.CAPTURE_VOLUMES,
               storage_durations=project_data.STORAGE, storage_volumes=project_data.STORAGE_VOLUMES,
               transport_durations=project_data.TRANSPORT, transport_volumes=project_data.TRANSPORT_VOLUMES,
               dist_override="lognormal"):
    '''
    Description: runs the process 1) building graph and add nodes
    -> 2) add intra-project edges
    -> 3) add inter-project edges
    Returns: G
    '''

    G = projGraph(replication_seed, sampling,
                  pipe_downstream, capture_pipe, capture_durations, capture_volumes,
                  storage_durations, storage_volumes,
                  transport_durations, transport_volumes, dist_override)
    projEdges(G, pipe_downstream, capture_pipe, capture_volumes, storage_volumes, transport_volumes, trunks)

    return G

#==================================================================
# MONTE CARLO
#==================================================================

def monte_carlo(n_reps, 
                sampling=True, 
                trunks = project_data.TRUNKS,
                pipe_downstream=project_data.PIPE_DOWNSTREAM,
                capture_pipe=project_data.CAPTURE_PIPE,
                base_rate=BASE_RATE, 
                threshold_frac=THRESHOLD_FRAC,
                max_rate=MAX_RATE, 
                capture_tolerance=CAPTURE_TOLERANCE,
                transport_tolerance=TRANSPORT_TOLERANCE, 
                storage_tolerance=STORAGE_TOLERANCE,
                capture_durations=project_data.CAPTURE, 
                capture_volumes=project_data.CAPTURE_VOLUMES,
                storage_durations=project_data.STORAGE, 
                storage_volumes=project_data.STORAGE_VOLUMES,
                transport_durations=project_data.TRANSPORT, 
                transport_volumes=project_data.TRANSPORT_VOLUMES,
                late_penalty = LATE_PENALTY,
                dist_override = "lognormal"):
    results = []

    num_cap = len(capture_volumes)
    num_trans = len(transport_volumes)
    num_stor = len(storage_volumes)

    for rep in range(n_reps):
        G = buildmodel(replication_seed=rep, sampling=sampling,
                       trunks=trunks, pipe_downstream=pipe_downstream, capture_pipe=capture_pipe, 
                       capture_durations=capture_durations,
                       capture_volumes=capture_volumes, storage_durations=storage_durations,
                       storage_volumes=storage_volumes, transport_durations=transport_durations,
                       transport_volumes=transport_volumes, dist_override=dist_override)

        CPM(G, threshold_frac)

        a_s, a_t, a_c = apply_attrition(G, pipe_downstream, capture_pipe, base_rate, threshold_frac,
                                         max_rate, capture_tolerance, transport_tolerance, storage_tolerance,
                                         late_penalty, replication_seed = rep)

        finite = [G.nodes[n]["EF"] for n in G.nodes
                if G.nodes[n]["EF"] != float("inf") and G.nodes[n]["abandoned"] is None]

        # getting the final survived volume from unabandoned storage FID joint nodes
        final_vol = 0
        for storage in storage_volumes:
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
            if stages == "definition joint node":
                c_def += 1
            elif stages == "FID joint node":
                c_app += 1
        
        t_def = 0
        t_app = 0
        for captures, stages in a_t.items():
            if stages == "definition joint node":
                t_def += 1
            elif stages == "FID joint node":
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
    if len(c_abandon_at_app) != 0:
        avg_c_abandon_at_app = cum_c_abandon_at_app/len(c_abandon_at_app)
    else:
        avg_c_abandon_at_app = 0

    cum_t_abandon_at_app = 0
    for rate in t_abandon_at_app:
        cum_t_abandon_at_app += rate
    if len(t_abandon_at_app) != 0:
        avg_t_abandon_at_app = cum_t_abandon_at_app/len(t_abandon_at_app)
    else:
        avg_t_abandon_at_app = 0
    
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
    results2 = monte_carlo(100, sampling = True, base_rate=0.05)
    print(analyze_monte_carlo(results2))

    G = buildmodel()
    
    print(immediate_upstream_project("projS1"))
    print(immediate_upstream_project("projT1"))
    print(everything_upstream("projS1"))
    print(everything_upstream("projT1"))
    
