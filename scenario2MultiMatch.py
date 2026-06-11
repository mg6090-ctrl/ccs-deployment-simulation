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

# dictionary for TS projects
TS = {
    "projS1":  {"definition": 48, "approval": 36, "construction": 72},  
    "projS2":  {"definition": 30, "approval": 50, "construction": 64},  
    "projS3":  {"definition": 48, "approval": 24, "construction": 60},   
    "projS4":  {"definition": 14, "approval": 20, "construction": 40},   
    "projS5":  {"definition": 48, "approval": 32, "construction": 60},   
    "projS6":  {"definition": 72, "approval": 48, "construction": 110}, 
    "projS7":  {"definition": 22, "approval": 32, "construction": 46},   
    "projS8":  {"definition": 38, "approval": 28, "construction": 56},   
    "projS9":  {"definition": 60, "approval": 40, "construction": 88},   
    "projS10": {"definition": 58, "approval": 46, "construction": 86},   
    "projS11": {"definition": 30, "approval": 38, "construction": 52},   
    "projS12": {"definition": 50, "approval": 30, "construction": 70},   
}

# clusters (1:multiple matching, TS -> [capture])
CLUSTERS = {
    "projS1":  ["projC1", "projC2"],    
    "projS2":  ["projC3", "projC4", "projC5"],    
    "projS3":  ["projC6"],    
    "projS4":  ["projC7", "projC8", "projC9", "projC10"],    
    "projS5":  ["projC11", "projC12"],   
    # "projS6":  ["projC12"],    
    # "projS7":  ["projC7"],    
    # "projS8":  ["projC8"],    
    # "projS9":  ["projC9"],    
    # "projS10": ["projC10"],   
    # "projS11": ["projC11"],   
    # "projS12": ["projC12"],   
}

# seed for shuffling before frac_split 
SEED = 42

# constants for the abandonment function
BASE_RATE = 0.05
MAX_RATE = 0.7
CAPTURE_TOLERANCE = 24
TS_TOLERANCE = 36
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
    # this method works for 1:multiple already
    def intra_nodes():
        # make one large graph
        G = nx.DiGraph()

        for ts, captures in CLUSTERS.items():
            # cluster number is determined by ts project
            cluster =  ts + " cluster"

            # add ts nodes
            for stage, dur in TS[ts].items():
                G.add_node(
                    (ts, stage),
                    duration = dur,
                    stage = stage,
                    cluster = cluster,
                    tech = "TS",
                    ES = 0.0,
                    EF = 0.0,
                    abandoned = None
                )

            # add ts commissioning node
            G.add_node(
                (ts, "commissioning"),
                duration = 0,
                stage = "commissioning",
                cluster = cluster,
                tech = "TS",
                ES = 0.0,
                EF = 0.0,
                abandoned = None
            )

            for capture in captures:
                # add capture nodes
                for stage, dur in CAPTURE[capture].items():
                    G.add_node(
                        (capture, stage),
                        duration = dur,
                        stage = stage,
                        cluster = cluster,
                        tech = "Capture",
                        ES = 0.0,
                        EF = 0.0,
                        abandoned = None
                    )
            
                # add capture commissioning node
                G.add_node(
                    (capture, "commissioning"),
                    duration = 0.0,
                    stage = "commissioning",
                    cluster = cluster,
                    tech = "Capture",
                    ES = 0.0,
                    EF = 0.0,
                    abandoned = None
                )

        return G

    # helper method for drawing intra-project edges only
    # this method works for 1:multiple already
    def intra_edges(G: nx.DiGraph):
        def graphEdges(G, pid):
            for a, b in zip(STAGES4[:-1], STAGES4[1:]):
                G.add_edge((pid, a), (pid, b))

        for ts, captures in CLUSTERS.items():
            graphEdges(G, ts)
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

