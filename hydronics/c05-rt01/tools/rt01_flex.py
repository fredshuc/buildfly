"""RT01-X: thermal-cycling flexibility screen of the bed-side lines.

Every hot/cold reversal swings the lines between each 3-way valve AB port and
its HX, and the HX-to-HX lines through FS and Q, by about 77 K (5 -> 82 C).
Model: 3D linear frame (Euler-Bernoulli, 12-DOF beams) along the as-designed
centre line from anchor to anchor, both anchors fixed (valve body / HX port);
corners are rigid joints (flexibility factor not credited -> conservative for
stress), component bodies (valve, union, FS, Q) 100x stiffer. Displacement
stress range S_E = sqrt((i*Mb)^2 + 4 Mt^2) / Z (B31.3 302.3.5 / 319.4.4 form),
SIF i: single 90 deg miter 2.55, LR elbow 1.39 (B31.3 App. D, h = T R/r2^2 /
(1+cot45)/2 T/r2), threaded joint 2.3 at Rp1/R1/NPT ends, 1.0 elsewhere.
Allowable S_A = f (1.25 Sc + 0.25 Sh), Sc = Sh = 115 MPa (316L), f = 6 N^-0.2.
No supports are modelled (none are defined in C05 for these lines).
"""
import math, numpy as np
from rt01_common import design, save_csv, save_json
from rt01_hydraulics import active_edges, all_paths

E = 195000.0; G = E / 2.6; ALPHA = 16.4e-6; DT = 77.0
OD, T = 33.7, 3.2
A = math.pi / 4 * (OD ** 2 - (OD - 2 * T) ** 2)
I = math.pi / 64 * (OD ** 4 - (OD - 2 * T) ** 4); J = 2 * I; Z = I / (OD / 2)
SIF = {"miter": 0.9 / ((1 + 1) / 2 * T / ((OD - T) / 2)) ** (2 / 3),
       "elbow": 0.9 / (T * 38.1 / ((OD - T) / 2) ** 2) ** (2 / 3)}   # applied to every corner in the elbow variant
SA_BASE = 1.25 * 115 + 0.25 * 115


def beam_k(L, scale=1.0):
    EA, EI, GJ = E * A * scale, E * I * scale, G * J * scale
    k = np.zeros((12, 12))
    k[0, 0] = k[6, 6] = EA / L; k[0, 6] = k[6, 0] = -EA / L
    k[3, 3] = k[9, 9] = GJ / L; k[3, 9] = k[9, 3] = -GJ / L
    for (v, th, s) in ((1, 5, 1), (2, 4, -1)):
        a, b, c, d = 12 * EI / L ** 3, 6 * EI / L ** 2, 4 * EI / L, 2 * EI / L
        k[v, v] = k[v + 6, v + 6] = a; k[v, v + 6] = k[v + 6, v] = -a
        k[v, th] = k[th, v] = s * b; k[v, th + 6] = k[th + 6, v] = s * b
        k[v + 6, th] = k[th, v + 6] = -s * b; k[v + 6, th + 6] = k[th + 6, v + 6] = -s * b
        k[th, th] = k[th + 6, th + 6] = c; k[th, th + 6] = k[th + 6, th] = d
    return k


def rot(p, q):
    x = (np.array(q) - np.array(p)); x /= np.linalg.norm(x)
    ref = np.array([0, 0, 1.0]) if abs(x[2]) < 0.9 else np.array([0, 1.0, 0])
    y = np.cross(ref, x); y /= np.linalg.norm(y); z = np.cross(x, y)
    R = np.vstack([x, y, z]); Tm = np.zeros((12, 12))
    for i in range(4):
        Tm[3 * i:3 * i + 3, 3 * i:3 * i + 3] = R
    return Tm


def chain_points(path, ports, routes):
    pts, rigid = [list(ports[path[0][0]])], []
    for (u, v, e) in path:
        if e["id"] in routes:
            r = routes[e["id"]]; P = r["points"] if r["a"] == u else r["points"][::-1]
            for p in P:
                pts.append(list(p)); rigid.append(False)
        else:
            for p in (ports[u], ports[v]):
                pts.append(list(p)); rigid.append(True)
    # close the chain at the anchor's equipment face (header run + connector to the HX/valve port)
    pts.append(list(ports[path[-1][1]])); rigid.append(False)
    # clean duplicates, mark segment rigidity by the point that ends it
    P, R = [pts[0]], []
    for p, rg in zip(pts[1:], rigid):
        if math.dist(p, P[-1]) > 1e-6:
            P.append(p); R.append(rg)
    return P, R


