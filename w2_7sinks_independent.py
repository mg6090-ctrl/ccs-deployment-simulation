import w2_network_pipelength

#==================================================================
# PARAMETERS AND CONSTANTS
#==================================================================

# Note that DACs now go from projC62 to projC631 because projC61 is non-DAC

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
    "projC631": 3,
}

W11_2_PHASE = {cap: PHASE_TESTING[DAC_PROJECTS[cap]-1] for cap in DAC_PROJECTS}

NO_PIPE_PROJECTS = [
    # DACS
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
    "projC631"
]

# phasing for BECCS (3) and refineries (4), derived from uncoordinated_multipliers.csv;
# DAC phasing (also in this dict) lives below in DAC_PROJECTS
W2_BRD_PROJECTS = {
        # refineries (phase 4)
        "projC21": 4,
        "projT21": 4,
        "projS21": 4,

        "projC23": 4,
        "projT23": 4,
        "projS23": 4,

        # BECCS (phase 3)
        "projC37": 3,
        "projT37": 3,
        "projS37": 3,

        "projC38": 3,
        "projT38": 3,
        "projS38": 3,

        "projC39": 3,
        "projT39": 3,
        "projS39": 3,

        "projC40": 3,
        "projT40": 3,
        "projS40": 3,

        "projC41": 3,
        "projT41": 3,
        "projS41": 3,

        "projC42": 3,
        "projT42": 3,
        "projS42": 3,

        "projC43": 3,
        "projT43": 3,
        "projS43": 3,

        "projC44": 3,
        "projT44": 3,
        "projS44": 3,

        "projC45": 3,
        "projT45": 3,
        "projS45": 3,

        "projC46": 3,
        "projT46": 3,
        "projS46": 3,

        "projC47": 3,
        "projT47": 3,
        "projS47": 3,

        "projC48": 3,
        "projT48": 3,
        "projS48": 3,

        "projC49": 3,
        "projT49": 3,
        "projS49": 3,

        "projC50": 3,
        "projT50": 3,
        "projS50": 3,

        "projC51": 3,
        "projT51": 3,
        "projS51": 3,

        "projC52": 3,
        "projT52": 3,
        "projS52": 3,

        "projC53": 3,
        "projT53": 3,
        "projS53": 3,

        "projC54": 3,
        "projT54": 3,
        "projS54": 3,

        "projC55": 3,
        "projT55": 3,
        "projS55": 3,

        "projC56": 3,
        "projT56": 3,
        "projS56": 3,

        "projC57": 3,
        "projT57": 3,
        "projS57": 3,

        "projC58": 3,
        "projT58": 3,
        "projS58": 3,

        "projC59": 3,
        "projT59": 3,
        "projS59": 3,

        "projC60": 3,
        "projT60": 3,
        "projS60": 3,

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

}

W2_BRD_PHASE = {proj: PHASE_TESTING[W2_BRD_PROJECTS[proj]-1] for proj in W2_BRD_PROJECTS}

#==================================================================
# DURATION MULTIPLIERS FOR PIPELINE
#==================================================================

PIPE_MULT = w2_network_pipelength.UNCOORD_PIPE_MULT

NO_PIPE_MULT = {project: 1 for project in PIPE_MULT}

#==================================================================
# PROJECT DATA 
#==================================================================

PROJECT_TYPE = {
                # non-DAC captures, from uncoordinated_multipliers.csv
                "projC0": "ethanol",  # Aemetis-Keyes
                "projC1": "NGCC",  # AES-Alamitos
                "projC2": "NGCC",  # AES-HuntingtonBeach
                "projC4": "hydrogen",  # AirLiquide-Rodeo
                "projC5": "hydrogen",  # AirProducts-Martinez
                "projC10": "gas_processing",  # CRC-ElkHills-GasPlant
                "projC12": "NGCC",  # Calpine-Sutter
                "projC13": "NGCC",  # Calpine-Delta
                "projC17": "cement",  # CalPortland-Mojave
                "projC18": "cement",  # CalPortland-OroGrande
                "projC19": "cement",  # CalPortland-Redding
                "projC20": "cement",  # Cemex-Victorville
                "projC21": "refinery",  # Chevron-Richmond
                "projC22": "NGCC",  # HighDesertPower
                "projC23": "refinery",  # LosAngelesRefinery
                "projC24": "NGCC",  # MarshLanding
                "projC25": "cement",  # MitsubishiCement
                "projC26": "NGCC",  # MossLanding
                "projC27": "cement",  # NationalCement-Lebec
                "projC29": "NGCC",  # PGE-Colusa
                "projC31": "ethanol",  # Pixley-Calgren
                "projC32": "NGCC",  # Sentinel-EnergyCenter
                "projC33": "NGCC",  # SCE-Mountainview
                "projC35": "cement",  # Tehachapi-Cement
                "projC37": "biomass_gasification",  # Butte-BECCS
                "projC38": "biomass_gasification",  # Colusa-BECCS
                "projC39": "biomass_gasification",  # ElDorado-BECCS
                "projC40": "biomass_gasification",  # Fresno-BECCS
                "projC41": "biomass_gasification",  # Glenn-BECCS
                "projC42": "biomass_gasification",  # Humboldt-BECCS
                "projC43": "biomass_gasification",  # Kern-BECCS
                "projC44": "biomass_gasification",  # Madera-BECCS
                "projC45": "biomass_gasification",  # Mendocino-BECCS
                "projC46": "biomass_gasification",  # Merced-BECCS
                "projC47": "biomass_gasification",  # Monterey-BECCS
                "projC48": "biomass_gasification",  # Plumas-BECCS
                "projC49": "biomass_gasification",  # SanJoaquin-BECCS
                "projC50": "biomass_gasification",  # Shasta-BECCS
                "projC51": "biomass_gasification",  # Sierra-BECCS
                "projC52": "biomass_gasification",  # Siskiyou-BECCS
                "projC53": "biomass_gasification",  # Sonoma-BECCS
                "projC54": "biomass_gasification",  # Stanislaus-BECCS
                "projC55": "biomass_gasification",  # Trinity-BECCS
                "projC56": "biomass_gasification",  # Tulare-BECCS
                "projC57": "biomass_gasification",  # Tuolumne-BECCS
                "projC58": "biomass_gasification",  # Ventura-BECCS
                "projC59": "biomass_gasification",  # Yolo-BECCS
                "projC60": "biomass_gasification",  # Yuba-BECCS
                "projC61": "NGCC",  # CRC-ElkHills-Powerplant (non-DAC, see note above)

                # DACS
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

                # storages (one per non-DAC capture, from uncoordinated_multipliers.csv)
                "projS0": "storage",
                "projS1": "storage",
                "projS2": "storage",
                "projS4": "storage",
                "projS5": "storage",
                "projS10": "storage",
                "projS12": "storage",
                "projS13": "storage",
                "projS17": "storage",
                "projS18": "storage",
                "projS19": "storage",
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
                "projS35": "storage",
                "projS37": "storage",
                "projS38": "storage",
                "projS39": "storage",
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
                "projS58": "storage",
                "projS59": "storage",
                "projS60": "storage",
                "projS61": "storage",

                # DAC storages
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

                # transports (one per non-DAC capture, from uncoordinated_multipliers.csv)
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
                "projT19": "transport",
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
                "projT61": "transport",

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
                    "projT19": "projS19",
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
                    "projT35": "projS35",
                    "projT37": "projS37",
                    "projT38": "projS38",
                    "projT39": "projS39",
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
                    "projT58": "projS58",
                    "projT59": "projS59",
                    "projT60": "projS60",
                    "projT61": "projS61",

                    # note: no DAC transports here: see CAPTURE_PIPE
                   }