def projGraph():
    '''
    Description: creating graph and adding nodes
    Returns: directed acyclic graph G
    '''
    # make one large graph
    G = nx.DiGraph()

    for ts, captures in CLUSTERS.items():
        # cluster number is determined by ts project
        cluster =  ts + " cluster"

        # add ts nodes
        for stage, dur in TS[ts].items():
            G.add_node(
                (ts, stage),
                duration = dur,
                stage = stage,
                cluster = cluster,
                tech = "TS",
                ES = 0.0,
                EF = 0.0,
                abandoned = None
            )

        # add commissioning node for TS
        G.add_node(
            (ts, "commissioning"),
            duration = 0.0,
            stage = "commissioning",
            cluster = cluster,
            tech = 'TS',
            ES = 0.0,
            EF = 0.0,
            abandoned = None
        )

        # add cluster-wide FID node (defined by TS)
        G.add_node(
            (ts, "FID joint node"), 
            duration = 0.0,
            stage = "FID joint node",
            cluster = cluster,
            tech = "joint",
            ES = 0.0,
            EF = 0.0,
            abandoned = None
        )

        for capture in captures:
            # add capture nodes
            for stage, dur in CAPTURE[capture].items():
                G.add_node(
                    (capture, stage),
                    duration = dur,
                    stage = stage,
                    cluster = cluster,
                    tech = "Capture",
                    ES = 0.0,
                    EF = 0.0,
                    abandoned = None
                )
            
            # add commissioning node for capture
            G.add_node(
                (capture, "commissioning"),
                duration = 0.0,
                stage = "commissioning",
                cluster = cluster,
                tech = 'Capture',
                ES = 0.0,
                EF = 0.0,
                abandoned = None
            )

            # add joint nodes
            for stage in ['definition']:
                joint_name = joint_naming(stage)
                G.add_node(
                    (capture, joint_name),
                    duration = 0.0,
                    stage = joint_name,
                    capture = capture,
                    cluster = cluster,
                    tech = "joint",
                    ES = 0.0,
                    EF = 0.0,
                    abandoned = None
                )
    
    return G

def projEdges(G: nx.DiGraph):
    '''
    Description: adds intra-project edges to G
    Args: G
    '''
    for ts in CLUSTERS.keys():
        # edge from ts app to FID joint node
        G.add_edge(
            (ts, "approval"),
            (ts, joint_naming("approval"))
        )

        captures = CLUSTERS[ts]
        for capture in captures:
            # edge from ts def to joint def
            G.add_edge(
                (ts, "definition"),
                (capture, joint_naming("definition"))
            )

            # edge from cap def to joint def
            G.add_edge(
                (capture, "definition"),
                (capture, joint_naming("definition"))
            )

            # edge from joint def to ts app
            G.add_edge(
                (capture, joint_naming("definition")),
                (ts, "approval")
            )

            # edge from joint def to cap app
            G.add_edge(
                (capture, joint_naming("definition")),
                (capture, "approval")
            )

            # edge from cap app to joint FID
            G.add_edge(
                (capture, "approval"),
                (ts, joint_naming("approval"))
            )

            # edge from joint FID to cap cons
            G.add_edge(
                (ts, joint_naming("approval")),
                (capture, "construction")
            )

            # edge from joint FID to ts cons 
            G.add_edge(
                (ts, joint_naming("approval")),
                (ts, "construction")
            )

            # edge from capture construction to capture commissioning
            G.add_edge(
                (capture, "construction"),
                (capture, "commissioning")
            )
            # edge from ts construction to capture commissioning
            G.add_edge(
                (ts, "construction"),
                (capture, "commissioning")
            )
            # edge from ts construction to ts commissioning
            G.add_edge(
                (ts, "construction"),
                (ts, "commissioning")
            )

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

# CURRENTLY DORMANT METHOD (DELAY IS STAGE + OWN BUNDLED TOGETHER)
def behind_schedule_delay(G_actual, G_base, project, stage):
    '''
     Total lateness at the moving-on point: how far past its unconstrained
    baseline a party clears this stage (reads the joint, so it bundles
    partner-waiting now and own-overruns once durations are stochastic).
    NOTE: currently equals stage_partner_wait; the two diverge only once
    stochastic durations introduce own-overruns. Decompose-vs-bundle TBD
    with Dr Greig
    Args: node (project, stage); expectation: do not enter a joint node because we need to get 
    this slip time for the TS and capture projects; it does not make sense to calculate it for 
    a joint node because joint nodes do not exist in the base graph
    Returns: slip time 
    '''

    node = (project, stage)

    base_EF = G_base.nodes[node]["EF"]

    # corresponding joint node for this stage in the graph with interdependencies is the next node
    # if (capture, definition) -> want EF of def joint node
    # if (capture, approval) -> want EF of app joint node
    # if (capture, cons) -> want EF of commissioning joint node 
    
    targets = target_node(G_actual, project, stage)
    actual_EF = max(G_actual.nodes[t]["EF"] for t in targets)

    # actual_EF = G_actual.node[node]["EF"]
    slip_time = actual_EF - base_EF
    
    return base_EF, actual_EF, slip_time

