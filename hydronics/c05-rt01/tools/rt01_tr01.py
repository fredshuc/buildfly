"""RT01-T: what valve stroke time makes a signal-loss closure acceptable?

Quasi-steady closure of one 1" ball valve (Kv_max 47.9, C05 value) in series with
the rest of the loop (lumped Kv_sys) at constant driving pressure; linear angle
travel over T_stroke. Inherent characteristic Kv/Kv_max = x^n (x = opening
fraction), n = 3 base, 2 and 4 sensitivity (typical full-bore ball valve; vendor
curve required). Outputs, per case:
  t_eff  = time for flow to fall from 90 % to 10 % of initial,
  a_max  = max |dv/dt| in the 27.3 mm bore,
  T_min  = shortest stroke giving a_max <= 0.5 m/s2 (C05/TR01 retained limit),
  T_8s   = shortest stroke giving t_eff >= 8 s (C05 D02 target),
  dp     = rigid-column surge rho * L * a_max for L = 13 m (internal) and per
           100 m of external source pipe (Joukowsky bound only for t_eff < 2L/a).
Valworx states the DPS drives closed on loss of 4-20 mA at motor speed and
holds position on loss of power unless BSR is fitted (manufacturer pages,
accessed 2026-10-14); stroke time on signal loss therefore equals powered
stroke time unless the vendor states otherwise - to be bench-measured.
"""
import math
from rt01_common import save_csv, save_json

D = 0.0273; A = math.pi * D ** 2 / 4; KV_MAX = 47.9; RHO = 1000.0
A_LIM = 0.5


def flow_frac(x, kv_sys, n):
    kv = KV_MAX * max(x, 0.0) ** n
    if kv <= 0:
        return 0.0
    r = (kv_sys / kv) ** 2 - (kv_sys / KV_MAX) ** 2
    return 1 / math.sqrt(1 + r)


def closure(T, q0, kv_sys, n, dt=0.002):
    v0 = q0 / 3600 / A
    t, prev, amax, t90, t10 = 0.0, 1.0, 0.0, None, None
    while t < T:
        t += dt
        phi = flow_frac(1 - t / T, kv_sys, n)
        a = v0 * (prev - phi) / dt
        amax = max(amax, a)
        if t90 is None and phi <= 0.9:
            t90 = t
        if t10 is None and phi <= 0.1:
            t10 = t
        prev = phi
    return (t10 - t90) if (t90 is not None and t10 is not None) else 0.0, amax


def solve_T(q0, kv_sys, n, target):
    lo, hi = 0.5, 600.0
    for _ in range(40):
        m = (lo + hi) / 2
        te, am = closure(m, q0, kv_sys, n, dt=m / 20000)
        ok = am <= A_LIM if target == "a" else te >= 8.0
        hi, lo = (m, lo) if ok else (hi, m)
    return hi


if __name__ == "__main__":
    cases = [  # name, q0 m3/h, driving dp across loop excl. this valve (bar)
        ("nominal_2.0_pump", 2.0, 0.59),       # BE: available minus 15 kPa
        ("source_cap_3.5", 3.5, 2.0),          # D07 hard cap, 0.2 MPa admission
        ("emergency_7.0", 7.0, 2.0),           # C05 D02 emergency bound
    ]
    out = []
    for name, q0, dp in cases:
        kv_sys = q0 / math.sqrt(dp)
        for n in (2, 3, 4):
            te9, am9 = closure(9.0, q0, kv_sys, n)
            Ta = solve_T(q0, kv_sys, n, "a"); T8 = solve_T(q0, kv_sys, n, "t8")
            out.append(dict(case=name, q0_m3h=q0, v0_m_s=round(q0 / 3600 / A, 3), Kv_sys=round(kv_sys, 2), n=n,
                            t_eff_at_9s_stroke_s=round(te9, 2), a_max_at_9s_m_s2=round(am9, 3),
                            dp_internal13m_at_9s_kPa=round(RHO * 13 * am9 / 1000, 1),
                            dp_per100m_external_at_9s_kPa=round(RHO * 100 * am9 / 1000, 1),
                            T_stroke_min_for_a_le_0p5_s=round(Ta, 1), T_stroke_min_for_teff_ge_8s_s=round(T8, 1)))
            print(out[-1])
    # Joukowsky reference
    a_w = math.sqrt(2.2e9 / RHO / (1 + 2.2e9 * 0.0273 / (193e9 * 0.0032)))
    jk = {q: RHO * a_w * q / 3600 / A / 1000 for q in (2.0, 3.5, 7.0)}
    save_csv("rt01_tr01_closure.csv", out)
    save_json("rt01_tr01_reference.json", dict(wave_speed_m_s=a_w, joukowsky_kPa=jk,
                                               note="instantaneous-closure bound; applies only if t_eff < 2L/a"))
    print("a =", round(a_w), "m/s; Joukowsky kPa:", {k: round(v) for k, v in jk.items()})
