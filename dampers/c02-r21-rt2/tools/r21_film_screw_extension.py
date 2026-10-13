"""RT2-06 follow-up: if the end STD08B screws are lengthened by EXT mm (to restore >= 2 pitches after a 0.8 mm keeper),
the tip grows from local z=16 to 16+EXT-0.8 beyond its current position (head raised 0.8). Checks the added tip cylinder
(d=3, local z 16..16+EXT-0.8 measured from the current head datum, i.e. world tip moves EXT-0.8 mm further) against all
bodies of the configuration (static at 0 deg; moving over 0..90 deg in 5 deg steps).
Usage: python -I r21_film_screw_extension.py <native dir> <r21_film_keeper.json> <out.json> [EXT=2.0]"""
import sys, os, json, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from native import bbox, common_vol, overlap_bb, dist
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCP.gp import gp_Ax2, gp_Pnt, gp_Dir
from OCP.TopLoc import TopLoc_Location
spec = importlib.util.spec_from_file_location('c', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'r21_common.py'))
H = importlib.util.module_from_spec(spec); spec.loader.exec_module(H)
NAT, KJ, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; EXT = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0
H.init(NAT); K = json.load(open(KJ)); RISE = 0.8
def grow(b, m): return (b[0] - m, b[1] - m, b[2] - m, b[3] + m, b[4] + m, b[5] + m)
out = dict(ext_mm=EXT, rise_mm=RISE, rows={})
for cfg in 'PR':
    O = json.load(open(f"{NAT}/R20_{cfg}_OCCURRENCES.json")); occ = {o['occurrence']: o for o in O}
    screws = sorted({h['body'] for r in K[cfg]['keeper_checks'] for h in r['hits'] if h['pn'] == 'STD08B'})
    rows = []
    for sc in screws:
        so = occ[sc]
        cyl = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, 0, 16.0), gp_Dir(0, 0, 1)), 1.5, EXT - RISE).Shape()
        tip = cyl.Moved(TopLoc_Location(H.trsf(so))); bt = bbox(tip)
        hits, near = [], (1e9, None)
        for o in O:
            if o['occurrence'] == sc: continue
            grp = o.get('moving') if o['source'] == 'R12' else None
            for ang in (range(0, 91, 5) if grp else [0]):
                s = H.place(o, ang); bs = bbox(s)
                if not overlap_bb(grow(bt, 3.0), bs): continue
                d = dist(tip, s)
                if d < near[0]: near = (d, o['occurrence'])
                if overlap_bb(bt, bs):
                    v = common_vol(tip, s)
                    if v > 1e-3: hits.append(dict(body=o['occurrence'], pn=o['pn'], angle=ang, mm3=round(v, 3)))
        rows.append(dict(screw=sc, hits=hits, min_gap_mm=round(near[0], 3) if near[1] else '>3', nearest=near[1]))
        print(cfg, rows[-1])
    out['rows'][cfg] = rows
json.dump(out, open(OUT, 'w'), indent=1)
