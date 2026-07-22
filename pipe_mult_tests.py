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
    "cement": {"definition": 24, "approval": 12, "construction": 36},
}

#==================================================================
# DURATION MULTIPLIERS FOR PIPELINE
#==================================================================

PIPE_MULT_MIN = {
    "projT11":  1,
    "projT12":  1,
    "projT13":  1,
    "projT14":  1.04,
    "projT15":  1,
    "projT16":  1.84,
    "projT17":  1,
    "projT18":  2.34,
    "projT19":  1,
    "projT110":  1,
    "projT111":  1.15,

    "projT21":  1,
    "projT22":  1,
    "projT23":  1,
    "projT24":  1,
    "projT25":  1.66,

    "projT31":  1,
    "projT32":  1,
    "projT33":  1,

    "projT41":  1,
    "projT42":  1.00,

    "projT51":  1.99,
    "projT52":  1,
    "projT53":  1.51,
    "projT54":  2.73,
    "projT55":  2.53,
    "projT56":  1,
    "projT57":  1
}

PIPE_MULT = {
    "projT11":  0.77,
    "projT12":  0.24,
    "projT13":  0.69,
    "projT14":  1.04,
    "projT15":  0.93,
    "projT16":  1.84,
    "projT17":  0.97,
    "projT18":  2.34,
    "projT19":  0.70,
    "projT110":  0.42,
    "projT111":  1.15,

    "projT21":  0.76,
    "projT22":  0.21,
    "projT23":  0.43,
    "projT24":  0.77,
    "projT25":  1.66,

    "projT31":  0.58,
    "projT32":  0.45,
    "projT33":  0.69,

    "projT41":  0.42,
    "projT42":  1.00,

    "projT51":  1.99,
    "projT52":  0.16,
    "projT53":  1.51,
    "projT54":  2.73,
    "projT55":  2.53,
    "projT56":  0.44,
    "projT57":  0.59
}

#==================================================================
# PROJECT DATA 
#==================================================================

PROJECT_TYPE = {"projC0": "ethanol",
                "projC1": "hydrogen", 
                "projC2": "hydrogen", 
                "projC3": "hydrogen", 
                "projC4": "hydrogen",
               "projC5": "hydrogen", 
               "projC6": "hydrogen", 
               # "projC7": "gas_processing", 
               "projC8": "gas_processing", 
               "projC9": "NGCC", 
               "projC10": "NGCC",
               "projC11": "NGCC", 
               "projC12": "cement", 
               "projC13": "cement", 
               # "projC14": "cement",
               "projC15": "cement", 
               # "projC16": "refinery", 
               "projC17": "legacy_biomass", 
               # "projC18": "legacy_biomass",
               # "projC19": "refinery", 
               "projC20": "NGCC",
               "projC21": "cement", 
               "projC22": "cement",
               # "projC23": "legacy_biomass", 
               "projC24": "NGCC",
               "projC25": "NGCC", 
               "projC26": "ethanol", 
               # "projC27": "legacy_biomass", 
               # "projC28": "legacy_biomass",
               "projC29": "NGCC", 
               # "projC30": "cement", 
               # "projC31": "NGCC", 
               # "projC32": "legacy_biomass", 
               "projC33": "biomass_gasification", 
               "projC34": "biomass_gasification", 
               "projC35": "biomass_gasification",
               "projC36": "biomass_gasification", 
               "projC37": "biomass_gasification", 
               "projC38": "biomass_gasification",
               "projC39": "biomass_gasification", 
               "projC40": "biomass_gasification", 
               "projC41": "biomass_gasification",
               "projC42": "biomass_gasification", 
               "projC43": "biomass_gasification", 
               "projC44": "biomass_gasification",
               "projC45": "biomass_gasification", 
               "projC46": "biomass_gasification", 
               "projC47": "biomass_gasification",
               "projC48": "biomass_gasification", 
               "projC49": "biomass_gasification", 
               "projC50": "biomass_gasification",
               "projC51": "biomass_gasification", 
               "projC52": "biomass_gasification", 
               "projC53": "biomass_gasification",
               "projC54": "biomass_gasification", 
               # "projC55": "biomass_gasification", 
               "projC56": "biomass_gasification",

               "projS0": "storage",
               "projS1": "storage", 
               # "projS2": "storage", 
               "projS3": "storage", 
               # "projS4": "storage",
               "projS5": "storage", 
               "projS6": "storage", 
               "projS7": "storage", 

               "projT11": "transport", "projT12": "transport", "projT13": "transport", "projT14": "transport",
               "projT15": "transport", "projT16": "transport", "projT17": "transport", "projT18": "transport", "projT19": "transport",
               "projT110": "transport", "projT111": "transport",

               "projT21": "transport", "projT22": "transport", "projT23": "transport", "projT24": "transport", "projT25": "transport",

               "projT31": "transport", "projT32": "transport", "projT33": "transport", 

               "projT41": "transport", "projT42": "transport", 

               "projT51": "transport", "projT52": "transport", "projT53": "transport", "projT54": "transport", "projT55": "transport",
               "projT56": "transport", "projT57": "transport"
               }

