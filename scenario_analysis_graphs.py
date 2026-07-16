import pandas as pd
import matplotlib.pyplot as plt
from scenario_analysis_w2 import (
    monte_carlo as w2_monte_carlo,
    analyze_monte_carlo as w2_analyze_monte_carlo,
    sensitivity_sweep as w2_sensitivity_sweep,
    two_variable_sweep as w2_two_variable_sweep,
    deployment_over_time as w2_deployment_over_time
)
from scenario_analysis_w1_1 import(
    monte_carlo as w11_monte_carlo,
    analyze_monte_carlo as w11_analyze_monte_carlo,
    sensitivity_sweep as w11_sensitivity_sweep,
    two_variable_sweep as w11_two_variable_sweep,
    deployment_over_time as w11_deployment_over_time
)

from scenario_analysis_w1_2 import(
    monte_carlo as w12_monte_carlo,
    analyze_monte_carlo as w12_analyze_monte_carlo,
    sensitivity_sweep as w12_sensitivity_sweep,
    two_variable_sweep as w12_two_variable_sweep,
    deployment_over_time as w12_deployment_over_time
)

import project_data as project_data

#==================================================================
# COMPARISON CHARTS
#==================================================================

def final_vol_compare():
    return

#==================================================================
# DEPLOYMENT OVER TIME
#==================================================================

def deployment_over_time_compare(w11_data, w12_data, w2_data):
    w11_deployment = w11_deployment_over_time(w11_data)
    w12_deployment = w12_deployment_over_time(w12_data)
    w2_deployment = w2_deployment_over_time(w2_data)

    fig, ax = plt.subplots(figsize=(9, 5))

    # the mean line
    line2,  = ax.plot(w2_deployment["year"], w2_deployment["mean"], color="#2c6fbb", lw=2, label="World 2")
    line11,  = ax.plot(w11_deployment["year"], w11_deployment["mean"], color="#bb782c", lw=2, label="World 1.1")
    line12,  = ax.plot(w12_deployment["year"], w12_deployment["mean"], color="#3abb2c", lw=2, label="World 1.2")

    # the p10-p90 uncertainty band (shaded region between two curves)
    ax.fill_between(w2_deployment["year"], w2_deployment["p10"], w2_deployment["p90"], color="#2c6fbb", alpha=0.2, label="World 2 10th–90th percentile")
    ax.fill_between(w11_deployment["year"], w11_deployment["p10"], w11_deployment["p90"], color="#bb782c", alpha=0.2, label="World 1.1 10th–90th percentile")
    ax.fill_between(w12_deployment["year"], w12_deployment["p10"], w12_deployment["p90"], color="#3abb2c", alpha=0.2, label="World 1.2 10th–90th percentile")

    ax.set_xlabel("year")
    ax.set_xticks(range(2025, 2047, 2))

    target = project_data.PLANNED_CAP_VOLUME
    
    ax.axhline(y=target, xmax = 0.91, color="black", linestyle = "--")
    ax.annotate(
        text=f"Goal\n{target:.1f}",
        xy=(2045, target),
        xytext=(1,0),
        textcoords="offset points",
        va="center",
        ha="left",
        color="black",
        fontweight="bold"
    )

    last_w2_y = w2_deployment["mean"][19]
    last_w11_y = w11_deployment["mean"][19]
    last_w12_y = w12_deployment["mean"][19]

    ax.annotate(
        text=f"{last_w2_y:.1f}",            # Formats value to 1 decimal place (e.g., "16.0")
        xy=(2045, last_w2_y),              # Position of the data point
        xytext=(1, 0),                    # Offset the text slightly to the right (8 points)
        textcoords="offset points",       # Uses point offset instead of data coordinates
        va="center",                      # Vertically centers the text on the line
        ha="left",                        # Aligns text to start left and go right
        color=line2.get_color(),           # Matches label color to the line color
        fontweight="bold"                 # Makes it easy to read
    )

    ax.annotate(
        text=f"{last_w11_y:.1f}",            # Formats value to 1 decimal place (e.g., "16.0")
        xy=(2045, last_w11_y),              # Position of the data point
        xytext=(1, 0),                    # Offset the text slightly to the right (8 points)
        textcoords="offset points",       # Uses point offset instead of data coordinates
        va="center",                      # Vertically centers the text on the line
        ha="left",                        # Aligns text to start left and go right
        color=line11.get_color(),           # Matches label color to the line color
        fontweight="bold"                 # Makes it easy to read
    )

    ax.annotate(
        text=f"{last_w12_y:.1f}",            # Formats value to 1 decimal place (e.g., "16.0")
        xy=(2045, last_w12_y),              # Position of the data point
        xytext=(1, 0),                    # Offset the text slightly to the right (8 points)
        textcoords="offset points",       # Uses point offset instead of data coordinates
        va="center",                      # Vertically centers the text on the line
        ha="left",                        # Aligns text to start left and go right
        color=line12.get_color(),           # Matches label color to the line color
        fontweight="bold"                 # Makes it easy to read
    )

    ax.set_ylabel("commissioned annual capture volume (Mt/yr)")
    ax.set_title("Deployment over time")
    ax.legend()
    plt.tight_layout()
    plt.savefig("deployment_comparison.png", dpi=120)

