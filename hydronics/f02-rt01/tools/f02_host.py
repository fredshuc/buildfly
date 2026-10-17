"""F02 vs the C05 retained host (2,810 BReps): pipes swept at OD33.7/ID27.3 with
exact single-cut miters, equipment solids, HX stubs; plus pipe-vs-pipe and
pipe-vs-equipment. Also insulated (+13 mm) pipe envelopes vs host."""
import sys, json, math, collections
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2] / "c05-rt01" / "tools"))
from OCP.TopoDS import TopoDS_Shape
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Builder
from rt01_common import jload
from rt01_occ import load, bbox, bb_overlap, compound, common_vol
from rt01_cad_elbows import build_spool, pvol
d = sys.argv[1]
P = {p["name"]: p for p in json.load(open(f"{d}/f02_parts.json"))}
L = json.load(open(f"{d}/f02_lines.json"))
host = [h for h in jload("internal/HOST_CONTEXT.json") if h["context_retained"]]
def rd(f):
    s = TopoDS_Shape(); BRepTools.Read_s(s, f"{d}/{f}", BRep_Builder()); return s
def tube(name, extra=0.0, solid=False):
    pts = L[name]; r = dict(points=pts, OD_mm=33.7 + 2 * extra, ID_mm=0.0 if solid else 27.3, bend_radii=[0] * (len(pts) - 2))
    return build_spool(r, ["miter90_1weld"] * (len(pts) - 2))
objs = {}
for n in L: objs[n] = tube(n)
for n, p in P.items():
    if not n.startswith("CENTERLINE"): objs[n] = [rd(p["file"])]
def host_hits(parts):
    bb = bbox(compound(parts)); hits = []
    for h in host:
        if bb_overlap(bb, h["bounds"]):
            v = pvol(parts, load(f"internal/context/{h['index']:04d}.brep"))
            if v > 1.0: hits.append((h["index"], h["group"], h["name"], round(v, 1)))
    return hits
res = {}; tot = collections.Counter(); vol = collections.Counter()
for n, parts in objs.items():
    hh = host_hits(parts); res[n] = hh
    k = "pipe" if n.startswith("CENTERLINE") else ("HX_stub" if n.startswith("INTERFACE") else "equipment")
    tot[k] += len(hh); vol[k] += sum(x[3] for x in hh)
    if hh: print(n, len(hh), round(sum(x[3] for x in hh) / 1000, 1), "cm3", sorted({str(x[1]) for x in hh}))
print("HOST PAIRS", dict(tot), {k: round(v / 1e6, 3) for k, v in vol.items()}, "L")
# insulated pipes vs host
ti = 0; tv = 0
for n in L:
    hh = host_hits(tube(n, 13.0, True)); ti += len(hh); tv += sum(x[3] for x in hh)
print("INSULATED PIPE HOST PAIRS", ti, round(tv / 1e6, 3), "L")
# internal: pipe vs pipe (excluding pairs that share an endpoint junction) and pipe vs equipment
names = list(objs); internal = []
def ends(n): return {tuple(L[n][0]), tuple(L[n][-1])} if n in L else set()
for i, a in enumerate(names):
    for b in names[i + 1:]:
        if not bb_overlap(bbox(compound(objs[a])), bbox(compound(objs[b]))): continue
        if a in L and b in L:
            # junction tee: one's endpoint lies on the other: report but tag
            pass
        v = sum(pvol(objs[a], q) for q in objs[b])
        if v > 1.0: internal.append((a, b, round(v, 1)))
for x in internal: print("INTERNAL", x)
json.dump(dict(host=res, internal=internal), open(f"{d}/f02_clash.json", "w"), indent=0)
