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
# GLOBAL SCHEDULE SCALING
#==================================================================
# Scales every project-type duration (definition/approval/construction) and
# the phase-testing enforcement months below by the same factor, so the
# whole schedule stretches or compresses together (e.g. to target a
# different overall w1.2 finish year: ~1.0 -> 2050, <1.0 -> 2045, >1.0 -> 2055).
DURATION_MULTIPLIER = 1

DURATION_BY_TYPE = {
    ptype: {stage: round(dur * DURATION_MULTIPLIER) for stage, dur in stages.items()}
    for ptype, stages in DURATION_BY_TYPE.items()
}

PHASE_ENFORCEMENT_STAGES_NEW = {
    # group 1
    "projC46": 3,
    "projC40": 3,
    "projC32": 4,
    "projC6": 2,
    "projC47": 3,
    "projC38": 3,
    "projC25": 3,
    "projC28": 3,
    "projC24": 3,
    "projC35": 3,
    "projC37": 3,
    "projC42": 3,
    "projC29": 3,
    "projC11": 2,
    "projC39": 3,

    # group 2
    "projC16": 1,
    "projC7": 1,
    "projC3": 1,
    "projC13": 4,
    "projC26": 3,
    "projC36": 3,
    "projC33": 3,
    "projC0": 2,
    "projC44": 4,
    "projC18": 2,
    "projC34": 4,

    # group 3
    "projC31": 3,
    "projC27": 3,

    # group 4
    "projC43": 3,
    "projC20": 2,

    # group 5
    "projC5": 2,
    "projC30": 3,
    "projC8": 2,
    "projC45": 4,
    "projC19": 2,
    "projC23": 2,
    "projC9": 2,
    "projC15": 4,
    "projC4": 2,
    "projC1": 2,
    "projC2": 2,
    "projC22": 2,
    "projC14": 2,
    "projC12": 2,
    "projC10": 2,
    "projC17": 2,
    "projC21": 2,

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
    "projC631": 5,
    "projC632": 5,
    "projC633": 5,
    "projC634": 5,
    "projC635": 5,
    "projC636": 5,
    "projC637": 5,
    "projC638": 5,
    "projC639": 5,
    "projC640": 5,
}

NO_PHASE_ENFORCEMENT = {cap: 0 for cap in PHASE_ENFORCEMENT_STAGES_NEW}

PHASE_TESTING = [round(month * DURATION_MULTIPLIER) for month in [40, 58, 76, 94, 112]]
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
    "projC631": 5,
    "projC632": 5,
    "projC633": 5,
    "projC634": 5,
    "projC635": 5,
    "projC636": 5,
    "projC637": 5,
    "projC638": 5,
    "projC639": 5,
    "projC640": 5,
}

W11_2_PHASE = {cap: PHASE_TESTING[DAC_PROJECTS[cap]-1] for cap in DAC_PROJECTS}

W11_PHASING_PROJ = {
    "projC61": 3,
    "projS61": 3,
    
    "projC62": 3,
    "projS62": 3,

    "projC63": 3,
    "projS63": 3,

    "projC64": 4,
    "projS64": 4,

    "projC65": 4,
    "projS65": 4,

    "projC66": 4,
    "projS66": 4,

    "projC67": 4,
    "projS67": 4,

    "projC68": 4,
    "projS68": 4,

    "projC69": 4,
    "projS69": 4,

    "projC610": 5,
    "projS610": 5,
    "projC611": 5,
    "projS611": 5,
    "projC612": 5,
    "projS612": 5,
    "projC613": 5,
    "projS613": 5,
    "projC614": 5,
    "projS614": 5,
    "projC615": 5,
    "projS615": 5,
    "projC616": 5,
    "projS616": 5,
    "projC617": 5,
    "projS617": 5,
    "projC618": 5,
    "projS618": 5,
    "projC619": 5,
    "projS619": 5,
    "projC620": 5,
    "projS620": 5,
    "projC621": 5,
    "projS621": 5,
    "projC622": 5,
    "projS622": 5,
    "projC623": 5,
    "projS623": 5,
    "projC624": 5,
    "projS624": 5,
    "projC625": 5,
    "projS625": 5,
    "projC626": 5,
    "projS626": 5,
    "projC627": 5,
    "projS627": 5,
    "projC628": 5,
    "projS628": 5,
    "projC629": 5,
    "projS629": 5,
    "projC630": 5,
    "projS630": 5,

    "projC631": 5,
    "projS631": 5,
    "projC632": 5,
    "projS632": 5,
    "projC633": 5,
    "projS633": 5,
    "projC634": 5,
    "projS634": 5,
    "projC635": 5,
    "projS635": 5,
    "projC636": 5,
    "projS636": 5,
    "projC637": 5,
    "projS637": 5,
    "projC638": 5,
    "projS638": 5,
    "projC639": 5,
    "projS639": 5,
    "projC640": 5,
    "projS640": 5,
}
W11_PHASING = {proj: PHASE_TESTING[W11_PHASING_PROJ[proj]-1] for proj in W11_PHASING_PROJ}

