"""RT2-06: film (P109/R109) end retention. (1) unbacked film area in the end strips relative to the U-frame shadow;
(2) a candidate end keeper (304 strip, film-local X0..46.774, Y0..7 and Y(L-7)..L, Z0.25..1.05, clamped by the existing
end M3 screw) checked against every body in the P and R configurations over rotor angles 0..90 deg (5 deg steps).
Bodies already at the end-screw stack (M3 screw/washer/nut at film-local (20, 2.5)) are reported separately.
Usage: python -I r21_film_keeper.py <native dir> <out.json>"""
import sys, os, json, math, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from native import bbox, volume, common_vol, box, dist, overlap_bb
from OCP.TopoDS import TopoDS_Shape
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Builder
from OCP.gp import gp_Trsf, gp_Ax1, gp_Pnt, gp_Dir, gp_Vec
from OCP.TopLoc import TopLoc_Location
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Common
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
NAT, OUT = sys.argv[1], sys.argv[2]
PARTS = {p['pn']: p for p in json.load(open(f"{NAT}/R20_PARTS.json"))}
AX = {'P1': (83.0, 1583.0), 'P2': (-82.0, 1583.0), 'R1': (-82.0, 1583.0)}
cache = {}
def local(pn):
    if pn not in cache:
        s = TopoDS_Shape(); BRepTools.Read_s(s, io.BytesIO(PARTS[pn]['brep'].encode()), BRep_Builder()); cache[pn] = s
    return cache[pn]
def trsf(o):
    u, v, n, p = o['u'], o['v'], o['n'], o['o']; g = gp_Trsf()
    g.SetValues(u[0], v[0], n[0], p[0], u[1], v[1], n[1], p[1], u[2], v[2], n[2], p[2]); return g
def rot(key, ang):
    x, z = AX[key]; a = ang * (-1 if key == 'P2' else 1); t = gp_Trsf()
    t.SetRotation(gp_Ax1(gp_Pnt(x, 0, z), gp_Dir(0, -1, 0)), math.radians(a)); return t
res = {}
for cfg, film, frame in [('P', 'P109', 'P110'), ('R', 'R109', 'R110')]:
    O = json.load(open(f"{NAT}/R20_{cfg}_OCCURRENCES.json"))
    L = PARTS[film]['features'][0]['height'] if isinstance(PARTS[film]['features'], list) else None
    fb = bbox(local(film)); L = fb[4]
    f = local(film); fr = local(frame)
    # film-local frame shadow: frame shape extruded through film thickness band
    t_film = fb[5] - fb[2]
    tt = gp_Trsf(); tt.SetTranslation(gp_Vec(0, 0, -0.375)); sh = fr.Moved(TopLoc_Location(tt))  # frame (1 mm) shifted to straddle film band 0..0.25 = its XY shadow
    def area(s, y0, y1):
        return common_vol(s, box(-5, y0, -0.01, 100, y1, t_film + 0.01)) / t_film
    strips = {}
    for y0, y1 in [(0, 5), (L - 5, L)]:
        fs = box(-5, y0, -0.01, 100, y1, t_film + 0.01)
        op = BRepAlgoAPI_Common(f, fs); op.Build(); fstrip = op.Shape()
        backed = common_vol(fstrip, sh) / t_film
        strips[f'Y{y0:g}-{y1:g}'] = dict(film_area_mm2=round(volume(fstrip) / t_film, 3), backed_by_frame_mm2=round(backed, 3),
                                         unbacked_mm2=round(volume(fstrip) / t_film - backed, 3))
    # keeper candidates in film-local coordinates (on the sliding face side, z from film top)
    keepers = [box(0, 0, t_film, 46.774, 7.0, t_film + 0.8), box(0, L - 7.0, t_film, 46.774, L, t_film + 0.8)]
    films = [o for o in O if o['pn'] == film]
    rows = []
    for fo in films:
        g = trsf(fo)
        ks = [k.Moved(TopLoc_Location(g)) for k in keepers]
        for ang in range(0, 91, 5):
            hits = []
            for o in O:
                if o['occurrence'] == fo['occurrence']: continue
                grp = o.get('moving') if o['source'] == 'R12' else None
                s = local(o['pn']).Moved(TopLoc_Location(trsf(o)))
                if grp and ang: s = local(o['pn']).Moved(TopLoc_Location(rot(grp, ang).Multiplied(trsf(o))))
                if not grp and ang: continue  # static bodies checked at 0 only
                b = bbox(s)
                for i, k in enumerate(ks):
                    if not overlap_bb(b, bbox(k)): continue
                    v = common_vol(k, s)
                    if v > 1e-3: hits.append(dict(keeper=i, body=o['occurrence'], pn=o['pn'], mm3=round(v, 3), moving=bool(grp)))
            rows.append(dict(film=fo['occurrence'], angle=ang, hits=hits))
    # minimum distance from keeper to the rotor envelope over angles (rotor is the moving body nearest)
    res[cfg] = dict(film_length=L, end_strips=strips, keeper_checks=rows)
    allh = [h for r in rows for h in r['hits']]
    import collections
    print(cfg, strips, 'keeper hits by pn:', dict(collections.Counter(h['pn'] for h in allh)), 'moving hits:', sum(h['moving'] for h in allh))
json.dump(res, open(OUT, 'w'), indent=1)
