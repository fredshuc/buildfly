"""RT01-H: independent rebuild of the four nominal hydraulic duties.

Steps
1. Rebuild the active supply->return path for H1/H2 x cold/hot from the flow
   graph with the actual H1/H2 valve states (FS, XV, MV open; bleeds closed),
   and confirm the path is the only simple path (no parallel branch).
2. Reproduce C05 calculate.py exactly (validation of our reading).
3. Re-estimate with geometry-resolved losses:
   - 90 deg single-weld miter, LR elbow, tee run / tee branch: Darby 3-K
     (K = K1/Re + Ki (1 + Kd / Dn_in^0.3)), Darby (2001) Chem. Eng. 108(4).
   - header traversed as run or as branch, from the actual port the path
     enters and leaves; header flow length = distance between those ports.
   - connector bore steps (sudden contraction/expansion, Crane TP-410).
   - HX, valves (Kv), meters, pump curve, 0.3 m, 10 kPa, 5 kPa: as C05 [S].
4. Operating flow at which margin = 0 with the C05 pump curve.
5. What-if: all miters on the active path replaced by LR (1.5D) elbows.
"""
import math, collections, json
from rt01_common import design, graph, headers, connections, save_json, save_csv, dot, sub, unit

PUMP = {0.5: 8.0, 1.72: 7.95, 2.0: 7.85, 2.58: 7.6}           # m, C05 [S]
WATER = {5: (1000.0, 0.00152), 80: (972.0, 0.000355)}          # C05 [S]
D, DT, EPS = 0.0273, 0.00852, 0.000015
DARBY = {  # K1, Ki, Kd
    "miter90_1weld": (1000, 0.27, 4.0),
    "elbow90_LR": (800, 0.056, 3.9),
    "elbow90_SR_welded": (800, 0.091, 4.0),
    "tee_branch_stubin": (1000, 0.34, 4.0),
    "tee_run_welded": (150, 0.05, 4.0),
}
BORE = {"NPT1_W33": 24.0, "R1_W33": 25.0, "RP1_W33": 25.0, "UF_G1": 23.5, "UF_G15": 30.0}


def darby(kind, Re, d_m=D):
    k1, ki, kd = DARBY[kind]
    return k1 / Re + ki * (1 + kd / (d_m / 0.0254) ** 0.3)


def f_sj(Re, eps=EPS, d=D):
    return 64 / Re if Re < 2300 else 0.25 / math.log10(eps / (3.7 * d) + 5.74 / Re ** 0.9) ** 2


def states(mode):
    g = graph()
    st = {}
    for t in g["components"]:
        if t.startswith("V_"):
            st[t] = "A" if ("_A_" in t) == (mode == "H1") else "B"
        elif t.startswith(("FS_", "XV_", "MV_")):
            st[t] = "OPEN"
        elif t.startswith("P_"):
            st[t] = "PASSAGE"
        else:
            st[t] = "CLOSED"           # bleeds
    return st


def active_edges(mode):
    g, st = graph(), states(mode)
    return [e for e in g["edges"] if e["active_when"] == "always"
            or st.get(e["control"], "CLOSED") in e["active_when"].split("|")]


def all_paths(src, dst, edges, limit=50):
    adj = collections.defaultdict(list)
    for e in edges:
        adj[e["from_port"]].append((e["to_port"], e))
        adj[e["to_port"]].append((e["from_port"], e))
    out = []

    def dfs(u, seen, acc):
        if len(out) >= limit:
            return
        if u == dst:
            out.append(list(acc)); return
        for v, e in adj[u]:
            if v not in seen:
                seen.add(v); acc.append((u, v, e)); dfs(v, seen, acc); acc.pop(); seen.discard(v)
    dfs(src, {src}, [])
    return out


