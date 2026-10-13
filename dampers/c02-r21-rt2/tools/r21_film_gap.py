"""Sanity/reference: minimum distance from each film (P109/R109) and from the keeper candidates to any moving R12 body over
rotor angles 0..90 deg (5 deg steps). Confirms the moving set actually approaches the film so a '>margin' result is meaningful.
Usage: python -I r21_film_gap.py <native dir> <r21_film_keeper.json>   (adds key 'film_gap_to_moving')"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from native import bbox, box, dist
from OCP.TopLoc import TopLoc_Location
import importlib.util
NAT, KJ = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location('c', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'r21_common.py'))
H = importlib.util.module_from_spec(spec); spec.loader.exec_module(H); H.init(NAT)
res = json.load(open(KJ)); out = {}
for cfg, film in [('P', 'P109'), ('R', 'R109')]:
    O = json.load(open(f"{NAT}/R20_{cfg}_OCCURRENCES.json"))
    fb = bbox(H.local(film)); L, t = fb[4], fb[5] - fb[2]
    keepers = [box(0, 0, t, 46.774, 7.0, t + 0.8), box(0, L - 7.0, t, 46.774, L, t + 0.8)]
    movers = [o for o in O if o['source'] == 'R12' and o.get('moving')]
    rows = []
    for fo in (o for o in O if o['pn'] == film):
        g = H.trsf(fo); fs = H.place(fo); ks = [k.Moved(TopLoc_Location(g)) for k in keepers]
        best_f, best_k = (math.inf, None), (math.inf, None)
        for ang in range(0, 91, 5):
            for o in movers:
                s = H.place(o, ang)
                d = dist(fs, s)
                if d < best_f[0]: best_f = (d, dict(body=o['occurrence'], pn=o['pn'], angle=ang))
                for k in ks:
                    d = dist(k, s)
                    if d < best_k[0]: best_k = (d, dict(body=o['occurrence'], pn=o['pn'], angle=ang))
        rows.append(dict(film=fo['occurrence'], film_min_gap_mm=round(best_f[0], 3), film_nearest=best_f[1],
                         keeper_min_gap_mm=round(best_k[0], 3), keeper_nearest=best_k[1]))
    out[cfg] = rows; print(cfg, rows)
res['film_gap_to_moving'] = out
json.dump(res, open(KJ, 'w'), indent=1)
