import world_2 as w2
import project_data as project_data
import networkx as nx
from world_2 import (
    BASE_RATE,
    THRESHOLD_FRAC,
    MAX_RATE,
    CAPTURE_TOLERANCE,
    TRANSPORT_TOLERANCE,
    STORAGE_TOLERANCE,
    LATE_PENALTY,
    buildmodel,
    CPM,
    apply_attrition,
    cluster_naming,
)

import pandas as pd
import numpy as np

#==================================================================
# NODE DATA COLLECTION
#==================================================================

def collect_node_rows(G: nx.DiGraph, rep, abandoned_c, abandoned_t, abandoned_s):
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
        tech = d.get("tech") is not None    

        limit_pred, limit_cat = limiting_pred(G, n)

        if tech == "capture":
            ab_stage = abandoned_c.get(project) if abandoned else None
        elif tech == "transport":
            ab_stage = abandoned_t.get(project) if abandoned else None
        elif tech == "storage":
            ab_stage = abandoned_s.get(project) if abandoned else None
        elif tech == "joint":
            ab_stage == "NA"
        
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
            "limit_pred": limit_pred,
            "limit_cat": limit_cat
            }  
        )
    return rows

def limiting_pred(G: nx.DiGraph, node):
    '''
    Returns the predecessor node that set the ES of this node and category of limitation
    '''
    es = G.nodes[node].get("ES")
    node_tech = G.nodes[node].get("tech")
    if es is None:
        return None, None
    
    for pred in G.predecessors(node):
        if G.nodes[pred].get("abandoned") is not None:
            continue 
        if G.nodes[pred].get("EF") is not None and abs(G.nodes[pred]["EF"] - es) < 1e-9:
            target_tech = G.nodes[pred].get("tech")
            if pred[0] == node[0]:
                category = "own schedule"
            elif target_tech == "capture":
                category = "capture"
            elif G.nodes[pred].get("tech") == "transport":
                category = "transport"
            elif G.nodes[pred].get("tech") == "storage":
                category = "storage"
            elif G.nodes[pred].get("tech") == "joint":
                category = "joint_threshold"
            else:
                category = "other"
            return pred[0], category
    
    return None, "starting node" # it started at ES = 0 

#==================================================================
# MONTE CARLO
#==================================================================

def monte_carlo(n_reps, 
                sampling=True, 
                trunks = project_data.TRUNKS,
                pipe_downstream=project_data.PIPE_DOWNSTREAM,
                capture_pipe=project_data.CAPTURE_PIPE,
                base_rate=BASE_RATE, 
                threshold_frac=THRESHOLD_FRAC,
                max_rate=MAX_RATE, 
                capture_tolerance=CAPTURE_TOLERANCE,
                transport_tolerance=TRANSPORT_TOLERANCE, 
                storage_tolerance=STORAGE_TOLERANCE,
                capture_durations=project_data.CAPTURE, 
                capture_volumes=project_data.CAPTURE_VOLUMES,
                storage_durations=project_data.STORAGE, 
                storage_volumes=project_data.STORAGE_VOLUMES,
                transport_durations=project_data.TRANSPORT, 
                transport_volumes=project_data.TRANSPORT_VOLUMES,
                late_penalty = LATE_PENALTY,
                dist_override = "lognormal"):
    
    results = []

    num_cap = len(capture_volumes)
    num_trans = len(transport_volumes)
    num_stor = len(storage_volumes)

    for rep in range(n_reps):
        G = buildmodel(replication_seed=rep, sampling=sampling,
                       trunks=trunks, pipe_downstream=pipe_downstream, capture_pipe=capture_pipe, 
                       capture_durations=capture_durations,
                       capture_volumes=capture_volumes, storage_durations=storage_durations,
                       storage_volumes=storage_volumes, transport_durations=transport_durations,
                       transport_volumes=transport_volumes, dist_override=dist_override)

        CPM(G, threshold_frac)

        a_s, a_t, a_c = apply_attrition(G, pipe_downstream, capture_pipe, base_rate, threshold_frac,
                                         max_rate, capture_tolerance, transport_tolerance, storage_tolerance,
                                         late_penalty, replication_seed = rep)

        finite = [G.nodes[n]["EF"] for n in G.nodes
                if G.nodes[n]["EF"] != float("inf") and G.nodes[n]["abandoned"] is None]

        # getting the final survived volume from unabandoned storage FID joint nodes
        final_vol = 0
        for storage in storage_volumes:
            fid = (cluster_naming(storage), "FID joint node")
            if not G.nodes[fid]["below_threshold"] and G.nodes[fid]["abandoned"] is None:
                final_vol += G.nodes[fid]["actual_volume"]
        
        results.append({
                "a_c": a_c,
                "a_t": a_t,
                "a_s": a_s,
                "rep": rep,
                "num_stor": num_stor,
                "storage abandoned": len(a_s),
                "num_trans": num_trans,
                "transport abandoned": len(a_t),
                "num_cap": num_cap,
                "capture abandoned": len(a_c),
                "completion": max(finite) if finite else 0,
                "final volume": final_vol
            }
        )

        collect_node_rows(G, rep, a_c, a_t, a_s)
    
    return results

