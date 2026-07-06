#==================================================================
# PROJECT DATA
#==================================================================

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
