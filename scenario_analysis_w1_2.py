import world_1_s2 as w1_2
import project_data as project_data
import networkx as nx
from world_1_s2 import (
    BASE_RATE,
    MAX_RATE,
    CAPTURE_TOLERANCE,
    FRAC_SPLIT,
    HAMMOCK_THRESHOLD,
    build_model,
    CPM,
    apply_attrition
)

import pandas as pd
import numpy as np

#==================================================================
# W1.2 BASELINE
#==================================================================

BASELINE = dict(
    base_rate=0.05, max_rate=0.2, frac_split=(0.2, 0.8), hammock_threshold=0.5,
    capture_tolerance=48, transport_tolerance=48, storage_tolerance=48,
    trunks=project_data.TRUNKS, pipe_downstream=project_data.PIPE_DOWNSTREAM, capture_pipe=project_data.CAPTURE_PIPE,
    capture_durations=project_data.CAPTURE, capture_volumes=project_data.CAPTURE_VOLUMES,
    storage_durations=project_data.STORAGE, storage_volumes=project_data.STORAGE_VOLUMES,
    transport_durations=project_data.TRANSPORT, transport_volumes=project_data.TRANSPORT_VOLUMES,
    sampling = True
)

#==================================================================
# NODE DATA COLLECTION
#==================================================================

