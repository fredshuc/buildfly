import json, math, sys
from OCP.TopoDS import TopoDS_Shape
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Builder
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.TopAbs import TopAbs_IN, TopAbs_ON, TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer
from OCP.gp import gp_Pnt
d = sys.argv[1]
P = {p["name"]: p for p in json.load(open(f"{d}/f02_parts.json"))}
L = {k: [tuple(x) for x in v] for k, v in json.load(open(f"{d}/f02_lines.json")).items()}
cls = {}
for n, p in P.items():
    if not n.startswith("EQUIP"): continue
    s = TopoDS_Shape(); BRepTools.Read_s(s, f"{d}/{p['file']}", BRep_Builder())
    e = TopExp_Explorer(s, TopAbs_SOLID); cs = []
    while e.More(): cs.append(BRepClass3d_SolidClassifier(e.Current())); e.Next()
    cls[n] = (cs, p["bbox"])
def state(n, q):
    cs, b = cls[n]
    if not all(b[i] - 1 <= q[i] <= b[i + 3] + 1 for i in range(3)): return "OUT"
    for c in cs:
        c.Perform(gp_Pnt(*q), 0.5)
        st = c.State()
        if st == TopAbs_IN: return "IN"
        if st == TopAbs_ON: return "ON"
    return "OUT"
print("== centreline length inside real equipment solids (mm)")
for k, v in L.items():
    for a, b in zip(v, v[1:]):
        for n in cls:
            N = 300; inn = sum(state(n, [a[i] + (b[i] - a[i]) * (j + .5) / N for i in range(3)]) == "IN" for j in range(N))
            if inn: print(f"{k:30s} {n:18s} {math.dist(a,b)*inn/N:7.1f}")
print("== endpoints vs real solids")
for k, v in L.items():
    for e in (v[0], v[-1]):
        t = [f"{state(n,e)}:{n}" for n in cls if state(n, e) != "OUT"]
        if t: print(f"{k:30s} {str(e):28s} {t}")
print("== equipment vs equipment (sampled overlap of solids, cm3)")
import itertools, random
rnd = random.Random(1)
for a, b in itertools.combinations(cls, 2):
    A, B = cls[a][1], cls[b][1]
    lo = [max(A[i], B[i]) for i in range(3)]; hi = [min(A[i+3], B[i+3]) for i in range(3)]
    if any(hi[i] <= lo[i] for i in range(3)): continue
    vol = math.prod(hi[i]-lo[i] for i in range(3)); N = 4000; c = 0
    for _ in range(N):
        q = [rnd.uniform(lo[i], hi[i]) for i in range(3)]
        c += state(a, q) == "IN" and state(b, q) == "IN"
    if c: print(f"{a:18s} {b:18s} {vol*c/N/1000:8.1f} cm3")
