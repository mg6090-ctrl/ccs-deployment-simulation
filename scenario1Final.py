import networkx as nx
import random

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

# fraction split
FRAC_SPLIT = (0.2, 0.8)

# seed for shuffling before frac_split 
SEED = 42

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
                    t_cluster = None,
                    abandoned = None
                )
            
            # add storage commissioning node
            G.add_node(
                (storage, "commissioning"),
                duration = 0.0,
                stage = "commissioning",
                tech = "storage",
                ES = 0.0,
                EF = 0.0,
                volume = STORAGE_VOLUMES[storage],
                s_cluster = storage_cluster,
                t_cluster = None,
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
                    duration = 0.0,
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

def fracSplit(captures):
        '''
        Description: helper method that splits capture into two batches based on risk aversion level
        Returns: tuple of ([approval pids], [construction pids])
        '''
        # seeding and introducing randomness
        rng = random.Random(SEED)
        shuffled = list(captures)
        rng.shuffle(shuffled)

        # number of capture projects in approval batch (risk-tolerant)
        approv_num = round(len(shuffled)*FRAC_SPLIT[0])

        # cuts the list of pids in two for the two sets (go ahead at approval and construction)
        return shuffled[:approv_num], shuffled[approv_num:]

def get_storage(G, capture):
    for storage, t_clusters in CLUSTERS.items():
        for transport, captures in t_clusters.items():
            for cap in captures:
                if cap == capture:
                    return storage

def get_transport(G, capture):
    for storage, t_clusters in CLUSTERS.items():
        for transport, captures in t_clusters.items():
            for cap in captures:
                if cap == capture:
                    return transport

def projGraph():
    # building the base graph with intra-project edges
    G = make_base_graph()

    for storage, t_cluster in CLUSTERS.items():
        cluster_captures = [c for caps in t_cluster.values() for c in caps]
        approval, construction = fracSplit(cluster_captures)

        for capture in approval:
            G.add_edge(
                (get_storage(G, capture), "approval"), 
                (capture, "construction")
            )

            G.add_edge(
                (get_transport(G, capture), "approval"),
                (capture, "construction")
            )

        for capture in construction:
            G.add_edge(
                (get_storage(G, capture), "construction"), 
                (capture, "construction")
            )

            G.add_edge(
                (get_transport(G, capture), "construction"),
                (capture, "construction")
            )
    
    # commissioning cascade: storage -> transport -> capture
    for storage, t_cluster in CLUSTERS.items():
        for transport, captures in t_cluster.items():
            G.add_edge((storage, "commissioning"), (transport, "commissioning"))
            for capture in captures:
                G.add_edge((transport, "commissioning"), (capture, "commissioning"))

    return G

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


#==================================================================
# MAIN (EXECUTION)
#==================================================================

G = projGraph()
CPM(G)