import pandas as pd
import matplotlib.pyplot as plt
from scenario_analysis_w2 import (
    BASELINE,
    monte_carlo,
    analyze_monte_carlo,
    sensitivity_sweep,
    two_variable_sweep,
)

#==================================================================
# TORNADO CHART METHODS
#==================================================================

def swing(sweep_df, param_col, metric_col="final vol"):
    lo = sweep_df.loc[sweep_df[param_col].idxmin(), metric_col]
    hi = sweep_df.loc[sweep_df[param_col].idxmax(), metric_col]
    return lo, hi

rows = []
def make_tornado(lp_df, base_df, thresh_df, max_df, metric_col):
    for name, df, col in [
        ("late_penalty", lp_df, "late_penalty"),
        ("base_rate", base_df, "base_rate"),
        ("threshold_fraction", thresh_df, "threshold_frac"),
        ("max_rate", max_df, "max_rate"),
        # ("sampling", sample_df, "sampling")
    ]:
        lo, hi = swing(df, col, metric_col)
        rows.append({"param": name, "low": lo, "high": hi, "swing": abs(hi-lo)})
    
    tornado = pd.DataFrame(rows).sort_values("swing") # ascending -> widest at top
    return tornado

#==================================================================
# EXECUTION (PLOTTING CHARTS)
#==================================================================

if __name__ == "__main__":
    
    # PLOTTING THE TORNADO CHARTS
    fig, ax = plt.subplots(figsize=(8,5))

    # getting sensitivity dataframes
    lp_df = sensitivity_sweep("late_penalty", [0.2, 0.6, 0.8, 1], 300)
    base_df = sensitivity_sweep("base_rate", [0, 0.05, 0.2], 300)
    thresh_df = sensitivity_sweep("threshold_frac", [0, 0.2, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9, 1], 300)
    max_df = sensitivity_sweep("max_rate", [0.05, 0.1, 0.2, 0.8, 0.9, 1.0], 300)
    # sample_df = sensitivity_sweep("sampling", False, 300)

    # get the baseline reading
    baseline_mc = monte_carlo(300)
    baseline_results = analyze_monte_carlo(baseline_mc)
    baseline_final_vol = baseline_results["average final vol of capture"]

    tornado = make_tornado(lp_df=lp_df, base_df=base_df, thresh_df=thresh_df, max_df=max_df, metric_col="final vol")

    for i, r in enumerate(tornado.itertuples()):
        ax.barh(i, abs(r.high - r.low), left=min(r.low, r.high), height=0.6, color="#4477aa")

        # label the LOW end and HIGH end of the bar with their values
        ax.text(r.low, i, f"{r.low:.1f}", va="center", ha="right", fontsize=8)
        ax.text(r.high, i, f"{r.high:.1f}", va="center", ha="left", fontsize=8)

    ax.set_yticks(range(len(tornado)))
    ax.set_yticklabels(tornado["param"])
    ax.axvline(baseline_final_vol, color="black", ls="--", lw=1, label="baseline")
    ax.set_xlabel("final volume")
    ax.set_title("Final vol sensitivity")
    ax.legend()
    plt.tight_layout()
    plt.savefig("final_vol_tornado.png", dpi=120)

    # PLOTTING THE HEAT MAP
    # assume df_2d has columns: late_penalty, threshold_frac, final_vol
    df_2d = two_variable_sweep("threshold_frac", [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], "late_penalty", [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], 300)
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
    plt.savefig("frac_pen_heatmap.png", dpi=120)

