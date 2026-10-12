"""Mass/CG estimate by physical class for the R16 P and R configurations (MAKE parts: volume x density;
purchased: catalogue mass where the BOM states it, else proxy volume x 7.85e-6 flagged as an upper bound).
Usage: python -I r16_mass.py <native dir> <out.json>"""
import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r16_native import R16
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
def rho(mat):
    m = mat.lower()
    if 'ptfe' in m: return 2.2e-6
    if 'rogers' in m or 'epdm' in m or 'foam' in m: return 0.35e-6
    if 'c93200' in m or 'cusn' in m or 'bronze' in m: return 8.8e-6
    if 'silica' in m or 'mica' in m: return 0.3e-6
    return 7.9e-6
CAT = {'BUY531': 4.0, 'BUY520': 1.98, 'BUY521': 1.98, 'BUY703': 0.5, 'BUY704': 0.016}
out = {}
for cfg in ['P', 'R']:
    N = R16(sys.argv[1], cfg); groups = {}
    for q in N.O:
        p = N.P[q['pn']]; s = N.world(q); g = GProp_GProps(); BRepGProp.VolumeProperties_s(s, g)
        v = abs(g.Mass()); c = g.CentreOfMass()
        mm = re.search(r'mass\s*([0-9.]+)\s*kg', p.get('material', ''))
        if q['pn'] in CAT: m, flag = CAT[q['pn']], 'catalogue'
        elif mm: m, flag = float(mm.group(1)), 'catalogue'
        else: m, flag = v * rho(p.get('material', '')), ('proxy_upper' if p.get('kind') == 'BUY' else 'volume')
        key = 'WET_VALVE' if q['source'] == 'R12' and q['physical_class'] in ('PRODUCT', 'WELDED_PRODUCT', 'PURCHASED_COMPLETE', 'LOCAL_RECEIVER_CANDIDATE') else \
              'WET_FIXTURE' if q['physical_class'] == 'INDEPENDENT_FIXTURE' else \
              ('RIG_FRAME' if q['pn'].startswith(('TF90', 'G90')) and q['pn'] not in ('TF900', 'TF901', 'TF902') else 'RIG_DRIVE')
        G = groups.setdefault(key, dict(mass_kg=0.0, mx=0.0, my=0.0, mz=0.0, proxy_kg=0.0))
        G['mass_kg'] += m; G['mx'] += m * c.X(); G['my'] += m * c.Y(); G['mz'] += m * c.Z()
        if flag == 'proxy_upper': G['proxy_kg'] += m
    for k, G in groups.items():
        M = G['mass_kg']; G['cg_world_mm'] = [round(G['mx'] / M, 1), round(G['my'] / M, 1), round(G['mz'] / M, 1)]
        for a in ('mx', 'my', 'mz'): G.pop(a)
        G['mass_kg'] = round(M, 1); G['proxy_kg'] = round(G['proxy_kg'], 1)
    out[cfg] = groups
json.dump(out, open(sys.argv[2], 'w'), indent=1); print(json.dumps(out, indent=1))
