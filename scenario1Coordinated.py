# DAG FOR SCENARIO 1 (COORDINATED)

import networkx as nx

#==================================================================
# PROJECT DICTIONARIES (INPUT DATA)
#==================================================================

# dictionary for capture projects
CAPTURE = {
    "projC1": {"definition": 12, "approval": 24, "construction": 48},
    "projC2": {"definition": 30, "approval": 48, "construction": 60},
    "projC3": {"definition": 24, "approval": 24, "construction": 36}
}

# dictionary for TS projects
TS = {
    "projS1": {"definition": 48, "approval": 36, "construction": 72},
    "projS2": {"definition": 60, "approval": 36, "construction": 96},
    "projS3": {"definition": 48, "approval": 24, "construction": 60}
}

# stages of projects
STAGES = ["definition", "approval", "construction"]
STAGES4 = ["definition", "approval", "construction"]

#==================================================================
# BUILDING THE DAG — ADDING NODES
#==================================================================

# function for adding nodes to the graph
def projGraph():
    # make one large graph
    G = nx.DiGraph()

    # helper function to add a node for each project stage
    def add_project(pid, stages, tech):
        for stage, dur in stages.items():
            G.add_node(
                (pid, stage),
                duration = dur,
                tech = tech,
                stage = stage,
                ES = 0.0,
                EF = 0.0
            )

    # add nodes for capture projects
    for pid, stages in CAPTURE.items():
        add_project(pid, stages, "Capture")
    
    # add nodes for TS projects
    for pid, stages in TS.items():
        add_project(pid, stages, 'TS')
    
    return G

# print the nodes and their attributes
G = projGraph()
for n in G.nodes:
    print(n, G.nodes[n])

#==================================================================
# BUILDING THE DAG — ADDING INTRA-PROJECT EDGES
#==================================================================

# function for adding intra-project edges to the graph
def projEdges(G):

    # helper method for adding intra-project edges to each project
    def graphEdges(G, pid):
        for a, b in zip(STAGES[:-1], STAGES[1:]):
            G.add_edge((pid, a), (pid, b))

    # adding intra-project edges for capture projects
    for pid in CAPTURE.keys():
        graphEdges(G, pid)

    # adding intra-project edges for TS projects 
    for pid in TS.keys():
        graphEdges(G, pid)

projEdges(G)
print(list(G.edges))
print(nx.is_directed_acyclic_graph(G)) 