# world_2.py looks up NO_PIPE_PROJECTS; world_1_s1.py and world_1_s2.py still refer to DAC_PROJECTS
NO_PIPE_PROJECTS = DAC_PROJECTS

# world 2 add in phasing for all DACs (captures + storage)
W2_BRD_PROJECTS = {    
        # DAC
        "projC61": 3,
        "projS61": 3,

        "projC62": 3,
        "projS62": 3,

        "projC63": 3,
        "projS63": 3,

        "projC64": 4,
        "projS64": 4,

        "projC65": 4,
        "projS65": 4,

        "projC66": 4,
        "projS66": 4,

        "projC67": 4,
        "projS67": 4,

        "projC68": 4,
        "projS68": 4,

        "projC69": 4,
        "projS69": 4,

        "projC610": 5,
        "projS610": 5,
        "projC611": 5,
        "projS611": 5,
        "projC612": 5,
        "projS612": 5,
        "projC613": 5,
        "projS613": 5,
        "projC614": 5,
        "projS614": 5,
        "projC615": 5,
        "projS615": 5,
        "projC616": 5,
        "projS616": 5,
        "projC617": 5,
        "projS617": 5,
        "projC618": 5,
        "projS618": 5,
        "projC619": 5,
        "projS619": 5,
        "projC620": 5,
        "projS620": 5,
        "projC621": 5,
        "projS621": 5,
        "projC622": 5,
        "projS622": 5,
        "projC623": 5,
        "projS623": 5,
        "projC624": 5,
        "projS624": 5,
        "projC625": 5,
        "projS625": 5,
        "projC626": 5,
        "projS626": 5,
        "projC627": 5,
        "projS627": 5,
        "projC628": 5,
        "projS628": 5,
        "projC629": 5,
        "projS629": 5,
        "projC630": 5,
        "projS630": 5,

        "projC631": 5,
        "projS631": 5,
        "projC632": 5,
        "projS632": 5,
        "projC633": 5,
        "projS633": 5,
        "projC634": 5,
        "projS634": 5,
        "projC635": 5,
        "projS635": 5,
        "projC636": 5,
        "projS636": 5,
        "projC637": 5,
        "projS637": 5,
        "projC638": 5,
        "projS638": 5,
        "projC639": 5,
        "projS639": 5,
        "projC640": 5,
        "projS640": 5,

}

W2_BRD_PHASE = {proj: PHASE_TESTING[W2_BRD_PROJECTS[proj]-1] for proj in W2_BRD_PROJECTS}

#==================================================================
# DURATION MULTIPLIERS FOR PIPELINE
#==================================================================

PIPE_MULT = {
    "projT11":  1.41,
    "projT12":  1.53,
    "projT13":  1.40,
    "projT14":  1.20,
    "projT15":  1.67,
    "projT16":  0.20,
    "projT17":  5.01,

    "projT21":  2.81,
    "projT22":  0.98,
    "projT23":  0.47,
    "projT24":  1.08,
    "projT25":  0.06,
    "projT26":  1.17,
    "projT27":  0.38,
    "projT28":  0.11,
    "projT29":  1.15,

    "projT31":  0.73,

    "projT41":  0.29,

    "projT51":  3.59,
    "projT52":  0.26,
    "projT53":  0.01,
    "projT54":  0.37,
    "projT55":  0.10,
    "projT56":  0.11,
    "projT57":  0.12,
    "projT58":  0.15,
    "projT59":  0.55,
    "projT510":  1.82,
    "projT511":  0.89,
    "projT512":  1.35,
    "projT513":  0.02,
        

    # note: no DAC pipe multipliers — DAC has no transport project at all
}

NO_PIPE_MULT = {project: 1 for project in PIPE_MULT}

#==================================================================
# PROJECT DATA 
#==================================================================

