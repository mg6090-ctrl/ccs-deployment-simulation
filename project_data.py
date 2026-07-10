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

PROJECT_TYPE = {"projC1": "ethanol", "projC2": "CHP", "projC3": "other_industrial", "projC4": "NGCC",
               "projC5": "gas_processing", "projC6": "hydrogen", "projC7": "hydrogen", 
               "projC8": "NGCC", "projC9": "hydrogen", "projC10": "hydrogen",
               "projC11": "NGCC", "projC12": "NGCC", "projC13": "NGCC", "projC14": "cement",
               "projC15": "cement", "projC16": "NGCC", "projC17": "cement", "projC18": "NGCC",
               "projC19": "NGCC", "projC20": "NGCC",
               "projS1": "storage",
               "projT1": "transport", "projT2": "transport", "projT3": "transport", "projT4": "transport",
               "projT5": "transport", "projT6": "transport"}

CAPTURE = {
    "projC1":  DURATION_BY_TYPE[PROJECT_TYPE["projC1"]],
    "projC2":  DURATION_BY_TYPE[PROJECT_TYPE["projC2"]],
    "projC3":  DURATION_BY_TYPE[PROJECT_TYPE["projC3"]],
    "projC4":  DURATION_BY_TYPE[PROJECT_TYPE["projC4"]],
    "projC5":  DURATION_BY_TYPE[PROJECT_TYPE["projC5"]],
    "projC6":  DURATION_BY_TYPE[PROJECT_TYPE["projC6"]],
    "projC7":  DURATION_BY_TYPE[PROJECT_TYPE["projC7"]],
    "projC8":  DURATION_BY_TYPE[PROJECT_TYPE["projC8"]],
    "projC9":  DURATION_BY_TYPE[PROJECT_TYPE["projC9"]],
    "projC10":  DURATION_BY_TYPE[PROJECT_TYPE["projC10"]],
    "projC11":  DURATION_BY_TYPE[PROJECT_TYPE["projC11"]],
    "projC12":  DURATION_BY_TYPE[PROJECT_TYPE["projC12"]],
    "projC13":  DURATION_BY_TYPE[PROJECT_TYPE["projC13"]],
    "projC14":  DURATION_BY_TYPE[PROJECT_TYPE["projC14"]],
    "projC15":  DURATION_BY_TYPE[PROJECT_TYPE["projC15"]],
    "projC16":  DURATION_BY_TYPE[PROJECT_TYPE["projC16"]],
    "projC17":  DURATION_BY_TYPE[PROJECT_TYPE["projC17"]],
    "projC18":  DURATION_BY_TYPE[PROJECT_TYPE["projC18"]],
    "projC19":  DURATION_BY_TYPE[PROJECT_TYPE["projC19"]],
    "projC20":  DURATION_BY_TYPE[PROJECT_TYPE["projC20"]],
}

CAPTURE_VOLUMES = {
    "projC1": 0.11456479, 
    "projC2": 0.1, 
    "projC3": 1.16088723, 
    "projC4": 5.3936315, 
    "projC5": 0.05928638, 
    "projC6": 0.74503409, 
    "projC7": 0.68691579, 
    "projC8": 5.77191104,
    "projC9": 0.79684855,
    "projC10": 0.55500457,
    "projC11": 2.36524677,
    "projC12": 2.87235057,
    "projC13": 2.50024,    
    "projC14": 1.27784973,
    "projC15": 1.75064696,
    "projC16": 2.76474897,
    "projC17": 1.09492648,
    "projC18": 1.76115055,
    "projC19": 1.42724397,
    "projC20": 1.72663998,
}

# dictionary for storage project duration
STORAGE = {
    "projS1":  DURATION_BY_TYPE[PROJECT_TYPE["projS1"]],
}

# capture volumes
STORAGE_VOLUMES = {
    "projS1": 34.92512792
}

# dictionary for transport project duration
TRANSPORT = {
    "projT1":  DURATION_BY_TYPE[PROJECT_TYPE["projT1"]],
    "projT2":  DURATION_BY_TYPE[PROJECT_TYPE["projT2"]],
    "projT3":  DURATION_BY_TYPE[PROJECT_TYPE["projT3"]],
    "projT4":  DURATION_BY_TYPE[PROJECT_TYPE["projT4"]],
    "projT5":  DURATION_BY_TYPE[PROJECT_TYPE["projT5"]],
    "projT6":  DURATION_BY_TYPE[PROJECT_TYPE["projT6"]],
}

# transport volumes
TRANSPORT_VOLUMES = {
    "projT1": 34.92512792,
    "projT2": 6.32691561,
    "projT3": 19.54104398,
    "projT4": 6.00996098,
    "projT5": 0.55500457,
    "projT6": 0.79684855,
}

# stores the pipe/storage every single transport flows into next
PIPE_DOWNSTREAM = {"projT1": "projS1",
                   "projT2": "projT1",
                   "projT3": "projT1",
                   "projT4": "projT3",
                   "projT5": "projT2",
                   "projT6": "projT1"
                   }

# stores the transport every single capture flows into next
CAPTURE_PIPE = {"projC1": "projT1", 
                "projC2": "projT1",
                "projC3": "projT1",
                "projC4": "projT1",
                "projC5": "projT1",
                "projC6": "projT1",
                "projC7": "projT1",
                "projC8": "projT2",
                "projC9": "projT6",
                "projC10": "projT5",
                "projC11": "projT3",
                "projC12": "projT3",
                "projC13": "projT3",
                "projC14": "projT3",
                "projC15": "projT3",
                "projC16": "projT3",
                "projC17": "projT4",
                "projC18": "projT4",
                "projC19": "projT4",
                "projC20": "projT4",
                }

TRUNKS = ["projT1"]

# getting the total capacity of all transport projects for the hammock node
TRANSPORT_CAPACITY = sum(TRANSPORT_VOLUMES.values())

CAPTURE_NUM = len(CAPTURE_VOLUMES)