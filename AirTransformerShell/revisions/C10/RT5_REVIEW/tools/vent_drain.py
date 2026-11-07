"""Locate every H01 vent/drain feature in a C10 installed STEP and report its nearest shell/damper part.
Usage: python -I vent_drain.py <C10_INSTALLED_S1.step> <out.json>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xcaf_leaves import leaves, bbox, overlap
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
L = leaves(sys.argv[1])
F = [(p, s, bbox(s)) for p, s in L if 'HEAT_EXCHANGERS' in p.split('/') and any(k in p.split('/')[-1].upper() for k in ('VENT', 'DRAIN'))]
H = [(p, s, bbox(s)) for p, s in L if any(g in p.split('/') for g in ('SHELL', 'DAMPERS'))]
out = []
for p, s, b in F:
    best = (80.0, None)
    for q, t, c in H:
        if not overlap(b, c, g=best[0]): continue
        d = BRepExtrema_DistShapeShape(s.wrapped, t.wrapped); d.Perform()
        if d.Value() < best[0]: best = (d.Value(), q.split('/')[-1])
    f = p.split('/'); zone = 'wet bay (X<-501.5)' if b[3] < -501.5 else ('air enclosure' if b[0] > -500 else 'crosses rear wall')
    out.append({'core': f[-3], 'feature': f[-1], 'bbox': [round(x, 1) for x in b], 'zone': zone, 'nearest_host_mm': round(best[0], 2) if best[1] else '>80', 'nearest_host': best[1]})
    print(out[-1], flush=True)
json.dump(out, open(sys.argv[2], 'w'), indent=1)