#==================================================================
# DISTRIBUTION OF FINAL VOLUME
#==================================================================

def w2_final_vol_distribution(w2_node_data):
    w2_df = w2_node_data
    survived = w2_df[(w2_df["tech"]=="capture") & (w2_df["stage"]=="commissioning") & (~w2_df["abandoned"])]
    final_vols = survived.groupby("rep")["volume"].sum()   # total delivered per rep
    # reps with zero survivors won't appear — add them back as 0:
    all_reps = w2_df["rep"].unique()
    final_vols = final_vols.reindex(all_reps, fill_value=0)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(final_vols, bins=20, color="#2c6fbb", edgecolor="white")
    ax.set_xlabel("final delivered volume")
    ax.set_ylabel("number of reps")
    ax.set_title("W2 deployment distribution across reps")
    plt.tight_layout()
    plt.savefig("w2_histogram.png", dpi=120)

def w11_final_vol_distribution(w11_node_data):
    w11_df = w11_node_data
    survived = w11_df[(w11_df["tech"]=="capture") & (w11_df["stage"]=="commissioning") & (~w11_df["abandoned"])]
    final_vols = survived.groupby("rep")["volume"].sum()   # total delivered per rep
    # reps with zero survivors won't appear — add them back as 0:
    all_reps = w11_df["rep"].unique()
    final_vols = final_vols.reindex(all_reps, fill_value=0)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(final_vols, bins=20, color="#bb782c", edgecolor="white")
    ax.set_xlabel("final delivered volume")
    ax.set_ylabel("number of reps")
    ax.set_title("W1.1 deployment distribution across reps")
    plt.tight_layout()
    plt.savefig("w11_histogram.png", dpi=120)

def w12_final_vol_distribution(w12_node_data):
    w12_df = w12_node_data
    survived = w12_df[(w12_df["tech"]=="capture") & (w12_df["stage"]=="commissioning") & (~w12_df["abandoned"])]
    final_vols = survived.groupby("rep")["volume"].sum()   # total delivered per rep
    # reps with zero survivors won't appear — add them back as 0:
    all_reps = w12_df["rep"].unique()
    final_vols = final_vols.reindex(all_reps, fill_value=0)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(final_vols, bins=20, color="#3abb2c", edgecolor="white")
    ax.set_xlabel("final delivered volume")
    ax.set_ylabel("number of reps")
    ax.set_title("W1.2 deployment distribution across reps")
    plt.tight_layout()
    plt.savefig("w12_histogram.png", dpi=120)

#==================================================================
# GENERAL TORNADO METHODS
#==================================================================

