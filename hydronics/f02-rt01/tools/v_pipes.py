import json, sys, math
from OCP.TopoDS import TopoDS_Shape, TopoDS
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Builder
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Torus
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
d = sys.argv[1]
parts = json.load(open(f"{d}/f02_parts.json"))
out = {}
for p in parts:
    n = p["name"]
    if not any(n.startswith(k) for k in ("FITUP", "HR_", "HS_", "CR_", "CS_")): continue
    s = TopoDS_Shape(); BRepTools.Read_s(s, f"{d}/{p['file']}", BRep_Builder())
    ends, cyl, tor = [], [], []
    e = TopExp_Explorer(s, TopAbs_FACE)
    while e.More():
        f = TopoDS.Face(e.Current()); a = BRepAdaptor_Surface(f); t = a.GetType()
        if t == GeomAbs_Plane:
            g = GProp_GProps(); BRepGProp.SurfaceProperties_s(f, g); c = g.CentreOfMass()
            ends.append((round(c.X(), 2), round(c.Y(), 2), round(c.Z(), 2)))
        elif t == GeomAbs_Cylinder: cyl.append(round(a.Cylinder().Radius(), 3))
        elif t == GeomAbs_Torus: tor.append((round(a.Torus().MajorRadius(), 2), round(a.Torus().MinorRadius(), 3)))
        e.Next()
    kind = "tee" if "TEE" in n else ("elbow" if tor else "straight")
    L = math.dist(ends[0], ends[1]) if kind == "straight" and len(ends) == 2 else None
    out[n] = dict(kind=kind, ends=ends, radii=sorted(set(cyl)), torus=sorted(set(tor)), length=L, volume=p["volume"])
json.dump(out, open(f"{d}/v_pipes.json", "w"), indent=0)
import collections
print(collections.Counter(v["kind"] for v in out.values()))
print("cyl radii", collections.Counter(r for v in out.values() for r in v["radii"]))
print("torus", collections.Counter(t for v in out.values() for t in v["torus"]))
st = [v["length"] for v in out.values() if v["kind"] == "straight"]
print("straights", len(st), "total mm", round(sum(st), 1), "min", round(min(st), 1), sorted(round(x, 1) for x in st)[:12])
for n, v in out.items():
    if v["kind"] == "tee": print(n, v["ends"], v["radii"])
