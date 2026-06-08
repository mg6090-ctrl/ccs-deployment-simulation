import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_node(("projA", "Definition"), duration=12, ES=0.0, EF=0.0)
G.add_node(("projA", "Approvals"), duration=18, ES=0.0, EF=0.0)
G.add_node(("projA", "Construction"), duration=24, ES=0.0, EF=0.0)
G.add_edge(("projA", "Definition"), ("projA", "Approvals"))
G.add_edge(("projA", "Approvals"), ("projA", "Construction"))

print(list(G.nodes))
print(G.nodes[("projA", "Definition")])          # the attribute dict
print(G.nodes[("projA", "Definition")]["duration"])
print(G.nodes[("projA", "Construction")]["ES"])
print(list(G.predecessors(("projA", "Approvals"))))
print(list(G.successors(("projA", "Definition"))))
print(list(G.successors(("projA", "Approvals"))))
print(list(G.successors(("projA", "Construction"))))
print(list(G.neighbors(("projA", "Approvals"))))

nx.draw(G, with_labels=True, font_weight='bold')