import networkx as nx
import random
import numpy as np
import pandas as pd

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
    "projS1":  {"definition": 48, "approval": 36, "construction": 72},   # slow vs fast C1 -> C waits, moderate slip
    "projS2":  {"definition": 30, "approval": 50, "construction": 64},   # ~matched to C2 -> low slip
    "projS3":  {"definition": 48, "approval": 24, "construction": 60},   # slow def vs fast C3 -> C waits
    "projS4":  {"definition": 14, "approval": 20, "construction": 40},   # fast vs slow C4 -> TS waits (tests TS-side)
    "projS5":  {"definition": 48, "approval": 32, "construction": 60},   # ~matched to C5 -> near-zero slip, survives
    "projS6":  {"definition": 72, "approval": 48, "construction": 110},  # very slow vs fast C6 -> extreme slip, dies
    "projS7":  {"definition": 22, "approval": 32, "construction": 46},   # tightly matched to C7 -> low slip, survives
    "projS8":  {"definition": 38, "approval": 28, "construction": 56},   # closely matched to C8 -> low slip
    "projS9":  {"definition": 60, "approval": 40, "construction": 88},   # slow vs fast C9 -> large slip, likely dies
    "projS10": {"definition": 58, "approval": 46, "construction": 86},   # ~matched to slow C10 -> low slip BUT late commission
    "projS11": {"definition": 30, "approval": 38, "construction": 52},   # ~matched to C11 -> low slip
    "projS12": {"definition": 50, "approval": 30, "construction": 70},   # slow vs fast C12 -> moderate-large slip
}

