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

NO_PIPE_PROJECTS = [
    # DACS
    "projC61",
    "projC62",
    "projC63",
    "projC64",
    "projC65",
    "projC66",
    "projC67",
    "projC68",
    "projC69",
    "projC610",
    "projC611",
    "projC612",
    "projC613",
    "projC614",
    "projC615",
    "projC616",
    "projC617",
    "projC618",
    "projC619",
    "projC620",
    "projC621",
    "projC622",
    "projC623",
    "projC624",
    "projC625",
    "projC626",
    "projC627",
    "projC628",
    "projC629",
    "projC630",
]

# add in phasing for all BECCS and refineries (captures + transports)
W2_BRD_PROJECTS = {
    # group 1 
        "projC29": 3,
        "projT29": 3,
        "projS29": 3,

        "projC42": 3,
        "projT42": 3,
        "projS42": 3,

        "projC37": 3,
        "projT37": 3,
        "projS37": 3,

        "projC39": 3,
        "projT39": 3,
        "projS39": 3,

        "projC25": 2,
        "projT25": 2,
        "projS25": 2,

        "projC28": 3,
        "projS28": 3,
        "projT28": 3,

        "projC24": 3,
        "projT24": 3,
        "projS24": 3,

        "projC35": 4,
        "projT35": 4,
        "projS35": 4,

        "projC32": 3,
        "projT40": 3,
        "projS46": 3,

        "projC47": 3,
        "projT47": 3,
        "projS47": 3,

        "projC38": 3,
        "projT38": 3,
        "projS38": 3,
    
        # group 2
        "projC13": 4,
        "projT13": 4,
        "projS13": 4,

        "projC26": 3,
        "projT26": 3,
        "projS26": 3,

        "projC36": 3,
        "projT36": 3,
        "projS36": 3,

        "projC34": 3,
        "projT34": 3,
        "projS34": 3,

        "projC33": 3,
        "projT33": 3,
        "projS33": 3,

        "projC44": 3,
        "projT44": 3,
        "projS44": 3,
    
        # group 3
        "projC31": 3,
        "projT31": 3,
        "projS31": 3,

        "projC27": 2, 
        "projT27": 2,
        "projS27": 2,
    
        # group 4
        "projC43": 2,
        "projT43": 2,
        "projS43": 2,

        "projC20": 2,
        "projT20": 2,
        "projS20": 2,
    
        # group 5
        "projC30": 2,
        "projT30": 2,
        "projS30": 2,

        "projC45": 4,
        "projT45": 4,
        "projS45": 4,
        
        "projC15": 4,
        "projT15": 4,
        "projS15": 4,

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

W2_BRD_PHASE = {proj: PHASE_TESTING[W2_BRD_PROJECTS[proj]-1] for proj in W2_BRD_PROJECTS}

#==================================================================
# DURATION MULTIPLIERS FOR PIPELINE
#==================================================================

PIPE_MULT = {
        "projT0": 0.05,
        "projT1": 2.22,
        "projT2": 2.5,
        "projT4": 0.55,
        "projT5": 0.25,
        "projT7": 1.67,
        "projT8": 1.74,
        "projT10": 0.07,
        "projT12": 0.04,
        "projT13": 0.01,
        "projT16": 0.37,
        "projT17": 0.79,
        "projT18": 1.79,
        "projT19": 1.26,
        "projT20": 2.12,
        "projT21": 0.59,
        "projT22": 1.87,
        "projT23": 2.04,
        "projT24": 0.02,
        "projT25": 2.33,
        "projT26": 0.77,
        "projT27": 0.57,
        "projT28": 0.29,
        "projT29": 0.44,
        "projT31": 0.13,
        "projT32": 3.10,
        "projT33": 2.28,
        "projT35": 0.68,
        
        "projT37": 0.34,
        "projT38": 0.34,
        "projT39": 0.75,
        
        
        "projT42": 2.10,
        "projT43": 0.30,
        
        "projT45": 1.26,
        
        "projT47": 0.83,
        "projT48": 0.82,
        
        "projT50": 1.24,
        "projT51": 0.92,
        "projT52": 2.14,
        "projT53": 0.99,
        
        "projT55": 1.23,
        "projT56": 0.32,
        "projT57": 0.72,
        "projT58": 0.44,
        "projT59": 0.36,
        "projT60": 0.56,
        "projT61": 

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

                # storages
                "projS0": "storage",
                "projS1": "storage",
                "projS2": "storage",
                "projS4": "storage",
                "projS5": "storage",
                
                "projS10":"storage",
                "projS12": "storage",
                "projS13": "storage",
                
                "projS17": "storage",
                "projS18": "storage",
                
                "projS20": "storage",
                "projS21": "storage",
                "projS22": "storage",
                "projS23": "storage",
                "projS24": "storage",
                "projS25": "storage",
                "projS26": "storage",
                "projS27": "storage",
                
                "projS29": "storage",
                "projS31": "storage",
                "projS32": "storage",
                "projS33": "storage",
                
                "projS37": "storage",
                "projS38": "storage",
                
                "projS40": "storage",
                "projS41": "storage",
                "projS42": "storage",
                "projS43": "storage",
                "projS44": "storage",
                "projS45": "storage",
                "projS46": "storage",
                "projS47": "storage",
                "projS48": "storage",
                "projS49": "storage",
                "projS50": "storage",
                "projS51": "storage",
                "projS52": "storage",
                "projS53": "storage",
                "projS54": "storage",
                "projS55": "storage",
                "projS56": "storage",
                "projS57": "storage",
                
                "projS59": "storage",
                "projS60": "storage",

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
                "projT5": "transport",
                
                "projT10": "transport",
                "projT12": "transport",
                "projT13": "transport",
                
                "projT17": "transport",
                "projT18": "transport",
                
                "projT20": "transport",
                "projT21": "transport",
                "projT22": "transport",
                "projT23": "transport",
                "projT24": "transport",
                "projT25": "transport",
                "projT26": "transport",
                "projT27": "transport",
                
                "projT29": "transport",
                "projT31": "transport",
                "projT32": "transport",
                "projT33": "transport",
                
                "projT37": "transport",
                "projT38": "transport",

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
                    "projT0": "projS0",
                    "projT1": "projS1",
                    "projT2": "projS2",
                    "projT4": "projS4",
                    "projT5": "projS5",

                    "projT10": "projS10",
                    "projT12": "projS12",
                    "projT13": "projS13",
                    
                    "projT17": "projS17",
                    "projT18": "projS18",
                   
                    "projT20": "projS20",
                    "projT21": "projS21",
                    "projT22": "projS22",
                    "projT23": "projS23",
                    "projT24": "projS24",
                    "projT25": "projS25",
                    "projT26": "projS26",
                    "projT27": "projS27",
                    
                    "projT29": "projS29",
                    "projT31": "projS31",
                    "projT32": "projS32",
                    "projT33": "projS33",
                    
                    "projT37": "projS37",
                    "projT38": "projS38",

                    "projT40": "projS40",
                    "projT41": "projS41",
                    "projT42": "projS42",
                    "projT43": "projS43",
                    "projT44": "projS44",
                    "projT45": "projS45",
                    "projT46": "projS46",
                    "projT47": "projS47",
                    "projT48": "projS48",
                    "projT49": "projS49",
                    "projT50": "projS50",
                    "projT51": "projS51",
                    "projT52": "projS52",
                    "projT53": "projS53",
                    "projT54": "projS54",
                    "projT55": "projS55",
                    "projT56": "projS56",
                    "projT57": "projS57",
                    
                    "projT59": "projS59",
                    "projT60": "projS60",

                    # note: no DAC transports here: see CAPTURE_PIPE
                   }

# stores the transport every single capture flows into next
CAPTURE_PIPE = {
    
                # group 1
                "projC46": "projT46",
                "projC40": "projT40",
                "projC32": "projT32",
                "projC6": "projT6",
                "projC47": "projT47",
                "projC38": "projT38",
                "projC25": "projT25",
                "projC28": "projT28",
                "projC24": "projT24",
                "projC35": "projT35",
                "projC37": "projT37",
                "projC42": "projT42",
                "projC29": "projT29",
                "projC11": "projT11",
                "projC39": "projT39",

                # group 2
                "projC16": "projT16",
                "projC7": "projT7",
                "projC3": "projT3",
                "projC13": "projT13",
                "projC26": "projT26",
                "projC36": "projT36",
                "projC33": "projT33",
                "projC0": "projT0",
                "projC44": "projT44",
                "projC18": "projT18",
                "projC34": "projT34",

                # group 3
                "projC31": "projT31",
                "projC27": "projT27",

                # group 4
                "projC43": "projT43",
                "projC20": "projT20",

                # group 5
                "projC5": "projT5",
                "projC30": "projT30",
                "projC8": "projT8",
                "projC45": "projT45",
                "projC19": "projT19",
                "projC23": "projT23",
                "projC9": "projT9",
                "projC15": "projT15",
                "projC4": "projT4",
                "projC1": "projT1",
                "projC2": "projT2",
                "projC22": "projT22",
                "projC14": "projT12",
                "projC12": "projT12",
                "projC10": "projT10",
                "projC17": "projT17",
                "projC21": "projT21",

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