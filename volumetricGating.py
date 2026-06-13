import networkx as nx

def is_threshold_joint(G: nx.DiGraph, node):
    return G.nodes[node]["tech"] == "joint" and G.nodes[node]["stage"] == "FID joint node"

def gather_input_specs(G: nx.DiGraph, joint):
    if is_threshold_joint != True:
        raise ValueError(f"{joint} is not a joint node")
    arrivals = []
    for node in G.predecessors(joint):
        volume = G.nodes[node]["volume"]
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