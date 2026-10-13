"""Minimal OCP loader for the C02 native database (BRep strings + o/u/v/n frames)."""
import json, io, sys, math
from OCP.TopoDS import TopoDS_Shape
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Builder
from OCP.gp import gp_Trsf
from OCP.TopLoc import TopLoc_Location
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakePrism, BRepPrimAPI_MakeCylinder
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace
from OCP.gp import gp_Pnt, gp_Vec, gp_Ax2, gp_Dir

class Native:
    def __init__(self, native_dir):
        self.P = json.load(open(f"{native_dir}/PARAMETRIC_PARTS_C02.json"))
        self.O = json.load(open(f"{native_dir}/OCCURRENCES_C02.json"))
        self.pm = {p['pn']: p for p in self.P}
        self.om = {o['occurrence']: o for o in self.O}
        self._cache = {}
    def local(self, pn):
        if pn not in self._cache:
            s = TopoDS_Shape(); BRepTools.Read_s(s, io.BytesIO(self.pm[pn]['brep'].encode()), BRep_Builder())
            self._cache[pn] = s
        return self._cache[pn]
    def world(self, occ):
        o = self.om[occ] if isinstance(occ, str) else occ
        u, v, n, p = o['u'], o['v'], o['n'], o['o']
        g = gp_Trsf(); g.SetValues(u[0], v[0], n[0], p[0], u[1], v[1], n[1], p[1], u[2], v[2], n[2], p[2])
        return self.local(o['pn']).Moved(TopLoc_Location(g))
    def occs(self, pn=None, cfg=None):
        for o in self.O:
            if pn and o['pn'] != pn: continue
            if cfg and cfg not in o.get('configs', ['AUTO', 'MANUAL']): continue
            yield o

def bbox(s):
    b = Bnd_Box(); BRepBndLib.Add_s(s, b, False); m, M = b.CornerMin(), b.CornerMax(); return [m.X(), m.Y(), m.Z(), M.X(), M.Y(), M.Z()]
def volume(s):
    g = GProp_GProps(); BRepGProp.VolumeProperties_s(s, g); return abs(g.Mass())
def common_vol(a, b):
    op = BRepAlgoAPI_Common(a, b); op.Build(); return volume(op.Shape()) if op.IsDone() else float('nan')
def dist(a, b):
    d = BRepExtrema_DistShapeShape(a, b); d.Perform(); return d.Value()
def box(x0, y0, z0, x1, y1, z1):
    return BRepPrimAPI_MakeBox(gp_Pnt(x0, y0, z0), gp_Pnt(x1, y1, z1)).Shape()
def prism(points, vec):
    poly = BRepBuilderAPI_MakePolygon()
    for p in points: poly.Add(gp_Pnt(*p))
    poly.Close(); f = BRepBuilderAPI_MakeFace(poly.Wire()).Face()
    return BRepPrimAPI_MakePrism(f, gp_Vec(*vec)).Shape()
def overlap_bb(a, b, tol=1e-5):
    return all(min(a[j+3], b[j+3]) - max(a[j], b[j]) > tol for j in range(3))