#==================================================================
# TOPOLOGICAL DATA FOR GRAPH
#==================================================================

# stores the pipe/storage every single transport flows into next
PIPE_DOWNSTREAM = {
                   # group 1
                   "projT11": "projS1",
                   "projT12": "projT11",
                   "projT13": "projS1",
                   "projT14": "projS1",
                   "projT16": "projS1",
                   "projT15": "projT16",
                   "projT17": "projT16",

                   "projT18": "projS0",
                   "projT19": "projS0",
                   "projT110": "projT18",
                   "projT111": "projT18",

                   # group 2
                   "projT21": "projS3",
                   "projT22": "projS3",
                   "projT23": "projT22",
                   "projT24": "projT22",
                   "projT25": "projT21",
                   
                   # group 3
                   "projT31": "projS5",
                   "projT32": "projS5",
                   "projT33": "projT32",
                   
                   # group 4
                   "projT41": "projS6",
                   "projT42": "projS6",

                   # group 5
                   "projT51": "projS7",
                   "projT52": "projS7",
                   "projT53": "projT51",
                   "projT54": "projT53",
                   "projT55": "projT54",
                   "projT56": "projS7",
                   "projT57": "projS7"
                   }

# stores the transport every single capture flows into next
CAPTURE_PIPE = {
                # group 1 
                "projC10": "projT11",
                "projC11": "projT11",
                "projC22": "projT12",
                "projC45": "projT13",
                "projC35": "projT14",
                "projC21": "projT15",
                "projC56": "projT15",
                "projC47": "projT15",
                "projC41": "projT17",
                "projC49": "projT16",
                "projC34": "projT16",

                "projC37": "projT18",
                "projC33": "projT19",
                "projC44": "projT19",
                "projC51": "projT18",
                "projC38": "projT18",
                "projC48": "projT111",
                "projC46": "projT110",
                
                # group 2
                "projC5": "projT25",
                "projC43": "projT25",
                "projC24": "projT21",
                "projC50": "projT22",
                "projC0": "projT22",
                "projC42": "projT23",
                "projC53": "projT24",
                
                # group 3
                "projC3": "projT31",
                "projC40": "projT32",
                "projC36": "projT33",
                
                # group 4
                "projC1": "projT41",
                "projC4": "projT41",
                "projC2": "projT41",
                "projC52": "projT42",
                
                # group 5
                "projC17": "projT52",
                "projC54": "projT56",
                "projC39": "projT57",
                "projC26": "projT51",
                "projC20": "projT51",
                "projC9": "projT51",
                "projC8": "projT51",
                "projC13": "projT51",
                "projC12": "projT51",
                "projC6": "projT51",
                "projC29": "projT53",
                "projC15": "projT54",
                "projC25": "projT55"
                }

TRUNKS = [
          # group 1
          "projT11",
          "projT13",
          "projT14",
          "projT16",

          "projT18",
          "projT19",
          
          # group 2
          "projT21",
          "projT22",
          
          # group 3
          "projT31",
          "projT32",
          
          # group 4
          "projT41",
          "projT42",

          # group 5
          "projT51",
          "projT52",
          "projT56",
          "projT57"
          
          ]

#==================================================================
# HELPER METHODS/ CALCULATIONS
#==================================================================

