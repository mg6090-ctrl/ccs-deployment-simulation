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

PHASE_ENFORCEMENT_STAGES_MODEL = {
    # group 1 
    "projC52": 2,
    "projC19": 4,
    "projC50": 1,
    "projC55": 1,
    "projC42": 2,
    "projC41": 1,
    "projC37": 1,
    "projC48": 1,
    "projC38": 4,
    "projC29": 4,
    "projC39": 1,
    "projC51": 3,
    "projC60": 3,
    "projC59": 4,
    "projC53": 4,
    "projC45": 4,
    "projC4": 1,
    "projC21": 1,
    "projC24": 1,
    "projC13": 1,
    "projC12": 3,

    # group 2
    "projC49": 1,
    "projC54": 1,
    "projC46": 1,
    "projC0": 3,
    "projC57": 2,

    # group 3
    "projC26": 3,
    "projC47": 1,
    "projC40": 1, 
    "projC44": 1,
    "projC28": 3,

    # group 4
    "projC56": 1,
    "projC31": 2,

    # group 5
    "projC10": 2,
    "projC43": 1,
    "projC27": 1,
    "projC58": 1,
    "projC16": 1,
    "projC17": 1,
    "projC35": 1,
    "projC22": 4,
    "projC18": 4,
    "projC20": 4,
    "projC33": 1,
    "projC25": 2,
    "projC32": 2,
    "projC7": 2,
    "projC8": 2,
    "projC23": 2,
    "projC1": 1,
    "projC2": 1,

    #DACs
    "projC61": 4,
    "projC62": 4,
    "projC63": 4,
    "projC64": 4,
    "projC65": 4,
    "projC66": 4,
    "projC67": 4,
    "projC68": 4,
    "projC69": 4,
    "projC610": 4,
    "projC611": 4,
    "projC612": 4,
    "projC613": 4,
    "projC614": 4,
    "projC615": 4,
    "projC616": 4,
    "projC617": 4,
}

PHASE_ENFORCEMENT_SIMCCS = {
    # group 1 
    "projC52": 120,
    "projC19": 60,
    "projC50": 72,
    "projC55": 72,
    "projC12": 72,
    "projC42": 120,
    "projC41": 72,
    "projC37": 120,
    "projC48": 120,
    "projC38": 120,
    "projC29": 72,
    "projC39": 120,
    "projC51": 72,
    "projC60": 120,
    "projC59": 120,
    "projC53": 72,
    "projC45": 72,
    "projC4": 60,
    "projC21": 36,
    "projC24": 72,
    "projC13": 72,

    # group 2
    "projC49": 120,
    "projC54": 120,
    "projC46": 120,
    "projC0": 72,
    "projC57": 72,

    # group 3
    "projC26": 60,
    "projC47": 120,
    "projC40": 120, 
    "projC44": 120,
    "projC28": 72,

    # group 4
    "projC56": 120,
    "projC31": 60,

    # group 5
    "projC10": 60,
    "projC43": 120,
    "projC27": 36,
    "projC58": 72,
    "projC16": 72,
    "projC17": 36,
    "projC35": 36,
    "projC22": 72,
    "projC18": 36,
    "projC20": 36,
    "projC33": 60,
    "projC25": 60,
    "projC32": 60,
    "projC7": 60,
    "projC8": 72,
    "projC23": 36,
    "projC1": 60,
    "projC2": 72
}

