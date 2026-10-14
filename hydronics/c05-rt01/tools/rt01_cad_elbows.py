"""RT01-CAD: build the 30 OD33.7 spools with the elbow assignment from
rt01_elbow_fit.json (end points, connectors, headers and valves unchanged), and
clash-check original vs revised spool against (a) the 2,810 retained host BReps
and (b) every other C05 physical occurrence. Writes revised world BReps and one
AP242 STEP of the revised spools to results/cad/.
Single-cut miters that are kept are built exactly (bisector-plane trimmed legs).
"""
import math, json, sys, time
from pathlib import Path
from OCP.BRepTools import BRepTools
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeHalfSpace, BRepPrimAPI_MakeBox
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCP.gp import gp_Pln, gp_Pnt, gp_Dir
from rt01_common import design, jload, OUT, save_csv, save_json
from rt01_occ import load, bbox, volume, common_vol, bb_overlap, compound, tube, torus_elbow, write_step, mc_symdiff
from rt01_elbow_fit import CTE

TOL_VOL = 1.0     # mm3; below this a common volume is reported as touching


def halfspace(p, n):
    """Solid half-space {x : (x-p).n <= 0}."""
    face = BRepBuilderAPI_MakeFace(gp_Pln(gp_Pnt(*p), gp_Dir(*n))).Face()
    ref = [p[i] - 10 * n[i] for i in range(3)]
    return BRepPrimAPI_MakeHalfSpace(face, gp_Pnt(*ref)).Solid()


def trim(shape, p, n):
    op = BRepAlgoAPI_Common(shape, halfspace(p, n)); op.Build(); return op.Shape()


def build_spool(r, kinds):
    P = r["points"]; ro, ri = r["OD_mm"] / 2, r["ID_mm"] / 2
    u = []
    for a, b in zip(P, P[1:]):
        L = math.dist(a, b); u.append([(y - x) / L for x, y in zip(a, b)])
    R = [CTE[k] for k in kinds]
    parts = []
    # straights
    for i in range(len(P) - 1):
        s, e = list(P[i]), list(P[i + 1])
        L = math.dist(s, e)
        s_off = R[i - 1] if i > 0 else 0.0
        e_off = R[i] if i < len(P) - 2 else 0.0
        ext_s = ro if (i > 0 and R[i - 1] == 0) else 0.0
        ext_e = ro if (i < len(P) - 2 and R[i] == 0) else 0.0
        start = [s[j] + u[i][j] * (s_off - ext_s) for j in range(3)]
        length = L - s_off - e_off + ext_s + ext_e
        if length > 1e-6:
            leg = tube(start, u[i], length, ro, ri)
            if ext_s:      # incoming miter at corner i-1: keep (x-P).(a+b) >= 0
                n = [-(u[i - 1][j] + u[i][j]) for j in range(3)]; leg = trim(leg, P[i], n)
            if ext_e:      # outgoing miter at corner i: keep (x-P).(a+b) <= 0
                n = [u[i][j] + u[i + 1][j] for j in range(3)]; leg = trim(leg, P[i + 1], n)
            parts.append(leg)
    # elbows
    for i, Rk in enumerate(R):
        if Rk > 0:
            a, b, c = u[i], u[i + 1], P[i + 1]
            ctr = [c[j] - Rk * a[j] + Rk * b[j] for j in range(3)]
            parts.append(torus_elbow(ctr, a, b, Rk, ro, ri))
    return parts


def pvol(parts, other):
    """Common volume of a list of non-overlapping solids with one shape (summed per solid)."""
    return sum(common_vol(p, other) for p in parts if bb_overlap(bbox(p), bbox(other)))


def clashes(parts, own_id, host_idx, others):
    bb = bbox(compound(parts)); hits = []
    for h in host_idx:
        if bb_overlap(bb, h["bounds"]):
            v = pvol(parts, load(f"internal/context/{h['index']:04d}.brep"))
            if v > TOL_VOL:
                hits.append(("HOST", h["index"], h["name"], h["group"], round(v, 1)))
    for o in others:
        if o["id"] != own_id and bb_overlap(bb, o["bounds"]):
            v = pvol(parts, load(o["world_brep"]))
            if v > TOL_VOL:
                hits.append(("C05", o["id"], o["kind"], "", round(v, 1)))
    return hits


if __name__ == "__main__":
    d = design(); routes = d["pipe_routes"]
    fit = json.loads((OUT / "rt01_elbow_fit.json").read_text())
    host = [h for h in jload("internal/HOST_CONTEXT.json") if h["context_retained"]]
    others = [o for o in d["occurrences"]]
    cad = OUT / "cad"; cad.mkdir(parents=True, exist_ok=True)
    rows, named = [], []
    only = set(sys.argv[1:])
    for eid, kinds in fit.items():
        if only and eid not in only:
            continue
        t0 = time.time()
        r = routes[eid]
        new = build_spool(r, kinds)
        old = load(f"cad/definitions/C05_SP_{eid}.brep")
        # self-check: rebuilding with all miters must reproduce the delivered solid
        allm = build_spool(r, ["miter90_1weld"] * len(kinds))
        vo, va, vn = volume(old), sum(map(volume, allm)), sum(map(volume, new))
        sym, va_mc = mc_symdiff([old], allm)
        ho = clashes([old], f"C05_SP_{eid}", host, others)
        hn = clashes(new, f"C05_SP_{eid}", host, others)
        ko = {(h[0], h[1]) for h in ho}; kn = {(h[0], h[1]) for h in hn}
        BRepTools.Write_s(compound(new), str(cad / f"RT01_SP_{eid}_ELBOWS.brep"))
        named.append((eid, compound(new)))
        rows.append(dict(edge=eid, fittings=" ".join({"elbow90_LR": "LR", "elbow90_SR_welded": "SR", "miter90_1weld": "M"}[k] for k in kinds),
                         vol_delivered_mm3=round(vo, 1), vol_rebuilt_all_miter_mm3=round(va, 1),
                         rebuild_symdiff_MC_mm3=round(sym, 0), rebuild_vol_MC_mm3=round(va_mc, 0), vol_revised_mm3=round(vn, 1),
                         clashes_delivered=len(ho), clash_vol_delivered_mm3=round(sum(h[4] for h in ho), 1),
                         clashes_revised=len(hn), clash_vol_revised_mm3=round(sum(h[4] for h in hn), 1),
                         removed=";".join(f"{a}:{b}" for a, b in sorted(ko - kn, key=str)),
                         added=";".join(f"{h[0]}:{h[1]}:{h[2]}:{h[4]}" for h in hn if (h[0], h[1]) not in ko),
                         sec=round(time.time() - t0, 1)))
        print(rows[-1], flush=True)
    if not only:
        save_csv("rt01_cad_elbows_clash.csv", rows)
        print("STEP write:", write_step(named, cad / "RT01_REVISED_DN25_SPOOLS_AP242.step"))