def c05_reproduce(path_edges, temp, q, H=None):
    """Line-for-line port of C05 calculate.py duty block."""
    d = design(); routes = d["pipe_routes"]
    hh_all = list(headers().values()); cc_all = list(connections().values())
    ids = [e["id"] for e in path_edges]
    nodes = set(p for e in path_edges for p in (e["from_port"], e["to_port"]))
    hh = [x for x in hh_all if x["node"] in nodes]; cc = [x for x in cc_all if x["port"] in nodes]
    L = sum(routes[i]["developed_mm"] / 1000 for i in ids if i in routes)
    L += sum(x["length_mm"] / 1000 for x in hh) + sum(math.dist(x["equipment_face"], x["weld_face"]) / 1000 for x in cc)
    K = sum(sum(1.5 if r == 0 else 1.0 for r in routes[i]["bend_radii"]) for i in ids if i in routes) + 2 * len(hh) + 1.5 * len(cc)
    rho, mu = WATER[temp]; H = pump_H(q) if H is None else H
    v = q / 3600 / (math.pi * D ** 2 / 4); re = rho * v * D / mu; f = f_sj(re)
    vt = q / 3600 / 27 / (math.pi * DT ** 2 / 4); rt = rho * vt * DT / mu
    ft = 64 / rt if rt < 2300 else 0.25 / (math.log10(0.0000015 / (3.7 * DT) + 5.74 / rt ** 0.9) ** 2)
    if 1800 < rt < 4000:
        ft = max(ft, .05)
    hx = 2 * (ft * 5.2 / DT + 18) * rho * vt * vt / 2 / 1000 + 4 * (.04 * 1.02 / .028 + 3) * rho * v * v / 2 / 1000
    valves = 2 * 100 * (q / 10) ** 2 * rho / 1000 + 5 * 100 * (q / 47.9) ** 2 * rho / 1000
    pipe = (f * L / D + K) * rho * v * v / 2 / 1000
    meters = 6 * (q / 2.58) ** 2
    total = hx + valves + pipe + meters
    avail = rho * 9.80665 * (H - .3) / 1000
    return dict(L_m=L, K=K, n_headers=len(hh), n_conn=len(cc), HX=hx, valves=valves, pipe_fittings=pipe,
                meters=meters, total=total, available=avail, margin=avail - total - 15)


def port_position(h, edge_id, node_component_edge):
    """Where on header h the path edge attaches: ROOT / MAIN / BRANCH, and axial position (mm)."""
    start, axis = h["start"], h["axis"]
    if edge_id == h["main_edge"]:
        return "MAIN", h["length_mm"]
    for b in h["branch_ports"]:
        if b["route"] == edge_id:
            return "BRANCH", dot(sub(b["center"], start), axis)
    return "ROOT", 0.0          # equipment/component edge (valve internal etc.) enters at the root


def geometry_path(path):
    """Ordered list of loss elements along the oriented path."""
    d = design(); routes = d["pipe_routes"]; H = headers(); C = connections()
    elems = []
    for i, (u, v, e) in enumerate(path):
        eid = e["id"]
        if eid in routes:
            r = routes[eid]
            elems.append(dict(type="pipe", id=eid, L_mm=r["developed_mm"], ID_mm=r["ID_mm"],
                              n_miter=sum(1 for x in r["bend_radii"] if x == 0)))
        else:
            elems.append(dict(type="component", id=eid, kind=e["kind"], control=e["control"]))
        # node v between this edge and the next
        if i + 1 < len(path) and v in H:
            h = H[v]; nxt = path[i + 1][2]["id"]
            pin, xin = port_position(h, eid, None)
            pout, xout = port_position(h, nxt, None)
            turn = "BRANCH" if "BRANCH" in (pin, pout) else "RUN"
            elems.append(dict(type="header", id=h["id"], node=v, enter=pin, leave=pout, flow=turn,
                              flow_len_mm=abs(xout - xin), full_len_mm=h["length_mm"]))
    # connectors: one per path node that owns an installed connection; direction matters
    conns = []
    nodes_in_order = [path[0][0]] + [v for (_, v, _) in path]
    for k, n in enumerate(nodes_in_order):
        if n in C:
            c = C[n]
            # flow goes pipe->equipment if the next edge is a component edge
            nxt = path[k][2] if k < len(path) else None
            to_equipment = nxt is not None and nxt["id"] not in routes
            conns.append(dict(type="connector", id=c["installed_id"], node=n, family=c["family"],
                              bore_mm=BORE[c["family"]], to_equipment=to_equipment,
                              len_mm=math.dist(c["equipment_face"], c["weld_face"])))
    return elems + conns


def k_step(d_small, d_big, contraction):
    b2 = (d_small / d_big) ** 2
    k_small = 0.5 * (1 - b2) if contraction else (1 - b2) ** 2
    return k_small / b2 ** 2                 # referred to pipe (big) velocity


