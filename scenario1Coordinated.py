# DAG FOR SCENARIO 1 (COORDINATED)

import networkx as nx
import random

#==================================================================
# CONSTANTS (INPUT DATA AND PARAMETERS)
#==================================================================

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
    # "projS2": {"definition": 60, "approval": 36, "construction": 96},
    # "projS3": {"definition": 48, "approval": 24, "construction": 60}
}

# stages of projects
STAGES = ["definition", "approval", "construction"]
STAGES4 = ["definition", "approval", "construction", "commission"]

# fraction split
FRAC_SPLIT = (0.2, 0.8)

#==================================================================
# BUILDING THE DAG — ADDING NODES
#==================================================================

def projGraph():
    '''
    Description: creating graph and adding nodes
    Returns: directed acyclic graph G
    '''
    # make one large graph
    G = nx.DiGraph()

    def add_project(pid, stages, tech):
        '''
        Description: helper function to add a node for each project stage
        Args: pid, stages, tech
        '''
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

#==================================================================
# BUILDING THE DAG — ADDING INTRA-PROJECT EDGES
#==================================================================

def projEdges(G: nx.DiGraph):
    '''
    Description: adds intra-project edges to G
    Args: G
    '''
    
    def graphEdges(G, pid):
        '''
        Description: helper method for adding intra-project edges to each project
        Args: G, pid
        '''
        for a, b in zip(STAGES[:-1], STAGES[1:]):
            G.add_edge((pid, a), (pid, b))

    # adding intra-project edges for capture projects
    for pid in CAPTURE.keys():
        graphEdges(G, pid)

    # adding intra-project edges for TS projects 
    for pid in TS.keys():
        graphEdges(G, pid)

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
# BUILDING THE DAG — ADDING INTER-PROJECT EDGES
#==================================================================

def projInterdep(G: nx.DiGraph):
    '''
    Description: adds inter-project edges to G
    Args: G
    '''
    
    def fracSplit():
        '''
        Description: helper method that splits capture into two batches based on risk aversion level
        Returns: tuple of ([approval pids], [construction pids])
        '''
        # number of capture projects in approval batch
        approv_num = round(len(CAPTURE)*FRAC_SPLIT[0])
        
        pids = [key for key in CAPTURE.keys()]
        
        # cuts the list of pids in two for the two sets (go ahead at approval and construction)
        return pids[:approv_num], pids[approv_num:]
    
    # loop through projects
    approval, construction = fracSplit()
    for pid in approval:
        G.add_edge(("projS1", "approval"), (pid, "construction"))
    for pid in construction:
        G.add_edge(("projS1", "construction"), (pid, "construction"))

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
    projInterdep(G)
    CPM(G)

    return G

#==================================================================
# MAIN (EXECUTION)
#==================================================================

G = buildmodel()

print("Checking if G is DAG: " + str(nx.is_directed_acyclic_graph(G)))
for n in G.nodes:
    print(n, G.nodes[n])