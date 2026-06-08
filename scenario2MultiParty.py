import networkx as nx
import random 

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
    "projC4": {"definition": 16, "approval": 32, "construction": 50}
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
print("Checking if G is DAG: " + str(nx.is_directed_acyclic_graph(G)))

# inspecting the nodes of G 
print("Printing out nodes of the graph: ")
for n in G.nodes:
    print(n, G.nodes[n])