def swing(sweep_df, param_col, metric_col="final vol"): 
    lo_row = sweep_df.loc[sweep_df[metric_col].idxmin()]
    hi_row = sweep_df.loc[sweep_df[metric_col].idxmax()]
    return (lo_row[param_col], lo_row[metric_col],   # low param value + its metric
            hi_row[param_col], hi_row[metric_col])    # high param value + its metric

#==================================================================
# W2 GRAPHS
#==================================================================

def w2_make_tornado(lp_df, base_df, thresh_df, max_df, metric_col, baseline):
    rows = []
    for name, df, col in [
        ("late_penalty", lp_df, "late_penalty"),
        ("base_rate", base_df, "base_rate"),
        ("threshold_fraction", thresh_df, "threshold_frac"),
        ("max_rate", max_df, "max_rate"),
        # ("sampling", sample_df, "sampling")
    ]:
        lo_param, lo_metric, hi_param, hi_metric = swing(df, col, metric_col)
        rows.append({"param": name,
                     "low_param": lo_param,
                     "high_param": hi_param,
                     "low_delta":  lo_metric - baseline,    # deviation from baseline at low param value
                     "high_delta": hi_metric - baseline,    # deviation at high param value
                     "swing": abs(hi_metric-lo_metric)})
    
    tornado = pd.DataFrame(rows).sort_values("swing") # ascending -> widest at top
    return tornado

def w2_plot_tornado():
    # PLOTTING THE TORNADO CHART FOR W2
    fig, ax = plt.subplots(figsize=(8,5))

    # getting sensitivity dataframes
    lp_df = w2_sensitivity_sweep("late_penalty", [0.2, 0.6, 0.8, 1], 300)
    base_df = w2_sensitivity_sweep("base_rate", [0, 0.05, 0.2], 300)
    thresh_df = w2_sensitivity_sweep("threshold_frac", [0, 0.2, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9, 1], 300)
    max_df = w2_sensitivity_sweep("max_rate", [0.05, 0.1, 0.2, 0.8, 0.9, 1.0], 300)
    # sample_df = sensitivity_sweep("sampling", False, 300)

    # get the baseline reading
    w2_baseline_mc, _ = w2_monte_carlo(300)
    w2_baseline_results = w2_analyze_monte_carlo(w2_baseline_mc)
    w2_baseline_final_vol = w2_baseline_results["average final vol of capture"]

    tornado = w2_make_tornado(lp_df=lp_df, base_df=base_df, thresh_df=thresh_df, max_df=max_df, metric_col="final vol", baseline=w2_baseline_final_vol)

    for i, r in enumerate(tornado.itertuples()):
        left = min(r.low_delta, r.high_delta)
        width = abs(r.high_delta - r.low_delta)
        ax.barh(i, width,  left=left, height=0.6, color="#4477aa")  # low param value

        offset = 0.5   # how far outside the bar end to place the label
        # negative-side label goes further left (outside), right-aligned
        ax.text(min(r.low_delta, r.high_delta) - offset, i,
                f"{r.low_param}\n({r.low_delta:+.1f})",
                va="center", ha="right", fontsize=7)
        # positive-side label goes further right (outside), left-aligned
        ax.text(max(r.low_delta, r.high_delta) + offset, i,
            f"{r.high_param}\n({r.high_delta:+.1f})",
            va="center", ha="left", fontsize=7)

    span = max(tornado["high_delta"].max(), tornado["low_delta"].max()) - min(tornado["high_delta"].min(), tornado["low_delta"].min())
    ax.set_xlim(-span*0.7, span*0.7)   # generous room on both sides for labels

    ax.axvline(0, color="black", lw=1)   # baseline is now at 0
    ax.text(0, len(tornado) - 0.3, f"baseline = {w2_baseline_final_vol:.1f}",
        ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_yticks(range(len(tornado)))
    ax.set_yticklabels(tornado["param"])
    ax.set_xlabel("change in final volume from baseline")
    ax.set_title("W2 sensitivity tornado (contributions relative to baseline)")
    plt.tight_layout()
    plt.savefig("w2_final_vol_tornado.png", dpi=120)

def w2_plot_heatmap():
     # PLOTTING THE HEAT MAP FOR W2 
    # assume df_2d has columns: late_penalty, threshold_frac, final_vol
    df_2d = w2_two_variable_sweep("threshold_frac", [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], "late_penalty", [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], 300)
    grid = df_2d.pivot(index="late_penalty", columns="threshold_frac", values="final vol")

    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(grid, origin="lower", aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(grid.columns)))
    ax.set_xticklabels(grid.columns)
    ax.set_yticks(range(len(grid.index)))
    ax.set_yticklabels(grid.index)
    ax.set_xlabel("threshold_frac")
    ax.set_ylabel("late_penalty")
    ax.set_title("Final volume across late_penalty × threshold_frac")
    fig.colorbar(im, ax=ax, label="final volume")

    # optional: annotate each cell with its value
    for i in range(len(grid.index)):
        for j in range(len(grid.columns)):
            ax.text(j, i, f"{grid.iloc[i,j]:.1f}", ha="center", va="center", color="white", fontsize=8)
    plt.tight_layout()
    plt.savefig("w2_frac_pen_heatmap.png", dpi=120)

