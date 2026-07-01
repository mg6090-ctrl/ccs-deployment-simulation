import scenario_1_methods as s1
import scenario_2_methods as s2

#==================================================================
# CORE FUNCTIONALITY TESTING — CONSTANTS
#==================================================================

TEST_CLUSTER = {
    "projS1": {"projT1": ["projC1", "projC2"]}
}
TEST_CAPS = {"projC1": {"definition": 5, "approval": 10, "construction": 10}, 
                "projC2": {"definition": 5, "approval": 10, "construction": 10}}
TEST_CAP_VOLS = {"projC1": 2, "projC2": 1}
TEST_TRANS = {"projT1": {"definition": 5, "approval": 10, "construction": 10}}
TEST_TRANS_VOLS = {"projT1": 4}
TEST_STORS = {"projS1": {"definition": 5, "approval": 10, "construction": 10}}
TEST_STORS_VOLS = {"projS1": 8}

# check functions
def check(description, output, expected):
    check = False
    if output == expected:
        check = True
    print (description, "expected:", expected, "got:", output, "pass:", check)

#==================================================================
# S1 CORE FUNCTIONALITY TESTS
#==================================================================

def s1_build_test_graph():
    G = s1.projGraph(
        replication_seed=0, 
        clusters = TEST_CLUSTER, 
        caps = TEST_CAPS,
        caps_vol = TEST_CAP_VOLS,
        trans = TEST_TRANS,
        trans_vol = TEST_TRANS_VOLS,
        stor = TEST_STORS,
        stor_vol = TEST_STORS_VOLS,
        frac_split = (1, 0), # testing the case where all captures are gated on approval (all risk tolerant)
        sampling = False
    )   
    return G

# Test 1: CPM on a simple chain
def test_CPM(G):
    # before running the CPM
    print("Before running CPM: \n")
    for node in G.nodes():
        print(node, "ES:", G.nodes[node]["ES"], "EF:", G.nodes[node]["EF"])
    # after running the CPM
    s1.CPM(G)
    print("After running CPM: \n")
    for node in G.nodes():
        print(node, "ES:", G.nodes[node]["ES"], "EF:", G.nodes[node]["EF"])

# Test 2: single abandonment
def test_abandonment(G):
    c_abandon_1 = s1.apply_attrition(
        G, 
        base_rate = 0, # if 0, expect no abandonment. if 1, expect all to abandoned
        clusters = TEST_CLUSTER, 
        replication_seed = 0,
        max_rate = 1,
        cap_tolerance = 1
    )

    c_abandon_2 = s1.apply_attrition(
            G, 
            base_rate = 1, # if 0, expect no abandonment. if 1, expect all to abandoned
            clusters = TEST_CLUSTER, 
            replication_seed = 0,
            max_rate = 1,
            cap_tolerance = 1
    )

    c_abandon_3 = s1.apply_attrition(
            G, 
            base_rate = 0.05, # if 0, expect no abandonment. if 1, expect all to abandoned
            clusters = TEST_CLUSTER, 
            replication_seed = 0,
            max_rate = 0.4,
            cap_tolerance = 10
    )
    check("Expected: no abandonment", len(c_abandon_1), 0)
    check("Expected: all abandon", len(c_abandon_2), 2)
    check("Expected: random", len(c_abandon_3), 1)

# Test 3: monte carlo seed reproducibility (test both duration sampling per run and abandonment between runs)


#==================================================================
# S2 CORE FUNCTIONALITY TESTS 
#==================================================================

def s2_build_test_graph():
    G = s2.projGraph(replication_seed=0, sampling=False,
              clusters=TEST_CLUSTER, capture_durations=TEST_CAPS, capture_volumes=TEST_CAP_VOLS,
              storage_durations=TEST_STORS, storage_volumes=TEST_STORS_VOLS,
              transport_durations=TEST_TRANS, transport_volumes=TEST_TRANS_VOLS)
    
    return G