PHASE_ENFORCEMENT_STAGES_NEW = {
    # group 1 
    "projC52": 3,
    "projC19": 3,
    "projC50": 2,
    "projC55": 2,
    "projC42": 3,
    "projC41": 2,
    "projC37": 3,
    "projC48": 3,
    "projC38": 4,
    "projC29": 3,
    "projC39": 3,
    "projC51": 3,
    "projC60": 3,
    "projC59": 4,
    "projC53": 4,
    "projC45": 4,
    "projC4": 2,
    "projC21": 4,
    "projC24": 1,
    "projC13": 1,
    "projC12": 2,

    # group 2
    "projC49": 3,
    "projC54": 3,
    "projC46": 3,
    "projC0": 2,
    "projC57": 3,

    # group 3
    "projC26": 3,
    "projC47": 3,
    "projC40": 2, 
    "projC44": 2,
    "projC28": 3,

    # group 4
    "projC56": 2,
    "projC31": 2,

    # group 5
    "projC10": 2,
    "projC43": 2,
    "projC27": 1,
    "projC58": 2,
    "projC16": 1,
    "projC17": 1,
    "projC35": 1,
    "projC22": 3,
    "projC18": 3,
    "projC20": 3,
    "projC33": 1,
    "projC25": 2,
    "projC32": 2,
    "projC7": 2,
    "projC8": 2,
    "projC23": 4,
    "projC1": 1,
    "projC2": 1,

    #DACs
    "projC61": 3,
    "projC62": 3,
    "projC63": 3,
    "projC64": 4,
    "projC65": 4,
    "projC66": 4,
    "projC67": 4,
    "projC68": 4,
    "projC69": 4,
    "projC610": 5,
    "projC611": 5,
    "projC612": 5,
    "projC613": 5,
    "projC614": 5,
    "projC615": 5,
    "projC616": 5,
    "projC617": 5,
    "projC618": 5,
    "projC619": 5,
    "projC620": 5,
    "projC621": 5,
    "projC622": 5,
    "projC623": 5,
    "projC624": 5,
    "projC625": 5,
    "projC626": 5,
    "projC627": 5,
    "projC628": 5,
    "projC629": 5,
    "projC630": 5,

}

NO_PHASE_ENFORCEMENT = {cap: 0 for cap in PHASE_ENFORCEMENT_STAGES_NEW}

PHASE_TESTING = [40, 58, 76, 94, 112]
PHASE_ENFORCEMENT_TEST = {cap: PHASE_TESTING[PHASE_ENFORCEMENT_STAGES_NEW[cap]-1] for cap in PHASE_ENFORCEMENT_STAGES_NEW}

DAC_PROJECTS = {
    "projC61": 3,
    "projC62": 3,
    "projC63": 3,
    "projC64": 4,
    "projC65": 4,
    "projC66": 4,
    "projC67": 4,
    "projC68": 4,
    "projC69": 4,
    "projC610": 5,
    "projC611": 5,
    "projC612": 5,
    "projC613": 5,
    "projC614": 5,
    "projC615": 5,
    "projC616": 5,
    "projC617": 5,
    "projC618": 5,
    "projC619": 5,
    "projC620": 5,
    "projC621": 5,
    "projC622": 5,
    "projC623": 5,
    "projC624": 5,
    "projC625": 5,
    "projC626": 5,
    "projC627": 5,
    "projC628": 5,
    "projC629": 5,
    "projC630": 5,
}

W11_2_PHASE = {cap: PHASE_TESTING[DAC_PROJECTS[cap]-1] for cap in DAC_PROJECTS}

# world_2.py looks up NO_PIPE_PROJECTS; world_1_s1.py and world_1_s2.py still refer to DAC_PROJECTS
NO_PIPE_PROJECTS = DAC_PROJECTS

#==================================================================
# DURATION MULTIPLIERS FOR PIPELINE
#==================================================================

PIPE_MULT = {
    "projT11":  0.65,
    "projT12":  1.15,
    "projT13":  3.63,
    "projT14":  2.47,
    "projT15":  1.49,
    "projT16":  0.25,
    "projT17":  0.73,
    "projT18":  1.29,
    "projT19":  1.29,
    "projT110":  1.02,
    "projT111":  1.05,

    "projT21":  0.59,
    "projT22":  1.33,
    "projT23":  0.37,

    "projT31":  1.74,
    "projT32":  0.76,
    "projT33":  0.77,

    "projT41":  0.18,

    "projT51":  0.22,
    "projT52":  0.34,
    "projT53":  0.36,
    "projT54":  0.50,
    "projT55":  2.96,
    "projT56":  1.44,
    "projT57":  1.23,
    "projT58":  0.54,
    "projT59":  0.24,
    "projT510":  0.24,
    "projT511":  0.14,

    # note: no DAC pipe multipliers — DAC has no transport project at all
}

NO_PIPE_MULT = {project: 1 for project in PIPE_MULT}

#==================================================================
# PROJECT DATA 
#==================================================================

