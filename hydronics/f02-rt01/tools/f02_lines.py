import sys, json, math
from OCP.TopoDS import TopoDS_Shape, TopoDS
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Builder, BRep_Tool
from OCP.TopExp import TopExp_Explorer, TopExp
from OCP.TopAbs import TopAbs_EDGE
d = sys.argv[1]
parts = json.load(open(f"{d}/f02_parts.json"))
lines = {}
for p in parts:
    if not p["name"].startswith("CENTERLINE"): continue
    s = TopoDS_Shape(); BRepTools.Read_s(s, f"{d}/{p['file']}", BRep_Builder())
    segs = []
    e = TopExp_Explorer(s, TopAbs_EDGE)
    while e.More():
        ed = TopoDS.Edge(e.Current())
        a = BRep_Tool.Pnt_s(TopExp.FirstVertex_s(ed)); b = BRep_Tool.Pnt_s(TopExp.LastVertex_s(ed))
        segs.append(((round(a.X(),2),round(a.Y(),2),round(a.Z(),2)),(round(b.X(),2),round(b.Y(),2),round(b.Z(),2))))
        e.Next()
    # chain into polyline
    pts = [segs[0][0], segs[0][1]]; rest = segs[1:]
    while rest:
        for i,(a,b) in enumerate(rest):
            if a == pts[-1]: pts.append(b); rest.pop(i); break
            if b == pts[-1]: pts.append(a); rest.pop(i); break
            if b == pts[0]: pts.insert(0, a); rest.pop(i); break
            if a == pts[0]: pts.insert(0, b); rest.pop(i); break
        else:
            print("DISCONNECTED", p["name"]); break
    lines[p["name"]] = pts
json.dump(lines, open(f"{d}/f02_lines.json","w"), indent=0)
for k,v in lines.items():
    L=sum(math.dist(a,b) for a,b in zip(v,v[1:]))
    dirs=[]
    for a,b in zip(v,v[1:]):
        u=[(y-x)/math.dist(a,b) for x,y in zip(a,b)]; dirs.append(u)
    ang=[round(math.degrees(math.acos(max(-1,min(1,sum(x*y for x,y in zip(p,q)))))),1) for p,q in zip(dirs,dirs[1:])]
    print(k, round(L,1), 'corners', ang, v)