# stores the transport every single capture flows into next
CAPTURE_PIPE = {

                # non-DAC captures, each with its own transport, from uncoordinated_multipliers.csv
                "projC0": "projT0",
                "projC1": "projT1",
                "projC2": "projT2",
                "projC4": "projT4",
                "projC5": "projT5",
                "projC10": "projT10",
                "projC12": "projT12",
                "projC13": "projT13",
                "projC17": "projT17",
                "projC18": "projT18",
                "projC19": "projT19",
                "projC20": "projT20",
                "projC21": "projT21",
                "projC22": "projT22",
                "projC23": "projT23",
                "projC24": "projT24",
                "projC25": "projT25",
                "projC26": "projT26",
                "projC27": "projT27",
                "projC29": "projT29",
                "projC31": "projT31",
                "projC32": "projT32",
                "projC33": "projT33",
                "projC35": "projT35",
                "projC37": "projT37",
                "projC38": "projT38",
                "projC39": "projT39",
                "projC40": "projT40",
                "projC41": "projT41",
                "projC42": "projT42",
                "projC43": "projT43",
                "projC44": "projT44",
                "projC45": "projT45",
                "projC46": "projT46",
                "projC47": "projT47",
                "projC48": "projT48",
                "projC49": "projT49",
                "projC50": "projT50",
                "projC51": "projT51",
                "projC52": "projT52",
                "projC53": "projT53",
                "projC54": "projT54",
                "projC55": "projT55",
                "projC56": "projT56",
                "projC57": "projT57",
                "projC58": "projT58",
                "projC59": "projT59",
                "projC60": "projT60",
                "projC61": "projT61",

                # DACs feed straight into its storage; DACs do not have
                # a pipeline, so no intermediate transport projects exist
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
                "projC631": "projS631"
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
    # non-DAC captures, from uncoordinated_multipliers.csv (rate_mt_per_yr)
    "projC0": 0.06,
    "projC1": 5.39,
    "projC2": 2.37,
    "projC4": 0.74,
    "projC5": 0.55,
    "projC10": 0.1,
    "projC12": 1.7,
    "projC13": 2.46,
    "projC17": 0.89,
    "projC18": 1.28,
    "projC19": 0.33,
    "projC20": 1.75,
    "projC21": 2.16,
    "projC22": 2.5,
    "projC23": 3.06,
    "projC24": 3.38,
    "projC25": 1.09,
    "projC26": 5.46,
    "projC27": 0.73,
    "projC29": 1.89,
    "projC31": 0.11,
    "projC32": 2.76,
    "projC33": 2.87,
    "projC35": 0.47,
    "projC37": 1.03,
    "projC38": 0.84,
    "projC39": 0.95,
    "projC40": 3.11,
    "projC41": 1.12,
    "projC42": 3.59,
    "projC43": 2.35,
    "projC44": 1.54,
    "projC45": 2.62,
    "projC46": 0.77,
    "projC47": 0.78,
    "projC48": 1.38,
    "projC49": 1.0,
    "projC50": 1.89,
    "projC51": 1.39,
    "projC52": 1.94,
    "projC53": 1.1,
    "projC54": 1.76,
    "projC55": 1.37,
    "projC56": 1.06,
    "projC57": 1.4,
    "projC58": 0.63,
    "projC59": 0.51,
    "projC60": 0.57,
    "projC61": 1.19,

    # DACs
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
    "projC631": 1
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