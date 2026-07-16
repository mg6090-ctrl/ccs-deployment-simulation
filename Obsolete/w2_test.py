# NOTE: NEED TO REWRITE THIS!

# Two spurs (projT2, projT3) feed a trunk (projT1); a capture (projC3)
# attaches directly to the trunk; trunk feeds storage (projS1).
#
#   projC1 ┐
#          ├─> projT2 (spurA) ─┐
#   projC2 ┘                   │
#                              ├─> projT1 (trunk) ─> projS1 (storage)
#   projC3 ────────────────────┤  (direct capture on trunk)
#                              │
#   projC4 ─> projT3 (spurB) ──┘

PIPE_DOWNSTREAM = {
    "projT2": "projT1",   # spurA -> trunk
    "projT3": "projT1",   # spurB -> trunk
    "projT1": "projS1",   # trunk -> storage
}

CAPTURE_PIPE = {
    "projC1": "projT2",   # -> spurA
    "projC2": "projT2",   # -> spurA
    "projC3": "projT1",   # -> trunk DIRECTLY
    "projC4": "projT3",   # -> spurB
}

TRUNKS = ["projT1"]

CAPTURE_VOLUMES = {"projC1": 1.5, "projC2": 1.5, "projC3": 2.0, "projC4": 1.5}
TRANSPORT_VOLUMES = {"projT1": 8, "projT2": 4, "projT3": 2}
STORAGE_VOLUMES = {"projS1": 10}

CAPTURE = {
    "projC1": {"definition": 5, "approval": 10, "construction": 10},
    "projC2": {"definition": 5, "approval": 10, "construction": 10},
    "projC3": {"definition": 6, "approval": 12, "construction": 12},
    "projC4": {"definition": 5, "approval": 10, "construction": 10},
}
TRANSPORT = {
    "projT1": {"definition": 8, "approval": 20, "construction": 20},
    "projT2": {"definition": 6, "approval": 15, "construction": 15},
    "projT3": {"definition": 6, "approval": 15, "construction": 15},
}
STORAGE = {"projS1": {"definition": 10, "approval": 24, "construction": 20}}

DATA = dict(
    trunks=TRUNKS, pipe_downstream=PIPE_DOWNSTREAM, capture_pipe=CAPTURE_PIPE,
    capture_durations=CAPTURE, capture_volumes=CAPTURE_VOLUMES,
    storage_durations=STORAGE, storage_volumes=STORAGE_VOLUMES,
    transport_durations=TRANSPORT, transport_volumes=TRANSPORT_VOLUMES,
)

def show(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}   {detail}")

import world_2 as s2

# ============================================================
# TEST 1 — full-collapse boundary: base=1,max=1,late=1 -> everything dies
# ============================================================
print("\n[1] Full collapse boundary")
res = s2.monte_carlo(50, sampling=True, base_rate=1.0, max_rate=1.0, late_penalty=1.0,
                     threshold_frac=0.5, **DATA)
a = s2.analyze_monte_carlo(res)
show("all reps collapse (all_abandoned rate == 1.0)",
     a["all abandoned rate"] == 1.0, f"got {a['all abandoned rate']}")
show("final volume ~ 0",
     a["average final vol of capture"] == 0.0, f"got {a['average final vol of capture']}")

# ============================================================
# TEST 2 — storage-marking fix: a storage collapse -> completion 0 -> counted
# ============================================================
print("\n[2] Storage marking fix")
# Force storage to fail its threshold by making its required fraction unreachable:
# run with a high threshold_frac so the storage FID can't fire.
res2 = s2.monte_carlo(30, sampling=True, base_rate=0.0, max_rate=0.0, late_penalty=0.0,
                      threshold_frac=0.99, **DATA)   # 0.99 -> very hard to meet
a2 = s2.analyze_monte_carlo(res2)
# if storage can't fire, those reps should show as collapsed (completion 0)
storage_deaths = sum(1 for r in res2 if r["a_s"])
completion_zero = sum(1 for r in res2 if r["completion"] == 0)
show("reps where storage abandoned are counted as completion 0",
     storage_deaths == 0 or completion_zero >= storage_deaths,
     f"storage_deaths={storage_deaths}, completion_zero={completion_zero}")

# ============================================================
# TEST 3 — cascade containment: kill ONE spur, siblings survive
# ============================================================
print("\n[3] Cascade containment (manual, one graph)")
G = s2.buildmodel(replication_seed=0, sampling=False, **{k:v for k,v in DATA.items()})
s2.CPM(G, 0.5)
# manually collapse spur projT2 and cascade
s2.mark_all_abandonment(G, "projT2", PIPE_DOWNSTREAM, CAPTURE_PIPE)
# projT2's captures (C1,C2) should be abandoned; projT3 and its cap C4 should NOT
c1 = G.nodes[("projC1","definition")]["abandoned"] is not None
c2 = G.nodes[("projC2","definition")]["abandoned"] is not None
t3 = G.nodes[("projT3","definition")]["abandoned"] is not None
c4 = G.nodes[("projC4","definition")]["abandoned"] is not None
show("spurA's captures C1,C2 abandoned", c1 and c2, f"C1={c1},C2={c2}")
show("sibling spurB (T3) NOT abandoned", not t3, f"T3 abandoned={t3}")
show("sibling's capture C4 NOT abandoned", not c4, f"C4 abandoned={c4}")

# ============================================================
# TEST 4 — cascade reach: kill the trunk, EVERYTHING upstream stranded
# ============================================================
print("\n[4] Cascade reach (manual, fresh graph)")
G2 = s2.buildmodel(replication_seed=0, sampling=False, **{k:v for k,v in DATA.items()})
s2.CPM(G2, 0.5)
s2.mark_all_abandonment(G2, "projT1", PIPE_DOWNSTREAM, CAPTURE_PIPE)
all_caps = ["projC1","projC2","projC3","projC4"]
all_pipes = ["projT1","projT2","projT3"]
caps_dead = all(G2.nodes[(c,"definition")]["abandoned"] is not None for c in all_caps)
pipes_dead = all(G2.nodes[(p,"definition")]["abandoned"] is not None for p in all_pipes)
show("all captures stranded by trunk death", caps_dead)
show("all pipes stranded by trunk death", pipes_dead)

# ============================================================
# TEST 5 — reproducibility: same seed -> same result
# ============================================================
print("\n[5] Reproducibility")
r_a = s2.monte_carlo(10, sampling=True, base_rate=0.1, max_rate=0.4, late_penalty=0.15,
                     threshold_frac=0.5, **DATA)
r_b = s2.monte_carlo(10, sampling=True, base_rate=0.1, max_rate=0.4, late_penalty=0.15,
                     threshold_frac=0.5, **DATA)
same = [x["completion"] for x in r_a] == [y["completion"] for y in r_b] \
       and [x["final volume"] for x in r_a] == [y["final volume"] for y in r_b]
show("identical results across two runs with same params", same)

print("\nDone.")