def collect_node_rows(G: nx.DiGraph, rep, abandoned_c, base_year=2026):
    '''
    After each replication run in monte carlo, run this to collect information from all graph nodes
    Inputs: G (digraph), rep (rep number), 
    abandoned_c, abandoned_s, abandoned_t (output of apply_attrition, dictionary of {project: stage})
    '''
    rows = []
    for n in G.nodes:
        d = G.nodes[n]
        project, stage = n[0], n[1]
        ES = d.get("ES")
        EF = d.get("EF", 0.0)
        
        abandoned = d.get("abandoned") is not None
        tech = d.get("tech")

        limit_proj, limit_stage, limit_tech, root_proj, root_stage, root_tech = limiting_pred(G, n)

        if tech == "capture":
            ab_stage = abandoned_c.get(project) if abandoned else None
        else:
            ab_stage = None
        
        # think about what parameters to collect 
        rows.append({
            "rep": rep,
            "project": project,
            "stage": stage,
            "tech": tech,
            "project_type": d.get("project_type"),
            "ES": ES,
            "EF": EF,
            "volume": d.get("volume"),
            "actual_volume": d.get("actual_volume", None),
            "committed_volume": d.get("committed_volume", None),
            "abandoned": abandoned,
            "abandonment_stage": ab_stage,
            "limit_proj": limit_proj,
            "limit_stage": limit_stage,
            "limit_tech": limit_tech,
            "root_proj": root_proj,
            "root_stage": root_stage,
            "root_tech": root_tech,
            "finish_year": base_year + int(EF//12) if EF and EF != float('inf') else None
            }  
        )
    return rows

def limiting_pred(G: nx.DiGraph, node):
    '''
    Returns the predecessor node that set the ES of the joint node and tech type
    '''
    limit_proj = limit_stage = limit_tech = None
    root_proj = root_stage = root_tech = None
    
    def find_binder(n):
        es = G.nodes[n].get("ES")
        if es is None:
            return None
        for p in G.predecessors(n):
            ef = G.nodes[p].get("EF")
            if ef is not None and abs(ef-es) < 1e-9:
                return p
        return None
    
    binder = find_binder(node)
    if binder is None:
        return limit_proj, limit_stage, limit_tech, root_proj, root_stage, root_tech
    limit_proj, limit_stage = binder[0], binder[1]
    limit_tech = G.nodes[binder].get("project_type")

    current = binder
    while G.nodes[current].get("ES") != 0:
        nxt = find_binder(current)
        if nxt is None:
            break
        current = nxt
    root_proj, root_stage = current[0], current[1]
    root_tech = G.nodes[current].get("project_type")
    
    return limit_proj, limit_stage, limit_tech, root_proj, root_stage, root_tech

#==================================================================
# MONTE CARLO
#==================================================================

def monte_carlo(
        n_reps, 
        base_rate = BASE_RATE, 
        max_rate = MAX_RATE,
        pipe_downstream = project_data.PIPE_DOWNSTREAM,
        capture_pipe = project_data.CAPTURE_PIPE,
        cap_tolerance = CAPTURE_TOLERANCE,
        replication_seed=0, 
        caps = project_data.CAPTURE,
        caps_vol = project_data.CAPTURE_VOLUMES,
        trans = project_data.TRANSPORT,
        trans_vol = project_data.TRANSPORT_VOLUMES,
        stor = project_data.STORAGE,
        stor_vol = project_data.STORAGE_VOLUMES,
        frac_split = FRAC_SPLIT,
        sampling = True,
        hammock_threshold = HAMMOCK_THRESHOLD,
        dist_override = "lognormal"
    ):
    
    results = []

    all_rows = []

    num_cap = len(caps)

    for rep in range(n_reps):

        G = build_model(
            rep, 
            sampling,
            pipe_downstream, 
            capture_pipe, 
            caps, caps_vol,
            stor, stor_vol,
            trans, trans_vol, 
            frac_split,
            dist_override
        )

        CPM(G, hammock_threshold=hammock_threshold)

        abandoned = apply_attrition(
                        G, 
                        base_rate = base_rate,  
                        replication_seed = rep,
                        max_rate = max_rate,
                        cap_tolerance = cap_tolerance
                    )

        CPM(G, hammock_threshold=hammock_threshold)

        final_vol = 0
        
        for capture in caps:
            if not G.nodes[(capture, "commissioning")]["abandoned"]:
                final_vol += G.nodes[(capture, "commissioning")]['volume']

        results.append({
                "c_abandon": abandoned,
                "rep": rep,
                "num_cap": num_cap,
                "n_c_abandoned": len(abandoned),
                "completion": max((G.nodes[n]["EF"] for n in G.nodes if G.nodes[n]['abandoned'] is None), default = 0),
                "final volume": final_vol
            }
        )

        all_rows.extend(collect_node_rows(G, rep, abandoned))

    node_df = pd.DataFrame(all_rows)
    return node_df
    #return results

def analyze_monte_carlo(results):
    cum_abandoned = 0.0
    cum_time = 0.0
    cum_vol = 0.0
    cap_abandon_rate = []
    cum_c_rate = 0.0

    for rep in results:
        cum_abandoned += rep["n_c_abandoned"]
        cum_time += rep["completion"]
        cum_vol += rep["final volume"]
        cap_abandon_rate.append(rep["n_c_abandoned"]/rep["num_cap"])
        cum_c_rate += rep["n_c_abandoned"]/rep["num_cap"]
    
    avg_abandoned = cum_abandoned/len(results)
    avg_c_abandon_rate = cum_c_rate/len(results)
    avg_time = cum_time/len(results)
    avg_vol = cum_vol/len(results)

    return {"average no. capture abandoned": avg_abandoned, 
            "average capture abandonment rate": avg_c_abandon_rate,
            "average completion time": avg_time,
            "average final volume": avg_vol}

#==================================================================
# SENSITIVITY ANALYSIS
#==================================================================

def sensitivity_sweep(param_name, values, n_reps):
    rows = []
    for v in values:
        results = monte_carlo(n_reps, **{param_name: v})   # only override, rest = defaults
        cap_abandonment = analyze_monte_carlo(results)["average capture abandonment rate"]
        final_vol = analyze_monte_carlo(results)["average final volume"]
        rows.append({param_name: v, "cap abandonment": cap_abandonment, "final vol": final_vol})
    return pd.DataFrame(rows)

def two_variable_sweep(param1, val1, param2, val2, n_reps):
    rows = []
    for v1 in val1:
        for v2 in val2:
            results = monte_carlo(n_reps, **{param1: v1, param2: v2})
            cap_abandonment = analyze_monte_carlo(results)["average capture abandonment rate"]
            final_vol = analyze_monte_carlo(results)["average final volume"]
            rows.append({param1: v1, param2: v2, "abandonment": cap_abandonment, "final vol": final_vol})
    return pd.DataFrame(rows)

def three_variable_sweep(param1, val1, param2, val2, param3, val3, n_reps):
    rows = []
    for v1 in val1:
        for v2 in val2:
            for v3 in val3:
                results = monte_carlo(n_reps, **{param1: v1, param2: v2, param3: v3})
                cap_abandonment = analyze_monte_carlo(results)["average capture abandonment rate"]
                final_vol = analyze_monte_carlo(results)["average final volume"]
                rows.append({param1: v1, param2: v2, "abandonment": cap_abandonment, "final vol": final_vol})
    return pd.DataFrame(rows)

#==================================================================
# EXECUTION
#================================================================== 

if __name__ == "__main__":
    # monte_carlo(3).to_csv("w1_2_trial_1.csv", index=False)
    two_variable_sweep("frac_split", [(0.1, 0.9), (0.2, 0.8), (0.3, 0.7), (0.4, 0.6), (0.8, 0.2)], "max_rate", [0.05, 0.1, 0.2, 0.3, 0.4], 300).to_csv("w12_split_max_sweep.csv", index=False)