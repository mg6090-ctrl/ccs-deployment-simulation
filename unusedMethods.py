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