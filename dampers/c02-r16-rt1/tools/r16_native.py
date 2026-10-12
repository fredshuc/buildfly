"""OCP loader for the R16 native catalogue (R16_PARTS.json + R16_<cfg>_OCCURRENCES.json). No project code imported."""
import json, io
from OCP.TopoDS import TopoDS_Shape
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Builder
from OCP.gp import gp_Trsf
from OCP.TopLoc import TopLoc_Location

class R16:
    def __init__(self, native_dir, cfg):
        self.P = {p['pn']: p for p in json.load(open(f"{native_dir}/R16_PARTS.json"))}
        self.O = json.load(open(f"{native_dir}/R16_{cfg}_OCCURRENCES.json"))
        self.om = {o['occurrence']: o for o in self.O}
        self.cfg = cfg; self._c = {}
    def local(self, pn):
        if pn not in self._c:
            s = TopoDS_Shape(); BRepTools.Read_s(s, io.BytesIO(self.P[pn]['brep'].encode()), BRep_Builder()); self._c[pn] = s
        return self._c[pn]
    @staticmethod
    def trsf(o):
        u, v, n, p = o['u'], o['v'], o['n'], o['o']
        g = gp_Trsf(); g.SetValues(u[0], v[0], n[0], p[0], u[1], v[1], n[1], p[1], u[2], v[2], n[2], p[2]); return g
    def world(self, occ, extra=None):
        o = self.om[occ] if isinstance(occ, str) else occ
        g = self.trsf(o)
        if extra is not None: g = extra.Multiplied(g)
        return self.local(o['pn']).Moved(TopLoc_Location(g))
