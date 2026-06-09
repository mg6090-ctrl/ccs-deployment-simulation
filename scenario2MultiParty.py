import networkx as nx
import random 
import numpy as np

#==================================================================
# CONSTANTS (INPUT DATA AND PARAMETERS)
#==================================================================

# stages of projects
STAGES = ["definition", "approval", "construction"]
STAGES4 = ["definition", "approval", "construction", "commission"]

# dictionary for capture projects
CAPTURE = {
    "projC1": {"definition": 12, "approval": 24, "construction": 48},
    "projC2": {"definition": 30, "approval": 48, "construction": 60},
    "projC3": {"definition": 24, "approval": 24, "construction": 36},
    # "projC4": {"definition": 16, "approval": 32, "construction": 50}
}

# dictionary for TS projects
TS = {
    "projS1": {"definition": 48, "approval": 36, "construction": 72},
    "projS2": {"definition": 60, "approval": 36, "construction": 96},
    "projS3": {"definition": 48, "approval": 24, "construction": 60}
}

# clusters (matching capture to transport)
CLUSTERS = {
    "projS1": ["projC1"],
    "projS2": ["projC2"],
    "projS3": ["projC3"],
}

# seed for shuffling before frac_split 
SEED = 42

# constants for the abandonment function
BASE_RATE = 0.2
MAX_RATE = 0.8
CAPTURE_TOLERANCE = 18
TS_TOLERANCE = 12

#==================================================================
# BUILDING THE DAG — ADDING NODES
#==================================================================

def joint_naming(stage):
    '''
    Description: naming the joint nodes
    Args: stage
    Returns: name of the joint node
    '''
    if stage == "construction":
        joint_name = "commissioning joint node"
    else:
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
                EF = 0.0
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
                    EF = 0.0
                )
            
            # add joint nodes
            for stage in STAGES:
                joint_name = joint_naming(stage)
                G.add_node(
                    (capture, joint_name),
                    duration = 0,
                    stage = joint_name,
                    capture = capture,
                    cluster = cluster,
                    tech = "Joint",
                    ES = 0.0,
                    EF = 0.0
                )
    
    return G

#==================================================================
# BUILDING THE DAG — ADDING EDGES
#==================================================================

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
            # adding the edge from capture construction to joint commissioning
            G.add_edge(
                (capture, "construction"),
                (capture, joint_naming("construction"))
            )
            # adding the edge from ts construction to joint commissioning
            G. add_edge(
                (ts, "construction"),
                (capture, joint_naming("construction"))
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
# DELAYS AND ABANDONMENT
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
                    EF = 0.0
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
                        EF = 0.0
                    )
        return G

    # helper method for drawing intra-project edges only
    def intra_edges(G: nx.DiGraph):
        def graphEdges(G, pid):
            for a, b in zip(STAGES[:-1], STAGES[1:]):
                G.add_edge((pid, a), (pid, b))

        for pid in CAPTURE.keys():
            graphEdges(G, pid)

        for pid in TS.keys():
            graphEdges(G, pid)

    # make a NEW graph without interdependent edges to evaluate baseline ES/EF
    G_indep = intra_nodes()
    intra_edges(G_indep)

    return G_indep

def slip_compute(node):
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

def calculate_attrition_probability(delay, tech):
    '''
    Description: returns attrition probability based on delay and tech
    Principle: slip past per-party tolerance baseline
    Args: delay (calculated from slip_compute) and tech
    Returns: probability
    '''
    if tech == "capture":
        if delay < CAPTURE_TOLERANCE:
            return BASE_RATE
        else:
            delay_factor = delay / CAPTURE_TOLERANCE
            return min(MAX_RATE, BASE_RATE * (1 + np.exp(delay_factor)))

    if tech == "TS":
        if delay < TS_TOLERANCE:
            return BASE_RATE
        else:
            delay_factor = delay / TS_TOLERANCE
            return min(MAX_RATE, BASE_RATE * (1 + np.exp(delay_factor)))

def apply_attrition():
    return

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

# G = buildmodel()

# checking that G is a DAG
# print("Checking if G is DAG: " + str(nx.is_directed_acyclic_graph(G)))

# inspecting the nodes of G 
# print("Printing out nodes of the graph: ")
# for n in G.nodes:
    # print(n, G.nodes[n])

# testing slip_compute
print(slip_compute(("projC1", "definition")))
print(slip_compute(("projC1", "approval")))
print(slip_compute(("projS1", "definition")))
print(slip_compute(("projS1", "approval")))