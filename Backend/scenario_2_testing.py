# test_scenario2.py
# Run from inside Backend with the venv active:  python -m models.scenario2Final_tests
# (or just paste into a scratch file next to the model and run it directly)

from models import scenario_2_final_refactored as s2

# ---------------------------------------------------------------------------
# YOUR SAVED BASELINE — fill these in from the numbers you recorded BEFORE
# refactoring (run the original monte_carlo(300) and copy the five averages).
# Until these are your real numbers, the defaults test below is not a real test.
# ---------------------------------------------------------------------------
BASELINE = {
    "storage_abandoned":   3.4,
    "transport_abandoned": 5.8,
    "capture_abandoned":   10.2,
    "completion":          129.9,
    "final_volume":        510.0,
}

N = 10          # reps — enough that averages are stable, not 10
TOL = 1e-9       # defaults should match EXACTLY (same seeds), so near-zero tolerance


def summarize(results):
    """Collapse a monte_carlo result list into the five averages we care about.
    Mirrors analyze_monte_carlo, but returns a dict so we can compare fields by name."""
    n = len(results)
    return {
        "storage_abandoned":   sum(r["supply abandoned"]    for r in results) / n,
        "transport_abandoned": sum(r["transport abandoned"] for r in results) / n,
        "capture_abandoned":   sum(r["capture abandoned"]   for r in results) / n,
        "completion":          sum(r["completion"]          for r in results) / n,
        "final_volume":        sum(r["final volume"]        for r in results) / n,
    }


def run(**overrides):
    """One Monte Carlo run with named overrides, returned as the five averages."""
    return summarize(s2.monte_carlo(N, **overrides))


# ===========================================================================
# TIER 1 — DEFAULTS MUST REPRODUCE THE BASELINE
# The refactor must not change behavior. With no overrides, every field should
# match what you recorded before any refactoring. If this fails, something in
# the rewiring changed the model — stop and trace before trusting anything else.
# ===========================================================================
def test_defaults_match_baseline():
    if any(v is None for v in BASELINE.values()):
        print("SKIP defaults test — fill in BASELINE first.\n")
        return
    got = run()  # no overrides = pure defaults
    print("TIER 1 — defaults vs baseline:")
    all_ok = True
    for field, expected in BASELINE.items():
        actual = got[field]
        ok = abs(actual - expected) <= TOL
        all_ok = all_ok and ok
        print(f"  {field:22} expected {expected:>10.4f}  got {actual:>10.4f}  {'OK' if ok else 'MISMATCH'}")
    print("  => PASS\n" if all_ok else "  => FAIL: defaults drifted; the refactor changed behavior.\n")


# ===========================================================================
# TIER 2 — EACH PARAMETER MOVES ITS OWN SIGNAL
# A passing Tier 1 only proves you didn't BREAK anything. It does NOT prove the
# parameters are live, because every default equals the old global. To prove a
# parameter actually reaches its consumer, we override it AWAY from the default
# and assert the right output field moves in the right direction.
#
# The key idea you designed: each parameter controls a DIFFERENT field.
#   base_rate / max_rate / tolerances  -> abandonment counts
#   threshold_frac                     -> cluster COLLAPSE (storage/transport) + volume
# So each test watches the field that parameter is supposed to govern.
# ===========================================================================
def test_overrides():
    base = run()  # default reference point to compare against
    print("TIER 2 — parameter override directional checks:")

    # base_rate UP -> more capture attrition. (Same logic that worked in scenario 1.)
    hi_base = run(base_rate=0.4)
    check("base_rate 0.05->0.4 raises capture_abandoned",
          hi_base["capture_abandoned"] > base["capture_abandoned"], base, hi_base, "capture_abandoned")

    # capture_tolerance DOWN -> delays cross the tolerance sooner -> more capture attrition.
    lo_tol = run(capture_tolerance=6)
    check("capture_tolerance 36->6 raises capture_abandoned",
          lo_tol["capture_abandoned"] > base["capture_abandoned"], base, lo_tol, "capture_abandoned")

    # max_rate UP -> lifts the ceiling on attrition probability -> at least not fewer abandoned.
    # (Effect only shows when some delay pushes prob to the cap, so we assert >= not >.)
    hi_max = run(max_rate=0.9)
    check("max_rate 0.4->0.9 does not reduce capture_abandoned",
          hi_max["capture_abandoned"] >= base["capture_abandoned"], base, hi_max, "capture_abandoned")

    # threshold_frac UP -> gates need more committed volume -> MORE cluster collapse.
    # Watch storage/transport abandoned (the cascade), NOT capture attrition.
    hi_thr = run(threshold_frac=0.9)
    check("threshold_frac 0.5->0.9 raises transport_abandoned",
          hi_thr["transport_abandoned"] > base["transport_abandoned"], base, hi_thr, "transport_abandoned")

    # threshold_frac DOWN -> gates clear easily -> LESS collapse, MORE final volume.
    lo_thr = run(threshold_frac=0.1)
    check("threshold_frac 0.5->0.1 raises final_volume",
          lo_thr["final_volume"] > base["final_volume"], base, lo_thr, "final_volume")


def check(label, condition, base, got, field):
    """Print a directional assertion with the before/after numbers so a failure is legible."""
    arrow = f"(default {base[field]:.3f} -> override {got[field]:.3f})"
    print(f"  {'OK  ' if condition else 'FAIL'}  {label}  {arrow}")


if __name__ == "__main__":
    test_defaults_match_baseline()
    test_overrides()