#==================================================================
# W1.1 GRAPHS
#==================================================================

def w11_make_tornado(base_df, risk_df, max_df, captol_df, metric_col, baseline):
    rows = []
    for name, df, col in [
        ("risk_tolerance", risk_df, "frac_split"),
        ("base_rate", base_df, "base_rate"),
        ("max_rate", max_df, "max_rate"),
        ("capture_tolerance", captol_df, "cap_tolerance"),
    ]:
        lo_param, lo_metric, hi_param, hi_metric = swing(df, col, metric_col)
        rows.append({"param": name, 
                     "low_param": lo_param,
                     "high_param": hi_param,
                    "low_delta":  lo_metric - baseline,    # deviation from baseline at low param value
                    "high_delta": hi_metric - baseline,    # deviation at high param value
                     "swing": abs(hi_metric-lo_metric)})
    
    tornado = pd.DataFrame(rows).sort_values("swing") # ascending -> widest at top
    return tornado

def w11_plot_tornado():
    # PLOTTING THE TORNADO CHART FOR W1.1
    fig, ax = plt.subplots(figsize=(8,5))

    # getting sensitivity dataframes
    w11_base_df = w11_sensitivity_sweep("base_rate", [0, 0.05, 0.2], 300)
    w11_max_df = w11_sensitivity_sweep("max_rate", [0.05, 0.1, 0.2, 0.8, 0.9, 1.0], 300)
    w11_captol_df = w11_sensitivity_sweep("cap_tolerance", [12, 24, 36, 48, 60], 300)
    w11_risk_df = w11_sensitivity_sweep("frac_split", [(0, 1), (1, 0)], 300)

    # get the baseline reading
    w11_baseline_mc, _ = w11_monte_carlo(300)
    w11_baseline_results = w11_analyze_monte_carlo(w11_baseline_mc)
    w11_baseline_final_vol = w11_baseline_results["average final volume"]

    tornado = w11_make_tornado(base_df=w11_base_df, 
                               max_df=w11_max_df, 
                               risk_df=w11_risk_df, 
                               captol_df=w11_captol_df, 
                               metric_col="final vol", 
                               baseline=w11_baseline_final_vol)

    for i, r in enumerate(tornado.itertuples()):
        left = min(r.low_delta, r.high_delta)
        width = abs(r.high_delta - r.low_delta)
        ax.barh(i, width, left=left, height=0.6, color="#4477aa")

        offset = 0.5   # how far outside the bar end to place the label
        # negative-side label goes further left (outside), right-aligned
        ax.text(min(r.low_delta, r.high_delta) - offset, i,
                f"{r.low_param}\n({r.low_delta:+.1f})",
                va="center", ha="right", fontsize=7)
        # positive-side label goes further right (outside), left-aligned
        ax.text(max(r.low_delta, r.high_delta) + offset, i,
            f"{r.high_param}\n({r.high_delta:+.1f})",
            va="center", ha="left", fontsize=7)

    span = max(tornado["high_delta"].max(), tornado["low_delta"].max()) - min(tornado["high_delta"].min(), tornado["low_delta"].min())
    ax.set_xlim(-span*0.8, span*0.8)   # generous room on both sides for labels

    ax.axvline(0, color="black", lw=1)   # baseline is now at 0
    ax.text(0, len(tornado) - 0.7, f"baseline = {w11_baseline_final_vol:.1f}",
        ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_yticks(range(len(tornado)))
    ax.set_yticklabels(tornado["param"])
    ax.set_xlabel("change in final volume from baseline")
    ax.set_title("W1.1 sensitivity tornado (contributions relative to baseline)")
    plt.tight_layout()
    plt.savefig("w11_final_vol_tornado.png", dpi=120)

def w11_plot_heatmap():
    # PLOTTING THE HEAT MAP FOR W1.1
    df_2d = w11_two_variable_sweep("frac_split", [(0, 1), (0.2, 0.8), (0.4, 0.6), (0.5, 0.5), (0.6, 0.4), (0.8, 0.2), (1, 0)], "max_rate", [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], 300)
    grid = df_2d.pivot(index="frac_split", columns="max_rate", values="final vol")

    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(grid, origin="lower", aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(grid.columns)))
    ax.set_xticklabels(grid.columns)
    ax.set_yticks(range(len(grid.index)))
    ax.set_yticklabels(grid.index)
    ax.set_xlabel("max_rate")
    ax.set_ylabel("frac_split")
    ax.set_title("Final volume across risk-tolerance × max rate")
    fig.colorbar(im, ax=ax, label="final volume")

    # optional: annotate each cell with its value
    for i in range(len(grid.index)):
        for j in range(len(grid.columns)):
            ax.text(j, i, f"{grid.iloc[i,j]:.1f}", ha="center", va="center", color="white", fontsize=8)
    plt.tight_layout()
    plt.savefig("w11_risk_max_heatmap.png", dpi=120)

