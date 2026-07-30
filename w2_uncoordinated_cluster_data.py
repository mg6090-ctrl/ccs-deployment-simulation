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

PHASE_TESTING = [40, 58, 76, 94, 112]

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

# add in phasing for all BECCS and refineries (captures + transports)
W2_PHASE = {
    # group 1 
        "projC52": 3,
        "projT52": 3,

        "projC50": 2,
        "projT50": 2,

        "projC55": 2,
        "projT55": 2,

        "projC42": 3,
        "projT42": 3,
        "projC41": 2,
        "projT41": 2,
        "projC37": 3,
        "projT37": 3,
        "projC48": 3,
        "projT48": 3,
        "projC38": 4,
        "projT38": 4,
        "projC39": 3,
        "projT39": 3,
        "projC51": 3,
        "projT51": 3,
        "projC60": 3,
        "projT60": 3,
        "projC59": 4,
        "projT59": 4,
        "projC53": 4,
        "projT53": 4,
        "projC45": 4,
        "projT45": 4,
    
        # group 2
        "projC49": 3,
        "projT49": 3,
        "projC54": 3,
        "projT54": 3,
        "projC46": 3,
        "projT46": 3,
        "projC57": 3,
        "projT57": 3,
    
        # group 3
        "projC47": 3,
        "projT47": 3,
        "projC40": 2, 
        "projT40": 2,
        "projC44": 2,
        "projT44": 2,
    
        # group 4
        "projC56": 2,
        "projT56": 2,
    
        # group 5
        
        "projC43": 2,
        "projT43": 2,
        
        "projC58": 2,
        "projT58": 2,
}

