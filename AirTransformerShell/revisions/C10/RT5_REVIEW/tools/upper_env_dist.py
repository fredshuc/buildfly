"""Minimum distance from the D03 UPPER motion envelopes to C09-installed HX members other than fins/tubes.
Usage: python -I upper_env_dist.py <C09_INSTALLED_S1.step> <D03_MOTION_AND_SERVICE.step> <out.json>"""
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xcaf_leaves import leaves, bbox, overlap
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
HX = [(p, s, bbox(s)) for p, s in leaves(sys.argv[1]) if 'HEAT_EXCHANGERS' in p.split('/')
      and not any(k in p.split('/')[-1].upper() for k in ('FIN', 'TUBE'))]
env = collections.defaultdict(list)
for p, s in leaves(sys.argv[2]):
    f = p.split('/')
    if len(f) > 2 and f[2].endswith('UPPER_MOTION'): env[f[2]].append((f[-1], s))
out = {}
for k, items in env.items():
    best = (25.0, None)
    for n, s in items:
        b = bbox(s)
        for p, h, hb in HX:
            if not overlap(b, hb, g=best[0]): continue
            d = BRepExtrema_DistShapeShape(s.wrapped, h.wrapped); d.Perform()
            if d.Value() < best[0]:
                q1, q2 = d.PointOnShape1(1), d.PointOnShape2(1)
                best = (d.Value(), [n, '/'.join(p.split('/')[-2:]), [round(q1.X(), 3), round(q1.Y(), 3), round(q1.Z(), 3)], [round(q2.X(), 3), round(q2.Y(), 3), round(q2.Z(), 3)]])
    out[k] = {'min_mm': round(best[0], 4), 'detail': best[1], 'hx_members_screened': len(HX)}
    print(k, out[k], flush=True)
json.dump(out, open(sys.argv[3], 'w'), indent=1)