def analyze_monte_carlo(results):
    cum_s_abandoned = 0.0
    cum_t_abandoned = 0.0
    cum_c_abandoned = 0.0
    cum_vol = 0.0
    cum_time = 0.0
    cap_abandon_rate = []
    trans_abandon_rate = []
    stor_abandon_rate = []
    cum_c_rate = 0.0
    cum_t_rate = 0.0
    cum_s_rate = 0.0
    all_abandoned = 0.0
    c_abandon_at_app = []
    t_abandon_at_app = []

    for rep in results:
        cum_s_abandoned += rep["storage abandoned"]
        cum_t_abandoned += rep["transport abandoned"]
        cum_c_abandoned += rep["capture abandoned"]

        cum_time += rep["completion"]
        if rep["completion"] == 0:
            all_abandoned += 1

        cum_vol += rep["final volume"]

        a_c = rep["a_c"]
        a_t = rep["a_t"]
        a_s = rep["a_s"]

        c_def = 0
        c_app = 0
        for captures, stages in a_c.items():
            if stages == "definition joint node":
                c_def += 1
            elif stages == "FID joint node":
                c_app += 1
        
        t_def = 0
        t_app = 0
        for captures, stages in a_t.items():
            if stages == "definition joint node":
                t_def += 1
            elif stages == "FID joint node":
                t_app += 1

        if len(a_c) != 0:
            c_abandon_at_app.append(c_app/len(a_c))
        if len(a_t) != 0:
            t_abandon_at_app.append(t_app/len(a_t))
        
        cap_abandon_rate.append(rep["capture abandoned"]/rep["num_cap"])
        cum_c_rate += rep["capture abandoned"]/rep["num_cap"]
        trans_abandon_rate.append(rep["transport abandoned"]/rep["num_trans"])
        cum_t_rate += rep["transport abandoned"]/rep["num_trans"]
        stor_abandon_rate.append(rep["storage abandoned"]/rep["num_stor"])
        cum_s_rate += rep["storage abandoned"]/rep["num_stor"]

    avg_s_abandoned = cum_s_abandoned/len(results)
    avg_t_abandoned = cum_t_abandoned/len(results)
    avg_c_abandoned = cum_c_abandoned/len(results)
    avg_vol = cum_vol/len(results)

    collapse_rate = all_abandoned/len(results)

    # abandonment rates
    avg_c_abandon_rate = cum_c_rate/len(results)
    avg_t_abandon_rate = cum_t_rate/len(results)
    avg_s_abandon_rate = cum_s_rate/len(results)

    # average time taken for completed projects — so denom can only include completed ones
    surviving = len(results) - all_abandoned
    if surviving > 0:
        avg_time = cum_time/surviving 
    else:
        avg_time = -1
    
    # average abandonment stage ratios
    cum_c_abandon_at_app = 0
    for rate in c_abandon_at_app:
        cum_c_abandon_at_app += rate
    if len(c_abandon_at_app) != 0:
        avg_c_abandon_at_app = cum_c_abandon_at_app/len(c_abandon_at_app)
    else:
        avg_c_abandon_at_app = 0

    cum_t_abandon_at_app = 0
    for rate in t_abandon_at_app:
        cum_t_abandon_at_app += rate
    if len(t_abandon_at_app) != 0:
        avg_t_abandon_at_app = cum_t_abandon_at_app/len(t_abandon_at_app)
    else:
        avg_t_abandon_at_app = 0
    
    return {"average no. capture abandoned": avg_c_abandoned,
            "average capture abandonment rate": avg_c_abandon_rate,
            "average no. transport abandoned": avg_t_abandoned,
            "average transport abandonment rate": avg_t_abandon_rate,
            "average no. storage abandoned": avg_s_abandoned, 
            "average storage abandonment rate": avg_s_abandon_rate,
            "all abandoned": all_abandoned,
            "all abandoned rate": collapse_rate,
            "average completion time of survived": avg_time,
            "average final vol of capture": avg_vol,
            "avg percent of capture abandoning at approval": avg_c_abandon_at_app,
            "avg percent of transport abandoning at approval": avg_t_abandon_at_app,
            }

#==================================================================
# DEPLOYMENT OVER TIME
#==================================================================

def deployment_over_time():
    '''
    For each rep, cumulative volume captured over time 
    Returns a dataframe of time, mean, p10, p90 over reps which we can then use to plot 
    '''
    