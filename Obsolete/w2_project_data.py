#==================================================================
# PARAMETERS AND CONSTANTS
#==================================================================

DURATION_BY_TYPE = {
    "storage": {"definition": 24, "approval": 30, "construction": 24},
    "transport": {"definition": 24, "approval": 24, "construction": 30},
    
    "NGCC": {"definition": 24, "approval": 12, "construction": 36},
    "ethanol": {"definition": 6, "approval": 9, "construction": 12},
    "gas_processing": {"definition": 6, "approval": 6, "construction": 6},
    "refinery": {"definition": 30, "approval": 24, "construction": 36},
    "legacy_biomass": {"definition": 18, "approval": 18, "construction": 30},
    "CHP": {"definition": 24, "approval": 12, "construction": 36},
    "other_industrial": {"definition": 24, "approval": 12, "construction": 36},
    
    "DAC": {"definition": 24, "approval": 12, "construction": 36},
    "biomass_gasification": {"definition": 24, "approval": 12, "construction": 36},
    "hydrogen": {"definition": 24, "approval": 12, "construction": 24},
    "cement": {"definition": 24, "approval": 12, "construction": 36}
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
               "projS1": "storage", "projS2": "storage", "projS3": "storage", "projS4": "storage",
               "projS5": "storage", "projS6": "storage", "projS7": "storage", "projS8": "storage",
               "projS9": "storage", "projS10": "storage",
               "projT1": "transport", "projT2": "transport", "projT3": "transport", "projT4": "transport",
               "projT5": "transport", "projT6": "transport", "projT7": "transport", "projT8": "transport",
               "projT9": "transport", "projT10": "transport"}

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

# dictionary for transport project duration
TRANSPORT = {
    "projT1":  DURATION_BY_TYPE[PROJECT_TYPE["projT1"]],
    "projT2":  DURATION_BY_TYPE[PROJECT_TYPE["projT2"]],
    "projT3":  DURATION_BY_TYPE[PROJECT_TYPE["projT3"]],
    "projT4":  DURATION_BY_TYPE[PROJECT_TYPE["projT4"]],
    "projT5":  DURATION_BY_TYPE[PROJECT_TYPE["projT5"]],
    "projT6":  DURATION_BY_TYPE[PROJECT_TYPE["projT6"]],
    "projT7":  DURATION_BY_TYPE[PROJECT_TYPE["projT7"]],
    "projT8":  DURATION_BY_TYPE[PROJECT_TYPE["projT8"]],
    "projT9":  DURATION_BY_TYPE[PROJECT_TYPE["projT9"]],
    "projT10":  DURATION_BY_TYPE[PROJECT_TYPE["projT10"]]
}

# transport volumes
TRANSPORT_VOLUMES = {
    "projT1": CAPTURE_VOLUMES["projC7"] + CAPTURE_VOLUMES["projC6"] + CAPTURE_VOLUMES["projC9"],
    "projT2": CAPTURE_VOLUMES["projC10"] + CAPTURE_VOLUMES["projC8"],
    "projT3": CAPTURE_VOLUMES["projC20"] + CAPTURE_VOLUMES["projC19"],
    "projT4": CAPTURE_VOLUMES["projC18"] + CAPTURE_VOLUMES["projC17"],
    "projT5": CAPTURE_VOLUMES["projC16"],
    "projT6": CAPTURE_VOLUMES["projC15"] + CAPTURE_VOLUMES["projC14"],
    "projT7": CAPTURE_VOLUMES["projC13"] + CAPTURE_VOLUMES["projC12"],
    "projT8": CAPTURE_VOLUMES["projC11"],
    "projT9": CAPTURE_VOLUMES["projC5"] + CAPTURE_VOLUMES["projC4"],
    "projT10": CAPTURE_VOLUMES["projC1"] + CAPTURE_VOLUMES["projC2"] + CAPTURE_VOLUMES["projC3"]
}

# dictionary for storage project duration
STORAGE = {
    "projS1":  DURATION_BY_TYPE[PROJECT_TYPE["projS1"]],
    "projS2":  DURATION_BY_TYPE[PROJECT_TYPE["projS2"]],
    "projS3":  DURATION_BY_TYPE[PROJECT_TYPE["projS3"]],
    "projS4":  DURATION_BY_TYPE[PROJECT_TYPE["projS4"]],
    "projS5":  DURATION_BY_TYPE[PROJECT_TYPE["projS5"]],
    "projS6":  DURATION_BY_TYPE[PROJECT_TYPE["projS6"]],
    "projS7":  DURATION_BY_TYPE[PROJECT_TYPE["projS7"]],
    "projS8":  DURATION_BY_TYPE[PROJECT_TYPE["projS8"]],
    "projS9":  DURATION_BY_TYPE[PROJECT_TYPE["projS9"]],
    "projS10":  DURATION_BY_TYPE[PROJECT_TYPE["projS10"]]
}

# capture volumes
STORAGE_VOLUMES = {
    "projS1": TRANSPORT_VOLUMES["projT1"],
    "projS2": TRANSPORT_VOLUMES["projT2"],
    "projS3": TRANSPORT_VOLUMES["projT3"],
    "projS4": TRANSPORT_VOLUMES["projT4"],
    "projS5": TRANSPORT_VOLUMES["projT5"],
    "projS6": TRANSPORT_VOLUMES["projT6"],
    "projS7": TRANSPORT_VOLUMES["projT7"],
    "projS8": TRANSPORT_VOLUMES["projT8"],
    "projS9": TRANSPORT_VOLUMES["projT9"],
    "projS10": TRANSPORT_VOLUMES["projT10"]
}

# stores the pipe/storage every single transport flows into next
PIPE_DOWNSTREAM = {"projT1": "projS1",
                   "projT2": "projS2",
                   "projT3": "projS3",
                   "projT4": "projS4",
                   "projT5": "projS5",
                   "projT6": "projS6",
                   "projT7": "projS7",
                   "projT8": "projS8",
                   "projT9": "projS9",
                   "projT10": "projS10"
                   }

# stores the transport every single capture flows into next
CAPTURE_PIPE = {"projC1": "projT10", 
                "projC2": "projT10",
                "projC3": "projT10",
                "projC4": "projT9",
                "projC5": "projT9",
                "projC6": "projT1",
                "projC7": "projT1",
                "projC8": "projT2",
                "projC9": "projT1",
                "projC10": "projT2",
                "projC11": "projT8",
                "projC12": "projT7",
                "projC13": "projT7",
                "projC14": "projT6",
                "projC15": "projT6",
                "projC16": "projT5",
                "projC17": "projT4",
                "projC18": "projT4",
                "projC19": "projT3",
                "projC20": "projT3",
                }

TRUNKS = ["projT1", "projT2", "projT3", "projT4", "projT5", "projT6", "projT7", "projT8", "projT9", "projT10"]

# sum of all capture volumes
PLANNED_CAP_VOLUME = sum(CAPTURE_VOLUMES.values())

# getting the total capacity of all transport projects for the hammock node
TRANSPORT_CAPACITY = sum(TRANSPORT_VOLUMES.values())

CAPTURE_NUM = len(CAPTURE_VOLUMES)