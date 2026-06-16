import networkx as nx
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

# seed for shuffling before frac_split 
SEED = 42

# constants for the abandonment function
THRESHOLD_FRAC = 0.5
BASE_RATE = 0.05
MAX_RATE = 0.7
CAPTURE_TOLERANCE = 24
STORAGE_TOLERANCE = 36
TRANSPORT_TOLERANCE = 24
SCALE = 60

#==================================================================
# BUILDING THE BASE GRAPH (NO INTERDEPENDENCIES)
#==================================================================

def make_base_graph():
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
                    duration = dur,
                    stage = stage,
                    tech = "storage",
                    ES = 0.0,
                    EF = 0.0,
                    volume = STORAGE_VOLUMES[storage],
                    s_cluster = storage_cluster,
                    transport_cluster = None,
                    abandoned = None
                )
            
            # add storage commissioning node
            G.add_node(
                (storage, "commissioning"),
                duration = 0,
                stage = "commissioning",
                tech = "storage",
                ES = 0.0,
                EF = 0.0,
                volume = STORAGE_VOLUMES[storage],
                s_cluster = storage_cluster,
                transport_cluster = None,
                abandoned = None
            )

            for transport, captures in transport_clusters.items():
                # cluster number is determined by ts project
                transport_cluster =  transport + " cluster"

                # add transport nodes
                for stage, dur in TRANSPORT[transport].items():
                    G.add_node(
                        (transport, stage),
                        duration = dur,
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
                    duration = 0,
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
                            duration = dur,
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

def projGraph():
    '''
    Description: creating graph and adding nodes
    Returns: directed acyclic graph G
    '''
    # make one large graph
    G = nx.DiGraph()
        
    for storage, transport_clusters in CLUSTERS.items():
        # layer 1: storage nodes
        storage_cluster = cluster_naming(storage) # naming the overarching storage cluster

        for stage, dur in STORAGE[storage].items():
            G.add_node(
                (storage, stage),
                duration = dur,
                stage = stage,
                tech = "storage",
                ES = 0.0,
                EF = 0.0,
                volume = STORAGE_VOLUMES[storage],
                actual_volume = 0.0,
                committed_volume = 0.0,
                s_cluster = storage_cluster,
                transport_cluster = None,
                abandoned = None
                )
            
        # add storage commissioning node
        G.add_node(
            (storage, "commissioning"),
            duration = 0,
            stage = "commissioning",
            tech = "storage",
            ES = 0.0,
            EF = 0.0,
            volume = STORAGE_VOLUMES[storage],
            actual_volume = 0.0,
            committed_volume = 0.0,
            s_cluster = storage_cluster,
            transport_cluster = None,
            abandoned = None
        )

        # add storage joint FID node
        G.add_node(
            (storage_cluster, "FID joint node"),
            duration = 0.0,
            stage = "FID joint node",
            tech = "joint",
            ES = 0.0,
            EF = 0.0,
            volume = STORAGE_VOLUMES[storage],
            actual_volume = 0.0,
            committed_volume = 0.0,
            t_cluster = None,
            s_cluster = storage_cluster,
            below_threshold = None,
            abandoned = None
        )

        for transport, captures in transport_clusters.items():
            # cluster number is determined by ts project
            transport_cluster =  cluster_naming(transport)

            # add transport nodes
            for stage, dur in TRANSPORT[transport].items():
                G.add_node(
                    (transport, stage),
                    duration = dur,
                    stage = stage,
                    tech = "transport",
                    ES = 0.0,
                    EF = 0.0,
                    volume = TRANSPORT_VOLUMES[transport],
                    actual_volume = 0.0,
                    committed_volume = 0.0,
                    t_cluster = transport_cluster,
                    s_cluster = storage_cluster,
                    abandoned = None
                )
            
            # adding a volumetric-gating node before transport approval
            G.add_node(
                (transport, "approval joint node"),
                duration = 0.0,
                stage = "approval joint node",
                tech = "joint",
                ES = 0.0,
                EF = 0.0,
                volume = TRANSPORT_VOLUMES[transport],
                actual_volume = 0.0,
                committed_volume = 0.0,
                t_cluster = transport_cluster,
                s_cluster = storage_cluster,
                below_threshold = None,
                abandoned = None
            )

            # add transport commissioning node
            G.add_node(
                (transport, "commissioning"),
                duration = 0,
                stage = "commissioning",
                tech = "transport",
                ES = 0.0,
                EF = 0.0,
                volume = TRANSPORT_VOLUMES[transport],
                actual_volume = 0.0,
                committed_volume = 0.0,
                t_cluster = transport_cluster,
                s_cluster = storage_cluster,
                abandoned = None
            )

            # transport cluster joint FID node
            G.add_node(
                (transport_cluster, "FID joint node"),
                duration = 0.0,
                stage = "FID joint node",
                tech = "joint",
                ES = 0.0,
                EF = 0.0,
                volume = TRANSPORT_VOLUMES[transport],
                actual_volume = 0.0,
                committed_volume = 0.0,
                t_cluster = transport_cluster,
                s_cluster = storage_cluster,
                below_threshold = None,
                abandoned = None
            )

            for capture in captures:
                # add capture nodes
                for stage, dur in CAPTURE[capture].items():
                    G.add_node(
                        (capture, stage),
                        duration = dur,
                        stage = stage,
                        tech = "capture",
                        ES = 0.0,
                        EF = 0.0,
                        volume = CAPTURE_VOLUMES[capture],
                        actual_volume = 0.0,
                        committed_volume = 0.0,
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
                    actual_volume = 0.0,
                    committed_volume = 0.0,
                    t_cluster = transport_cluster,
                    s_cluster = storage_cluster,
                    abandoned = None
                )

                # joint nodes within the transport cluster (between transport and capture)
                for stage in ['definition']:
                    joint_name = joint_naming(stage)
                    G.add_node(
                        (capture, joint_name),
                        duration = 0.0,
                        stage = joint_name,
                        tech = "joint",
                        ES = 0.0,
                        EF = 0.0,
                        volume = CAPTURE_VOLUMES[capture], # this needs to be cap vol
                        actual_volume = CAPTURE_VOLUMES[capture], # this is set because def joints sync (aren't threshold)
                        committed_volume = 0.0,
                        t_cluster = transport_cluster,
                        s_cluster = storage_cluster,
                        abandoned = None
                    )
        
    return G

def projEdges(G: nx.DiGraph):
    '''
    Description: adds intra-project edges to G
    Args: G
    '''
    # edges between the storage nodes
    for storage, transport_clusters in CLUSTERS.items():
       
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
    if not is_threshold_joint:
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

def CPM(G: nx.DiGraph):
    '''
    Description: runs critical path method (CPM), updating ES and EF 
    Args: G
    '''
    for node in nx.topological_sort(G):
        # case where it is a volumetric control gate (FID joint nodes)
        if is_threshold_joint(G, node):
            arrivals = gather_input_specs(G, node)
            capacity = G.nodes[node]["volume"]
            fire = threshold_gating(arrivals, capacity, THRESHOLD_FRAC)
            if fire is None:
                G.nodes[node]["ES"] = float("inf")
                G.nodes[node]["EF"] = float("inf")
                G.nodes[node]["below_threshold"] = True
                G.nodes[node]["actual_volume"] = 0.0
            else:
                G.nodes[node]["ES"] = fire
                G.nodes[node]["EF"] = fire
                G.nodes[node]["below_threshold"] = False
                G.nodes[node]["committed_volume"] = sum(v for v,t in arrivals) # realized throughput
                G.nodes[node]["actual_volume"] = min(
                    G.nodes[node].get("committed_volume"), G.nodes[node].get("volume"))
        
        else:
            preds = list(G.predecessors(node))

            # the new ES is the max of the EF of the preceeding node(s) and the original ES
            max_preds = max((G.nodes[p]["EF"] for p in preds), default = 0.0)

            updated_ES = max(max_preds, G.nodes[node].get("ES", 0.0))
            
            # update the ES and EF of each node
            G.nodes[node]["ES"] = updated_ES
            G.nodes[node]["EF"] = updated_ES + G.nodes[node]["duration"]

#==================================================================
# CALCULATING PROJECT DELAYS (NEED TO EDIT)
#==================================================================

def transport_captures(G: nx.DiGraph, transport):
    for storage, t_cluster in CLUSTERS.items():
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

def stage_delay(G: nx.DiGraph, node):
    '''
    Description: calculates delay at a specific stage
    This code works because joint nodes have duration 0
    Args: constrained graph with interdepencies, node
    Returns: the stage delay at that specific node 
    '''
    # Looks up target node via target_node(), allows it to accommodate multiple successors
    # robust for 1: multiple configuration 
    project, stage = node[0], node[1]
    targets = target_node(G, project, stage)
    max_delay = 0
    for target in targets:
        delay = G.nodes[target]["EF"] - G.nodes[(project, stage)]["EF"]
        if delay > max_delay:
            max_delay = delay
    
    return max_delay

#==================================================================
# PROJECT ABANDONMENT (NEED TO EDIT)
#==================================================================

def calculate_attrition_probability(delay, tech): 
    '''
    Description: returns attrition probability based on delay and tech
    Principle: slip past partner wait baseline
    Args: delay (calculated from stage_delay) and tech
    Returns: probability
    '''
    if tech == "capture":
        tolerance = CAPTURE_TOLERANCE
    elif tech == "transport":
        tolerance = TRANSPORT_TOLERANCE
    else:
        tolerance = STORAGE_TOLERANCE
    
    if delay < tolerance:
        return BASE_RATE
    else:
        delay_factor = (delay - tolerance)/SCALE
        return min(MAX_RATE, BASE_RATE + (MAX_RATE - BASE_RATE) * (1 - np.exp(-delay_factor)))

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
            G.nodes[(project, s)]["abandoned"] = stage
    
    # if it is a transport project -> mark every node in the transport cluster as abandoned
    elif tech == "transport":
        for node in G.nodes():
            if G.nodes[node]["t_cluster"] == transport_cluster:
                G.nodes[node]["abandoned"] = stage

    # if it is a storage project -> mark every node in the storage cluster as abandoned
    elif tech == "storage":
        for node in G.nodes():
            if G.nodes[node]["s_cluster"] == storage_cluster:
                G.nodes[node]["abandoned"] = stage

def threshold_failed(G, joint_node):
    return G.nodes[joint_node]["below_threshold"] == True

def time_slip_at_gate (G: nx.DiGraph, rng, parties, stage, abandoned_t, abandoned_s):
    '''
    For each tech in parties, calculates delays and rolls abandonment at this stage
    '''

def threshold_test_at_gate (G: nx.DiGraph, joint_node, owner, stage, abandoned_t, abandoned_s):
    '''
    If threshold test is not met, collapse the owner of the joint_node 
    '''

        

            
        

#==================================================================
# RUNNING THE MODEL
#==================================================================

def buildmodel():
    '''
    Description: runs the process 1) building graph and add nodes 
    -> 2) add intra-project edges
    -> 3) add inter-project edges
    -> 4) run CPM
    Returns: G
    '''

    G = projGraph()
    projEdges(G)

    return G

#==================================================================
# VISUALIZATION
#==================================================================

def visualize(G, storage_filter=None):
    '''
    Draw the three-tier DAG left-to-right by stage.
    Pass a storage id (e.g. "projS1") to draw just that storage cluster.
    Colors: storage=blue, transport=green, capture=orange, joint=red.
    Abandoned nodes are drawn faded.
    '''
    # x-position per stage (left to right through the lifecycle)
    stage_x = {
        "definition": 0,
        "definition joint node": 1,
        "approval joint node": 2,
        "approval": 3,
        "FID joint node": 4,
        "construction": 5,
        "commissioning": 6,
    }

    # pick nodes: one storage cluster or everything
    if storage_filter:
        sc = storage_filter + " cluster"
        nodes = [n for n in G.nodes if G.nodes[n].get("s_cluster") == sc]
    else:
        nodes = list(G.nodes)

    if not nodes:
        print(f"No nodes found for filter {storage_filter}")
        return

    # assign each project a horizontal band (y), grouped by tier so tiers stack
    tier_order = {"storage": 0, "transport": 1, "capture": 2, "joint": 3}
    # sort projects by tier then name so related nodes sit near each other
    projects = sorted(
        {n[0] for n in nodes},
        key=lambda p: p  # alphabetical; tweak if you want tier-grouped
    )
    y_of = {p: i for i, p in enumerate(projects)}

    pos = {}
    for n in nodes:
        proj, stage = n
        x = stage_x.get(stage, 0)
        y = y_of[proj]
        pos[n] = (x, y)

    # color by tech; fade if abandoned
    color_map = {
        "storage":   "#4C72B0",   # blue
        "transport": "#55A868",   # green
        "capture":   "#DD8452",   # orange
        "joint":     "#C44E52",   # red
    }
    colors, edgecolors = [], []
    for n in nodes:
        tech = G.nodes[n].get("tech", "")
        base = color_map.get(tech, "#888888")
        if G.nodes[n].get("abandoned") is not None:
            colors.append("#DDDDDD")          # faded fill for abandoned
            edgecolors.append(base)            # keep tier color as outline
        else:
            colors.append(base)
            edgecolors.append("black")

    # short labels: project + abbreviated stage
    def short(stage):
        return {
            "definition": "def",
            "approval": "app",
            "construction": "con",
            "commissioning": "com",
            "definition joint node": "defJ",
            "approval joint node": "appJ",
            "FID joint node": "FID",
        }.get(stage, stage[:4])

    labels = {n: f"{n[0]}\n{short(n[1])}" for n in nodes}

    sub = G.subgraph(nodes)
    plt.figure(figsize=(16, max(6, len(projects) * 0.8)))
    nx.draw(
        sub, pos,
        node_color=colors,
        edgecolors=edgecolors,
        linewidths=1.5,
        node_size=1400,
        with_labels=True,
        labels=labels,
        font_size=6,
        arrows=True,
        arrowsize=10,
        edge_color="#bbbbbb",
        width=1.0,
    )

    # column headers along the top
    ymax = len(projects)
    for stage, x in stage_x.items():
        plt.text(x, ymax, short(stage), ha="center", fontsize=8, fontweight="bold")

    title = "CCS three-tier DAG"
    if storage_filter:
        title += f" — {storage_filter} cluster"
    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

#==================================================================
# MAIN (EXECUTION)
#==================================================================

G_actual = buildmodel()
CPM(G_actual)

# make DAG with no joint nodes (no interdependencies) and run CPM
G_base = make_base_graph()
CPM(G_base)

visualize(G_actual, storage_filter="projS1")