#==================================================================
# W1.2 GRAPHS
#==================================================================

def w12_make_tornado(base_df, risk_df, max_df, captol_df, hammock_df, metric_col, baseline):
    rows = []
    for name, df, col in [
        ("risk_tolerance", risk_df, "frac_split"),
        ("base_rate", base_df, "base_rate"),
        ("max_rate", max_df, "max_rate"),
        ("capture_tolerance", captol_df, "cap_tolerance"),
        ("hammock_threshold", hammock_df, "hammock_threshold")
    ]:
        lo_param, lo_metric, hi_param, hi_metric = swing(df, col, metric_col)
        rows.append({"param": name, 
                     "low_param": lo_param,
                     "high_param": hi_param,
                    "low_delta":  lo_metric - baseline,    # deviation from baseline at low param value
                    "high_delta": hi_metric - baseline,    # deviation at high param value
                     "swing": abs(hi_metric-lo_metric)})
    
    tornado = pd.DataFrame(rows).sort_values("swing") # ascending -> widest at top
    return tornado

def w12_plot_tornado():
    # PLOTTING THE TORNADO CHART FOR W1.2
    fig, ax = plt.subplots(figsize=(8,5))

    # getting sensitivity dataframes
    w12_base_df = w12_sensitivity_sweep("base_rate", [0, 0.05, 0.2], 300)
    w12_max_df = w12_sensitivity_sweep("max_rate", [0.05, 0.1, 0.2, 0.8, 0.9, 1.0], 300)
    w12_captol_df = w12_sensitivity_sweep("cap_tolerance", [12, 24, 36, 48, 60], 300)
    w12_risk_df = w12_sensitivity_sweep("frac_split", [(0, 1), (1, 0)], 300)
    w12_hammock_df = w12_sensitivity_sweep("hammock_threshold", [0, 1], 300)

    # get the baseline reading
    w12_baseline_mc, _ = w12_monte_carlo(300)
    w12_baseline_results = w12_analyze_monte_carlo(w12_baseline_mc)
    w12_baseline_final_vol = w12_baseline_results["average final volume"]

    tornado = w12_make_tornado(base_df=w12_base_df, 
                               max_df=w12_max_df, 
                               risk_df=w12_risk_df, 
                               captol_df=w12_captol_df, 
                               hammock_df=w12_hammock_df,
                               metric_col="final vol", 
                               baseline=w12_baseline_final_vol)

    for i, r in enumerate(tornado.itertuples()):
        left = min(r.low_delta, r.high_delta)
        width = abs(r.high_delta - r.low_delta)
        ax.barh(i, width, left=left, height=0.6, color="#4477aa")

        offset = 0.5   # how far outside the bar end to place the label
        # negative-side label goes further left (outside), right-aligned
        ax.text(min(r.low_delta, r.high_delta) - offset, i,
                f"{r.low_param}\n({r.low_delta:+.1f})",
                va="center", ha="right", fontsize=7)
        # positive-side label goes further right (outside), left-aligned
        ax.text(max(r.low_delta, r.high_delta) + offset, i,
            f"{r.high_param}\n({r.high_delta:+.1f})",
            va="center", ha="left", fontsize=7)

    span = max(tornado["high_delta"].max(), tornado["low_delta"].max()) - min(tornado["high_delta"].min(), tornado["low_delta"].min())
    ax.set_xlim(-span*0.9, span*0.9)   # generous room on both sides for labels

    ax.axvline(0, color="black", lw=1)   # baseline is now at 0
    ax.text(0, len(tornado) - 0.7, f"baseline = {w12_baseline_final_vol:.1f}",
        ha="center", va="bottom", fontsize=9, fontweight="bold")
    
    ax.set_yticks(range(len(tornado)))
    ax.set_yticklabels(tornado["param"])
    ax.set_xlabel("change in final volume from baseline")
    ax.set_title("W1.2 sensitivity tornado (contributions relative to baseline)")
    plt.tight_layout()
    plt.savefig("w12_final_vol_tornado.png", dpi=120)