def solve(P, R, corner_kind, sub=40.0):
    nodes, elems, tags = [np.array(P[0], float)], [], {}
    for i in range(1, len(P)):
        a, b = np.array(P[i - 1], float), np.array(P[i], float)
        n = max(1, int(math.ceil(np.linalg.norm(b - a) / sub)))
        for k in range(1, n + 1):
            nodes.append(a + (b - a) * k / n); elems.append((len(nodes) - 2, len(nodes) - 1, R[i - 1]))
        tags[len(nodes) - 1] = "corner" if 0 < i < len(P) - 1 else "end"
    N = len(nodes); K = np.zeros((6 * N, 6 * N)); F = np.zeros(6 * N); fe = []
    for (a, b, rg) in elems:
        L = np.linalg.norm(nodes[b] - nodes[a]); Tm = rot(nodes[a], nodes[b]); s = 100.0 if rg else 1.0
        kl = beam_k(L, s); kg = Tm.T @ kl @ Tm
        idx = list(range(6 * a, 6 * a + 6)) + list(range(6 * b, 6 * b + 6))
        K[np.ix_(idx, idx)] += kg
        ft = np.zeros(12); P0 = E * A * s * ALPHA * DT; ft[0], ft[6] = -P0, P0
        F[idx] += Tm.T @ ft; fe.append((idx, kl, Tm, ft))
    fixed = list(range(0, 6)) + list(range(6 * (N - 1), 6 * N))
    free = [i for i in range(6 * N) if i not in fixed]
    u = np.zeros(6 * N); u[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
    # element end forces (local), nodal stress ranges
    smax, at, worst = 0.0, None, {}
    for (idx, kl, Tm, ft), (a, b, rg) in zip(fe, elems):
        f = kl @ (Tm @ u[idx]) - ft
        for end, node in ((0, a), (6, b)):
            Mt = abs(f[end + 3]); Mb = math.hypot(f[end + 4], f[end + 5])
            tag = tags.get(node, "")
            i_ = SIF[corner_kind] if tag == "corner" else (2.3 if tag == "end" else 1.0)
            if rg:
                continue
            S = math.sqrt((i_ * Mb) ** 2 + 4 * Mt ** 2) / Z
            if S > worst.get(node, 0):
                worst[node] = S
    node, smax = max(worst.items(), key=lambda t: t[1])
    # anchor reactions
    Ru = K @ u - F
    r0, r1 = Ru[0:6], Ru[6 * (N - 1):]
    return dict(S_E_max_MPa=smax, at=[round(x, 1) for x in nodes[node]], at_tag=tags.get(node, "straight"),
                anchor_start_F_N=float(np.linalg.norm(r0[:3])), anchor_start_M_Nm=float(np.linalg.norm(r0[3:]) / 1000),
                anchor_end_F_N=float(np.linalg.norm(r1[:3])), anchor_end_M_Nm=float(np.linalg.norm(r1[3:]) / 1000),
                free_growth_mm=float(np.linalg.norm(np.array(P[-1]) - np.array(P[0])) * ALPHA * DT))


if __name__ == "__main__":
    d = design(); ports, routes = d["ports"], d["pipe_routes"]
    chains = [("A_L_AB", "H1", "V_A_L:AB", "HX_A_L:P1"), ("A_U_AB", "H1", "V_A_U:AB", "HX_A_U:P7"),
              ("A_bed_link", "H1", "HX_A_L:P7", "HX_A_U:P1"),
              ("B_L_AB", "H2", "V_B_L:AB", "HX_B_L:P1"), ("B_U_AB", "H2", "V_B_U:AB", "HX_B_U:P7"),
              ("B_bed_link", "H2", "HX_B_L:P7", "HX_B_U:P1")]
    out = []
    for name, mode, s, t in chains:
        edges = [e for e in active_edges(mode) if e["kind"] not in ("HX_internal",)]
        path = min(all_paths(s, t, edges), key=len)
        P, R = chain_points(path, ports, routes)
        dev = sum(math.dist(a, b) for a, b in zip(P, P[1:]))
        for kind in ("miter", "elbow"):
            r = solve(P, R, kind)
            for N in (7000, 1e5, 5e5):
                f = min(1.0, 6.0 * N ** -0.2); SA = f * SA_BASE
                out.append(dict(chain=name, anchors=f"{s} .. {t}", centreline_mm=round(dev, 0), corners=len(P) - 2,
                                corner_type=kind, SIF=round(SIF[kind], 2), cycles_N=int(N), f=round(f, 3),
                                S_A_MPa=round(SA, 1), S_E_max_MPa=round(r["S_E_max_MPa"], 1), ratio=round(r["S_E_max_MPa"] / SA, 2),
                                at=r["at"], at_tag=r["at_tag"],
                                anchor_start_F_N=round(r["anchor_start_F_N"]), anchor_start_M_Nm=round(r["anchor_start_M_Nm"], 1),
                                anchor_end_F_N=round(r["anchor_end_F_N"]), anchor_end_M_Nm=round(r["anchor_end_M_Nm"], 1)))
            print(out[-1])
    save_csv("rt01_flex_screen.csv", out)
    save_json("rt01_flex_sif.json", dict(SIF=SIF, Z_mm3=Z, I_mm4=I, A_mm2=A, alpha=ALPHA, dT=DT, E=E))
