"""Map R21 FASTENER_OR_SMALL_HARDWARE enquiry rows to standard designations where the CAD envelope matches the
standard's nominal head/nut/washer dimensions; flag mismatches for an engineering decision.
Usage: python -I r21_fastener_map.py <R21 tables dir> <out.csv>
Reference nominal dimensions (ISO 4762 dk/k/s; ISO 7089 d1/d2/h; ISO 4032 m/s; ISO 7042 m/s) are standard
table values typed here; verify against the purchased standard edition."""
import sys, csv, json, re
ISO4762 = {'M2': (3.8, 2, 1.5), 'M2.5': (4.5, 2.5, 2), 'M3': (5.5, 3, 2.5), 'M4': (7, 4, 3), 'M5': (8.5, 5, 4), 'M6': (10, 6, 5),
           'M8': (13, 8, 6), 'M10': (16, 10, 8), 'M12': (18, 12, 10), 'M16': (24, 16, 14)}
ISO7380 = {'M3': (5.7, 1.65), 'M4': (7.6, 2.2), 'M5': (9.5, 2.75), 'M6': (10.5, 3.3), 'M8': (14, 4.4), 'M10': (17.5, 5.5)}
ISO7089 = {'M3': (3.2, 7, 0.5), 'M4': (4.3, 9, 0.8), 'M5': (5.3, 10, 1.0), 'M6': (6.4, 12, 1.6), 'M8': (8.4, 16, 1.6), 'M10': (10.5, 20, 2.0),
           'M12': (13, 24, 2.5), 'M16': (17, 30, 3.0)}
ISO4032 = {'M3': (2.4, 5.5), 'M4': (3.2, 7), 'M6': (5.2, 10), 'M8': (6.8, 13), 'M10': (8.4, 16), 'M12': (10.8, 18), 'M16': (14.8, 24)}
ISO7042 = {'M5': (5.1, 8), 'M6': (6.0, 10), 'M8': (8.0, 13), 'M10': (10.0, 16), 'M12': (12.0, 18), 'M16': (16.0, 24)}
rows = list(csv.DictReader(open(f"{sys.argv[1]}/R21_PURCHASE_TECHNICAL_ENQUIRIES.csv", encoding='utf-8-sig')))
out = []
def thread_d(t): return t.split('-')[0]
for r in rows:
    if r['purchase_group'] != 'FASTENER_OR_SMALL_HARDWARE': continue
    f = json.loads(r['inherited_feature_contract'] or '[]'); notes = r['inherited_notes']; d = f[0] if f else {}
    desig, status, note = '', 'NEEDS_DECISION', ''
    m = re.search(r'ISO\s?(\d{3,4})', notes)
    if m and not d:
        desig = re.search(r'ISO\s?\d{3,4}[^;,"]*', notes).group(0).strip(); status = 'STANDARD_NAMED_IN_NOTES'
    elif d.get('type') in ('fastener', 'bolt'):
        th = thread_d(d['thread']); L = d.get('underhead_L', d.get('length'))
        ref = ISO4762.get(th)
        if ref and abs(d['head_d'] - ref[0]) < 0.3 and abs(d['head_h'] - ref[1]) < 0.3:
            desig = f"ISO 4762 {th}x{L:g} {r['material']}"; status = 'MATCHES_ISO4762'
            if d.get('hex') and abs(d['hex'] - ref[2]) > 0.01: note = f"CAD hex {d['hex']} vs ISO {ref[2]} (envelope only)"
            if d.get('thread_length') and d['thread_length'] >= L: note = (note + '; ' if note else '') + 'CAD full thread: confirm standard thread length b covers required engagement'
        elif th in ISO7380 and abs(d['head_d'] - ISO7380[th][0]) < 0.3 and abs(d['head_h'] - ISO7380[th][1]) < 0.3:
            desig = f"ISO 7380-1 {th}x{L:g} {r['material']}"; status = 'MATCHES_ISO7380'
            note = 'confirm stainless property class offered for ISO 7380 (A4-70 more common than A4-80)'
        else:
            note = f"head {d.get('head_d')}x{d.get('head_h')} not ISO 4762 {th} {ref[:2] if ref else ''} nor ISO 7380"
    elif d.get('type') == 'washer':
        hit = [k for k, v in ISO7089.items() if abs(v[1] - d['od']) < 0.2 and abs(v[2] - d['t']) < 0.05]
        if hit and 'R8_HOOD' not in r['PN'] and 'HARD' not in r['PN']:
            desig = f"ISO 7089 {hit[0]} {r['material']}"; status = 'MATCHES_ISO7089'
            if abs(ISO7089[hit[0]][0] - d['id']) > 0.05: note = f"CAD id {d['id']} vs ISO {ISO7089[hit[0]][0]}"
        else:
            note = f"{d['od']}/{d['id']}x{d['t']} not ISO 7089 nominal" + (' (custom tolerance/material in notes)' if ('R8_HOOD' in r['PN'] or 'HARD' in r['PN']) else '')
    elif d.get('type') == 'hexnut':
        th = d['thread']; h = d['height']; s = d['across_flats']
        if th in ISO7042 and abs(ISO7042[th][0] - h) < 0.3 and abs(ISO7042[th][1] - s) < 0.3:
            desig = f"ISO 7042 {th} {r['material']} (all-metal prevailing torque)"; status = 'MATCHES_ISO7042'
        elif th in ISO4032 and abs(ISO4032[th][1] - s) < 0.3:
            status = 'NEEDS_DECISION'; note = f"{th} m{h} s{s}: height matches a polyamide-insert nut (e.g. ISO 10511/DIN 985), BOM says all-metal lock nut; decide"
        else:
            note = f"{th} m{h} s{s}: no ISO 7042 size (BOM says all-metal lock nut); choose standard"
    out.append(dict(PN=r['PN'], net_need=r['net_need'], material=r['material'], proposed_designation=desig, status=status, note=note))
with open(sys.argv[2], 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
import collections
c = collections.Counter(o['status'] for o in out); pcs = collections.Counter()
for o in out: pcs[o['status']] += int(float(o['net_need'] or 0))
print(c, pcs)
for o in out:
    if o['status'] == 'NEEDS_DECISION' or o['note']: print(o['PN'], o['net_need'], o['status'], o['proposed_designation'], '|', o['note'])
