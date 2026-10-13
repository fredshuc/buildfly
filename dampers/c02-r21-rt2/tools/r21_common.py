"""Shared loaders for the R21 checks (R20 native parts, occurrence frames, R17+ motion convention)."""
import json, math, io
from OCP.TopoDS import TopoDS_Shape
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Builder
from OCP.gp import gp_Trsf, gp_Ax1, gp_Pnt, gp_Dir
from OCP.TopLoc import TopLoc_Location
AX = {'P1': (83.0, 1583.0), 'P2': (-82.0, 1583.0), 'R1': (-82.0, 1583.0)}
PARTS, cache = {}, {}
def init(nat):
    PARTS.update({p['pn']: p for p in json.load(open(f"{nat}/R20_PARTS.json"))})
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
def place(o, ang=0.0):
    g = trsf(o); grp = o.get('moving') if o.get('source') == 'R12' else None
    if grp and ang: g = rot(grp, ang).Multiplied(g)
    return local(o['pn']).Moved(TopLoc_Location(g))
