"""RT01-E: which of the active-path miters can take a standard butt-weld elbow
without moving any end point, connector, header or valve.

Fitting options per 90 deg corner on OD33.7 spools (centre-to-end = bend radius):
  LR 1.5D  38.1 mm  (ASME B16.9 NPS1 LR; DIN 2605-1 type 3 OD33.7 ~38 mm) - confirm with supplier
  SR 1.0D  25.4 mm  (ASME B16.9 NPS1 SR)
  MITER     0  mm  (C05 single-cut miter, kept)
Constraint per straight piece: sum of fitting centre-to-ends at its two ends
<= piece centreline length (fitting-to-fitting butt weld allowed; elbow welded
directly to a connector/header weld face allowed). DP over corners minimises
sum K at the cold 2.0 m3/h Reynolds number.
"""
import math, json
from rt01_common import design, save_csv, save_json
from rt01_hydraulics import darby, WATER, D, active_edges, all_paths, geometry_path, best_estimate, zero_margin_flow

CTE = {"elbow90_LR": 38.1, "elbow90_SR_welded": 25.4, "miter90_1weld": 0.0}


def seglens(r):
    P = r["points"]
    return [math.dist(p, q) for p, q in zip(P, P[1:])]


def assign(r, Re):
    L = seglens(r); n = len(L) - 1           # corners
    if n <= 0:
        return [], 0.0
    opts = list(CTE)
    # dp[i][k] = min cost for corners 0..i with corner i using option k
    INF = float("inf")
    dp = [[INF] * len(opts) for _ in range(n)]; bk = [[None] * len(opts) for _ in range(n)]
    for k, o in enumerate(opts):
        if CTE[o] <= L[0] + 1e-9:
            dp[0][k] = darby(o, Re)
    for i in range(1, n):
        for k, o in enumerate(opts):
            for j, p in enumerate(opts):
                if dp[i - 1][j] < INF and CTE[p] + CTE[o] <= L[i] + 1e-9:
                    c = dp[i - 1][j] + darby(o, Re)
                    if c < dp[i][k]:
                        dp[i][k], bk[i][k] = c, j
    best, kb = INF, None
    for k, o in enumerate(opts):
        if dp[n - 1][k] < INF and CTE[o] <= L[n] + 1e-9 and dp[n - 1][k] < best:
            best, kb = dp[n - 1][k], k
    seq = [kb]
    for i in range(n - 1, 0, -1):
        seq.append(bk[i][seq[-1]])
    return [opts[k] for k in reversed(seq)], best


if __name__ == "__main__":
    rho, mu = WATER[5]
    v = 2.0 / 3600 / (math.pi * D ** 2 / 4); Re = rho * v * D / mu
    d = design(); out = []; fit = {}
    for eid, r in d["pipe_routes"].items():
        if r["OD_mm"] != 33.7 or not r["bend_radii"]:
            continue
        kinds, cost = assign(r, Re)
        fit[eid] = kinds
        out.append(dict(edge=eid, a=r["a"], b=r["b"], corners=len(kinds), pieces_mm=[round(x, 1) for x in seglens(r)],
                        fittings=kinds, n_LR=kinds.count("elbow90_LR"), n_SR=kinds.count("elbow90_SR_welded"),
                        n_miter_kept=kinds.count("miter90_1weld"),
                        K_C05_miters=round(len(kinds) * darby("miter90_1weld", Re), 3), K_fitted=round(cost, 3)))
    save_csv("rt01_elbow_fit.csv", out)
    save_json("rt01_elbow_fit.json", fit)
    tot = {k: sum(o[k] for o in out) for k in ("corners", "n_LR", "n_SR", "n_miter_kept")}
    print("OD33.7 spools with corners:", len(out), tot)
    duty = []
    for mode in ("H1", "H2"):
        edges = active_edges(mode)
        for temp, s, t in ((5, "CS", "CR"), (80, "HS", "HR")):
            path = all_paths(s, t, edges)[0]; elems = geometry_path(path)
            on = [e["id"] for e in elems if e["type"] == "pipe"]
            c = {k: sum(o[k] for o in out if o["edge"] in on) for k in ("corners", "n_LR", "n_SR", "n_miter_kept")}
            be = best_estimate(elems, temp, 2.0); ft = best_estimate(elems, temp, 2.0, fit=fit)
            ft_hi = best_estimate(elems, temp, 2.0, fit=fit, conn_factor=2.0, miter_factor=1.25)
            q0 = zero_margin_flow(lambda q: best_estimate(elems, temp, q, fit=fit)["margin"])
            duty.append(dict(case=f"{mode}_{temp}C", **c, BE_margin_kPa=round(be["margin"], 2),
                             fitted_margin_kPa=round(ft["margin"], 2), fitted_margin_low_kPa=round(ft_hi["margin"], 2),
                             fitted_K_corners=round(ft["K_corners"], 2), Q_zero_margin_fitted=round(q0, 3)))
            print(duty[-1])
    save_csv("rt01_elbow_fit_duties.csv", duty)
    for o in out:
        print(o["edge"], o["a"], "->", o["b"], o["pieces_mm"], [k[:5] for k in o["fittings"]])