PROJECT_TYPE = {
                # group 1
                "projC52": "biomass_gasification",
                "projC42": "biomass_gasification",
                "projC55": "biomass_gasification",
                "projC50": "biomass_gasification",
                "projC19": "cement",
                "projC48": "biomass_gasification",
                "projC37": "biomass_gasification",
                "projC41": "biomass_gasification",
                "projC38": "biomass_gasification",
                "projC29": "NGCC",
                "projC45": "biomass_gasification",
                "projC53": "biomass_gasification",
                "projC59": "biomass_gasification",
                "projC60": "biomass_gasification",
                "projC51": "biomass_gasification",
                "projC39": "biomass_gasification",
                "projC4": "hydrogen",
                "projC21": "refinery",
                "projC13": "NGCC",
                "projC24": "NGCC",
                "projC12": "NGCC",

                # group 2
                "projC49": "biomass_gasification",
                "projC54": "biomass_gasification",
                "projC46": "biomass_gasification",
                "projC57": "biomass_gasification",
                "projC0": "ethanol",

                # group 3
                "projC26": "NGCC",
                "projC47": "biomass_gasification",
                "projC40": "biomass_gasification",
                "projC44": "biomass_gasification",
                "projC28": "NGCC",

                # group 4
                "projC56": "biomass_gasification",
                "projC31": "ethanol",

                # group 5
                "projC10": "gas_processing",
                "projC43": "biomass_gasification",
                "projC16": "NGCC",
                "projC58": "biomass_gasification",
                "projC27": "cement",
                "projC17": "cement",
                "projC35": "cement",
                "projC7": "ethanol",
                "projC23": "refinery",
                "projC8": "ethanol",
                "projC1": "NGCC",
                "projC2": "NGCC",
                "projC22": "NGCC",
                "projC18": "cement",
                "projC20": "cement",
                "projC33": "NGCC",
                "projC25": "cement",
                "projC32": "NGCC",

                # DACS
                "projC61": "DAC",
                "projC62": "DAC",
                "projC63": "DAC",
                "projC64": "DAC",
                "projC65": "DAC",
                "projC66": "DAC",
                "projC67": "DAC",
                "projC68": "DAC",
                "projC69": "DAC",
                "projC610": "DAC",
                "projC611": "DAC",
                "projC612": "DAC",
                "projC613": "DAC",
                "projC614": "DAC",
                "projC615": "DAC",
                "projC616": "DAC",
                "projC617": "DAC",
                "projC618": "DAC",
                "projC619": "DAC",
                "projC620": "DAC",
                "projC621": "DAC",
                "projC622": "DAC",
                "projC623": "DAC",
                "projC624": "DAC",
                "projC625": "DAC",
                "projC626": "DAC",
                "projC627": "DAC",
                "projC628": "DAC",
                "projC629": "DAC",
                "projC630": "DAC",

                # storages
                "projS1": "storage", 
                "projS2": "storage", 
                "projS3": "storage", 
                "projS5": "storage", 
                "projS10": "storage", 

                # DAC storages
                "projS61": "storage",
                "projS62": "storage",
                "projS63": "storage",
                "projS64": "storage",
                "projS65": "storage",
                "projS66": "storage",
                "projS67": "storage",
                "projS68": "storage",
                "projS69": "storage",
                "projS610": "storage",
                "projS611": "storage",
                "projS612": "storage",
                "projS613": "storage",
                "projS614": "storage",
                "projS615": "storage",
                "projS616": "storage",
                "projS617": "storage",
                "projS618": "storage",
                "projS619": "storage",
                "projS620": "storage",
                "projS621": "storage",
                "projS622": "storage",
                "projS623": "storage",
                "projS624": "storage",
                "projS625": "storage",
                "projS626": "storage",
                "projS627": "storage",
                "projS628": "storage",
                "projS629": "storage",
                "projS630": "storage",

                # group 1 transports
                "projT11": "transport", "projT12": "transport", "projT13": "transport", "projT14": "transport",
                "projT15": "transport", "projT16": "transport", "projT17": "transport", "projT18": "transport", "projT19": "transport",
                "projT110": "transport", "projT111": "transport",

                # group 2 transports
                "projT21": "transport", "projT22": "transport", "projT23": "transport",

                # group 2 transports
                "projT31": "transport", "projT32": "transport", "projT33": "transport", 

                # group 4 transports 
                "projT41": "transport",

                # group 5 transports
                "projT51": "transport", "projT52": "transport", "projT53": "transport", "projT54": "transport", "projT55": "transport",
                "projT56": "transport", "projT57": "transport", "projT58": "transport", "projT59": "transport", "projT510": "transport", 
                "projT511": "transport",

                # note: no DAC transports — DAC has no real pipeline, so CAPTURE_PIPE points DAC captures straight at their storage
               }

