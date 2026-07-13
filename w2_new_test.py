"""
Checks for two W2 behaviors:
  (A) roll ONCE per joint predecessor (child pipe = one transport-unit, not N captures)
  (B) late-arriving projects still count in downstream volume thresholds
Plus CPM invariants.
"""
import world_2 as s2

# ---- PASTE YOUR DUMMY TREE HERE ----
PIPE_DOWNSTREAM = {"projT2":"projT1", "projT3":"projT1", "projT1":"projS1"}
CAPTURE_PIPE = {"projC1":"projT2","projC2":"projT2","projC3":"projT1","projC4":"projT3"}
TRUNKS = ["projT1"]
CAPTURE_VOLUMES = {"projC1":1.5,"projC2":1.5,"projC3":2.0,"projC4":1.5}
TRANSPORT_VOLUMES = {"projT1":8,"projT2":4,"projT3":2}
STORAGE_VOLUMES = {"projS1":10}
CAPTURE = {c:{"definition":5,"approval":10,"construction":10} for c in CAPTURE_VOLUMES}
TRANSPORT = {t:{"definition":6,"approval":15,"construction":15} for t in TRANSPORT_VOLUMES}
STORAGE = {"projS1":{"definition":10,"approval":24,"construction":20}}
DATA = dict(trunks=TRUNKS, pipe_downstream=PIPE_DOWNSTREAM, capture_pipe=CAPTURE_PIPE,
            capture_durations=CAPTURE, capture_volumes=CAPTURE_VOLUMES,
            storage_durations=STORAGE, storage_volumes=STORAGE_VOLUMES,
            transport_durations=TRANSPORT, transport_volumes=TRANSPORT_VOLUMES)
# ---- confirm these function names match your world_2.py ----
# buildmodel, CPM, cluster_naming, joint_naming, gather_input_specs,
# cluster_owner, get_tech, immediate_upstream_project

_p = _f = 0
def chk(name, ok, detail=""):
    global _p, _f
    _p += ok; _f += (not ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}   {detail}")

# ---------- (B) late volume still counts ----------
def check_late_volume():
    print("\n[B] late volume counts in committed_volume")
    G = s2.buildmodel(replication_seed=0, sampling=False, **DATA)
    s2.CPM(G, threshold_frac=0.5)
    for pipe in TRANSPORT_VOLUMES:
        fid = (s2.cluster_naming(pipe), s2.joint_naming("approval"))
        if fid not in G.nodes: continue
        committed = G.nodes[fid].get("committed_volume", 0.0)
        arrivals = s2.gather_input_specs(G, fid)
        expected = sum(v for v, t in arrivals)
        chk(f"{pipe} FID committed == sum of ALL arrivals",
            abs(committed - expected) < 1e-6,
            f"committed={committed:.4f} expected={expected:.4f}")

    # force one capture very late, confirm its volume still gathered
    G2 = s2.buildmodel(replication_seed=0, sampling=False, **DATA)
    late = list(CAPTURE_VOLUMES)[0]
    G2.nodes[(late, "approval")]["duration"] = 999
    s2.CPM(G2, threshold_frac=0.5)
    fid = (s2.cluster_naming(CAPTURE_PIPE[late]), s2.joint_naming("approval"))
    arrivals = s2.gather_input_specs(G2, fid)
    chk(f"late capture {late} volume still gathered",
        any(abs(v - CAPTURE_VOLUMES[late]) < 1e-6 for v, t in arrivals))

# ---------- (A) one roll per predecessor, child pipe = one unit ----------
def check_roll_units():
    print("\n[A] child pipe = one predecessor unit at trunk joint")
    G = s2.buildmodel(replication_seed=0, sampling=False, **DATA)
    s2.CPM(G, threshold_frac=0.5)
    trunk = TRUNKS[0]
    fid = (s2.cluster_naming(trunk), s2.joint_naming("approval"))
    preds = list(G.predecessors(fid))
    child_joints = [p for p in preds if G.nodes[p].get("tech") == "joint"]
    caps = [p for p in preds if G.nodes[p].get("tech") == "capture"]
    _, child_pipes = s2.immediate_upstream_project(trunk)
    print(f"     trunk FID preds: {len(caps)} captures + {len(child_joints)} child joints")
    chk("each child pipe = exactly one predecessor unit",
        len(child_joints) == len(child_pipes),
        f"child_joints={len(child_joints)} child_pipes={len(child_pipes)}")

# ---------- (A2) child joint owner reads as transport ----------
def check_child_as_transport():
    print("\n[A2] child joint recovered to a transport-tech owner")
    G = s2.buildmodel(replication_seed=0, sampling=False, **DATA)
    s2.CPM(G, threshold_frac=0.5)
    trunk = TRUNKS[0]
    fid = (s2.cluster_naming(trunk), s2.joint_naming("approval"))
    for p in G.predecessors(fid):
        if G.nodes[p].get("tech") == "joint":
            owner = s2.cluster_owner(p)
            chk(f"child joint {p[0]} -> owner {owner} tech == transport",
                s2.get_tech(G, owner) == "transport",
                f"tech={s2.get_tech(G, owner)}")

# ---------- CPM invariant ----------
def check_cpm():
    print("\n[CPM] ES >= latest non-abandoned predecessor EF")
    G = s2.buildmodel(replication_seed=0, sampling=False, **DATA)
    s2.CPM(G, threshold_frac=0.5)
    ok = True
    for n in G.nodes:
        if G.nodes[n].get("tech") == "joint": continue
        preds = [p for p in G.predecessors(n) if G.nodes[p].get("abandoned") is None]
        if not preds: continue
        if G.nodes[n]["ES"] + 1e-6 < max(G.nodes[p]["EF"] for p in preds):
            ok = False
    chk("every node ES >= latest predecessor EF", ok)

if __name__ == "__main__":
    check_late_volume()
    check_roll_units()
    check_child_as_transport()
    check_cpm()
    print(f"\n{_p} passed, {_f} failed")