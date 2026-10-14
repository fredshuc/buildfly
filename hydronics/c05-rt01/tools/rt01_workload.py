"""RT01-W: reconcile C05 workload/BOM claims from the native design.
Checks centre-line lengths, miter count, terminal/joint classes, header branch
geometry (stub length, pitch, weld-to-weld distance), water volume and 316L mass.
"""
import math, collections
from rt01_common import design, headers, connections, rows, save_json, dot, sub

if __name__ == "__main__":
    d = design(); R = d["pipe_routes"]; H = headers(); C = connections()
    L = collections.defaultdict(float)
    for r in R.values():
        L[r["OD_mm"]] += r["developed_mm"] / 1000
    corners = sum(len(r["bend_radii"]) for r in R.values())
    water = sum(r["developed_mm"] * math.pi * (r["ID_mm"] / 2) ** 2 / 1e6 for r in R.values())
    steel = sum(r["developed_mm"] * math.pi / 4 * (r["OD_mm"] ** 2 - r["ID_mm"] ** 2) for r in R.values()) * 8.0e-6
    # pipe ends: classify what each end meets
    weld_faces = {tuple(round(x, 3) for x in c["weld_face"]) for c in C.values()}
    hdr_faces = set()
    for h in H.values():
        hdr_faces.add(tuple(round(x, 3) for x in h["main_face"]))
        for b in h["branch_ports"]:
            hdr_faces.add(tuple(round(x, 3) for x in b["face"]))
    ends = collections.Counter()
    for r in R.values():
        for p in (r["points"][0], r["points"][-1]):
            k = tuple(round(x, 3) for x in p)
            ends["connector_weld_face" if k in weld_faces else "header_face" if k in hdr_faces else "other_commodity_or_undefined"] += 1
    branches = sum(len(h["branch_ports"]) for h in H.values())
    caps = sum(1 for h in H.values() if "cap" in h["root_interface"].lower())
    roots_conn = sum(1 for h in H.values() if h["root_interface"].startswith("C05_CONN"))
    # header branch geometry
    stub, pitch, toe = [], [], []
    for h in H.values():
        ro = h["OD_mm"] / 2
        xs = sorted(dot(sub(b["center"], h["start"]), h["axis"]) for b in h["branch_ports"])
        for b in h["branch_ports"]:
            reach = math.dist(b["face"], b["center"])
            stub.append(reach - ro)
            rb = b["OD"] / 2
            flank = reach - math.sqrt(max(ro ** 2 - rb ** 2, 0))
            toe.append(reach - ro)
        pitch += [b - a for a, b in zip(xs, xs[1:])]
    out = dict(centreline_m={str(k): round(v, 4) for k, v in L.items()}, total_m=round(sum(L.values()), 4),
               corners=corners, pipe_ends=dict(ends), header_branches=branches, header_caps=caps,
               header_roots_to_connectors=roots_conn, headers=len(H),
               joint_subtotal_C05_definition=corners + ends["connector_weld_face"] + ends["header_face"] + branches + roots_conn + caps,
               pipe_water_l=round(water, 3), pipe_316L_kg=round(steel, 2),
               header_branch_stub_from_OD_mm=dict(min=round(min(stub), 2), max=round(max(stub), 2)),
               header_branch_pitch_mm=dict(min=round(min(pitch), 1), max=round(max(pitch), 1)),
               branch_clear_gap_between_adjacent_OD21_mm=round(min(pitch) - 21.3, 1))
    for k, v in out.items():
        print(k, v)
    save_json("rt01_workload.json", out)
