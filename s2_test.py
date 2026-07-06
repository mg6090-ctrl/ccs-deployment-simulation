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

import scenario_2_edits as s2

G1 = s2.buildmodel(trunks=TRUNKS, pipe_downstream=PIPE_DOWNSTREAM, 
                  capture_pipe=CAPTURE_PIPE, capture_durations=CAPTURE, capture_volumes=CAPTURE_VOLUMES,
                  storage_durations=STORAGE, storage_volumes=STORAGE_VOLUMES, transport_durations=TRANSPORT,
                  transport_volumes=TRANSPORT_VOLUMES)

print(s2.traversal_order(G1))
print("No attrition, expecting empty dicts: \n")
# print(s2.apply_attrition(G1, pipe_downstream=PIPE_DOWNSTREAM, capture_pipe=CAPTURE_PIPE, base_rate=0, max_rate=0, threshold_frac=0.5, late_penalty=0))
results_1 = s2.monte_carlo(5, 
                sampling=True, 
                trunks = TRUNKS,
                pipe_downstream=PIPE_DOWNSTREAM,
                capture_pipe=CAPTURE_PIPE,
                base_rate=0, 
                threshold_frac=0.5,
                max_rate=0,
                capture_durations=CAPTURE, 
                capture_volumes=CAPTURE_VOLUMES,
                storage_durations=STORAGE, 
                storage_volumes=STORAGE_VOLUMES,
                transport_durations=TRANSPORT, 
                transport_volumes=TRANSPORT_VOLUMES,
                late_penalty = 0)
print(s2.analyze_monte_carlo(results_1))

G2 = s2.buildmodel(trunks=TRUNKS, pipe_downstream=PIPE_DOWNSTREAM, 
                  capture_pipe=CAPTURE_PIPE, capture_durations=CAPTURE, capture_volumes=CAPTURE_VOLUMES,
                  storage_durations=STORAGE, storage_volumes=STORAGE_VOLUMES, transport_durations=TRANSPORT,
                  transport_volumes=TRANSPORT_VOLUMES)
print("Full attrition, expecting all dicts to be full: \n")
# print(s2.apply_attrition(G2, pipe_downstream=PIPE_DOWNSTREAM, capture_pipe=CAPTURE_PIPE, base_rate=1, max_rate=1, threshold_frac=0.5, late_penalty=0))
results_2 = s2.monte_carlo(100, 
                sampling=True, 
                trunks = TRUNKS,
                pipe_downstream=PIPE_DOWNSTREAM,
                capture_pipe=CAPTURE_PIPE,
                base_rate=0.05, 
                threshold_frac=0.5,
                max_rate=0.4,
                capture_durations=CAPTURE, 
                capture_volumes=CAPTURE_VOLUMES,
                storage_durations=STORAGE, 
                storage_volumes=STORAGE_VOLUMES,
                transport_durations=TRANSPORT, 
                transport_volumes=TRANSPORT_VOLUMES,
                late_penalty = 0)
print(s2.analyze_monte_carlo(results_2))
