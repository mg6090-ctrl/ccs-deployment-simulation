#==================================================================
# VISUALIZATION
#==================================================================

def visualize(G, storage_filter=None):
    '''
    Draw the three-tier DAG left-to-right by stage.
    Pass a storage id (e.g. "projS1") to draw just that storage cluster.
    Colors: storage=blue, transport=green, capture=orange, joint=red.
    Abandoned nodes are drawn faded.
    '''
    # x-position per stage (left to right through the lifecycle)
    stage_x = {
        "definition": 0,
        "definition joint node": 1,
        "approval joint node": 2,
        "approval": 3,
        "FID joint node": 4,
        "construction": 5,
        "commissioning": 6,
    }

    # pick nodes: one storage cluster or everything
    if storage_filter:
        sc = storage_filter + " cluster"
        nodes = [n for n in G.nodes if G.nodes[n].get("s_cluster") == sc]
    else:
        nodes = list(G.nodes)

    if not nodes:
        print(f"No nodes found for filter {storage_filter}")
        return

    # assign each project a horizontal band (y), grouped by tier so tiers stack
    tier_order = {"storage": 0, "transport": 1, "capture": 2, "joint": 3}
    # sort projects by tier then name so related nodes sit near each other
    projects = sorted(
        {n[0] for n in nodes},
        key=lambda p: p  # alphabetical; tweak if you want tier-grouped
    )
    y_of = {p: i for i, p in enumerate(projects)}

    pos = {}
    for n in nodes:
        proj, stage = n
        x = stage_x.get(stage, 0)
        y = y_of[proj]
        pos[n] = (x, y)

    # color by tech; fade if abandoned
    color_map = {
        "storage":   "#4C72B0",   # blue
        "transport": "#55A868",   # green
        "capture":   "#DD8452",   # orange
        "joint":     "#C44E52",   # red
    }
    colors, edgecolors = [], []
    for n in nodes:
        tech = G.nodes[n].get("tech", "")
        base = color_map.get(tech, "#888888")
        if G.nodes[n].get("abandoned") is not None:
            colors.append("#DDDDDD")          # faded fill for abandoned
            edgecolors.append(base)            # keep tier color as outline
        else:
            colors.append(base)
            edgecolors.append("black")

    # short labels: project + abbreviated stage
    def short(stage):
        return {
            "definition": "def",
            "approval": "app",
            "construction": "con",
            "commissioning": "com",
            "definition joint node": "defJ",
            "approval joint node": "appJ",
            "FID joint node": "FID",
        }.get(stage, stage[:4])

    labels = {n: f"{n[0]}\n{short(n[1])}" for n in nodes}

    sub = G.subgraph(nodes)
    plt.figure(figsize=(16, max(6, len(projects) * 0.8)))
    nx.draw(
        sub, pos,
        node_color=colors,
        edgecolors=edgecolors,
        linewidths=1.5,
        node_size=1400,
        with_labels=True,
        labels=labels,
        font_size=6,
        arrows=True,
        arrowsize=10,
        edge_color="#bbbbbb",
        width=1.0,
    )

    # column headers along the top
    ymax = len(projects)
    for stage, x in stage_x.items():
        plt.text(x, ymax, short(stage), ha="center", fontsize=8, fontweight="bold")

    title = "CCS three-tier DAG"
    if storage_filter:
        title += f" — {storage_filter} cluster"
    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.show()