def cluster_ts(project):
    '''
    Description: returns the cluster (keyed by ts project) that a project is part of
    Args: project
    Returns: name of the ts project that defines the cluster
    '''
    if project in CLUSTERS: # checking if the project is a ts project (just return itself)
        return project
    for ts, caps in CLUSTERS.items():
        if project in caps:
            return ts
    else:
        raise ValueError(f"{project} does not exist")

def target_node(G: nx.DiGraph, project, stage):
    '''
    Description: gets the target node (next node) give the current node
    Args: Graph, project, stage, capture (optional) 
    Returns: a list of target nodes
    '''
    # Many-to-one -> set of joints, aggregate per sync rule (TBD with mentor + data).
    ts = cluster_ts(project)
    is_ts = G.nodes[(project, stage)]["tech"] == "TS"

    if stage == "construction":
        return ([(project, "commissioning")])
    
    elif stage == "approval":
        return ([(ts, joint_naming(stage))])
    
    elif stage == "definition":
        if is_ts:
            return ([(cap, joint_naming(stage)) for cap in CLUSTERS[ts]])
        else:
            return ([(project, joint_naming(stage))])
        
    else:
        raise ValueError(f"{stage} is not a valid stage")

def stage_delay(G, project, stage):
    '''
    Description: calculates delay at a specific stage
    Args: constrained graph with interdepencies, node
    Returns: the stage delay at that specific node 
    '''
    # Looks up target node via target_node(), allows it to accommodate multiple successors
    # robust for 1: multiple configuration 
    targets = target_node(G, project, stage)
    max_delay = 0
    for target in targets:
        delay = G.nodes[target]["EF"] - G.nodes[(project, stage)]["EF"]
        if delay > max_delay:
            max_delay = delay
    
    return max_delay

def stage_partner_wait(G: nx.DiGraph, node):
    '''
    Description: returns the cumulative and per-stage wait time for partner at the node
    Args: constrained graph with interdepencies, node
    Returns: cumulative wait time of that project up to (and including) that node
    '''
    # for each node, calculate the cumulative time spent waiting for the other actor up to (and 
    # including that stage).

    project, current_stage = node[0], node[1]
    
    cumulative = 0.0
    for stage in STAGES:
        cumulative += stage_delay(G, project, stage)
        if stage == current_stage:
            break
    return cumulative

#==================================================================
# PROJECT ABANDONMENT
#==================================================================

def calculate_attrition_probability(delay, tech):
    '''
    Description: returns attrition probability based on delay and tech
    Principle: slip past cumulative partner wait baseline
    Args: delay (calculated from slip_compute) and tech
    Returns: probability
    '''
    if tech == "Capture":
        tolerance = CAPTURE_TOLERANCE
    else:
        tolerance = TS_TOLERANCE
    
    if delay < tolerance:
        return BASE_RATE
    else:
        delay_factor = (delay - tolerance)/SCALE
        return min(MAX_RATE, BASE_RATE + (MAX_RATE - BASE_RATE) * (1 - np.exp(-delay_factor)))

def mark_abandonment(G, ts, captures, stage):
    '''
    Description: marks all nodes of all projects in a cluster as abandoned (annotates stage of 
    abandonment)
    Args: Graph, ts (defines the cluster), list of captures in that cluster, stage
    Returns: marks nodes as abandoned
    '''
    for s in ["definition", "approval"]:
        G.nodes[(ts, s)]["abandoned"] = stage
    
    G.nodes[(ts, joint_naming("approval"))]["abandoned"] = stage
    G.nodes[(ts, "commissioning")]["abandoned"] = stage

    for capture in captures:
        for s in ["definition", "approval"]:
            G.nodes[(capture, s)]["abandoned"] = stage
        G.nodes[(capture, joint_naming("definition"))]["abandoned"] = stage
        G.nodes[(capture, "commissioning")]["abandoned"] = stage