NO_PIPE_PROJECTS = {
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

#==================================================================
# DURATION MULTIPLIERS FOR PIPELINE
#==================================================================

PIPE_MULT = {
        "projT0": 0.21,
        "projT1": 2.34,
        "projT2": 2.53,
        "projT4": 0.65,
        "projT7": 1.96,
        "projT8": 2.05,
        "projT10": 0.17,
        "projT12": 0.17,
        "projT13": 0.08,
        "projT16": 0.44,
        "projT17": 0.87,
        "projT18": 1.96,
        "projT19": 1.36,
        "projT20": 2.30,
        "projT21": 0.81,
        "projT22": 1.92,
        "projT23": 2.01,
        "projT24": 0.17,
        "projT25": 2.45,
        "projT26": 1.30,
        "projT27": 0.61,
        "projT28": 0.19,
        "projT29": 0.35,
        "projT31": 0.11,
        "projT32": 3.15,
        "projT33": 2.34,
        "projT35": 0.80,
        "projT37": 0.19,
        "projT38": 0.26,
        "projT39": 0.73,
        "projT40": 0.35,
        "projT41": 0.05,
        "projT42": 2.29,
        "projT43": 0.37,
        "projT44": 0.33,
        "projT45": 1.31,
        "projT46": 0.42,
        "projT47": 0.97,
        "projT48": 0.74,
        "projT49": 0.17,
        "projT50": 1.34,
        "projT51": 0.94,
        "projT52": 2.37,
        "projT53": 1.01,
        "projT54": 0.15,
        "projT55": 1.29,
        "projT56": 0.10,
        "projT57": 0.93,
        "projT58": 0.52,
        "projT59": 0.35,
        "projT60": 0.53,

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
                "projS0": "storage",
                "projS1": "storage", 
                "projS2": "storage", 
                "projS3": "storage", 
                "projS5": "storage", 
                "projS10": "storage", 
                "projS12": "storage",
                "projS16": "storage",
                "projS17": "storage",
                "projS18": "storage",

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

                # transports
                "projT0": "transport",
                "projT1": "transport",
                "projT2": "transport",
                "projT4": "transport",
                "projT7": "transport",
                "projT8": "transport",
                "projT10": "transport",
                "projT12": "transport",
                "projT13": "transport",
                "projT16": "transport",
                "projT17": "transport",
                "projT18": "transport",
                "projT19": "transport",
                "projT20": "transport",
                "projT21": "transport",
                "projT22": "transport",
                "projT23": "transport",
                "projT24": "transport",
                "projT25": "transport",
                "projT26": "transport",
                "projT27": "transport",
                "projT28": "transport",
                "projT29": "transport",
                "projT31": "transport",
                "projT32": "transport",
                "projT33": "transport",
                "projT35": "transport",
                "projT37": "transport",
                "projT38": "transport",
                "projT39": "transport",
                "projT40": "transport",
                "projT41": "transport",
                "projT42": "transport",
                "projT43": "transport",
                "projT44": "transport",
                "projT45": "transport",
                "projT46": "transport",
                "projT47": "transport",
                "projT48": "transport",
                "projT49": "transport",
                "projT50": "transport",
                "projT51": "transport",
                "projT52": "transport",
                "projT53": "transport",
                "projT54": "transport",
                "projT55": "transport",
                "projT56": "transport",
                "projT57": "transport",
                "projT58": "transport",
                "projT59": "transport",
                "projT60": "transport",

                # note: no DAC transports — DAC has no real pipeline, so CAPTURE_PIPE
                # points DAC captures straight at their storage (see dac_no_pipeline_proxy)
               }

#==================================================================
# TOPOLOGICAL DATA FOR GRAPH
#==================================================================

# stores the pipe/storage every single transport flows into next
PIPE_DOWNSTREAM = {
                    "projT0": "projS2",
                    "projT1": "projS5",
                    "projT2": "projS5",
                    "projT4": "projS1",
                    "projT7": "projS5",
                    "projT8": "projS5",
                    "projT10": "projS5",
                    "projT12": "projS18",
                    "projT13": "projS16",
                    "projT16": "projS5",
                    "projT17": "projS5",
                    "projT18": "projS5",
                    "projT19": "projS0",
                    "projT20": "projS5",
                    "projT21": "projS1",
                    "projT22": "projS5",
                    "projT23": "projS5",
                    "projT24": "projS16",
                    "projT25": "projS5",
                    "projT26": "projS2",
                    "projT27": "projS5",
                    "projT28": "projS3",
                    "projT29": "projS0",
                    "projT31": "projS10",
                    "projT32": "projS5",
                    "projT33": "projS5",
                    "projT35": "projS5",
                    "projT37": "projS0",
                    "projT38": "projS0",
                    "projT39": "projS17",
                    "projT40": "projS3",
                    "projT41": "projS0",
                    "projT42": "projS0",
                    "projT43": "projS5",
                    "projT44": "projS3",
                    "projT45": "projS0",
                    "projT46": "projS2",
                    "projT47": "projS3",
                    "projT48": "projS0",
                    "projT49": "projS12",
                    "projT50": "projS0",
                    "projT51": "projS18",
                    "projT52": "projS0",
                    "projT53": "projS18",
                    "projT54": "projS2",
                    "projT55": "projS0",
                    "projT56": "projS10",
                    "projT57": "projS2",
                    "projT58": "projS5",
                    "projT59": "projS18",
                    "projT60": "projS18",

                    # note: no DAC transports here: see CAPTURE_PIPE
                   }

# stores the transport every single capture flows into next
CAPTURE_PIPE = {
                # group 1 
                "projC52": "projT52",
                "projC19": "projT19",
                "projC42": "projT42",
                "projC55": "projT55",
                "projC50": "projT50",
                "projC48": "projT48",
                "projC37": "projT37",
                "projC41": "projT41",
                "projC38": "projT38",
                "projC29": "projT29",
                "projC45": "projT45",
                "projC53": "projT53",
                "projC59": "projT59",
                "projC39": "projT39",
                "projC51": "projT51",
                "projC60": "projT60",
                "projC4": "projT4",
                "projC21": "projT21",
                "projC24": "projT24",
                "projC13": "projT13",
                "projC12": "projT12",

                # group 2
                "projC49": "projT49",
                "projC54": "projT54",
                "projC46": "projT46",
                "projC0": "projT0",
                "projC57": "projT57",

                # group 3
                "projC26": "projT26",
                "projC47": "projT47",
                "projC40": "projT40",
                "projC44": "projT44",
                "projC28": "projT28",

                # group 4
                "projC56": "projT56",
                "projC31": "projT31",

                # group 5
                "projC43": "projT43",
                "projC10": "projT10",
                "projC27": "projT27",
                "projC58": "projT58",
                "projC16": "projT16",
                "projC35": "projT35",
                "projC17": "projT17",
                "projC22": "projT22", 
                "projC18": "projT18",
                "projC20": "projT20",
                "projC33": "projT33",
                "projC25": "projT25",
                "projC32": "projT32",
                "projC7": "projT7",
                "projC23": "projT23", 
                "projC8": "projT8",
                "projC1": "projT1",
                "projC2": "projT2",

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

TRUNKS = [transport for transport in PIPE_DOWNSTREAM]

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