def best_estimate(elems, temp, q, elbow="miter90_1weld", conn_factor=1.0, miter_factor=1.0, H=None, fit=None):
    rho, mu = WATER[temp]; H = pump_H(q) if H is None else H
    v = q / 3600 / (math.pi * D ** 2 / 4); dyn = rho * v * v / 2 / 1000; Re = rho * v * D / mu; f = f_sj(Re)
    L = sum(e["L_mm"] for e in elems if e["type"] == "pipe") / 1000
    L += sum(e["flow_len_mm"] for e in elems if e["type"] == "header") / 1000
    L += sum(e["len_mm"] for e in elems if e["type"] == "connector") / 1000
    nm = sum(e["n_miter"] for e in elems if e["type"] == "pipe")
    if fit is None:
        k_corner = nm * darby(elbow, Re) * miter_factor
    else:   # per-corner fitting assignment {edge: [kind,...]}; unlisted spools keep miters
        k_corner = 0.0
        for e in elems:
            if e["type"] == "pipe":
                kinds = fit.get(e["id"], ["miter90_1weld"] * e["n_miter"])
                k_corner += sum(darby(k, Re) * (miter_factor if k == "miter90_1weld" else 1.0) for k in kinds)
    k_head = sum(darby("tee_branch_stubin" if e["flow"] == "BRANCH" else "tee_run_welded", Re)
                 for e in elems if e["type"] == "header")
    k_conn = conn_factor * sum(k_step(e["bore_mm"], 27.3, e["to_equipment"]) if e["bore_mm"] < 27.3
                               else k_step(27.3, e["bore_mm"], not e["to_equipment"]) * ((e["bore_mm"] / 27.3) ** 4)
                               for e in elems if e["type"] == "connector")
    ref = c05_terms(temp, q)
    friction = f * L / D * dyn
    out = dict(Re=Re, v_m_s=v, dyn_kPa=dyn, f=f, L_m=L, n_corners=nm,
               K_corners=k_corner, K_headers=k_head, K_connectors=k_conn,
               friction_kPa=friction, corners_kPa=k_corner * dyn, headers_kPa=k_head * dyn,
               connectors_kPa=k_conn * dyn, HX=ref["HX"], valves=ref["valves"], meters=ref["meters"])
    out["total"] = friction + (k_corner + k_head + k_conn) * dyn + ref["HX"] + ref["valves"] + ref["meters"]
    out["available"] = rho * 9.80665 * (H - .3) / 1000
    out["margin"] = out["available"] - out["total"] - 15
    return out


def c05_terms(temp, q):
    rho, mu = WATER[temp]
    v = q / 3600 / (math.pi * D ** 2 / 4)
    vt = q / 3600 / 27 / (math.pi * DT ** 2 / 4); rt = rho * vt * DT / mu
    ft = 64 / rt if rt < 2300 else 0.25 / (math.log10(0.0000015 / (3.7 * DT) + 5.74 / rt ** 0.9) ** 2)
    if 1800 < rt < 4000:
        ft = max(ft, .05)
    hx_tubes = 2 * (ft * 5.2 / DT + 18) * rho * vt * vt / 2 / 1000
    hx_necks = 4 * (.04 * 1.02 / .028 + 3) * rho * v * v / 2 / 1000
    return dict(HX=hx_tubes + hx_necks, HX_tubes=hx_tubes, HX_necks=hx_necks, Re_tube=rt,
                valves=2 * 100 * (q / 10) ** 2 * rho / 1000 + 5 * 100 * (q / 47.9) ** 2 * rho / 1000,
                meters=6 * (q / 2.58) ** 2)


def pump_H(q):
    qs = sorted(PUMP); 
    if q <= qs[0]:
        return PUMP[qs[0]]
    for a, b in zip(qs, qs[1:]):
        if q <= b:
            return PUMP[a] + (PUMP[b] - PUMP[a]) * (q - a) / (b - a)
    a, b = qs[-2], qs[-1]
    return PUMP[b] + (PUMP[b] - PUMP[a]) * (q - b) / (b - a)


def zero_margin_flow(fn):
    lo, hi = 0.5, 3.5
    for _ in range(60):
        m = (lo + hi) / 2
        if fn(m) >= 0:
            lo = m
        else:
            hi = m
    return lo