def immediate_upstream_project(project, pipe_downstream = PIPE_DOWNSTREAM, capture_pipe = CAPTURE_PIPE):
    # Returns a list of projects that link directly into the given project
    direct_pipes = []
    direct_captures = []
    for upstream, downstream in pipe_downstream.items():
        if downstream == project:
            direct_pipes.append(upstream)
    
    for capture, transport in capture_pipe.items():
        if transport == project:
            direct_captures.append(capture)
    
    return direct_captures, direct_pipes

def everything_upstream(project, pipe_downstream = PIPE_DOWNSTREAM, capture_pipe = CAPTURE_PIPE):
    upstream_pipes = []
    upstream_captures = []

    direct_captures, direct_pipes = immediate_upstream_project(project, pipe_downstream, capture_pipe)
    upstream_captures.extend(direct_captures)

    for pipe in direct_pipes:
        upstream_pipes.append(pipe)
        caps, pipes = everything_upstream(pipe, pipe_downstream, capture_pipe)
        upstream_captures.extend(caps)
        upstream_pipes.extend(pipes)
    
    return upstream_captures, upstream_pipes

def total_vol(project, pipe_downstream = PIPE_DOWNSTREAM, capture_pipe = CAPTURE_PIPE):
    upstream_captures, upstream_pipes = everything_upstream(project, pipe_downstream, capture_pipe)
    sum = 0
    for capture in upstream_captures:
        sum += CAPTURE_VOLUMES[capture]
    return sum 

#==================================================================
# DURATIONS AND VOLUMES
#==================================================================

