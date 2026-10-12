"""Propose release waves for the P1 kit from R16_CONFIGURED_MANUFACTURING_GAPS.csv.
Classification rules are explicit below; the output is a planning proposal for L1, not a release.
Usage: python -I r16_release_waves.py <R16 tables dir> <out.csv> <out_summary.json>"""
import sys, csv, json, collections
rows = list(csv.DictReader(open(f"{sys.argv[1]}/R16_CONFIGURED_MANUFACTURING_GAPS.csv", encoding='utf-8-sig')))
def n(x):
    try: return int(float(x))
    except Exception: return 0
WET_STABLE = {'P101','P102A','P102B','P102C','P102D','P102E','P103B','P103F','P104','P105A','P105B','P106','P109','P110',
              'R101','R102A','R102B','R103B','R103F','R104','R105A','R106','R109','R110','R112','R113',
              'S301A','S301B','S301C','S303','S311','S312','S313','F602','F603','STD01PC'}
FEEDBACK_FRAME = {'A705','A706','A707','A709','A710'}
BLOCKED_ROOT = {'P107','G840P1','G840P2','G843','R107'}
WET_FIXTURE = {'F620','F621','F622','F623','P107B'}
GLAND_EXT = {'J401','J402','STD04C','J403','J404','J405','J406','J407','J408','STD03C','STD05B','F604','BUY548','BUY402','HW_N6','HW_W6_1p6_12'}
B_EXT = {'A703P','A703R','A704R8','B850','B851','B852','B853','HW_R11_GUIDE_M5','BUY_R9_DS001500A','HW_R9_HARD_W5'}
CRITICAL_BUY = {'BUY504','BUY520','BUY521','BUY530','BUY531','BUY703','BUY704','BUY_R13_7206','BUY_R13_BK2'}
ECO_REWORK = {'D886': 'ECO-C: add keyway under arm root (re-phase +90 deg on P2)',
              'TF903': 'ECO-A: two new M8 holes for relocated wet-end TF909 posts',
              'G900': 'ECO-A: shorten wet end 45.5 mm and re-drill post holes',
              'TF909': 'ECO-A: relocate two wet-end posts -45.5 mm (no part change)',
              'G901': 'ECO-A: relocate -45.5 mm (no part change)'}
out = []
for r in rows:
    pn, kind, gap = r['PN'], r['kind'], r['manufacturing_gap']; req, rel = n(r['P1_required']), n(r['released_quantity'])
    if pn in ECO_REWORK: wave, why = 'ECO (released part, rework/reposition)', ECO_REWORK[pn]
    elif kind == 'BUY' and pn in CRITICAL_BUY: wave, why = 'RFQ-NOW (critical bought, written confirmation)', 'long-lead / interface-defining'
    elif kind == 'BUY' and pn in GLAND_EXT | B_EXT: wave, why = 'W2 (with gland/B extension)', 'quantity follows station allocation'
    elif kind == 'BUY': wave, why = 'W1 (commodity hardware, authorize)', 'standard A4/8.8 catalogue items'
    elif pn in WET_STABLE: wave, why = 'W1 (release now)', 'inherited C02 geometry unchanged by R12-R16; no R16 blocker touches it'
    elif pn in FEEDBACK_FRAME: wave, why = 'W1 (release now)', 'feedback frame geometry stable since R9; hood interface unchanged'
    elif pn == 'B200_R13': wave, why = 'W2 (after weld/straightness spec)', 'needs weld sequence, runout and journal protection definition'
    elif pn in GLAND_EXT: wave, why = 'W2 (after SP04 first-article dims)', 'extend single-station release to 6 stations after SP04 dimensional FAI'
    elif pn in B_EXT: wave, why = 'W3 (after B01 measurement)', 'installed feedback branches wait for B01/E01 data'
    elif pn in BLOCKED_ROOT: wave, why = 'HOLD (root/host decision)', 'P host interface; R01 G843 acceptance'
    elif pn in WET_FIXTURE: wave, why = 'SUPERSEDE (wet-bay support)', 'bench fixture or upstream fixture receiver; decide with the rig-mounted wet support'
    elif rel >= req and req > 0: wave, why = 'RELEASED', r['release_scope'] or r['batches']
    else: wave, why = 'REVIEW', gap
    out.append(dict(PN=pn, kind=kind, P1_required=req, released=rel, gap=gap, proposed_wave=wave, rationale=why, material=r['material']))
with open(sys.argv[2], 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
S = collections.OrderedDict()
for o in out:
    s = S.setdefault(o['proposed_wave'], dict(PN=0, pieces=0, examples=[]))
    s['PN'] += 1; s['pieces'] += o['P1_required']
    if len(s['examples']) < 12: s['examples'].append(o['PN'])
json.dump(S, open(sys.argv[3], 'w'), indent=1, ensure_ascii=False)
for k, v in S.items(): print(f"{k:50s} PN {v['PN']:3d}  pcs {v['pieces']:5d}  e.g. {', '.join(v['examples'][:8])}")
