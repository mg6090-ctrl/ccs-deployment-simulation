import networkx as nx

#==================================================================
# UNUSED PROJECT DELAY METHODS
#==================================================================

# CURRENTLY DORMANT METHOD (DELAY IS STAGE + OWN BUNDLED TOGETHER)
def behind_schedule_delay(G_actual, G_base, project, stage):
    '''
    THIS FUNCTION IS NOT IN USE!
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

def stage_partner_wait(G: nx.DiGraph, node):
    '''
    THIS FUNCTION IS NOT IN USE!
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

def apply_attrition(G: nx.DiGraph):
    # random seed
    rng = random.Random(SEED)

    # empty lists for storing abandoned_clusters (DO I NEED THIS?)
    abandoned_transport_clusters = {}
    abandoned_storage_clusters = {}
    
    for storage in CLUSTERS.keys():
        if storage in abandoned_storage_clusters:
                continue
        
        for stage in ["definition", "approval"]:
            for transport in CLUSTERS[storage].keys():
                if transport in abandoned_transport_clusters:
                    continue
                
                for capture in CLUSTERS[storage][transport]:
                    cap_delay = stage_delay(G, (capture, stage))
                    cap_prob = calculate_attrition_probability(cap_delay, "capture")
                    capture_dies = rng.random() < cap_prob
                    if capture_dies:
                        mark_abandonment(G, capture, stage)
                
                CPM(G) # re-run the CPM to re-time before going into transport
                
                # threshold joint node checking after CPM run and abandonments
                approval_joint = (transport, "approval joint node")
                transport_fid_joint = (cluster_naming(transport), "FID joint node")
                
                if stage == "definition" and threshold_failed(G, approval_joint):
                    mark_abandonment(G, transport, stage)
                    abandoned_transport_clusters[transport] = stage
                    continue

                if stage == "approval" and threshold_failed(G, transport_fid_joint):
                    mark_abandonment(G, transport, stage)
                    abandoned_transport_clusters[transport] = stage
                    continue
                
                # stochastic abandonment for transport nodes if threshold is cleared
                trans_delay = stage_delay(G, (transport, stage))
                trans_prob = calculate_attrition_probability(trans_delay, "transport")
                trans_dies = rng.random() < trans_prob
                if trans_dies:
                    mark_abandonment(G, transport, stage)
                    abandoned_transport_clusters[transport] = stage
            
        CPM(G) # re-run the CPM to re-time before going to storage 
        
        # threshold checking at storage cluster joint FID node
        storage_fid_joint = (cluster_naming(storage), "FID joint node")

        if threshold_failed(G, storage_fid_joint):
            mark_abandonment(G, storage, "approval")
            abandoned_storage_clusters[storage] = "approval"
            continue

        # stochastic abandonment if volumetric threshold is cleared
        stor_delay = stage_delay(G, (storage, "approval"))
        stor_prob = calculate_attrition_probability(stor_delay, "storage")
        stor_dies = rng.random() < stor_prob
        if stor_dies:
            mark_abandonment(G, storage, "approval")
            abandoned_storage_clusters[storage] = "approval"


#==================================================================
# SCENARIO 1 FINAL RENDITION DAG BUILDING
#==================================================================

    # OLD CODE
    # adding in the interdependencies
    for storage, t_clusters in CLUSTERS.items():
        
        for transport, captures in t_clusters.items():

            for capture in captures:
                # in each storage cluster:
                # add edges from storage app to each cap cons
                G.add_edge(
                    (storage, "approval"),
                    (capture, "construction")
                )

                # add storage cons to each cap cons
                G.add_edge(
                    (storage, "construction"),
                    (capture, "construction")
                )

                # add edges from transport app to cap cons
                G.add_edge(
                    (transport, "approval"),
                    (capture, "construction")
                )

                 # add edges from transport cons to cap cons
                G.add_edge(
                    (transport, "construction"),
                    (capture, "construction")
                )