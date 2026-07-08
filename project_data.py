#==================================================================
# PARAMETERS AND CONSTANTS
#==================================================================

DURATION_BY_TYPE = {
    "storage": {"definition": 24, "approval": 30, "construction": 24},
    "transport": {"definition": 9, "approval": 36, "construction": 30},

    "NGCC": {"definition": 12, "approval": 24, "construction": 36},
    "ethanol": {"definition": 6, "approval": 9, "construction": 12},
    "gas_processing": {"definition": 6, "approval": 6, "construction": 6},
    
    # the following have not been confirmed and are placeholders:
    "DAC": {"definition": 12, "approval": 24, "construction": 36},
    "CHP": {"definition": 12, "approval": 24, "construction": 36},
    "legacy_biomass": {"definition": 12, "approval": 24, "construction": 36},
    "refinery": {"definition": 12, "approval": 24, "construction": 36},
    "biomass_gasification": {"definition": 12, "approval": 24, "construction": 36},
    "hydrogen": {"definition": 12, "approval": 24, "construction": 36},
    "cement": {"definition": 12, "approval": 24, "construction": 36},
    "other_industrial": {"definition": 12, "approval": 24, "construction": 36}
}

#==================================================================
# PROJECT DATA 
#==================================================================

PROJECT_TYPE = {"projC1": "NGCC", "projC2": "NGCC", "projC3": "NGCC", "projC4": "NGCC",
               "projC5": "ethanol", "projC6": "ethanol",
               "projC7": "gas_processing", "projC8": "gas_processing",
               "projS1": "storage",
               "projT1": "transport"}

CAPTURE = {
    "projC1":  DURATION_BY_TYPE[PROJECT_TYPE["projC1"]],
    "projC2":  DURATION_BY_TYPE[PROJECT_TYPE["projC2"]],
    "projC3":  DURATION_BY_TYPE[PROJECT_TYPE["projC3"]],
    "projC4":  DURATION_BY_TYPE[PROJECT_TYPE["projC4"]],
    "projC5":  DURATION_BY_TYPE[PROJECT_TYPE["projC5"]],
    "projC6":  DURATION_BY_TYPE[PROJECT_TYPE["projC6"]],
    "projC7":  DURATION_BY_TYPE[PROJECT_TYPE["projC7"]],
    "projC8":  DURATION_BY_TYPE[PROJECT_TYPE["projC8"]]
}

CAPTURE_VOLUMES = {
    "projC1": 1.469847, "projC2": 1.112612, "projC3": 0.823186, "projC4": 0.241809, 
    "projC5": 0.060437, "projC6": 0.114565, 
    "projC7": 1.011104, "projC8": 0.059286                  
}

# dictionary for storage projects
STORAGE = {
    "projS1":  DURATION_BY_TYPE[PROJECT_TYPE["projS1"]]  
}

# capture volumes
STORAGE_VOLUMES = {
    "projS1": 6
}

# dictionary for transport projects
TRANSPORT = {
    "projT1":  DURATION_BY_TYPE[PROJECT_TYPE["projT1"]]
}

# transport volumes
TRANSPORT_VOLUMES = {
    "projT1": 6
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

TRUNKS = ["projT1"]

# getting the total capacity of all transport projects for the hammock node
TRANSPORT_CAPACITY = sum(TRANSPORT_VOLUMES.values())