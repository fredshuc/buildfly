"""1-D Z-manifold distribution model for one C09 bed, using the measured plenum profiles.
Usage: python c09_header_model.py <plenum_profile_bedA.json> <out.json>
Geometry: coil length 1.000 m along X (fin X -410..590), width W = 0.630 m (seat span).
Top plenum depth d_top(x): ray-cast roof (AIR_TOP_SPLITTER) minus Z1175, capped at 0.180 m (Pin height)
upstream of the splitter start; optional +delta for open frame interior above the fin top (1143.35).
Bottom plenum depth d_bot(x): Z620 minus floor, capped at 0.248 m (Pout seat height 372..552 + 68 frame).
P (S1): dividing = top, inlet at x=0 (-X); combining = bottom, outlet at x=1 (+X).  Z-type.
R (S2): dividing = bottom, inlet at x=1 (+X, Rin floor opening); combining = top, outlet at x=0 (Rout). Z-type.
Coil: two cores in series per band, dp = n*60 Pa*(0.6 v/2.21 + 0.4 (v/2.21)^2), n = 1 or 2 (assumption:
no C05 air-side curve is in the package; 60 Pa/core at 2.21 m/s is the RT3 placeholder).
Header: dividing regain k_d, combining loss k_c, Darcy f = 0.02. Inlet-jet momentum, damper wakes,
the 40 mm HX rail shadow and inter-stage lateral mixing are NOT modelled."""
import json, sys, math
import numpy as np
rho, W, H, N = 1.18, 0.630, 1.0, 50
prof = json.load(open(sys.argv[1]))
X = np.array([r['X'] for r in prof], float); xs = (X + 410) / 1000
dt = np.array([r['top_depth_mm'] for r in prof], float) / 1000
db = np.array([r['bottom_depth_mm'] for r in prof], float) / 1000
dt = np.minimum(dt, 0.180)
db = np.where(X > 370, 0.248, np.minimum(db, 0.248))
def prof_at(arr, x): return np.interp(x, xs, arr)
def coil(v, n): return n * 60 * (0.6 * v / 2.21 + 0.4 * (v / 2.21) ** 2)
def invcoil(p, n):
    if p <= 0: return 0.0
    a, b = n * 60 * 0.6 / 2.21, n * 60 * 0.4 / 2.21 ** 2
    return (-a + math.sqrt(a * a + 4 * b * p)) / (2 * b)
def dh(d): d = max(d, 1e-3); return 2 * W * d / (W + d)
def solve(Q, mode, n, kd, kc, delta, f=0.02):
    xb = np.linspace(0, H, N + 1); dz = H / N
    top = prof_at(dt, xb) + delta; bot = prof_at(db, xb)
    if mode == 'P': ddiv, dcom, inlet0 = top, bot, True
    else: ddiv, dcom, inlet0 = bot, top, False
    q = np.full(N, Q / N)
    for it in range(600):
        if inlet0:   # flow in +x in both headers
            Qd = np.array([q[i:].sum() for i in range(N + 1)]); Qc = np.array([q[:i].sum() for i in range(N + 1)])
        else:        # flow in -x in both headers
            Qd = np.array([q[:i].sum() for i in range(N + 1)]); Qc = np.array([q[i:].sum() for i in range(N + 1)])
        Vd = Qd / (W * np.maximum(ddiv, 1e-3)); Vc = Qc / (W * np.maximum(dcom, 1e-3))
        pd = np.zeros(N); pc = np.zeros(N)
        order = range(N) if inlet0 else range(N - 1, -1, -1)
        p = 0.0
        for i in order:   # dividing: march downstream from inlet
            up, dn = (i, i + 1) if inlet0 else (i + 1, i)
            p += kd * rho / 2 * (Vd[up] ** 2 - Vd[dn] ** 2) - f * dz / dh(ddiv[up]) * rho / 2 * Vd[up] ** 2
            pd[i] = p
        p = 0.0
        for i in order:   # combining: march downstream from closed end
            up, dn = (i, i + 1) if inlet0 else (i + 1, i)
            p += -kc * rho / 2 * (Vc[dn] ** 2 - Vc[up] ** 2) - f * dz / dh(dcom[dn]) * rho / 2 * Vc[dn] ** 2
            pc[i] = p
        dpi = pd - pc
        lo, hi = -2000, 4000
        for _ in range(70):
            mid = (lo + hi) / 2
            if sum(invcoil(mid + x, n) for x in dpi) * W * dz > Q: hi = mid
            else: lo = mid
        qn = np.array([invcoil((lo + hi) / 2 + x, n) for x in dpi]) * W * dz
        if np.max(np.abs(qn - q)) < 1e-9 * Q: q = qn; break
        q = 0.7 * q + 0.3 * qn
    v = q / (W * dz); r = v / v.mean()
    last = r[xb[1:] > 0.9].mean()
    return dict(face_v_mean_ms=round(float(v.mean()), 3), min_over_mean=round(float(r.min()), 3), max_over_mean=round(float(r.max()), 3),
                cv_pct=round(float(r.std() * 100), 2), last_100mm_over_mean=round(float(last), 3),
                band10=[round(float(b), 3) for b in r.reshape(10, -1).mean(1)], iterations=it)
out = dict(assumptions=__doc__, cases=[])
for mode, Q in (('P', 4870), ('P', 2435), ('R', 2435), ('R', 4870)):
    for n in (1, 2):
        for kd, kc in ((0.6, 1.8), (1.0, 2.2)):
            for delta in (0.0, 0.032):
                r = solve(Q / 3600, mode, n, kd, kc, delta)
                out['cases'].append(dict(mode=mode, Q_m3h=Q, cores_in_series=n, k_div=kd, k_comb=kc, frame_interior_m=delta, **r))
                print(mode, Q, n, kd, kc, delta, {k: r[k] for k in ('min_over_mean', 'max_over_mean', 'cv_pct', 'last_100mm_over_mean')})
json.dump(out, open(sys.argv[2], 'w'), indent=1)