def apply_attrition(G: nx.DiGraph):
    # random seed
    rng = random.Random(SEED)

    # empty list for storing abandoned_clusters
    abandoned_clusters = {}
    
    for stage in STAGES:
        for ts, captures in CLUSTERS.items():

            if ts in abandoned_clusters:
                continue

            ts_wait = stage_partner_wait(G, (ts, stage))
            p_ts = calculate_attrition_probability(ts_wait, "TS")
            cluster_dies = rng.random() < p_ts # here we roll the dice once for TS and each capture
            # KEEP AN EYE OUT FOR THE MATH HERE — AM I DOUBLE ROLLING? WLL NEED TO CONFIRM LATER

            if not cluster_dies:
                for cap in captures:
                    capture_wait = stage_partner_wait(G, (cap, stage))
                    p_capture = calculate_attrition_probability(capture_wait, "Capture")
                
                    # abandonment criteria
                    if rng.random() < p_capture:
                        cluster_dies = True
                        break
       
            if cluster_dies:
                abandoned_clusters[ts] = stage
                mark_abandonment(G, ts, captures, stage)

    return abandoned_clusters

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

def visualize(G, cluster_filter=None):
    '''
    Draw the DAG left-to-right by stage. Optionally pass a TS id to draw just one cluster.
    '''
    # x-coordinate per stage column (left to right)
    stage_x = {
        "definition": 0,
        "definition joint node": 1,
        "approval": 2,
        "FID joint node": 3,
        "construction": 4,
        "commissioning": 5,
    }

    # pick nodes (one cluster or all)
    if cluster_filter:
        nodes = [n for n in G.nodes if G.nodes[n]["cluster"] == cluster_filter + " cluster"]
    else:
        nodes = list(G.nodes)

    # assign positions: x by stage, y spread by project
    pos = {}
    # group projects to give each a y-band
    projects = sorted({n[0] for n in nodes})
    y_of = {p: i for i, p in enumerate(projects)}
    for n in nodes:
        proj, stage = n
        x = stage_x.get(stage, 0)
        y = y_of[proj]
        pos[n] = (x, y)

    # color by tech
    color_map = {"TS": "#4C72B0", "Capture": "#55A868", "joint": "#C44E52"}
    colors = [color_map.get(G.nodes[n]["tech"], "#888888") for n in nodes]

    sub = G.subgraph(nodes)
    plt.figure(figsize=(14, 8))
    nx.draw(
        sub, pos,
        node_color=colors,
        node_size=1500,
        with_labels=True,
        labels={n: f"{n[0]}\n{n[1][:8]}" for n in nodes},  # short labels
        font_size=6,
        arrows=True,
        edge_color="#aaaaaa",
    )
    plt.title(f"CCS DAG{' — ' + cluster_filter if cluster_filter else ''}")
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

# checking that G is a DAG
# print("Checking if G is DAG: " + str(nx.is_directed_acyclic_graph(G)))

# inspecting the nodes of G 
# print("Printing out nodes of the graph: ")
# for n in G.nodes:
 # print(n, G.nodes[n])

print(list(G_actual.predecessors(("projS1", "approval"))))
print(list(G_actual.predecessors(("projC1", "approval"))))
print(list(G_actual.predecessors(("projS2", "FID joint node"))))
print(list(G_actual.neighbors(("projS2", "FID joint node"))))

print("Running tests")
print(apply_attrition(G_actual))
print(stage_partner_wait(G_actual, ("projC5", "definition")))
print(calculate_attrition_probability(0, "Capture"))
print(calculate_attrition_probability(0, "TS"))
print(stage_partner_wait(G_actual, ("projC6", "construction")))
print(list(G_actual.successors(("projS5", "construction"))))
visualize(G_actual, cluster_filter="projS2")