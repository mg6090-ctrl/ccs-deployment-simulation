#==================================================================
# PROJECT DATA
#==================================================================

CAPTURE = {
    "projC1":  {"definition": 12, "approval": 24, "construction": 36},
    "projC2":  {"definition": 12, "approval": 24, "construction": 36},
    "projC3":  {"definition": 12, "approval": 24, "construction": 36},
    "projC4":  {"definition": 12, "approval": 24, "construction": 36},
    "projC5":  {"definition": 6, "approval": 9, "construction": 12},
    "projC6":  {"definition": 6, "approval": 9, "construction": 12},
    "projC7":  {"definition": 6, "approval": 6, "construction": 6},
    "projC8":  {"definition": 6, "approval": 6, "construction": 6},
}

CAPTURE_VOLUMES = {
    "projC1": 1.469847, "projC2": 1.112612, "projC3": 0.823186, "projC4": 0.241809, 
    "projC5": 0.060437, "projC6": 0.114565, 
    "projC7": 1.011104, "projC8": 0.059286                  
}

# dictionary for storage projects
STORAGE = {
    "projS1":  {"definition": 24, "approval": 30, "construction": 24}   
}

# capture volumes
STORAGE_VOLUMES = {
    "projS1": 6
}

# dictionary for transport projects
TRANSPORT = {
    "projT1":  {"definition": 9, "approval": 36, "construction": 30}
}

# transport volumes
TRANSPORT_VOLUMES = {
    "projT1": 6
}

CLUSTERS = {
    "projS1":  {
        "projT1": ["projC1", "projC2", "projC3", "projC4", "projC5", "projC6", "projC7", "projC8"]
        }
}

# stores the pipe/storage every single transport flows into next
PIPE_DOWNSTREAM = {"projT1": "projS1"}

# stores the transport every single capture flows into next
CAPTURE_PIPE = {"projC1": "projT1", 
                "projC2": "projT1",
                "projC3": "projT1",
                "projC4": "projT1",
                "projC5": "projT1",
                "projC6": "projT1",
                "projC7": "projT1",
                "projC8": "projT1"}