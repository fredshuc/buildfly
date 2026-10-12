"""Grid over the two measurable drivers (crown rolling-hysteresis arm, encoder-half grip stiffness kt),
worst control (MAX_UNEQUAL/MIRROR, seat mu 0.12). Usage: python -I b_measurement_grid.py <R9 evidence dir> <out.json>"""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__)); ev, outp = sys.argv[1], sys.argv[2]
src = open(os.path.join(here, 'b_equaliser_sensitivity.py')).read().split('rows = []')[0]
sys.argv = [sys.argv[0], ev, os.devnull]; g = {}; exec(compile(src, 'b_model', 'exec'), g)
rows = []
for arm in [0.030, 0.015, 0.005]:
    for kt in [1e5, 3e5, 1e6]:
        worst = None
        for name, r in g['controls'][:2]:
            res = g['run'](r, mu_seat=.12, rolling_arm=arm, R_sphere=20, kt=kt)
            if worst is None or res['max_thermal_or_cool_deg'] > worst['max_thermal_or_cool_deg']: worst = dict(res, control=name)
        worst.update(rolling_arm_mm=arm, kt_Nmm_rad=kt); rows.append(worst)
        print(f"arm {arm:.3f} mm  kt {kt:.0e}  thermal/cool {worst['max_thermal_or_cool_deg']:.4f} deg  residual {abs(worst['residual_deg']):.4f} deg  proof-peak {worst['max_any_deg']:.4f} deg")
json.dump(rows, open(outp, 'w'), indent=1)
