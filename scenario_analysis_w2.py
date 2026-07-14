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
# W2 BASELINE
#==================================================================

BASELINE = dict(
    base_rate=0.05, max_rate=0.2, late_penalty=0.2, threshold_frac=0.5,
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

def collect_node_rows(G: nx.DiGraph, rep, abandoned_c, abandoned_t, abandoned_s, base_year=2026):
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

        limit_proj, limit_stage, limit_tech, root_proj, root_stage, root_tech = limiting_pred_at_joint(G, n)

        if tech == "capture":
            ab_stage = abandoned_c.get(project) if abandoned else None
        elif tech == "transport":
            ab_stage = abandoned_t.get(project) if abandoned else None
        elif tech == "storage":
            ab_stage = abandoned_s.get(project) if abandoned else None
        elif tech == "joint":
            ab_stage = "NA"
        
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
            "finish_year": base_year + int(EF//12) if EF is not None and EF != float('inf') else None
            }  
        )
    return rows

def limiting_pred_at_joint(G: nx.DiGraph, node):
    '''
    Returns the predecessor node that set the ES of the joint node and tech type
    '''
    limit_proj = limit_stage = limit_tech = None
    root_proj = root_stage = root_tech = None

    # handle the joint nodes
    if G.nodes[node].get("tech") != "joint":
        return None, None, None, None, None, None
    
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
    while G.nodes[current].get("tech") == "joint":
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

def monte_carlo(n_reps, 
                sampling=True, 
                trunks = project_data.TRUNKS,
                pipe_downstream=project_data.PIPE_DOWNSTREAM,
                capture_pipe=project_data.CAPTURE_PIPE,
                base_rate=BASELINE["base_rate"], 
                threshold_frac=BASELINE["threshold_frac"],
                max_rate=BASELINE["max_rate"], 
                capture_tolerance=BASELINE["capture_tolerance"], 
                transport_tolerance=BASELINE["transport_tolerance"],
                storage_tolerance=BASELINE["storage_tolerance"],
                capture_durations=project_data.CAPTURE, 
                capture_volumes=project_data.CAPTURE_VOLUMES,
                storage_durations=project_data.STORAGE, 
                storage_volumes=project_data.STORAGE_VOLUMES,
                transport_durations=project_data.TRANSPORT, 
                transport_volumes=project_data.TRANSPORT_VOLUMES,
                late_penalty = BASELINE["late_penalty"],
                dist_override = "lognormal"):
    
    results = []

    num_cap = len(capture_volumes)
    num_trans = len(transport_volumes)
    num_stor = len(storage_volumes)

    all_rows = []

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

        all_rows.extend(collect_node_rows(G, rep, a_c, a_t, a_s))
    
    node_df = pd.DataFrame(all_rows)
    
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

def deployment_over_time(data):
    '''
    For each rep, cumulative volume captured over time 
    Returns a dataframe of time, mean, p10, p90 over reps which we can then use to plot 
    '''
    cumulative_vol_per_year = []

    df = pd.read_csv(data)
    full_years = list(range(2026, 2046))

    reps = df["rep"].unique()
    for rep in reps:
        cap_comm = df[(df["rep"] == rep) & (df["tech"]=="capture") & (df["stage"]=="commissioning") & (df["abandoned"] == False)]
        yearly = cap_comm.groupby("finish_year")["volume"].sum()
        cumulative = yearly.cumsum()
        aligned = cumulative.reindex(full_years).ffill().fillna(0)
        cumulative_vol_per_year.append(aligned)

    arr = np.array(cumulative_vol_per_year)
    mean = arr.mean(axis=0) # averages across reps for each time point
    p10  = np.percentile(arr, 10, axis=0)
    p90  = np.percentile(arr, 90, axis=0)

    return pd.DataFrame({"year": list(full_years), "mean": mean, "p10": p10, "p90": p90})

#==================================================================
# ABANDONMENT SUMMARY NOTE: THIS IS WRONG BECAUSE RUN 0 SHOULD BE ALL ABANDONED
#==================================================================

def abandonment_summary(data):
    df = pd.read_csv(data)

    # one row per capture per rep (definition stage = always present, one per capture)
    caps = df[(df["tech"] == "capture") & (df["stage"] == "definition")]

    # per rep: what fraction of captures abandoned?
    rate_per_rep = caps.groupby("rep")["abandoned"].mean()
    #   groupby("rep") -> splits into the 100 reps
    #   ["abandoned"].mean() -> fraction True (abandoned) in each rep = that rep's rate

    # now summarize those 100 rates:
    return {
        "mean": rate_per_rep.mean(),
        "p10":  rate_per_rep.quantile(0.10),
        "p90":  rate_per_rep.quantile(0.90),
    }

#==================================================================
# BOTTLENECK ANALYSIS NOTE: INCOMPLETE, NEED TO CONSIDER COLLECTION
#==================================================================