CAPTURE = {
    "projC0":  DURATION_BY_TYPE[PROJECT_TYPE["projC0"]],
    "projC1":  DURATION_BY_TYPE[PROJECT_TYPE["projC1"]],
    "projC2":  DURATION_BY_TYPE[PROJECT_TYPE["projC2"]],
    "projC3":  DURATION_BY_TYPE[PROJECT_TYPE["projC3"]],
    "projC4":  DURATION_BY_TYPE[PROJECT_TYPE["projC4"]],
    "projC5":  DURATION_BY_TYPE[PROJECT_TYPE["projC5"]],
    "projC6":  DURATION_BY_TYPE[PROJECT_TYPE["projC6"]],
    # "projC7":  DURATION_BY_TYPE[PROJECT_TYPE["projC7"]],
    "projC8":  DURATION_BY_TYPE[PROJECT_TYPE["projC8"]],
    "projC9":  DURATION_BY_TYPE[PROJECT_TYPE["projC9"]],
    "projC10":  DURATION_BY_TYPE[PROJECT_TYPE["projC10"]],
    "projC11":  DURATION_BY_TYPE[PROJECT_TYPE["projC11"]],
    "projC12":  DURATION_BY_TYPE[PROJECT_TYPE["projC12"]],
    "projC13":  DURATION_BY_TYPE[PROJECT_TYPE["projC13"]],
    # "projC14":  DURATION_BY_TYPE[PROJECT_TYPE["projC14"]],
    "projC15":  DURATION_BY_TYPE[PROJECT_TYPE["projC15"]],
    # "projC16":  DURATION_BY_TYPE[PROJECT_TYPE["projC16"]],
    "projC17":  DURATION_BY_TYPE[PROJECT_TYPE["projC17"]],
    # "projC18":  DURATION_BY_TYPE[PROJECT_TYPE["projC18"]],
    # "projC19":  DURATION_BY_TYPE[PROJECT_TYPE["projC19"]],
    "projC20":  DURATION_BY_TYPE[PROJECT_TYPE["projC20"]],

    "projC21":  DURATION_BY_TYPE[PROJECT_TYPE["projC21"]],
    "projC22":  DURATION_BY_TYPE[PROJECT_TYPE["projC22"]],
    # "projC23":  DURATION_BY_TYPE[PROJECT_TYPE["projC23"]],
    "projC24":  DURATION_BY_TYPE[PROJECT_TYPE["projC24"]],
    "projC25":  DURATION_BY_TYPE[PROJECT_TYPE["projC25"]],
    "projC26":  DURATION_BY_TYPE[PROJECT_TYPE["projC26"]],
    # "projC27":  DURATION_BY_TYPE[PROJECT_TYPE["projC27"]],
    # "projC28":  DURATION_BY_TYPE[PROJECT_TYPE["projC28"]],
    "projC29":  DURATION_BY_TYPE[PROJECT_TYPE["projC29"]],
    # "projC30":  DURATION_BY_TYPE[PROJECT_TYPE["projC30"]],
    # "projC31":  DURATION_BY_TYPE[PROJECT_TYPE["projC31"]],
    # "projC32":  DURATION_BY_TYPE[PROJECT_TYPE["projC32"]],
    "projC33":  DURATION_BY_TYPE[PROJECT_TYPE["projC33"]],
    "projC34":  DURATION_BY_TYPE[PROJECT_TYPE["projC34"]],
    "projC35":  DURATION_BY_TYPE[PROJECT_TYPE["projC35"]],
    "projC36":  DURATION_BY_TYPE[PROJECT_TYPE["projC36"]],
    "projC37":  DURATION_BY_TYPE[PROJECT_TYPE["projC37"]],
    "projC38":  DURATION_BY_TYPE[PROJECT_TYPE["projC38"]],
    "projC39":  DURATION_BY_TYPE[PROJECT_TYPE["projC39"]],
    "projC40":  DURATION_BY_TYPE[PROJECT_TYPE["projC40"]],

    "projC41":  DURATION_BY_TYPE[PROJECT_TYPE["projC41"]],
    "projC42":  DURATION_BY_TYPE[PROJECT_TYPE["projC42"]],
    "projC43":  DURATION_BY_TYPE[PROJECT_TYPE["projC43"]],
    "projC44":  DURATION_BY_TYPE[PROJECT_TYPE["projC44"]],
    "projC45":  DURATION_BY_TYPE[PROJECT_TYPE["projC45"]],
    "projC46":  DURATION_BY_TYPE[PROJECT_TYPE["projC46"]],
    "projC47":  DURATION_BY_TYPE[PROJECT_TYPE["projC47"]],
    "projC48":  DURATION_BY_TYPE[PROJECT_TYPE["projC48"]],
    "projC49":  DURATION_BY_TYPE[PROJECT_TYPE["projC49"]],
    "projC50":  DURATION_BY_TYPE[PROJECT_TYPE["projC50"]],
    "projC51":  DURATION_BY_TYPE[PROJECT_TYPE["projC51"]],
    "projC52":  DURATION_BY_TYPE[PROJECT_TYPE["projC52"]],
    "projC53":  DURATION_BY_TYPE[PROJECT_TYPE["projC53"]],
    "projC54":  DURATION_BY_TYPE[PROJECT_TYPE["projC54"]],
    # "projC55":  DURATION_BY_TYPE[PROJECT_TYPE["projC55"]],
    "projC56":  DURATION_BY_TYPE[PROJECT_TYPE["projC56"]],
}

CAPTURE_VOLUMES = {
    "projC0": 0.06,
    "projC1": 0.56, 
    "projC2": 0.74, 
    "projC3": 0.55, 
    "projC4": 0.69, 
    "projC5": 0.8, 
    "projC6": 0.75, 
    # "projC7": 0, 
    "projC8": 0.06,
    "projC9": 1.7,
    "projC10": 2.46,
    "projC11": 1.94,
    "projC12": 0.89,
    "projC13": 1.28,    
    # "projC14": 0,
    "projC15": 1.75,
    # "projC16": 0,
    "projC17": 0.42,
    # "projC18": 0,
    # "projC19": 0,
    "projC20": 3.38,
    "projC21": 1.09, 
    "projC22": 0.73, 
    # "projC23": 0, 
    "projC24": 1.44, 
    "projC25": 1.89, 
    "projC26": 0.11, 
    # "projC27": 0, 
    # "projC28": 0,
    "projC29": 1.75,
    # "projC30": 0,
    # "projC31": 0,
    # "projC32": 0,
    "projC33": 1.03,    
    "projC34": 0.84,
    "projC35": 0.95,
    "projC36": 3.11,
    "projC37": 1.12,
    "projC38": 3.59,
    "projC39": 2.35,
    "projC40": 1.54,
    "projC41": 2.62, 
    "projC42": 0.77, 
    "projC43": 0.78, 
    "projC44": 1.38, 
    "projC45": 1.00,
    "projC46": 1.89,
    "projC47": 1.39,
    "projC48": 1.94,
    "projC49": 1.10,
    "projC50": 1.76,    
    "projC51": 1.37,
    "projC52": 1.06,
    "projC53": 1.4,
    "projC54": 0.63,
    # "projC55": 0,
    "projC56": 0.57
}

