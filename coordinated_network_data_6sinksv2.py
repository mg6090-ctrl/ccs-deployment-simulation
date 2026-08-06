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

    # group 4
    "projC56": 2,
    "projC31": 2,

    # group 5
    "projC11": 2,
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
    "projS64": 4,

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
}
W11_PHASING = {proj: PHASE_TESTING[W11_PHASING_PROJ[proj]-1] for proj in W11_PHASING_PROJ}

# world_2.py looks up NO_PIPE_PROJECTS; world_1_s1.py and world_1_s2.py still refer to DAC_PROJECTS
NO_PIPE_PROJECTS = DAC_PROJECTS

#==================================================================
# DURATION MULTIPLIERS FOR PIPELINE
#==================================================================

PIPE_MULT = {
    "projT11":  0.83,
    "projT12":  0.15,
    "projT13":  0.06,

    "projT21":  1.40,
    "projT22":  0.97,
    "projT23":  1.76,
    "projT24":  1.43,
    "projT25":  0.33,

    "projT31":  0.61,

    "projT41":  0.24,

    "projT51":  0.95,
    "projT52":  2.41,
    "projT53":  0.56,
    "projT54":  1.67,
    "projT55":  0.49,
    "projT56":  0.30,
    "projT57":  0.82,
    "projT58":  0.13,
    "projT59":  0.43,

    'projT71':  2.87,
    "projT72":  2.24,
    "projT73":  1.53,
    "projT74":  0.93,
    "projT75":  1.07,
    "projT76":  0.66,
    "projT77":  1.17,

    # note: no DAC pipe multipliers — DAC has no transport project at all
}

NO_PIPE_MULT = {project: 1 for project in PIPE_MULT}

#==================================================================
# PROJECT DATA 
#==================================================================

PROJECT_TYPE = {
                # group 1
                "projC4": "hydrogen",
                "projC21": "refinery",
                "projC13": "NGCC",
                "projC24": "NGCC",

                # group 2
                "projC49": "biomass_gasification",
                "projC54": "biomass_gasification",
                "projC46": "biomass_gasification",
                "projC57": "biomass_gasification",
                "projC0": "ethanol",
                "projC39": "biomass_gasification",
                "projC26": "NGCC",
                "projC47": "biomass_gasification",

                # group 3
                "projC40": "biomass_gasification",
                "projC44": "biomass_gasification",

                # group 4
                "projC56": "biomass_gasification",
                "projC31": "ethanol",

                # group 5
                "projC11": "gas_processing",
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

                # group 7
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
                "projS0": "storage",

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
                "projT11": "transport", "projT12": "transport", "projT13": "transport",

                # group 2 transports
                "projT21": "transport", "projT22": "transport", "projT23": "transport", "projT24": "transport", "projT25": "transport", 

                # group 3 transports
                "projT31": "transport",

                # group 4 transports 
                "projT41": "transport",

                # group 5 transports
                "projT51": "transport", "projT52": "transport", "projT53": "transport", "projT54": "transport", "projT55": "transport",
                "projT56": "transport", "projT57": "transport", "projT58": "transport", "projT59": "transport",

                # group 7 transports
                "projT71": "transport", "projT72": "transport", "projT73": "transport", "projT74": "transport", "projT75": "transport",
                "projT76": "transport", "projT77": "transport",

                # note: no DAC transports — DAC has no real pipeline, so CAPTURE_PIPE points DAC captures straight at their storage
               }

#==================================================================
# TOPOLOGICAL DATA FOR GRAPH
#==================================================================

# stores the pipe/storage every single transport flows into next
PIPE_DOWNSTREAM = {
                   # group 1
                   "projT11": "projS1",
                   "projT12": "projT11",
                   "projT13": "projT11",

                   # group 2
                   "projT21": "projS2",
                   "projT23": "projS2",
                   "projT24": "projT23",
                   "projT25": "projT23",
                   "projT22": "projT21",
                   
                   # group 3
                   "projT31": "projS3",
                   
                   # group 4
                   "projT41": "projS10",

                   # group 5
                   "projT51": "projT52",
                   "projT52": "projS5",
                   "projT53": "projT52",
                   "projT54": "projT52",
                   "projT55": "projT54",
                   "projT56": "projT54",
                   "projT57": "projT56",
                   "projT58": "projT52",
                   "projT59": "projT52",

                   # group 7
                   "projT71": "projS0",
                   "projT72": "projT71",
                   "projT73": "projT72",
                   "projT76": "projT71",
                   "projT77": "projT71",
                   "projT74": "projT71",
                   "projT75": "projT74",

                    # note: no DAC transports here: see CAPTURE_PIPE
                   }

# stores the transport every single capture flows into next
CAPTURE_PIPE = {
                # group 1 
                "projC4": "projT12",
                "projC21": "projT11",
                "projC24": "projT11",
                "projC13": "projT13",
                
                # group 2
                "projC49": "projT24",
                "projC54": "projT25",
                "projC46": "projT25",
                "projC0": "projT23",
                "projC57": "projT23",
                "projC39": "projT24",
                "projC26": "projT21",
                "projC47": "projT22",

                # group 3
                "projC40": "projT31",
                "projC44": "projT31",

                # group 4
                "projC56": "projT41",
                "projC31": "projT41",

                # group 5
                "projC43": "projT51",
                "projC11": "projT53",
                "projC27": "projT52",
                "projC58": "projT52",
                "projC16": "projT52",
                "projC35": "projT51",
                "projC17": "projT51",
                "projC22": "projT54", 
                "projC18": "projT54",
                "projC20": "projT54",
                "projC33": "projT55",
                "projC25": "projT56",
                "projC32": "projT57",
                "projC7": "projT58",
                "projC23": "projT52", 
                "projC8": "projT59",
                "projC1": "projT59",
                "projC2": "projT59",

                # group 7
                "projC52": "projT77",
                "projC19": "projT71",
                "projC42": "projT73",
                "projC55": "projT76",
                "projC50": "projT76",
                "projC48": "projT74",
                "projC37": "projT74",
                "projC41": "projT71",
                "projC38": "projT71",
                "projC29": "projT71",
                "projC45": "projT72",
                "projC53": "projT72",
                "projC59": "projT72",
                "projC51": "projT75",
                "projC60": "projT75",

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
          
          # group 2
          "projT21",
          "projT23",
          
          # group 3
          "projT31",
          
          # group 4
          "projT41",

          # group 5
          "projT52",

          # group 7
          "projT71"

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

    # group 4
    "projC56": 1.06,
    "projC31": 0.11,

    # group 5
    "projC11": 0.06,
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