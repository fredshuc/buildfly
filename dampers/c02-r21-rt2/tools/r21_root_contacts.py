"""RT2-07: contact graph of the feedback/equaliser root (A703*, A704R8, A705-A710, B850-B853, HW_R11_GUIDE_M5) in the
P and R native configurations at 0 deg. For each occurrence: neighbours within GAP mm (distance) and any overlap volume.
Usage: python -I r21_root_contacts.py <native dir> <out.json>"""
import sys, os, json, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from native import bbox, common_vol, dist, overlap_bb
spec = importlib.util.spec_from_file_location('c', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'r21_common.py'))
H = importlib.util.module_from_spec(spec); spec.loader.exec_module(H)
NAT, OUT = sys.argv[1], sys.argv[2]; H.init(NAT)
ROOT = {'A703P', 'A703R', 'A704R8', 'A705', 'A706', 'A707', 'A710', 'B850', 'B851', 'B852', 'B853', 'HW_R11_GUIDE_M5'}
GAP = 0.10
def grow(b, m): return (b[0] - m, b[1] - m, b[2] - m, b[3] + m, b[4] + m, b[5] + m)
res = {}
for cfg in 'PR':
    O = json.load(open(f"{NAT}/R20_{cfg}_OCCURRENCES.json"))
    shapes = {o['occurrence']: H.place(o) for o in O}
    bbs = {k: bbox(s) for k, s in shapes.items()}
    pn = {o['occurrence']: o['pn'] for o in O}
    rows = []
    for o in O:
        if o['pn'] not in ROOT: continue
        a = o['occurrence']; nb = []
        for b, s in shapes.items():
            if b == a or not overlap_bb(grow(bbs[a], GAP), bbs[b]): continue
            d = dist(shapes[a], s)
            if d <= GAP:
                v = common_vol(shapes[a], s) if overlap_bb(bbs[a], bbs[b]) else 0.0
                nb.append(dict(body=b, pn=pn[b], gap_mm=round(d, 4), overlap_mm3=round(v, 3)))
        rows.append(dict(occurrence=a, pn=o['pn'], neighbours=nb))
    res[cfg] = rows
    for r in rows: print(cfg, r['pn'], r['occurrence'], sorted({(n['pn'], n['gap_mm'] > 1e-6, n['overlap_mm3'] > 0) for n in r['neighbours']}))
json.dump(res, open(OUT, 'w'), indent=1)
