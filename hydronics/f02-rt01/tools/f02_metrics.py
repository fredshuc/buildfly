import json, math, sys, collections
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2] / "c05-rt01" / "tools"))
from rt01_hydraulics import darby, WATER, D, c05_terms, f_sj, pump_H
d = sys.argv[1]
L = {k: [tuple(x) for x in v] for k, v in json.load(open(f"{d}/f02_lines.json")).items()}
C = json.load(open(f"{d}/f02_clash.json"))
r = 33.7 / 2
tot_len = sum(math.dist(a, b) for v in L.values() for a, b in zip(v, v[1:]))
corners = sum(len(v) - 2 for v in L.values())
# miter piece g_min
bad = []
for k, v in L.items():
    u = [[(y - x) / math.dist(a, b) for x, y in zip(a, b)] for a, b in zip(v, v[1:])]
    for i, (a, b) in enumerate(zip(v, v[1:])):
        Ls = math.dist(a, b)
        A = u[i - 1] if i > 0 else None; B = u[i + 1] if i < len(u) - 1 else None
        if A and B: g = Ls - r * math.dist(A, B)
        elif A or B: g = Ls - r
        else: g = Ls
        if g < 25: bad.append((k, i + 1, round(Ls, 1), round(g, 1)))
print("total centreline m", round(tot_len / 1000, 3), "corners", corners, "lines", len(L))
print("pieces g_min<25:", bad)
# internal conflict classes
def endpoints(n): return [L[n][0], L[n][-1]] if n in L else []
def on(p, n, tol=.5):
    v = L[n]
    for a, b in zip(v, v[1:]):
        ab = [b[i]-a[i] for i in range(3)]; l2 = sum(x*x for x in ab)
        t = max(0, min(1, sum((p[i]-a[i])*ab[i] for i in range(3))/l2)); q = [a[i]+ab[i]*t for i in range(3)]
        if math.dist(p, q) < tol: return True
    return False
cls = collections.defaultdict(list)
attach = {  # line -> equipment it terminates on (from topology run)
}
for a, b, v in C["internal"]:
    if a in L and b in L:
        tee = any(on(p, b) for p in endpoints(a)) or any(on(p, a) for p in endpoints(b))
        cls["tee junction (expected)" if tee else "pipe crosses/overlaps pipe"].append((a, b, v))
    else:
        ln, eq = (a, b) if a in L else (b, a)
        cls["pipe vs equipment"].append((ln, eq, v))
for k, v in cls.items():
    print(f"== {k}: {len(v)} pairs, {round(sum(x[2] for x in v)/1000,1)} cm3")
    for x in v: print("   ", x)
# hydraulic estimate, H1 cold, bed A, return leg unknown -> bound 0 / 1.2 m + 2 corners
segs = ["CENTERLINE_SOURCE_CS","CENTERLINE_PUMP_TO_HEADER_CS","CENTERLINE_CS_A","CENTERLINE_HX_A_L_CLOSE","CENTERLINE_A_LOWER_TO_FS","CENTERLINE_A_FS_TO_Q","CENTERLINE_A_Q_TO_UPPER","CENTERLINE_HX_A_U_CLOSE","CENTERLINE_CR_A"]
Lp = sum(math.dist(a,b) for s in segs for a,b in zip(L[s],L[s][1:])) + 1000 + 292.2   # header run Y450->-550, FS gap
nc = sum(len(L[s])-2 for s in segs)
for temp in (5, 80):
    rho, mu = WATER[temp]; q = 2.0
    v = q/3600/(math.pi*D**2/4); dyn = rho*v*v/2/1000; Re = rho*v*D/mu; f = f_sj(Re); ref = c05_terms(temp, q)
    avail = rho*9.80665*(pump_H(q)-.3)/1000 - 15
    for ret_L, ret_c in ((0, 0), (1200, 2)):
        for el in ("miter90_1weld", "elbow90_LR"):
            K = (nc + ret_c)*darby(el, Re) + 3*darby("tee_branch_stubin", Re) + 14*0.12   # 3 tee turns, ~14 connectors
            tot = f*(Lp+ret_L)/1000/D*dyn + K*dyn + ref["HX"] + ref["valves"] + ref["meters"]
            print(f"H1 {temp}C path {round((Lp+ret_L)/1000,2)} m corners {nc+ret_c} {el}: total {tot:.1f} kPa margin {avail-tot:+.1f}")
