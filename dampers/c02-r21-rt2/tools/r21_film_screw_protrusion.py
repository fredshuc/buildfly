"""RT2-06 follow-up: thread protrusion of the film end screws (STD08B) beyond their nut, before and after a 0.8 mm keeper.
For each end screw touched by the keeper candidate, projects screw and the nearest nut (HW_N3, else any nut on the axis)
onto the screw axis n and reports protrusion = screw tip - nut far face. F06 requires >= 2 full pitches (M3: 1.0 mm).
Usage: python -I r21_film_screw_protrusion.py <native dir> <r21_film_keeper.json> <out.json>"""
import sys, os, json, math, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from native import bbox
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
from OCP.gp import gp_Trsf, gp_Vec, gp_Ax3, gp_Pnt, gp_Dir
from OCP.TopLoc import TopLoc_Location
spec = importlib.util.spec_from_file_location('c', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'r21_common.py'))
H = importlib.util.module_from_spec(spec); spec.loader.exec_module(H)
NAT, KJ, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; H.init(NAT)
K = json.load(open(KJ)); RISE, PITCH = 0.8, 0.5
def axial_range(shape, o, n):
    # bounding range of the shape projected on axis n through point o: transform into a frame whose Z is n
    t = gp_Trsf(); t.SetTransformation(gp_Ax3(gp_Pnt(*o), gp_Dir(*n)))
    s = shape.Moved(TopLoc_Location(t)); b = bbox(s); return b[2], b[5]
out = {}
for cfg in 'PR':
    O = json.load(open(f"{NAT}/R20_{cfg}_OCCURRENCES.json")); occ = {o['occurrence']: o for o in O}
    screws = sorted({h['body'] for r in K[cfg]['keeper_checks'] for h in r['hits'] if h['pn'] == 'STD08B'})
    nuts = [o for o in O if o['pn'] in ('HW_N3',)]
    rows = []
    for sc in screws:
        so = occ[sc]; n = so['n']; p = so['o']
        sh = H.place(so); z0, z1 = axial_range(sh, p, n)
        # nearest nut whose centre lies on the screw axis (radial offset < 0.5 mm)
        best = None
        for nu in nuts:
            c = nu['o']; d = [c[i] - p[i] for i in range(3)]; ax = sum(d[i] * n[i] for i in range(3))
            rad = math.sqrt(max(0.0, sum(x * x for x in d) - ax * ax))
            if rad < 0.5 and (best is None or abs(ax) < abs(best[1])): best = (nu, ax)
        if best is None: rows.append(dict(screw=sc, nut=None)); continue
        nz0, nz1 = axial_range(H.place(best[0]), p, n)
        # screw tip is the end of the screw range farther from its head; head is at the local origin side
        tip = z1 if abs(z1) > abs(z0) else z0; sgn = 1 if tip > 0 else -1
        nut_far = nz1 if sgn > 0 else nz0
        prot = (tip - nut_far) * sgn
        rows.append(dict(screw=sc, nut=best[0]['occurrence'], screw_axial_range=[round(z0, 3), round(z1, 3)],
                         nut_axial_range=[round(nz0, 3), round(nz1, 3)], protrusion_mm=round(prot, 3),
                         protrusion_after_keeper_mm=round(prot - RISE, 3), pitches_after=round((prot - RISE) / PITCH, 2)))
    out[cfg] = rows
    for r in rows: print(cfg, r)
json.dump(out, open(OUT, 'w'), indent=1)