PROJECT_TYPE = {
                # group 1
                "projC46": "biomass_gasification",
                "projC40": "biomass_gasification",
                "projC32": "biomass_gasification",
                "projC6": "NGCC",
                "projC47": "biomass_gasification",
                "projC38": "biomass_gasification",
                "projC25": "biomass_gasification",
                "projC28": "biomass_gasification",
                "projC24": "biomass_gasification",
                "projC35": "biomass_gasification",
                "projC37": "biomass_gasification",
                "projC42": "biomass_gasification",
                "projC29": "biomass_gasification",
                "projC11": "cement",
                "projC39": "biomass_gasification",

                # group 2
                "projC16": "NGCC",
                "projC7": "NGCC",
                "projC3": "hydrogen",
                "projC13": "refinery",
                "projC26": "biomass_gasification",
                "projC36": "biomass_gasification",
                "projC33": "biomass_gasification",
                "projC0": "ethanol",
                "projC44": "biomass_gasification",
                "projC18": "NGCC",
                "projC34": "biomass_gasification",

                # group 3
                "projC31": "biomass_gasification",
                "projC27": "biomass_gasification",

                # group 4
                "projC43": "biomass_gasification",
                "projC20": "ethanol",

                # group 5
                "projC5": "gas_processing",
                "projC30": "biomass_gasification",
                "projC8": "NGCC",
                "projC45": "biomass_gasification",
                "projC19": "cement",
                "projC23": "cement",
                "projC9": "cement",
                "projC15": "refinery",
                "projC4": "hydrogen",
                "projC1": "NGCC",
                "projC2": "NGCC",
                "projC22": "NGCC",
                "projC14": "NGCC",
                "projC12": "cement",
                "projC10": "cement",
                "projC17": "cement",
                "projC21": "NGCC",

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
                "projC631": "DAC",
                "projC632": "DAC",
                "projC633": "DAC",
                "projC634": "DAC",
                "projC635": "DAC",
                "projC636": "DAC",
                "projC637": "DAC",
                "projC638": "DAC",
                "projC639": "DAC",
                "projC640": "DAC",

                # storages
                "projS0": "storage",
                "projS1": "storage", 
                "projS2": "storage", 
                "projS3": "storage", 
                "projS4": "storage", 

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
                "projS631": "storage",
                "projS632": "storage",
                "projS633": "storage",
                "projS634": "storage",
                "projS635": "storage",
                "projS636": "storage",
                "projS637": "storage",
                "projS638": "storage",
                "projS639": "storage",
                "projS640": "storage",

                # group 1 transports
                "projT11": "transport", "projT12": "transport", "projT13": "transport", "projT14": "transport", "projT15": "transport", 
                "projT16": "transport", "projT17": "transport",

                # group 2 transports
                "projT21": "transport", "projT22": "transport", "projT23": "transport", "projT24": "transport", "projT25": "transport", 
                "projT26": "transport", "projT27": "transport", "projT28": "transport", "projT29": "transport", 

                # group 3 transports
                "projT31": "transport",

                # group 4 transports 
                "projT41": "transport",

                # group 5 transports
                "projT51": "transport", "projT52": "transport", "projT53": "transport", "projT54": "transport", "projT55": "transport",
                "projT56": "transport", "projT57": "transport", "projT58": "transport", "projT59": "transport", "projT510": "transport",
                "projT511": "transport", "projT512": "transport", "projT513": "transport", 

                # note: no DAC transports — DAC has no real pipeline, so CAPTURE_PIPE points DAC captures straight at their storage
               }

#==================================================================
# TOPOLOGICAL DATA FOR GRAPH
#==================================================================

# stores the pipe/storage every single transport flows into next
PIPE_DOWNSTREAM = {
                   # group 1
                   "projT11": "projS0",
                   "projT12": "projS0",
                   "projT13": "projT12",
                   "projT17": "projS0",
                   "projT15": "projT17",
                   "projT16": "projT17",
                   "projT14": "projT17",

                   # group 2
                   "projT21": "projS1",
                   "projT22": "projS1",
                   "projT23": "projT22",
                   "projT24": "projS1",
                   "projT25": "projT21",
                   "projT26": "projT21",
                   "projT27": "projT21",
                   "projT28": "projT21",
                   "projT29": "projT28",
                   
                   
                   # group 3
                   "projT31": "projS4",
                   
                   # group 4
                   "projT41": "projS2",

                   # group 5
                   "projT51": "projS3",
                   "projT52": "projT51",
                   "projT53": "projT51",
                   "projT54": "projT51",
                   "projT55": "projT51",
                   "projT56": "projT51",
                   "projT57": "projT56",
                   "projT58": "projT51",
                   "projT59": "projT51",
                   "projT510": "projT51",
                   "projT511": "projT510",
                   "projT512": "projT510",
                   "projT513": "projT510",

                    # note: no DAC transports here: see CAPTURE_PIPE
                   }