def w12_plot_heatmap():
    # PLOTTING THE HEAT MAP FOR W1.2
    df_2d = w12_two_variable_sweep("frac_split", [(0, 1), (0.2, 0.8), (0.4, 0.6), (0.5, 0.5), (0.6, 0.4), (0.8, 0.2), (1, 0)], "hammock_threshold", [0, 0.2, 0.4, 0.5, 0.6, 0.8, 1], 300)
    grid = df_2d.pivot(index="frac_split", columns="hammock_threshold", values="final vol")

    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(grid, origin="lower", aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(grid.columns)))
    ax.set_xticklabels(grid.columns)
    ax.set_yticks(range(len(grid.index)))
    ax.set_yticklabels(grid.index)
    ax.set_xlabel("hammok_threshold")
    ax.set_ylabel("frac_split")
    ax.set_title("Final volume across risk-tolerance × build-out threshold")
    fig.colorbar(im, ax=ax, label="final volume")

    # optional: annotate each cell with its value
    for i in range(len(grid.index)):
        for j in range(len(grid.columns)):
            ax.text(j, i, f"{grid.iloc[i,j]:.1f}", ha="center", va="center", color="white", fontsize=8)
    plt.tight_layout()
    plt.savefig("w12_risk_ham_heatmap.png", dpi=120)

#==================================================================
# EXECUTION
#==================================================================

if __name__ == "__main__":
    # w2_plot_tornado()
    # w2_plot_heatmap()
    # w11_plot_tornado()
    # w11_plot_heatmap()
    # w12_plot_tornado()
    # w12_plot_heatmap()
    _, w11_node_data = w11_monte_carlo(300)
    _, w12_node_data = w12_monte_carlo(300)
    _, w2_node_data = w2_monte_carlo(300)

    deployment_over_time_compare(w11_node_data, w12_node_data, w2_node_data)
    # w2_final_vol_distribution(w2_node_data)
    # w11_final_vol_distribution(w11_node_data)
    # w12_final_vol_distribution(w12_node_data)



