import sys, json
from OCP.TopoDS import TopoDS
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID, TopAbs_EDGE, TopAbs_FACE, TopAbs_VERTEX, TopAbs_SHELL, TopAbs_WIRE
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GeomAbs import GeomAbs_Line, GeomAbs_Circle

def cnt(s, t):
    e = TopExp_Explorer(s, t); n = 0
    while e.More(): n += 1; e.Next()
    return n

from OCP.STEPControl import STEPControl_Reader
from OCP.TopoDS import TopoDS_Iterator
r = STEPControl_Reader(); assert r.ReadFile(sys.argv[1]) == IFSelect_RetDone; r.TransferRoots(); root = r.OneShape()
tr = r.WS().TransferReader()
out = []; outdir = sys.argv[2]
it = TopoDS_Iterator(root); k = 0
while it.More():
    s = it.Value(); it.Next(); k += 1
    ent = tr.EntityFromShapeResult(s, 1)
    name = ent.Name().ToCString() if ent is not None and hasattr(ent, "Name") and ent.Name() is not None else f"item{k}"
    b = Bnd_Box(); BRepBndLib.Add_s(s, b, False); m, M = b.CornerMin(), b.CornerMax()
    g = GProp_GProps(); BRepGProp.VolumeProperties_s(s, g); v = g.Mass()
    gl = GProp_GProps(); BRepGProp.LinearProperties_s(s, gl); L = gl.Mass()
    nl = nc = 0; e = TopExp_Explorer(s, TopAbs_EDGE)
    while e.More():
        c = BRepAdaptor_Curve(TopoDS.Edge(e.Current())); tp = c.GetType()
        nl += tp == GeomAbs_Line; nc += tp == GeomAbs_Circle; e.Next()
    out.append(dict(name=name, type=str(s.ShapeType()).split('.')[-1], solids=cnt(s, TopAbs_SOLID), faces=cnt(s, TopAbs_FACE),
                    edges=cnt(s, TopAbs_EDGE), line_edges=nl, circle_edges=nc, vertices=cnt(s, TopAbs_VERTEX),
                    volume=round(v, 1), edge_length=round(L, 1),
                    bbox=[round(x, 2) for x in (m.X(), m.Y(), m.Z(), M.X(), M.Y(), M.Z())]))
    BRepTools.Write_s(s, f"{outdir}/{k:02d}.brep"); out[-1]["file"] = f"{k:02d}.brep"
json.dump(out, open(f"{outdir}/f02_parts.json", "w"), indent=1)
for o in out: print(o)