#==================================================================
# TOPOLOGICAL DATA FOR GRAPH
#==================================================================

# stores the pipe/storage every single transport flows into next
PIPE_DOWNSTREAM = {
                   # group 1
                   "projT11": "projS1",
                   "projT12": "projS1",
                   "projT13": "projS1",
                   "projT14": "projT13",
                   "projT15": "projT13",
                   "projT16": "projT13",
                   "projT17": "projT13",
                   "projT18": "projT13",
                   "projT19": "projT17",
                   "projT110": "projT16",
                   "projT111": "projT15",

                   # group 2
                   "projT21": "projS2",
                   "projT22": "projS2",
                   "projT23": "projT22",
                   
                   # group 3
                   "projT31": "projS3",
                   "projT32": "projT31",
                   "projT33": "projS3",
                   
                   # group 4
                   "projT41": "projS10",

                   # group 5
                   "projT51": "projS5",
                   "projT52": "projT55",
                   "projT53": "projT55",
                   "projT54": "projT55",
                   "projT55": "projS5",
                   "projT56": "projT55",
                   "projT57": "projT55",
                   "projT58": "projT55",
                   "projT59": "projT56",
                   "projT510": "projT59",
                   "projT511": "projT56",

                    # note: no DAC transports here: see CAPTURE_PIPE
                   }

# stores the transport every single capture flows into next
CAPTURE_PIPE = {
                # group 1 
                "projC52": "projT18",
                "projC19": "projT13",
                "projC42": "projT19",
                "projC55": "projT17",
                "projC50": "projT17",
                "projC48": "projT110",
                "projC37": "projT110",
                "projC41": "projT16",
                "projC38": "projT13",
                "projC29": "projT13",
                "projC45": "projT14",
                "projC53": "projT14",
                "projC59": "projT14",
                "projC39": "projT111",
                "projC51": "projT15",
                "projC60": "projT15",
                "projC4": "projT12",
                "projC21": "projT12",
                "projC24": "projT11",
                "projC13": "projT11",
                "projC12": "projT15",

                # group 2
                "projC49": "projT21",
                "projC54": "projT23",
                "projC46": "projT23",
                "projC0": "projT22",
                "projC57": "projT22",

                # group 3
                "projC26": "projT31",
                "projC47": "projT32",
                "projC40": "projT33",
                "projC44": "projT33",
                "projC28": "projT31",

                # group 4
                "projC56": "projT41",
                "projC31": "projT41",

                # group 5
                "projC43": "projT52",
                "projC10": "projT51",
                "projC27": "projT53",
                "projC58": "projT53",
                "projC16": "projT53",
                "projC35": "projT54",
                "projC17": "projT54",
                "projC22": "projT55", 
                "projC18": "projT55",
                "projC20": "projT55",
                "projC33": "projT58",
                "projC25": "projT57",
                "projC32": "projT57",
                "projC7": "projT511",
                "projC23": "projT56", 
                "projC8": "projT59",
                "projC1": "projT59",
                "projC2": "projT510",

                # DACs feed straight into its storage; DACs do not have
                # a pipeline, so no intermediate transport projects exist
                "projC61": "projS61",
                "projC62": "projS62",
                "projC63": "projS63",
                "projC64": "projS64",
                "projC65": "projS65",
                "projC66": "projS66",
                "projC67": "projS67",
                "projC68": "projS68",
                "projC69": "projS69",
                "projC610": "projS610",
                "projC611": "projS611",
                "projC612": "projS612",
                "projC613": "projS613",
                "projC614": "projS614",
                "projC615": "projS615",
                "projC616": "projS616",
                "projC617": "projS617",
                "projC618": "projS618",
                "projC619": "projS619",
                "projC620": "projS620",
                "projC621": "projS621",
                "projC622": "projS622",
                "projC623": "projS623",
                "projC624": "projS624",
                "projC625": "projS625",
                "projC626": "projS626",
                "projC627": "projS627",
                "projC628": "projS628",
                "projC629": "projS629",
                "projC630": "projS630",
                }

