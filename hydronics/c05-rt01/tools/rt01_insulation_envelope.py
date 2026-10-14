"""RT01-I: space claim of pipe insulation that C05 does not model.

The 34 OD33.7 main-loop spools carry 5 C (below bay dew point) or 82 C water,
or alternate between them, yet all 102 C05 spools are bare. Build each main
spool as a solid insulation envelope (OD + 2 x 13 mm, typical elastomeric
cold-service thickness; exact miter trims) and count conflicts against the
retained host and against other water objects (other main spools also as
envelopes, everything else bare). Compare with the bare-pipe counts.
"""
import json, sys
from rt01_common import design, jload, save_csv
from rt01_occ import load, bbox, bb_overlap, compound
from rt01_cad_elbows import build_spool, pvol, TOL_VOL

INS = 13.0


def envelope(r, extra):
    rr = dict(r); rr["OD_mm"] = r["OD_mm"] + 2 * extra; rr["ID_mm"] = 0.0
    return build_spool(rr, ["miter90_1weld"] * len(r["bend_radii"]))


if __name__ == "__main__":
    d = design(); routes = d["pipe_routes"]
    main = [e for e, r in routes.items() if r["OD_mm"] == 33.7]
    host = [h for h in jload("internal/HOST_CONTEXT.json") if h["context_retained"]]
    env = {e: envelope(routes[e], INS) for e in main}
    bare = {e: [load(f"cad/definitions/C05_SP_{e}.brep")] for e in main}
    occ = d["occurrences"]
    # objects a spool is welded to (its own end connectors / headers) are not conflicts
    from rt01_common import headers, connections
    H, C = headers(), connections()
    k = lambda p: tuple(round(x, 2) for x in p)
    own = {}
    for e in main:
        ends = {k(routes[e]["points"][0]), k(routes[e]["points"][-1])}
        o = {c["installed_id"] + sfx for c in C.values() if k(c["weld_face"]) in ends
             for sfx in ("", "_TAIL", "_NUT", "_SEAL")}
        o |= {h["id"] for h in H.values() if k(h["main_face"]) in ends or any(k(b["face"]) in ends for b in h["branch_ports"])}
        own[e] = o
    only_water = "--water-only" in sys.argv
    rows = []
    for e in main:
        for label, parts in (("bare", bare[e]), ("insulated13", env[e])):
            bb = bbox(compound(parts)); nh = vh = nw = vw = 0
            for h in ([] if only_water else host):
                if bb_overlap(bb, h["bounds"]):
                    v = pvol(parts, load(f"internal/context/{h['index']:04d}.brep"))
                    if v > TOL_VOL:
                        nh += 1; vh += v
            for o in occ:
                oid = o["id"]
                if oid == f"C05_SP_{e}" or oid in own[e]:
                    continue
                other_main = oid.startswith("C05_SP_") and oid[7:] in env
                obb = bbox(compound(env[oid[7:]])) if (label != "bare" and other_main) else o["bounds"]
                if not bb_overlap(bb, obb):
                    continue
                if label != "bare" and other_main:
                    v = sum(pvol(parts, q) for q in env[oid[7:]])
                else:
                    v = pvol(parts, load(o["world_brep"]))
                if v > TOL_VOL:
                    nw += 1; vw += v
            rows.append(dict(edge=e, case=label, host_pairs=nh, host_vol_cm3=round(vh / 1000, 2),
                             water_pairs=nw, water_vol_cm3=round(vw / 1000, 2)))
            print(rows[-1], flush=True)
    save_csv("rt01_insulation_envelope_water.csv" if only_water else "rt01_insulation_envelope.csv", rows)
