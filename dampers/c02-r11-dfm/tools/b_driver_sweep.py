"""Sweep of the B-model drivers (rolling arm, seat friction, crown radius, sphere radius, kt) on MAX_UNEQUAL.
Usage: python -I b_driver_sweep.py <R9 evidence dir> [out.json]"""
import sys, json, os
OUTP = sys.argv[2] if len(sys.argv) > 2 else 'results_b_driver_sweep.json'
sys.argv = [sys.argv[0], sys.argv[1], os.devnull]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'b_equaliser_sensitivity.py')).read().split('rows = []')[0]
g = {}; exec(compile(src, 'b_model', 'exec'), g)
r = g['controls'][0][1]; rows = []
for label, kw in [('baseline mu.12 arm.03 Rs20 Rc4', dict(mu_seat=.12, rolling_arm=.03, R_sphere=20)),
                  ('rolling arm 0.005', dict(mu_seat=.12, rolling_arm=.005, R_sphere=20)),
                  ('seat mu 0.05', dict(mu_seat=.05, rolling_arm=.03, R_sphere=20)),
                  ('crown R2', dict(mu_seat=.12, rolling_arm=.03, R_sphere=20, R_crown=2.0)),
                  ('crown R8', dict(mu_seat=.12, rolling_arm=.03, R_sphere=20, R_crown=8.0)),
                  ('Rs 30', dict(mu_seat=.12, rolling_arm=.03, R_sphere=30)),
                  ('kt 3e5', dict(mu_seat=.12, rolling_arm=.03, R_sphere=20, kt=3e5)),
                  ('kt 1e6', dict(mu_seat=.12, rolling_arm=.03, R_sphere=20, kt=1e6))]:
    res = g['run'](r, **kw); res['case'] = label; rows.append(res)
    print(f"{label:34s} thermal/cool {res['max_thermal_or_cool_deg']:.6f}  residual {res['residual_deg']:+.6f}  heat {res['pure_heat_deg']:.6f}")
json.dump(rows, open(OUTP, 'w'), indent=1)