# stores the transport every single capture flows into next
CAPTURE_PIPE = {
                # group 1
                "projC46": "projT12",
                "projC40": "projT12",
                "projC32": "projT13",
                "projC6": "projT11",
                "projC47": "projT11",
                "projC38": "projT11",
                "projC25": "projT16",
                "projC28": "projT14",
                "projC24": "projT14",
                "projC35": "projT14",
                "projC37": "projT17",
                "projC42": "projT17",
                "projC29": "projT17",
                "projC11": "projT15",
                "projC39": "projT15",

                # group 2
                "projC16": "projT22",
                "projC7": "projT22",
                "projC3": "projT22",
                "projC13": "projT23",
                "projC26": "projT24",
                "projC36": "projT25",
                "projC33": "projT27",
                "projC0": "projT28",
                "projC44": "projT29",
                "projC18": "projT21",
                "projC34": "projT26",

                # group 3
                "projC31": "projT31",
                "projC27": "projT31",

                # group 4
                "projC43": "projT41",
                "projC20": "projT41",

                # group 5
                "projC5": "projT55",
                "projC30": "projT54",
                "projC8": "projT56",
                "projC45": "projT57",
                "projC19": "projT58",
                "projC23": "projT59",
                "projC9": "projT59",
                "projC15": "projT51",
                "projC4": "projT53",
                "projC1": "projT51",
                "projC2": "projT52",
                "projC22": "projT511",
                "projC14": "projT510",
                "projC12": "projT510",
                "projC10": "projT513",
                "projC17": "projT512",
                "projC21": "projT512",

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
                "projC631": "projS631",
                "projC632": "projS632",
                "projC633": "projS633",
                "projC634": "projS634",
                "projC635": "projS635",
                "projC636": "projS636",
                "projC637": "projS637",
                "projC638": "projS638",
                "projC639": "projS639",
                "projC640": "projS640",
                
                }

TRUNKS = [
          # group 1
          "projT11",
          "projT12",
          "projT17",
          
          # group 2
          "projT21",
          "projT22",
          "projT24",
          
          # group 3
          "projT31",
          
          # group 4
          "projT41",

          # group 5
          "projT51",

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
    "projC46": 0.51,
    "projC40": 1.10,
    "projC32": 2.62,
    "projC6": 1.70,
    "projC47": 0.57,
    "projC38": 1.39,
    "projC25": 0.84,
    "projC28": 1.12,
    "projC24": 1.03,
    "projC35": 1.38,
    "projC37": 1.89,
    "projC42": 1.37,
    "projC29": 3.59,
    "projC11": 0.33,
    "projC39": 1.94,

    # group 2
    "projC16": 3.38,
    "projC7": 2.46,
    "projC3": 0.55,
    "projC13": 2.16,
    "projC26": 0.95,
    "projC36": 1.00,
    "projC33": 0.77,
    "projC0": 0.06,
    "projC44": 1.40,
    "projC18": 5.46,
    "projC34": 0.78,

    # group 3
    "projC31": 1.54,
    "projC27": 3.11,

    # group 4
    "projC43": 1.06,
    "projC20": 0.11,

    # group 5
    "projC5": 0.1,
    "projC30": 2.35,
    "projC8": 1.94,
    "projC45": 0.63,
    "projC19": 0.73,
    "projC23": 0.47,
    "projC9": 0.89,
    "projC15": 3.06,
    "projC4": 0.67,
    "projC1": 5.39,
    "projC2": 2.37,
    "projC22": 2.87,
    "projC14": 2.50,
    "projC12": 1.75,
    "projC10": 1.28,
    "projC17": 1.09,
    "projC21": 2.76,

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
    "projC630": 1,
    "projC631": 1,
    "projC632": 1,
    "projC633": 1,
    "projC634": 1,
    "projC635": 1,
    "projC636": 1,
    "projC637": 1,
    "projC638": 1,
    "projC639": 1,
    "projC640": 1,

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