"""Bed-side (header -> bed A -> header) comparison v0498B / C05 R1 / F02, H1 cold, 2.0 m3/h:
pipe + corner losses only (HX, valves, FS, Q, meters excluded: v0498B has no FS/Q)."""
import sys, json, math
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2] / "c05-rt01" / "tools"))
from rt01_hydraulics import darby, WATER, D, f_sj
from rt01_common import design
vp = json.load(open(sys.argv[1]))           # v0498B pipes
f2 = {k: [tuple(x) for x in v] for k, v in json.load(open(sys.argv[2])).items()}
rho, mu = WATER[5]; v = 2.0/3600/(math.pi*D**2/4); dyn = rho*v*v/2/1000; Re = rho*v*D/mu; f = f_sj(Re)
def dp(L_mm, n, kind): return f*L_mm/1000/D*dyn + n*darby(kind, Re)*dyn
groups = ["CS_A-LB", "FITUP_A-L_AB", "FITUP_A_INTERSTAGE", "FITUP_A-U_AB", "CR_A-UB"]
sel = {k: x for k, x in vp.items() if any(k.startswith(g + "_") for g in groups)}
nE = sum(x["kind"] == "elbow" for x in sel.values()); Ls = sum(x["length"] for x in sel.values() if x["kind"] == "straight")
Lv = Ls + nE * math.pi / 2 * 38.1
r = design()["pipe_routes"]; c5 = ["E052", "E058", "E075", "E076", "E077", "E070", "E064"]
Lc = sum(r[e]["developed_mm"] for e in c5); nc = sum(len(r[e]["bend_radii"]) for e in c5)
f2s = ["CENTERLINE_CS_A", "CENTERLINE_HX_A_L_CLOSE", "CENTERLINE_A_LOWER_TO_FS", "CENTERLINE_A_FS_TO_Q", "CENTERLINE_A_Q_TO_UPPER", "CENTERLINE_HX_A_U_CLOSE", "CENTERLINE_CR_A"]
Lf = sum(math.dist(a, b) for s in f2s for a, b in zip(f2[s], f2[s][1:])) + 292.2; nf = sum(len(f2[s]) - 2 for s in f2s)
out = dict(
  v0498B=dict(L_m=round(Lv/1000, 2), corners=nE, corner_type="LR 1.5D elbow", dp_kPa=round(dp(Lv, nE, "elbow90_LR"), 1), note="bed link 0.31 m; no FS/Q; HX ports of earlier layout"),
  C05=dict(L_m=round(Lc/1000, 2), corners=nc, corner_type="single-cut miter", dp_kPa=round(dp(Lc, nc, "miter90_1weld"), 1), dp_if_elbows=round(dp(Lc, nc, "elbow90_LR"), 1)),
  F02=dict(L_m=round(Lf/1000, 2), corners=nf, corner_type="sharp (undefined)", dp_kPa_miter=round(dp(Lf, nf, "miter90_1weld"), 1), dp_kPa_LR=round(dp(Lf, nf, "elbow90_LR"), 1)))
print(json.dumps(out, indent=1))
json.dump(out, open(sys.argv[3], "w"), indent=1)