def bottleneck_analysis(data):
    '''
    Understanding what project is holding up each joint decision node 
    (tracing back to roots if necessary)
    '''
    df = pd.read_csv(data)
    joint_nodes = df[df["tech"]=="joint"]
    reps = df["rep"].unique()

#==================================================================
# SENSITIVITY ANALYSIS
#==================================================================

def sensitivity_sweep(param_name, values, n_reps):
    rows = []
    for v in values:
        results = monte_carlo(n_reps, **{param_name: v})   # only override, rest = defaults
        cap_abandonment = analyze_monte_carlo(results)["average capture abandonment rate"]
        final_vol = analyze_monte_carlo(results)["average final vol of capture"]
        all_abandon = analyze_monte_carlo(results)["all abandoned rate"]
        rows.append({param_name: v, "cap abandonment": cap_abandonment, "final vol": final_vol, "all abandon": all_abandon})
    return pd.DataFrame(rows)

def two_variable_sweep(param1, val1, param2, val2, n_reps):
    rows = []
    for v1 in val1:
        for v2 in val2:
            results = monte_carlo(n_reps, **{param1: v1, param2: v2})
            cap_abandonment = analyze_monte_carlo(results)["average capture abandonment rate"]
            final_vol = analyze_monte_carlo(results)["average final vol of capture"]
            all_abandon = analyze_monte_carlo(results)["all abandoned rate"]
            rows.append({param1: v1, param2: v2, "abandonment": cap_abandonment, "final vol": final_vol, "all abandon": all_abandon})
    return pd.DataFrame(rows)

def three_variable_sweep(param1, val1, param2, val2, param3, val3, n_reps):
    rows = []
    for v1 in val1:
        for v2 in val2:
            for v3 in val3:
                results = monte_carlo(n_reps, **{param1: v1, param2: v2, param3: v3})
                cap_abandonment = analyze_monte_carlo(results)["average capture abandonment rate"]
                final_vol = analyze_monte_carlo(results)["average final vol of capture"]
                all_abandon = analyze_monte_carlo(results)["all abandoned rate"]
                rows.append({param1: v1, param2: v2, "abandonment": cap_abandonment, "final vol": final_vol, "all abandon": all_abandon})
    return pd.DataFrame(rows)

#==================================================================
# EXECUTION
#================================================================== 

if __name__ == "__main__":
    #===========================
    # Getting node level data
    #===========================

    # monte_carlo(3).to_csv('trial_1.csv', index=False)
    # deployment_over_time('trial_1.csv').to_csv('deployment_trial_1.csv', index=False)
    # print(abandonment_summary('trial_1.csv'))

     #monte_carlo(100).to_csv('trial_2.csv', index=False)
    # deployment_over_time('trial_2.csv').to_csv('deployment_trial_2.csv', index=False)
    # print(abandonment_summary('trial_2.csv'))

    #===========================
    # Single var sweeps
    #===========================

    # sensitivity_sweep("late_penalty", [0.2, 0.3, 0.4, 0.5, 0.6], 300).to_csv('lp_sensitivity_300.csv', index=False)
    # sensitivity_sweep("threshold_frac", [0.2, 0.3, 0.4, 0.5, 0.6, 0.7], 300).to_csv('thresholdfrac_sensitivity_300.csv', index=False)
    # sensitivity_sweep("max_rate", [0.05, 0.1, 0.15, 0.2], 300).to_csv('maxrate_sensitivity_300.csv', index=False)
    # sensitivity_sweep("base_rate", [0.01, 0.05, 0.1, 0.15], 300).to_csv('baserate_sensitivity_300.csv', index=False)
    # sensitivity_sweep("transport_tolerance", [48, 60, 100, 200], 300).to_csv('transtol2_sensitivity_300.csv', index=False)
    # sensitivity_sweep("storage_tolerance", [12, 24, 48, 60, 100, 200], 300).to_csv('stortol_sensitivity_300.csv', index=False)
    # sensitivity_sweep("capture_tolerance", [12, 48, 60, 100, 200], 300).to_csv('captol3_sensitivity_300.csv', index=False)
    # sensitivity_sweep("threshold_frac", [0.2, 0.3, 0.4, 0.5, 0.6, 0.7], 500).to_csv('thresholdfrac_sensitivity_500.csv', index=False)

    #===========================
    # Multi var sweeps
    #===========================

    two_variable_sweep("threshold_frac", [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], "late_penalty", [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], 500).to_csv('frac_late_sweep.csv', index=False)
    # two_variable_sweep("threshold_frac", [0.2, 0.4, 0.6, 0.8], "storage_tolerance", [12, 24, 48, 60, 72], 300).to_csv('frac_stortol_sweep.csv', index=False)
    # three_variable_sweep("threshold_frac", [0.2, 0.4, 0.6, 0.8], "storage_tolerance", [12, 24, 48, 60], "late_penalty", [0.2, 0.3, 0.4, 0.5], 300).to_csv("three_sweep.csv", index=False)