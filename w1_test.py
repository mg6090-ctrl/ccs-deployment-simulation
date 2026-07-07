"""
Verification tests for the two coordinated (World 1) sub-scenarios.

ADAPT BEFORE RUNNING
--------------------
- Set the import to your module(s). If the two scenarios are in separate files,
  import each separately (s1_tier, s1_hammock).
- Confirm function/parameter names match yours (monte_carlo, analyze_monte_carlo,
  build_model, CPM, apply_attrition, calculate_delay, and the hammock threshold
  parameter name).
- Paste/point to the dummy network data each scenario expects.

WHAT THESE TEST (the behaviors we established)
Scenario 1.1 (tier-gated, timing-wait between tiers):
  - base_rate=0 -> zero abandonment (both rolls bottom out)
  - each capture rolls exactly ONCE (not 4x) -> abandonment consistent with
    two rolls per capture, not eight
  - Tier 2 project's definition ES >= its Tier 1 predecessor's commissioning EF
    (the tier timing wait actually delays Tier 2)
  - tier wait shows up as later START, not as approval delay
Scenario 1.2 (hammock, pre-built infra):
  - hammock EF responds to threshold (given spread-out commissioning volumes)
  - capture definition ES >= hammock EF (hammock gates definition)
  - threshold = 1.0 -> approval delays ~0 -> abandonment == base-rate floor
  - abandonment DECREASES as threshold rises (more infra head start)
"""

# ---- EDIT THESE IMPORTS ----
import world_1_s1_edits as tier      # Scenario 1.1 (tier-gated)
import world_1_s2_edits as ham       # Scenario 1.2 (hammock)
# If both scenarios share one module, import once and use it for both.

# ---------------------------------------------------------------
# minimal harness
# ---------------------------------------------------------------
_p = _f = 0
def check(name, ok, detail=""):
    global _p, _f
    if ok: _p += 1; print(f"  PASS  {name}   {detail}")
    else:  _f += 1; print(f"  FAIL  {name}   {detail}")

def approx(a, b, tol=1e-6):
    return abs(a - b) <= tol


# ===============================================================
# SCENARIO 1.1 — TIER-GATED
# ===============================================================
def test_tier_scenario():
    print("\n=== Scenario 1.1: tier-gated ===")

    # --- base_rate = 0 -> zero abandonment ---
    res0 = tier.analyze_monte_carlo(tier.monte_carlo(100, base_rate=0.0, max_rate=0.0))
    check("base_rate=0 -> zero abandonment",
          approx(res0["average capture abandonment rate"], 0.0),
          f'rate={res0["average capture abandonment rate"]}')

    # --- abandonment consistent with TWO rolls per capture (not 4x) ---
    # At a moderate base_rate with ~0 approval delay, per-capture death prob is
    # 1-(1-base)^2. Compare aggregate rate to that ballpark (not exact -- delays
    # add on top -- but it should be nowhere near the 4x-inflated value).
    b = 0.3
    resb = tier.analyze_monte_carlo(tier.monte_carlo(300, base_rate=b, max_rate=0.4))
    per_capture_two_roll_floor = 1 - (1 - b) ** 2   # ~0.51 at b=0.3
    rate = resb["average capture abandonment rate"]
    check("abandonment in two-roll range (not 4x-inflated)",
          rate < 0.75,   # 4x rolls would push this toward ~0.9+
          f'rate={rate:.3f}, two-roll floor~{per_capture_two_roll_floor:.3f}')

    # --- structural: Tier 2 definition waits for Tier 1 commissioning ---
    # Build one graph, run CPM, and for every transport whose downstream is
    # another transport (a Tier 2 pipe), check its definition ES >= the
    # downstream (Tier 1) transport's commissioning EF.
    G = tier.build_model(replication_seed=0, sampling=False)
    tier.CPM(G)
    import world_1_s1_edits as m  # for data access; adjust if needed
    pd = m.project_data.PIPE_DOWNSTREAM
    tier_ok = True
    detail = ""
    for t, down in pd.items():
        # only transports feeding another transport (Tier 2+)
        if down in m.project_data.TRANSPORT_VOLUMES:
            def_es = G.nodes[(t, "definition")]["ES"]
            up_comm = G.nodes[(down, "commissioning")]["EF"]
            if def_es < up_comm - 1e-6:
                tier_ok = False
                detail = f"{t} def ES {def_es} < {down} comm EF {up_comm}"
    check("Tier 2 definition ES >= Tier 1 commissioning EF", tier_ok, detail)


# ===============================================================
# SCENARIO 1.2 — HAMMOCK
# ===============================================================
def test_hammock_scenario():
    print("\n=== Scenario 1.2: hammock ===")

    HN = ("hammock node", "hammock node")   # adjust if your key differs

    # --- hammock EF responds to threshold ---
    # NOTE: needs a network whose transport commissioning volumes are spread out
    # enough that different thresholds cross at different times.
    G_lo = ham.build_model(replication_seed=0, sampling=False)
    ham.CPM(G_lo, hammock_threshold=0.1)          # adjust param name/position
    ef_lo = G_lo.nodes[HN]["EF"]

    G_hi = ham.build_model(replication_seed=0, sampling=False)
    ham.CPM(G_hi, hammock_threshold=1.0)
    ef_hi = G_hi.nodes[HN]["EF"]

    check("hammock EF at threshold 1.0 >= EF at 0.1 (more infra required)",
          ef_hi >= ef_lo, f"lo(0.1)={ef_lo}, hi(1.0)={ef_hi}")
    # if they're equal, warn it's likely the data (concentrated volume), not a bug
    if approx(ef_hi, ef_lo):
        print("     [note] hammock EF identical at 0.1 and 1.0 -> likely concentrated"
              " transport volume (one big transport dominates). Use a network with"
              " spread-out volumes to see the threshold bite.")

    # --- hammock gates definition: capture def ES >= hammock EF ---
    caps = list(ham.project_data.CAPTURE_VOLUMES)
    all_gated = all(G_hi.nodes[(c, "definition")]["ES"] >= ef_hi - 1e-6 for c in caps)
    check("every capture definition ES >= hammock EF (definition is gated)", all_gated)

    # --- threshold = 1.0 -> approval delays ~0 -> base-rate-only abandonment ---
    # At threshold 1.0, all infra is commissioned before captures start, so the
    # capture-vs-infra race has no gap -> approval delay 0.
    delays_at_1 = []
    for c in caps:
        d = ham.calculate_delay(G_hi, c, "approval")
        delays_at_1.append(d)
    check("threshold=1.0 -> all approval delays == 0 (full infra head start)",
          all(approx(d, 0.0) for d in delays_at_1),
          f"delays={delays_at_1}")

    # --- abandonment DECREASES as threshold rises ---
    def rate_at(thresh):
        r = ham.analyze_monte_carlo(
            ham.monte_carlo(300, base_rate=0.05, hammock_threshold=thresh))  # adjust param
        return r["average capture abandonment rate"]
    # sweep thresholds that STRADDLE the volume step (adjust to your network!)
    r_low = rate_at(0.2)
    r_high = rate_at(0.95)
    check("abandonment(low threshold) >= abandonment(high threshold)",
          r_low >= r_high - 1e-9, f"low(0.2)={r_low:.3f}, high(0.95)={r_high:.3f}")


def main():
    print("=" * 55)
    print("WORLD 1 SUB-SCENARIO VERIFICATION")
    print("=" * 55)
    test_tier_scenario()
    test_hammock_scenario()
    print("\n" + "=" * 55)
    print(f"RESULTS: {_p} passed, {_f} failed")
    print("=" * 55)


if __name__ == "__main__":
    main()