# dictionary for storage project duration
STORAGE = {
    "projS0":  DURATION_BY_TYPE[PROJECT_TYPE["projS0"]],
    "projS1":  DURATION_BY_TYPE[PROJECT_TYPE["projS1"]],
    # "projS2":  DURATION_BY_TYPE[PROJECT_TYPE["projS2"]],
    "projS3":  DURATION_BY_TYPE[PROJECT_TYPE["projS3"]],
    # "projS4":  DURATION_BY_TYPE[PROJECT_TYPE["projS4"]],
    "projS5":  DURATION_BY_TYPE[PROJECT_TYPE["projS6"]],
    "projS6":  DURATION_BY_TYPE[PROJECT_TYPE["projS6"]],
    "projS7":  DURATION_BY_TYPE[PROJECT_TYPE["projS7"]]
}

# capture volumes
STORAGE_VOLUMES = {
    "projS0": total_vol("projS0"),
    "projS1": total_vol("projS1"),
    # "projS2": 0,
    "projS3": total_vol("projS3"),
    # "projS4": 0,
    "projS5": total_vol("projS5"),
    "projS6": total_vol("projS6"),
    "projS7": total_vol("projS7")
}

# pipe length multiplier is only applied to the construction stage in this trial
SCALED_STAGES = {"definition", "approval", "construction"}

def scaled_transport_duration(project, DICT):
    mult = DICT[project]
    return {
        stage: (mult * dur if stage in SCALED_STAGES else dur)
        for stage, dur in DURATION_BY_TYPE[PROJECT_TYPE[project]].items()
    }

# dictionary for transport project duration
TRANSPORT = {project: scaled_transport_duration(project, PIPE_MULT) for project in PIPE_MULT}

# transport volumes REMEMBER TO ADD THESE!
TRANSPORT_VOLUMES = {
    "projT11": total_vol("projT11"),
    "projT12": total_vol("projT12"),
    "projT13": total_vol("projT13"),
    "projT14": total_vol("projT14"),
    "projT15": total_vol("projT15"),
    "projT16": total_vol("projT16"),
    "projT17": total_vol("projT17"),
    "projT18": total_vol("projT18"),
    "projT19": total_vol("projT19"),
    "projT110": total_vol("projT110"),
    "projT111": total_vol("projT111"),

    "projT21": total_vol("projT21"),
    "projT22": total_vol("projT22"),
    "projT23": total_vol("projT23"),
    "projT24": total_vol("projT24"),
    "projT25": total_vol("projT25"),

    "projT31": total_vol("projT31"),
    "projT32": total_vol("projT32"),
    "projT33": total_vol("projT33"),

    "projT41": total_vol("projT41"),
    "projT42": total_vol("projT42"),
    
    "projT51": total_vol("projT51"),
    "projT52": total_vol("projT52"),
    "projT53": total_vol("projT53"),
    "projT54": total_vol("projT54"),
    "projT55": total_vol("projT55"),
    "projT56": total_vol("projT56"),
    "projT57": total_vol("projT57")
}

#==================================================================
# CHECKS
#==================================================================

# sum of all capture volumes
PLANNED_CAP_VOLUME = sum(CAPTURE_VOLUMES.values())

# getting the total capacity of all transport projects for the hammock node
TRANSPORT_CAPACITY = sum(TRANSPORT_VOLUMES.values())

CAPTURE_NUM = len(CAPTURE_VOLUMES)

# print(PLANNED_CAP_VOLUME)

STOR_VOL = sum(STORAGE_VOLUMES.values())
# print(STOR_VOL)

# print(total_vol("projS7"))
# print(total_vol("projS6"))
# print(total_vol("projS3"))
# print(total_vol("projS1"))
# print(total_vol("projS0"))
# print(total_vol("projT14"))
# print(total_vol("projT13"))
# print(total_vol("projT15"))