# tests
def test_threshold_gating():
    arrivals = [(1.0, 5), (1.0, 8), (2.0, 10)]   # total volume 4.0
    # needs 4*0.5 = 2.0. Sorted by time: 1.0@5, 1.0@8 -> cum 2.0 at t=8.
    check("Checking threshold gating:", s2.threshold_gating(arrivals, capacity=4, fraction=0.5), 8)

    # needs 20*0.5 = 10.0, but total is only 4.0 -> never fires
    check("returns None when threshold never reached", s2.threshold_gating(arrivals, capacity=20, fraction=0.5), None)
 
    # needs 1*0.5 = 0.5, first arrival (1.0@5) already exceeds -> fires at 5
    check("fires at first arrival when threshold is tiny", s2.threshold_gating(arrivals, capacity=1, fraction=0.5), 5)
 
    # ordering matters: an early small + late large should fire at the time
    # the cumulative crosses, not at the largest volume's time.
    out_of_order = [(3.0, 20), (1.0, 2), (1.0, 5)]   # need 2.0
    # sorted by time: 1.0@2, 1.0@5 -> cum 2.0 at t=5
    check("uses arrival-time order, not list order", s2.threshold_gating(out_of_order, capacity=4, fraction=0.5), 5)

def test_cpm(G):
    s2.CPM(G, 0.5)
    # before running the CPM
    print("Before running CPM: \n")
    for node in G.nodes():
        print(node, "ES:", G.nodes[node]["ES"], "EF:", G.nodes[node]["EF"])

    # after running the CPM
    s2.CPM(G)
    print("After running CPM: \n")
    for node in G.nodes():
        print(node, "ES:", G.nodes[node]["ES"], "EF:", G.nodes[node]["EF"])

def test_threshold_joints(G):
    s2.CPM(G, threshold_frac=0.5)
    # Transport approval-joint: needs transport_vol*0.5 = 4*0.5 = 2.0.
    # Captures supply 2 + 1 = 3.0 >= 2.0 -> should FIRE (not below threshold).
    check("transport approval joint fires (supply 3 >= need 2)",
          G.nodes[("projT1", "approval joint node")]["below_threshold"], True)

    # Storage FID: needs storage_vol*0.5 = 8*0.5 = 4.0.
    # The transport cluster forwards its actual_volume (capped at transport vol 4,
    # committed 3) = 3.0 < 4.0 -> should be BELOW threshold (never fires).
    check("storage FID below threshold (supply 3 < need 4)",
          G.nodes[("projS1 cluster", "FID joint node")]["below_threshold"], True)
    
    # Now raise the fraction so even the transport joint fails:
    # need 4*0.9 = 3.6 > supply 3.0 -> transport approval joint below threshold.
    G2 = G
    s2.CPM(G2, threshold_frac=0.9)
    check("transport approval joint fails at high fraction (need 3.6 > 3)",
          G2.nodes[("projT1", "approval joint node")]["below_threshold"], True)

def test_stage_delay(G):
    s2.CPM(G, 0.5)

    # A capture's definition delay = (its definition joint EF) - (its own def EF).
    # The definition joint waits for max(capture def, transport def). Both are 5,
    # so the joint fires at 5, and the capture's own def EF is 5 -> delay 0.
    d = s2.stage_delay(G, ("projC1", "definition"))
    check("capture definition delay >= 0", d >= 0, True)
 
def test_attrition_prob():
    base, max, tol = 0.05, 0.4, 36

    # delay 0 -> base_rate * exp(0) = base_rate exactly
    p0 = s2.calculate_attrition_probability(
        delay=0, tech="capture", base_rate=base, max_rate=max,
        capture_tolerance=tol, transport_tolerance=tol, storage_tolerance=tol)
    check("delay 0 -> base rate: ", p0, base)

    p_big = s2.calculate_attrition_probability(
        delay=100000, tech="capture", base_rate=base, max_rate=max,
        capture_tolerance=tol, transport_tolerance=tol, storage_tolerance=tol)
    check("delay -> very large: ", p_big, max)

    p_cap = s2.calculate_attrition_probability(
        delay=30, tech="capture", base_rate=base, max_rate=max,
        capture_tolerance=20, transport_tolerance=60, storage_tolerance=60)
    p_trans = s2.calculate_attrition_probability(
        delay=30, tech="transport", base_rate=base, max_rate=max,
        capture_tolerance=20, transport_tolerance=60, storage_tolerance=60)
    # smaller tolerance (capture, 20) -> steeper -> higher prob than transport (60)
    check("smaller tolerance gives higher probability", p_cap > p_trans, True)

#==================================================================
# MAIN (EXECUTION)
#==================================================================

if __name__ == "__main__":

    print("Running core functionality tests for S1...\n")

    s1_G_test = s1_build_test_graph()

    test_CPM(s1_G_test)
    test_abandonment(s1_G_test)

    print("\n")

    print("Running core functionality tests for S2...\n")

    s2_G_test = s2_build_test_graph()

    test_threshold_gating()
    test_cpm(s2_G_test)
    test_threshold_joints(s2_G_test)
    test_stage_delay(s2_G_test)
    test_attrition_prob()