if __name__ == "__main__":
    c05 = {(r["state"], int(r["water_C"]), float(r["Q_m3_h"])): r
           for r in __import__("rt01_common").rows("internal/C05_PUMP_DUTY_16_POINTS.csv")}
    res, table = {}, []
    for mode in ("H1", "H2"):
        edges = active_edges(mode)
        for temp, s, t in ((5, "CS", "CR"), (80, "HS", "HR")):
            paths = all_paths(s, t, edges)
            assert len(paths) == 1, (mode, temp, len(paths))
            path = paths[0]
            elems = geometry_path(path)
            key = f"{mode}_{temp}C"
            res[key] = dict(path=[e["id"] for (_, _, e) in path], unique_simple_paths=len(paths),
                            headers=[e for e in elems if e["type"] == "header"],
                            connectors=[e for e in elems if e["type"] == "connector"],
                            spools=[e for e in elems if e["type"] == "pipe"])
            for q in PUMP:
                rp = c05_reproduce([e for (_, _, e) in path], temp, q)
                ref = float(c05[(mode, temp, q)]["margin_after_10kPa_source_and5kPa_reserve"])
                be = best_estimate(elems, temp, q)
                lo = best_estimate(elems, temp, q, conn_factor=0.5, miter_factor=0.8)
                hi = best_estimate(elems, temp, q, conn_factor=2.0, miter_factor=1.25)
                lr = best_estimate(elems, temp, q, elbow="elbow90_LR")
                lr_hi = best_estimate(elems, temp, q, elbow="elbow90_LR", conn_factor=2.0, miter_factor=1.25)
                table.append(dict(case=key, Q_m3_h=q, C05_margin_kPa=round(ref, 3),
                                  reproduced_margin_kPa=round(rp["margin"], 3), repro_delta=round(rp["margin"] - ref, 9),
                                  C05_K=rp["K"], C05_headers=rp["n_headers"], C05_connectors=rp["n_conn"],
                                  BE_corners=be["n_corners"], BE_K_corners=round(be["K_corners"], 2),
                                  BE_K_headers=round(be["K_headers"], 2), BE_K_connectors=round(be["K_connectors"], 2),
                                  BE_friction_kPa=round(be["friction_kPa"], 2), BE_corners_kPa=round(be["corners_kPa"], 2),
                                  BE_headers_kPa=round(be["headers_kPa"], 2), BE_connectors_kPa=round(be["connectors_kPa"], 2),
                                  HX_kPa=round(be["HX"], 2), valves_kPa=round(be["valves"], 2), meters_kPa=round(be["meters"], 2),
                                  BE_total_kPa=round(be["total"], 2), available_kPa=round(be["available"], 2),
                                  BE_margin_kPa=round(be["margin"], 2), BE_margin_low_kPa=round(hi["margin"], 2),
                                  BE_margin_high_kPa=round(lo["margin"], 2),
                                  LR_elbow_margin_kPa=round(lr["margin"], 2), LR_elbow_margin_low_kPa=round(lr_hi["margin"], 2)))
            # zero-margin flows
            pe = [e for (_, _, e) in path]
            res[key]["Q_zero_margin_C05"] = zero_margin_flow(lambda q: c05_reproduce(pe, temp, q)["margin"])
            res[key]["Q_zero_margin_BE"] = zero_margin_flow(lambda q: best_estimate(elems, temp, q)["margin"])
            res[key]["Q_zero_margin_LR"] = zero_margin_flow(lambda q: best_estimate(elems, temp, q, elbow="elbow90_LR")["margin"])
    save_csv("rt01_hydraulic_duties.csv", table)
    save_json("rt01_hydraulic_paths.json", res)
    for r in table:
        if r["Q_m3_h"] == 2.0:
            print({k: r[k] for k in ("case", "C05_margin_kPa", "reproduced_margin_kPa", "C05_K", "BE_corners", "BE_K_corners",
                                     "BE_K_headers", "BE_K_connectors", "BE_total_kPa", "BE_margin_kPa", "BE_margin_low_kPa",
                                     "BE_margin_high_kPa", "LR_elbow_margin_kPa", "LR_elbow_margin_low_kPa")})
    for k, v in res.items():
        print(k, "Q@0 margin C05 %.3f  BE %.3f  LR %.3f" % (v["Q_zero_margin_C05"], v["Q_zero_margin_BE"], v["Q_zero_margin_LR"]))
        print("   headers:", [(h["node"], h["enter"], h["leave"], h["flow"], h["flow_len_mm"]) for h in v["headers"]])
