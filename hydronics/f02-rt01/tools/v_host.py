"""v0498B C4 solids vs the C05 retained host (2,810 BReps) and against each other."""
import sys, json, collections, itertools
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2] / "c05-rt01" / "tools"))
from OCP.TopoDS import TopoDS_Shape
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Builder
from rt01_common import jload
from rt01_occ import load, bbox, bb_overlap, common_vol
d = sys.argv[1]
parts = json.load(open(f"{d}/f02_parts.json"))
host = [h for h in jload("internal/HOST_CONTEXT.json") if h["context_retained"]]
S = {}
for p in parts:
    s = TopoDS_Shape(); BRepTools.Read_s(s, f"{d}/{p['file']}", BRep_Builder()); S[p["name"]] = s
def cat(n):
    if "LRQ24A" in n: return "actuator_envelope"
    if "R3025" in n or "ZR2325" in n: return "valve_union"
    return "pipe"
res = {}; tot = collections.Counter(); vol = collections.Counter(); grp = collections.Counter()
for n, s in S.items():
    bb = bbox(s); hh = []
    for h in host:
        if bb_overlap(bb, h["bounds"]):
            v = common_vol(s, load(f"internal/context/{h['index']:04d}.brep"))
            if v > 1.0: hh.append((h["index"], str(h["group"]), h["name"], round(v, 1)))
    res[n] = hh; tot[cat(n)] += len(hh); vol[cat(n)] += sum(x[3] for x in hh)
    for x in hh: grp[(cat(n), x[1])] += 1
print("HOST PAIRS", dict(tot), {k: round(v / 1e6, 3) for k, v in vol.items()}, "L")
print("by group", grp.most_common(25))
hx = [(n, x) for n, hh in res.items() for x in hh if x[1] == "HX"]
print("vs HX host:", [(n, x[2][:60], x[3]) for n, x in hx])
internal = []
names = list(S)
for a, b in itertools.combinations(names, 2):
    if not bb_overlap(bbox(S[a]), bbox(S[b])): continue
    v = common_vol(S[a], S[b])
    if v > 1.0: internal.append((a, b, round(v, 1)))
print("INTERNAL", len(internal), round(sum(x[2] for x in internal) / 1000, 1), "cm3")
for x in internal: print("  ", x)
json.dump(dict(host=res, internal=internal), open(f"{d}/v_clash.json", "w"), indent=0)
