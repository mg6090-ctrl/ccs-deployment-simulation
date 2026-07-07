"""
Visualize the coordinated (S1) tier-gated DAG and run structural sanity checks.

HOW TO RUN
----------
Edit the import to your module, paste/point to your project_data, then:
    python3 visualize_tier_dag.py

It prints structural checks FIRST (these catch the construction bugs without you
having to read the picture), then draws the graph to tier_dag.png.

WHAT THE CHECKS CATCH
- isolated nodes (built but never wired -> a Step that references the wrong var)
- nodes whose key isn't a (name, stage) tuple of strings (garbage keys from
  list/char iteration bugs)
- captures missing their def->app->cons->comm chain (the Step 1 bug)
- cross-tier edges present (Step 4) -> confirms tier gating actually wired
- cycles (not a DAG)
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import world_1_s1_edits as m


def build():
    G = m.projGraph(replication_seed=0, sampling=False)
    m.projEdges(G)
    return G


def structural_checks(G):
    print("=" * 60)
    print("STRUCTURAL CHECKS")
    print("=" * 60)
    print(f"nodes: {G.number_of_nodes()}, edges: {G.number_of_edges()}")

    # 1. garbage node keys (should all be (str, str))
    bad_keys = [n for n in G.nodes
                if not (isinstance(n, tuple) and len(n) == 2
                        and isinstance(n[0], str) and isinstance(n[1], str))]
    if bad_keys:
        print(f"\n[!] {len(bad_keys)} GARBAGE node keys (list/char iteration bug):")
        for n in bad_keys[:10]:
            print(f"      {n!r}")

    # 2. isolated nodes
    isolated = [n for n in G.nodes if G.degree(n) == 0]
    if isolated:
        print(f"\n[!] {len(isolated)} isolated nodes (built, never wired):")
        for n in isolated[:15]:
            print(f"      {n}")

    # 3. every capture should have def->app->cons->comm chain
    stages = ["definition", "approval", "construction", "commissioning"]
    caps = sorted({n[0] for n in G.nodes
                   if isinstance(n, tuple) and G.nodes[n].get("tech") == "capture"})
    for c in caps:
        chain_ok = all(G.has_edge((c, a), (c, b))
                       for a, b in zip(stages, stages[1:]))
        if not chain_ok:
            print(f"[!] capture {c} missing part of its def->app->cons->comm chain")

    # 4. cross-tier gating edges present? (Tier1 commissioning -> Tier2 definition)
    cross_tier = [(u, v) for u, v in G.edges
                  if isinstance(u, tuple) and isinstance(v, tuple)
                  and u[1] == "commissioning" and v[1] == "definition"]
    print(f"\ncross-tier gating edges (Tier1 commissioning -> Tier2 definition): {len(cross_tier)}")
    for e in cross_tier[:10]:
        print(f"      {e[0]} -> {e[1]}")

    # 5. DAG?
    if not nx.is_directed_acyclic_graph(G):
        print("\n[!!] NOT A DAG -- cycle present:")
        try:
            for e in nx.find_cycle(G):
                print(f"       {e[0]} -> {e[1]}")
        except nx.NetworkXNoCycle:
            pass
    else:
        print("is a valid DAG: yes")


STAGE_COL = {"definition": 0, "approval": 1, "construction": 2, "commissioning": 3}


def layout(G):
    # x by stage, y grouped by project
    projects = sorted({n[0] for n in G.nodes if isinstance(n, tuple)})
    ypos = {p: i for i, p in enumerate(projects)}
    pos = {}
    for n in G.nodes:
        if not (isinstance(n, tuple) and len(n) == 2):
            continue
        name, stage = n
        x = STAGE_COL.get(stage, 4)
        pos[n] = (x * 2.5, -ypos.get(name, 0) * 1.3)
    return pos


def tech_color(G, n):
    return {"capture": "#E0552F", "transport": "#2F7FE0",
            "storage": "#8888aa", "joint": "#cccccc"}.get(
        G.nodes[n].get("tech"), "white")


def main():
    G = build()
    structural_checks(G)

    pos = layout(G)
    drawable = [n for n in G.nodes if n in pos]

    fig, ax = plt.subplots(figsize=(16, max(8, len(set(n[0] for n in drawable)) * 0.5)))
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#aaaaaa", width=0.7,
                           arrows=True, arrowsize=8, connectionstyle="arc3,rad=0.05")
    nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=drawable,
                           node_color=[tech_color(G, n) for n in drawable],
                           edgecolors="#333", node_size=900)
    nx.draw_networkx_labels(G, pos, ax=ax,
                            labels={n: f"{n[0]}\n{n[1][:4]}" for n in drawable},
                            font_size=5.5)
    ax.legend(handles=[
        Patch(facecolor="#E0552F", label="capture"),
        Patch(facecolor="#2F7FE0", label="transport"),
        Patch(facecolor="#8888aa", label="storage"),
    ], loc="lower right")
    ax.set_title("Coordinated tier-gated DAG")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("tier_dag.png", dpi=130, bbox_inches="tight")
    print("\nSaved tier_dag.png")


if __name__ == "__main__":
    main()