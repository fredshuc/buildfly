"""Ray-cast the C09 shell at bed-A centre (Y=-425) for the plenum depth profiles.
Usage: python -I plenum_profile.py <C09_SHELL.step> <out.json>
Top plenum depth  = first shell hit above Z1175 (upper HX envelope top) minus 1175.
Bottom plenum depth = 620 (lower HX frame datum) minus first shell hit below Z620."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xcaf_leaves import leaves, bbox
import cadquery as cq
Y = -425.0
L = [(p, s) for p, s in leaves(sys.argv[1]) if bbox(s)[1] <= Y <= bbox(s)[4]]
def hits(x, z0, z1):
    e = cq.Edge.makeLine(cq.Vector(x, Y, z0), cq.Vector(x, Y, z1)); out = []
    for p, s in L:
        b = bbox(s)
        if not (b[0] <= x <= b[3]) or max(z0, z1) < b[2] or min(z0, z1) > b[5]: continue
        try:
            for v in e.intersect(s).Vertices(): out.append((v.Z, p.split('/')[-1]))
        except Exception: pass
        try:
            sec = s.intersect(cq.Solid.makeBox(0.2, 0.2, abs(z1 - z0), cq.Vector(x - 0.1, Y - 0.1, min(z0, z1))))
            if sec.Volume() > 1e-6: bz = bbox(sec); out.append((bz[2] if z1 > z0 else bz[5], p.split('/')[-1]))
        except Exception: pass
    return out
rows = []
for x in range(-410, 600, 20):
    up = hits(x, 1175.0, 1540.0); dn = hits(x, 620.0, 0.0)
    top = min(up) if up else (None, None); bot = max(dn) if dn else (None, None)
    rows.append({'X': x, 'roof_Z': round(top[0], 2) if top[0] else None, 'roof_part': top[1], 'top_depth_mm': round(top[0] - 1175, 2) if top[0] else None,
                 'floor_Z': round(bot[0], 2) if bot[0] else None, 'floor_part': bot[1], 'bottom_depth_mm': round(620 - bot[0], 2) if bot[0] else None})
    print(rows[-1], flush=True)
json.dump(rows, open(sys.argv[2], 'w'), indent=1)