# clusters (1:1 matching, TS -> [capture])
CLUSTERS = {
    "projS1":  ["projC1"],    # moderate mismatch -> moderate abandon risk
    "projS2":  ["projC2"],    # matched -> survives, mid commission
    "projS3":  ["projC3"],    # mismatch -> capture slips
    "projS4":  ["projC4"],    # TS-side slip (capture slow) -> tests TS abandoning
    "projS5":  ["projC5"],    # control: matched -> survives, mid commission
    "projS6":  ["projC6"],    # extreme mismatch -> reliably dies
    "projS7":  ["projC7"],    # matched + small durations -> survives, EARLY commission
    "projS8":  ["projC8"],    # matched -> survives, mid commission
    "projS9":  ["projC9"],    # large mismatch -> likely dies
    "projS10": ["projC10"],   # matched but BIG durations -> survives, LATE commission
    "projS11": ["projC11"],   # matched -> survives, mid commission
    "projS12": ["projC12"],   # moderate-large mismatch -> borderline
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
    def intra_edges(G: nx.DiGraph):
        def graphEdges(G, pid):
            for a, b in zip(STAGES4[:-1], STAGES4[1:]):
                G.add_edge((pid, a), (pid, b))

        for pid in CAPTURE.keys():
            graphEdges(G, pid)

        for pid in TS.keys():
            graphEdges(G, pid)

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
    
    joint_name = stage + " joint node"
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
            for stage in ['definition', 'approval']:
                joint_name = joint_naming(stage)
                G.add_node(
                    (capture, joint_name),
                    duration = 0.0,
                    stage = joint_name,
                    capture = capture,
                    cluster = cluster,
                    tech = "Joint",
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
        captures = CLUSTERS[ts]
        for capture in captures:
            for current_stage, next_stage in zip(STAGES[:-1], STAGES[1:]):
              # adding the edge from the current ts stage to joint node
              G.add_edge(
                  (ts, current_stage),
                  (capture, joint_naming(current_stage))
              )  
              # adding the edge from the current capture stage to joint node
              G.add_edge(
                  (capture, current_stage),
                  (capture, joint_naming(current_stage))
              )
              # adding the edge from the joint node to the next ts stage
              G. add_edge(
                  (capture, joint_naming(current_stage)),
                  (ts, next_stage)
              )
              # adding the edge from the joint node to the next capture stage
              G. add_edge(
                  (capture, joint_naming(current_stage)),
                  (capture, next_stage)
              )
            
            # add joint commissioning node
            # adding the edge from capture construction to capture commissioning
            G.add_edge(
                (capture, "construction"),
                (capture, "commissioning")
            )
            # adding the edge from ts construction to capture commissioning
            G.add_edge(
                (ts, "construction"),
                (capture, "commissioning")
            )
            # add the edge from ts construction to ts commissioning
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

def behind_schedule_delay(node):
    '''
    Description: returns slip time of a given node
    Args: node (project, stage); expectation: do not enter a joint node because we need to get 
    this slip time for the TS and capture projects; it does not make sense to calculate it for 
    a joint node because joint nodes do not exist in the base graph
    Returns: slip time 
    '''

    # make DAG with no joint nodes (no interdependencies) and run CPM
    G_base = make_base_graph()
    CPM(G_base)

    # make DAG with interdependencies (actual) and run CPM
    G_actual = projGraph()
    projEdges(G_actual)
    CPM(G_actual)

    base_EF = G_base.nodes[node]["EF"]

    # corresponding joint node for this stage in the graph with interdependencies is the next node
    # if (capture, definition) -> want EF of def joint node
    # if (capture, approval) -> want EF of app joint node
    # if (capture, cons) -> want EF of commissioning joint node 
    actual_EF = G_actual.nodes[list(G_actual.successors(node))[0]]["EF"]

    # actual_EF = G_actual.node[node]["EF"]
    slip_time = actual_EF - base_EF
    
    return base_EF, actual_EF, slip_time

def stage_delay(G, node):
    '''
    Description: calculates delay at a specific stage
    Args: constrained graph with interdepencies, node
    Returns: the stage delay at that specific node 
    '''
    # KEY ASSUMPTION: EACH NODE ONLY FEEDS INTO ONE SUCCESSOR NODE. THIS WOULD NOT BE 
    # TRUE FOR TS PROJECTS IF WE DON'T HAVE 1:1 MATCHING (RIGHT NOW IT WORKS)
    return G.nodes[list(G.successors(node))[0]]["EF"] - G.nodes[node]["EF"]

def stage_partner_wait(G: nx.DiGraph, node):
    '''
    Description: returns the cumulative and per-stage wait time for partner at the node
    Args: constrained graph with interdepencies, node
    Returns: cumulative wait time of that project up to (and including) that node
    '''
    # for each node, calculate the cumulative time spent waiting for the other actor up to (and 
    # including that stage).

    project = node[0]
    target_stage = node[1]
    cumulative = 0.0
    for stage in STAGES:
        cumulative += stage_delay(G, (project, stage))
        if stage == target_stage:
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

def mark_abandonment(G, ts, capture, stage):
    for s in STAGES:
        G.nodes[(ts, s)]["abandoned"] = stage
        G.nodes[(capture, s)]["abandoned"] = stage
    for s in ["definition", "approval"]:
        G.nodes[(capture, joint_naming(s))]["abandoned"] = stage
    

def apply_attrition(G: nx.DiGraph):
    # random seed
    rng = random.Random(SEED)

    # empty list for storing abandoned_clusters
    abandoned_clusters = {}
    
    for stage in STAGES:
        for ts, captures in CLUSTERS.items():
            if ts in abandoned_clusters:
                continue
            capture = captures[0] # because we are in the 1:1 case right now
            capture_wait = stage_partner_wait(G, (capture, stage))
            ts_wait = stage_partner_wait(G, (ts, stage))

            p_capture = calculate_attrition_probability(capture_wait, "Capture")
            p_ts = calculate_attrition_probability(ts_wait, "TS")

            # abandonment criteria
            if rng.random() < p_capture or rng.random() < p_ts:
                abandoned_clusters[ts] = stage
                mark_abandonment(G, ts, capture, stage)
    
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
    CPM(G)

    return G

#==================================================================
# MAIN (EXECUTION)
#==================================================================

G = buildmodel()

# checking that G is a DAG
# print("Checking if G is DAG: " + str(nx.is_directed_acyclic_graph(G)))

# inspecting the nodes of G 
# print("Printing out nodes of the graph: ")
# for n in G.nodes:
    # print(n, G.nodes[n])

print(apply_attrition(G))
print(stage_partner_wait(G, ("projC5", "definition")))
print(calculate_attrition_probability(0, "Capture"))
print(calculate_attrition_probability(0, "TS"))
print(stage_partner_wait(G, ("projC6", "construction")))
print(list(G.successors(("projS5", "construction"))))
print(stage_delay(G, ("projS5", "construction")))
print(stage_delay(G, ("projC5", "construction")))