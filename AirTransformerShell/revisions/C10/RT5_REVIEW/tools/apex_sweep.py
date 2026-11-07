"""Sweep the top-plenum apex depth g (linear taper from the measured 159 mm at X-270 to g at X590,
bottom plenum as measured in C10) through c09_header_model.py. Usage: python apex_sweep.py <profile.json> <out.json>"""
import json, sys, subprocess, os, tempfile
base = json.load(open(sys.argv[1])); here = os.path.dirname(os.path.abspath(__file__)); res = []
for g in (8, 20, 30, 40, 50, 67.5, 90, 120):
    prof = []
    for r in base:
        r = dict(r); X = r['X']
        if X >= -270: r['top_depth_mm'] = 159.07 + (g - 159.07) * (X + 270) / 860
        prof.append(r)
    with tempfile.TemporaryDirectory() as td:
        pi, po = os.path.join(td, 'p.json'), os.path.join(td, 'o.json')
        json.dump(prof, open(pi, 'w')); subprocess.run([sys.executable, os.path.join(here, 'c09_header_model.py'), pi, po], capture_output=True, check=True)
        cases = json.load(open(po))['cases']
    for c in cases:
        if c['cores_in_series'] == 2 and c['frame_interior_m'] == 0.032 and ((c['mode'], c['Q_m3h']) in (('P', 4870), ('R', 2435))):
            res.append(dict(apex_mm=g, mode=c['mode'], Q=c['Q_m3h'], k_div=c['k_div'], cv=c['cv_pct'], mn=c['min_over_mean'], mx=c['max_over_mean'], last100=c['last_100mm_over_mean']))
            print(res[-1], flush=True)
json.dump(res, open(sys.argv[2], 'w'), indent=1)
