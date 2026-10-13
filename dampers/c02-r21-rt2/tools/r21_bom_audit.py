"""Consistency audit of the R21 factory entry index, net-need BOM and classified gaps (RT2-01).
Usage: python -I r21_bom_audit.py <R21_WORK/deliverables> <out.json>"""
import sys, csv, json, collections, os
D = sys.argv[1]
def rd(p): return list(csv.DictReader(open(os.path.join(D, p), encoding='utf-8-sig')))
idx = rd('tables/R21_CURRENT_FACTORY_ENTRY_INDEX.csv'); bom = rd('tables/R21_NET_NEED_BOM.csv'); gaps = rd('tables/R21_CLASSIFIED_GAPS.csv')
def n(x):
    try: return int(float(x))
    except Exception: return 0
out = {}
out['index_rows'] = len(idx); out['bom_rows'] = len(bom); out['gap_rows'] = len(gaps)
out['bom_need_sum'] = sum(n(r['net_physical_need']) for r in bom)
out['bom_issued_sum'] = sum(n(r['issued_scoped_quantity']) for r in bom)
out['bom_unissued_sum'] = sum(n(r['not_yet_issued_quantity']) for r in bom)
out['bom_excluded_station_sum'] = sum(n(r['excluded_independent_station_quantity']) for r in bom)
# row-level arithmetic: need == issued + unissued ?
bad = [dict(PN=r['PN'], need=r['net_physical_need'], issued=r['issued_scoped_quantity'], unissued=r['not_yet_issued_quantity'])
       for r in bom if n(r['net_physical_need']) != n(r['issued_scoped_quantity']) + n(r['not_yet_issued_quantity'])]
out['rows_need_ne_issued_plus_unissued'] = bad
over = [dict(PN=r['PN'], need=r['net_physical_need'], issued=r['issued_scoped_quantity']) for r in bom if n(r['issued_scoped_quantity']) > n(r['net_physical_need'])]
out['rows_issued_exceeds_need'] = over
dup = [k for k, v in collections.Counter((r['PN'], r['physical_family']) for r in bom).items() if v > 1]
out['bom_duplicate_PN_family'] = dup
# index: PN+allocation unique?
ia = collections.Counter((r['PN'], r['allocation']) for r in idx)
out['index_duplicate_PN_allocation'] = [k for k, v in ia.items() if v > 1]
out['index_allocations'] = collections.Counter(r['allocation'] for r in idx)
out['index_release'] = collections.Counter(r['release'] for r in idx)
# PN issued in BOM but missing from index; and index PN with product allocation but zero issued in BOM
idx_pn = {r['PN'] for r in idx}
out['bom_issued_PN_not_in_index'] = sorted({r['PN'] for r in bom if n(r['issued_scoped_quantity']) > 0 and r['PN'] not in idx_pn})
bom_pn = {r['PN']: r for r in bom}
out['index_PN_not_in_bom'] = sorted({r['PN'] for r in idx if r['PN'] not in bom_pn})
# index entries pointing to missing files
missing = []
for r in idx:
    p = os.path.join(D, 'factory', r['packet'])
    if not os.path.exists(p): missing.append(r['packet'])
out['index_packets_missing'] = missing[:20]; out['index_packets_missing_count'] = len(missing)
# gaps
out['gap_class'] = collections.Counter(r['gap_class'] for r in gaps)
out['gap_unissued_pieces_by_class'] = {k: sum(n(r['not_yet_issued_quantity']) for r in gaps if r['gap_class'] == k) for k in out['gap_class']}
out['gap_rows_by_class_PN'] = {k: [r['PN'] for r in gaps if r['gap_class'] == k] for k in out['gap_class']}
# BOM rows with unissued>0 but no gap row
gp = {r['PN'] for r in gaps}
out['unissued_without_gap_row'] = sorted({r['PN'] for r in bom if n(r['not_yet_issued_quantity']) > 0 and r['PN'] not in gp})
out['kind_summary'] = {k: dict(rows=sum(1 for r in bom if r['kind'] == k), need=sum(n(r['net_physical_need']) for r in bom if r['kind'] == k),
                              issued=sum(n(r['issued_scoped_quantity']) for r in bom if r['kind'] == k),
                              unissued=sum(n(r['not_yet_issued_quantity']) for r in bom if r['kind'] == k)) for k in sorted({r['kind'] for r in bom})}
json.dump(out, open(sys.argv[2], 'w'), indent=1, default=list)
print(json.dumps(out, indent=1, default=list)[:6000])