TRUNKS = [
          # group 1
          "projT11",
          "projT12",
          "projT13",
          
          # group 2
          "projT21",
          "projT22",
          
          # group 3
          "projT31",
          "projT33",
          
          # group 4
          "projT41",

          # group 5
          "projT51",
          "projT55",

          # note: no DAC trunks — DAC has no transport projects
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
    project: DURATION_BY_TYPE[ptype]
    for project, ptype in PROJECT_TYPE.items()
    if project.startswith("projC")
}

CAPTURE_VOLUMES = {
    # group 1 
    "projC52": 1.94,
    "projC19": 0.33,
    "projC50": 1.89,
    "projC55": 1.37,
    "projC42": 3.59,
    "projC41": 1.12,
    "projC37": 1.03,
    "projC48": 1.38,
    "projC38": 0.84,
    "projC29": 1.89,
    "projC39": 0.95,
    "projC51": 1.39,
    "projC60": 0.57,
    "projC59": 0.51,
    "projC53": 1.10,
    "projC45": 2.62,
    "projC4": 0.74,
    "projC21": 2.16,
    "projC24": 3.38,
    "projC13": 2.46,
    "projC12": 1.70,

    # group 2
    "projC49": 1.00,
    "projC54": 1.76,
    "projC46": 0.77,
    "projC0": 0.06,
    "projC57": 1.40,

    # group 3
    "projC26": 5.46,
    "projC47": 0.78,
    "projC40": 3.11, 
    "projC44": 1.54,
    "projC28": 1.44,

    # group 4
    "projC56": 1.06,
    "projC31": 0.11,

    # group 5
    "projC10": 0.1,
    "projC43": 2.35,
    "projC27": 0.73,
    "projC58": 0.63,
    "projC16": 1.94,
    "projC17": 0.89,
    "projC35": 0.47,
    "projC22": 2.5,
    "projC18": 1.28,
    "projC20": 1.75,
    "projC33": 2.87,
    "projC25": 1.09,
    "projC32": 2.76,
    "projC7": 0.8,
    "projC8": 0.75,
    "projC23": 3.06,
    "projC1": 5.39,
    "projC2": 2.37,

    # DACs
    "projC61": 1,
    "projC62": 1,
    "projC63": 1,
    "projC64": 1,
    "projC65": 1,
    "projC66": 1,
    "projC67": 1,
    "projC68": 1,
    "projC69": 1,
    "projC610": 1,
    "projC611": 1,
    "projC612": 1,
    "projC613": 1,
    "projC614": 1,
    "projC615": 1,
    "projC616": 1,
    "projC617": 1,
    "projC618": 1,
    "projC619": 1,
    "projC620": 1,
    "projC621": 1,
    "projC622": 1,
    "projC623": 1,
    "projC624": 1,
    "projC625": 1,
    "projC626": 1,
    "projC627": 1,
    "projC628": 1,
    "projC629": 1,
    "projC630": 1
}

# dictionary for storage project duration
STORAGE = {
    project: DURATION_BY_TYPE[ptype]
    for project, ptype in PROJECT_TYPE.items()
    if project.startswith("projS")
}

# capture volumes
STORAGE_VOLUMES = {project: total_vol(project) for project in STORAGE}

# pipe length multiplier is only applied to the construction stage in this trial
SCALED_STAGES = {"definition", "construction"}

def scaled_transport_duration(project, DICT):
    mult = DICT.get(project, 1)
    return {
        stage: (mult * dur if stage in SCALED_STAGES else dur)
        for stage, dur in DURATION_BY_TYPE[PROJECT_TYPE[project]].items()
    }

# all transport projects, independent of whether PIPE_MULT has an entry for them yet
TRANSPORT_PROJECTS = [project for project, ptype in PROJECT_TYPE.items() if ptype == "transport"]

# dictionary for transport project duration (defaults to a 1x multiplier if missing from PIPE_MULT)
TRANSPORT = {project: scaled_transport_duration(project, PIPE_MULT) for project in TRANSPORT_PROJECTS}

# transport volumes REMEMBER TO ADD THESE!
TRANSPORT_VOLUMES = {project: total_vol(project) for project in TRANSPORT_PROJECTS}

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