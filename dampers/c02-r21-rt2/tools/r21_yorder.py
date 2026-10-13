"""Order of the R-configuration drive-line bodies along the shaft axis (world Y) to establish the torque path
(input gear -> stop arm -> leaf). Prints Y range and bbox of selected parts for occurrences near the R1 axis.
Usage: python -I r21_yorder.py <native dir> <cfg P|R>"""
import sys, os, json, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from native import bbox
spec = importlib.util.spec_from_file_location('c', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'r21_common.py'))
H = importlib.util.module_from_spec(spec); spec.loader.exec_module(H)
NAT, cfg = sys.argv[1], sys.argv[2]; H.init(NAT)
O = json.load(open(f"{NAT}/R20_{cfg}_OCCURRENCES.json"))
rows = []
for o in O:
    b = bbox(H.place(o))
    # near either shaft axis: X in [-82-60,-82+60] or [83-60, 83+60], Z in [1583-60,1583+60]
    near = any(abs((b[0] + b[3]) / 2 - x) < 60 for x in (-82, 83)) and abs((b[2] + b[5]) / 2 - 1583) < 60
    if near and (b[3] - b[0]) < 260:
        rows.append((b[1], b[4], o['pn'], o['occurrence'], o.get('moving'), o['source'], [round(v, 1) for v in b]))
for r in sorted(rows): print(f"{r[0]:9.1f} {r[1]:9.1f} {r[2]:16s} {r[3]:34s} {str(r[4]):5s} {r[5]:5s} {r[6]}")
