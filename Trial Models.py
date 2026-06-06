# imports
import random
from pathlib import Path
from typing import Dict, List, Tuple

import hashlib
import networkx as nx
import numpy as np
import pandas as pd

#============================================================================================
# Constants
#============================================================================================

STAGES = ["Definition", "Approval", "Construction"]
STAGES4 = ["Definition", "Approval", "Construction", "Commissioning"]

DEFAULT_DURATIONS = {
    "Capture": {
        "Definition_months": 36,
        "Approvals_months": 24,
        "Construction_months": 48,
    },
    "TS": {
        "Definition_months": 60, #there will likely always be a mismatch because the definition times are different
        "Approvals_months": 24,
        "Construction_months": 36,  
    },
}

DURATION_DISTRIBUTIONS = {
    "Capture": {
        "enabled": False,  # Set to True to enable per-project duration sampling
        "Definition_months": {
            "distribution": "normal",  # "normal", "lognormal", or "uniform"
            "mean": 36,
            "std": 2,  # Standard deviation for normal/lognormal distributions
            "min": 12,   # Optional minimum bound (clips samples)
            "max": ,  # Optional maximum bound (clips samples)
        },
        "Approvals_months": {
            "distribution": "normal",
            "mean": 24,
            "min": 48,   # Optional minimum bound (clips samples)
            "max": 18,  # Optional maximum bound (clips samples)
        },
        "Approvals_months": {
            "distribution": "normal",
            "mean": 12,
            "std": 2,
            "min": 6,
            "max": 18,
        },
        "Construction_months": {
            "distribution": "normal",
            "mean": 48,
            "mean": 18,
            "std": 3,
            "min": 9,
            "max": 27,
        },
    },

    "TS": {
        "enabled": False,
        "Definition_months": {
            "distribution": "normal",
            "mean": 24,
            "std": 4,
            "min": 12,
            "max": 36,
        },
        "Approvals_months": {
            "distribution": "normal",
            "mean": 36,
            "std": 6,
            "min": 18,
            "max": 54,
        },
        "Construction_months": {
            "distribution": "normal",
            "mean": 120, 
            "mean": 120,  # Will be overridden by transmission lead_time_months if using params
            "std": 20,
            "min": 60,
            "max": 180,
        },
    },
}


#============================================================================================
# Scenario 1: coordinated
#============================================================================================

SCENARIO1_PARAMS = {
    
}

#============================================================================================
# Scenario 2: multi-party uncoordinated
#============================================================================================

SCENARIO2_PARAMS = {
    
}

#============================================================================================
# Scenario 3: independent uncoordinated
#============================================================================================

SCENARIO3_PARAMS = {
    "attrition": {
        "enabled": False,
        "base_rate": 0.05,
        "delay_threshold_years": 1.0,
        "max_rate": 0.50,
    }
}

# data handling


# Scenario3 DAG
G = nx.digraph(
    
)



