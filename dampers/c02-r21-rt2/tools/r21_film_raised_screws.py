"""RT2-06 follow-up: with a 0.8 mm keeper under the end STD08B heads, the heads rise 0.8 mm along the film normal.
Check every raised end screw (those the keeper candidate touches, from r21_film_keeper.py output) against every moving
R12 body over rotor angles 0..90 deg (2.5 deg steps plus 0.1 and 89.9). Both normal senses are tested (conservative).
Distances are evaluated only for bodies whose bounding boxes come within MARGIN mm; otherwise the gap is reported as >MARGIN.
Usage: python -I r21_film_raised_screws.py <native dir> <r21_film_keeper.json>   (adds key 'raised_end_screws')"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from native import bbox, common_vol, dist, overlap_bb
from OCP.gp import gp_Trsf, gp_Vec
from OCP.TopLoc import TopLoc_Location
import importlib.util
NAT, KJ = sys.argv[1], sys.argv[2]
MARGIN, RISE = 5.0, 0.8
spec = importlib.util.spec_from_file_location('c', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'r21_common.py'))
H = importlib.util.module_from_spec(spec); spec.loader.exec_module(H)
H.init(NAT)
res = json.load(open(KJ))
angles = sorted(set([0.1, 89.9] + [i * 2.5 for i in range(37)]))
def grow(b, m): return (b[0] - m, b[1] - m, b[2] - m, b[3] + m, b[4] + m, b[5] + m)
raised = {}
for cfg, film in [('P', 'P109'), ('R', 'R109')]:
    O = json.load(open(f"{NAT}/R20_{cfg}_OCCURRENCES.json"))
    hit_screws = sorted({h['body'] for r in res[cfg]['keeper_checks'] for h in r['hits'] if h['pn'] == 'STD08B'})
    films = [o for o in O if o['pn'] == film]
    movers = [o for o in O if o['source'] == 'R12' and o.get('moving')]
    rows = []
    for sc in hit_screws:
        so = next(o for o in O if o['occurrence'] == sc)
        b0 = bbox(H.place(so)); c = [(b0[i] + b0[i + 3]) / 2 for i in range(3)]
        n = min(films, key=lambda o: sum((o['o'][i] - c[i]) ** 2 for i in range(3)))['n']
        variants = []
        for sgn in (1, -1):
            t = gp_Trsf(); t.SetTranslation(gp_Vec(sgn * RISE * n[0], sgn * RISE * n[1], sgn * RISE * n[2]))
            rs = H.local(so['pn']).Moved(TopLoc_Location(t.Multiplied(H.trsf(so)))); variants.append((rs, bbox(rs)))
        mind, hits, near = math.inf, 0, None
        for ang in angles:
            for o in movers:
                s = H.place(o, ang); bs = bbox(s)
                for rs, br in variants:
                    if not overlap_bb(grow(br, MARGIN), bs): continue
                    if overlap_bb(br, bs) and common_vol(rs, s) > 1e-3: hits += 1
                    d = dist(rs, s)
                    if d < mind: mind, near = d, dict(body=o['occurrence'], pn=o['pn'], angle=ang)
        rows.append(dict(screw=sc, min_gap_mm=(round(mind, 3) if mind < math.inf else f'>{MARGIN}'), nearest=near, overlaps=hits))
    raised[cfg] = rows
    print(cfg, rows)
res['raised_end_screws'] = dict(rise_mm=RISE, angles=angles, margin_mm=MARGIN, rows=raised)
json.dump(res, open(KJ, 'w'), indent=1)
