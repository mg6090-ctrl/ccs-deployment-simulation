#==================================================================
# VISUALIZATION
#==================================================================

"""
Visualize the S2 CCS DAG to check the wiring by eye.

It builds the graph with sampling off (fixed durations) and draws it with a
layered left-to-right layout that mirrors your hand-drawn DAG:
  definition -> def-joints -> approval -> FID-joints -> cluster FID -> construction -> commissioning

Joint nodes are drawn as colored squares (like the red nodes in your diagram),
project stage nodes as circles. Hover isn't available in a static PNG, so every
node is labeled. If the graph is dense, open the PNG and zoom.

WHAT TO CHECK against your reference diagram:
  - Does each def-joint fan OUT to the approval of everything upstream of it?
  - Does the storage cluster FID joint fan out to everyone's construction?
  - Do the FID-joints chain upward (spur FID -> trunk FID -> cluster FID)?
  - Are there any stray edges (e.g. a joint pointing at the wrong stage),
    or missing edges (a project whose approval/construction has no gate)?
  - Any isolated nodes (built but never wired) show up off on their own.
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import world_2_edits as m 

# ----------------------------------------------------------------------
# Stage ordering: assigns each node an x-column by its lifecycle stage,
# so the layout reads left-to-right like your diagram.
# ----------------------------------------------------------------------
STAGE_COLUMN = {
    "definition": 0,
    "definition joint node": 1,
    "approval": 2,
    "FID joint node": 3,
    "construction": 5,
    "commissioning": 6,
}
# cluster FID joint gets its own column (4) between the FID joints and construction.
CLUSTER_FID_COLUMN = 4

def node_column(G, node):
    """Assign an x-column to a node based on its stage."""
    stage = G.nodes[node].get("stage", "")
    name = node[0]
    # storage cluster FID joint sits in its own column
    if stage == "FID joint node" and "cluster" in str(name) and "storage" in str(name).lower():
        return CLUSTER_FID_COLUMN
    # Heuristic: the storage cluster FID joint is the one whose name starts with a storage cluster.
    # Fall back to stage-based column.
    return STAGE_COLUMN.get(stage, 4)


def is_joint(G, node):
    return G.nodes[node].get("tech") == "joint"


def build_layout(G):
    """
    Layered layout: x by stage column, y spread within each column.
    Returns pos dict {node: (x, y)}.
    """
    columns = {}
    for node in G.nodes:
        col = node_column(G, node)
        columns.setdefault(col, []).append(node)

    pos = {}
    for col, nodes in columns.items():
        # sort nodes within a column for stable vertical ordering
        nodes_sorted = sorted(nodes, key=lambda n: str(n))
        n = len(nodes_sorted)
        for i, node in enumerate(nodes_sorted):
            # spread vertically, centered
            y = (n - 1) / 2.0 - i
            pos[node] = (col * 3.0, y * 1.2)
    return pos


def short_label(node):
    """Compact label: 'projC1\napproval' -> 'projC1\napp'."""
    name, stage = node[0], node[1]
    abbrev = {
        "definition": "def",
        "approval": "app",
        "construction": "cons",
        "commissioning": "com",
        "definition joint node": "DEFj",
        "FID joint node": "FIDj",
    }
    return f"{name}\n{abbrev.get(stage, stage)}"


def main():
    # Build graph + edges (sampling off for deterministic durations)
    G = m.projGraph(replication_seed=0, sampling=False)
    m.projEdges(G)

    print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    # Report isolated nodes (built but never wired) -- a common bug signal
    isolated = [n for n in G.nodes if G.degree(n) == 0]
    if isolated:
        print(f"\n[!] {len(isolated)} ISOLATED nodes (no edges) -- likely a wiring gap:")
        for n in isolated:
            print(f"      {n}")

    # Report nodes with no incoming gate at approval/construction (missing gate signal)
    for n in G.nodes:
        stage = G.nodes[n].get("stage")
        if stage in ("approval", "construction"):
            preds = list(G.predecessors(n))
            if not preds:
                print(f"[!] {n} has NO predecessors (ungated {stage})")

    # Check it's actually a DAG (a cycle is a serious bug)
    if not nx.is_directed_acyclic_graph(G):
        print("\n[!!] GRAPH HAS A CYCLE -- not a DAG. Cycles found:")
        try:
            cyc = nx.find_cycle(G)
            for e in cyc:
                print(f"       {e[0]} -> {e[1]}")
        except nx.NetworkXNoCycle:
            pass

    pos = build_layout(G)

    # Split nodes by type for drawing
    joint_nodes = [n for n in G.nodes if is_joint(G, n)]
    proj_nodes = [n for n in G.nodes if not is_joint(G, n)]

    fig, ax = plt.subplots(figsize=(22, 14))

    nx.draw_networkx_edges(
        G, pos, ax=ax, edge_color="#999999", width=0.8,
        arrows=True, arrowsize=10, arrowstyle="-|>",
        connectionstyle="arc3,rad=0.05",
    )
    nx.draw_networkx_nodes(
        G, pos, ax=ax, nodelist=proj_nodes,
        node_color="white", edgecolors="#555555", linewidths=1.2,
        node_size=1400, node_shape="o",
    )
    nx.draw_networkx_nodes(
        G, pos, ax=ax, nodelist=joint_nodes,
        node_color="#E0552F", edgecolors="#B03D1D", linewidths=1.2,
        node_size=1600, node_shape="s",
    )
    nx.draw_networkx_labels(
        G, pos, ax=ax,
        labels={n: short_label(n) for n in G.nodes},
        font_size=6.5, font_color="black",
    )

    ax.legend(handles=[
        Patch(facecolor="white", edgecolor="#555555", label="Project stage node"),
        Patch(facecolor="#E0552F", edgecolor="#B03D1D", label="Joint node (time-slip + volume)"),
    ], loc="lower left", fontsize=11)

    ax.set_title("S2 CCS DAG -- built graph (check against reference diagram)", fontsize=14)
    ax.axis("off")
    plt.tight_layout()
    out = "ccs_dag.png"
    plt.savefig(out, dpi=130, bbox_inches="tight")
    print(f"\nSaved {out} -- open and zoom to check the wiring.")


if __name__ == "__main__":
    main()