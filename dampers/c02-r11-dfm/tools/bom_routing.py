"""Process-route classification and tolerance digest for the C02 R11 native database.
Usage: python -I bom_routing.py <native dir> <BOM_FULL.csv> <out.json> <out.csv>"""
import sys, json, re, csv, collections
P = json.load(open(f"{sys.argv[1]}/PARAMETRIC_PARTS_C02.json"))
O = json.load(open(f"{sys.argv[1]}/OCCURRENCES_C02.json"))
bom = {r['PN']: r for r in csv.DictReader(open(sys.argv[2], encoding='utf-8-sig'))}
qty = collections.Counter(o['pn'] for o in O)
SEAL = re.compile(r'Rogers|EPDM|PTFE|iglidur|mica|silica|foil', re.I)
TOL = re.compile(r'(?:±|\+)\s?0\.0[0-3]\d*|平面度\s?0\.0[0-3]|Ra\s?0\.[0-4]|[0-9]+(?:m6|h6|H7|p6|s6)|HRC|淬硬|轮廓0\.0[0-3]|同轴0\.0[0-5]|平行0\.0[0-3]|0\.01\b')
WELD = re.compile(r'焊|a=?\d(?:\.\d)?\s*(?:连续|角焊)|a[1-4](?:\.5)?焊|ER308L')
def route(p):
    k, m = p.get('kind'), p.get('material', '')
    ft = [f['type'] for f in p['features']]
    b = p.get('bbox') or [0]*6; dims = sorted(round(b[i+3]-b[i], 2) for i in range(3))
    if k in ('BUY', 'PURCHASE_SUBPART'): return 'PURCHASED'
    if k in ('WELD_ASSEMBLY',): return 'WELDMENT'
    if k in ('KIT', 'KIT_ASSEMBLY', 'REFERENCE'): return 'KIT/REFERENCE'
    if SEAL.search(m): return 'SEAL/GASKET/INSULATION (die/waterjet/skive)'
    if 'shim' in m: return 'PRECISION SHIM (laser/etch)'
    if any(t in ft for t in ('shaft', 'steppedshaft', 'tube', 'pin', 'washer', 'ring', 'guided_screw', 'solid_head_stud', 'male_thread', 'disc_spring')): return 'TURNED'
    if dims[0] <= 3.0 and dims[1] > 20: return 'SHEET (laser + deburr, some bend/weld)'
    return 'MILLED/PRISMATIC (plate or bar)'
rows = []
for p in P:
    notes = ' '.join(p.get('notes') or [])
    r = bom.get(p['pn'], {})
    rows.append(dict(pn=p['pn'], name=p.get('name'), material=p.get('material'), route=route(p),
                     instances=qty.get(p['pn'], 0), status=r.get('status', p.get('engineering_status', '')),
                     revision=p.get('revision'), tight_tol_tokens=sorted(set(TOL.findall(notes))),
                     weld_note=bool(WELD.search(notes))))
summary = collections.defaultdict(lambda: dict(pns=0, instances=0, pns_with_tight_tol=0, pns_with_weld_notes=0))
for r in rows:
    s = summary[r['route']]; s['pns'] += 1; s['instances'] += r['instances']
    s['pns_with_tight_tol'] += bool(r['tight_tol_tokens']); s['pns_with_weld_notes'] += r['weld_note']
status = collections.Counter(r['status'] for r in rows)
purchased = [dict(pn=r['pn'], name=r['name'], instances=r['instances']) for r in rows if r['route'] == 'PURCHASED']
tight = [dict(pn=r['pn'], name=r['name'], route=r['route'], tokens=r['tight_tol_tokens']) for r in rows if r['tight_tol_tokens']]
json.dump(dict(summary=summary, status=status, purchased=purchased, tight_tolerance_parts=tight), open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
with open(sys.argv[4], 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader()
    for r in rows: r = dict(r); r['tight_tol_tokens'] = ' '.join(r['tight_tol_tokens']); w.writerow(r)
for k, v in sorted(summary.items()): print(f"{k:45s} {v}")
print(status); print(len(purchased), 'purchased PNs'); print(len(tight), 'PNs with tight-tolerance tokens')
for t in tight: print('  ', t['pn'], t['name'], t['tokens'])
