"""Independent RT5 all-group screen of a C10 installed STEP.
Usage: python -I c10_screen.py <C10_INSTALLED_Sx.step> <out.json>
Groups = SHELL, DAMPERS, HEAT_EXCHANGERS, WATER_RACK, FIRST_SPOOLS (path field match).
Every cross-group pair and every intra-group pair of DAMPERS, WATER_RACK, FIRST_SPOOLS is screened
(bbox prefilter, exact intersect, 0.001 mm^3). Intra-SHELL is left to the owner's parent-delta rule;
intra-HX is the owner product."""
import sys, json, time, collections, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xcaf_leaves import leaves, bbox, overlap
TOL = 1e-3; t0 = time.time()
GROUPS = ('SHELL', 'DAMPERS', 'HEAT_EXCHANGERS', 'WATER_RACK', 'FIRST_SPOOLS')
L = leaves(sys.argv[1]); G = collections.defaultdict(list)
for p, s in L:
    f = p.split('/'); g = next((k for k in GROUPS if any(x.startswith(k) for x in f)), 'OTHER:' + (f[1] if len(f) > 1 else f[0]))
    G[g].append((p, s, bbox(s)))
inv = {k: len(v) for k, v in G.items()}; print('leaves', len(L), inv, flush=True)
def screen(A, B, same=False):
    cand = 0; hits = []
    for i, (pa, sa, ba) in enumerate(A):
        for j, (pb, sb, bb_) in enumerate(B):
            if same and j <= i: continue
            if not overlap(ba, bb_): continue
            cand += 1
            try: v = sa.intersect(sb).Volume()
            except Exception as e: hits.append([pa, pb, 'ERR ' + str(e)[:60]]); continue
            if v > TOL: hits.append([pa, pb, round(v, 4)])
    return {'candidate_pairs': cand, 'overlaps': hits}
res = {'file': os.path.basename(sys.argv[1]), 'inventory': inv, 'threshold_mm3': TOL}
keys = sorted(G)
for a, b in itertools.combinations(keys, 2):
    r = screen(G[a], G[b]); res[a + '_x_' + b] = r; print(a, b, r['candidate_pairs'], len(r['overlaps']), round(time.time()-t0), flush=True)
for a in ('DAMPERS', 'WATER_RACK', 'FIRST_SPOOLS'):
    r = screen(G[a], G[a], True); res[a + '_x_' + a] = r; print(a, a, r['candidate_pairs'], len(r['overlaps']), round(time.time()-t0), flush=True)
def gb(lst):
    bs = [x[2] for x in lst]; return [round(min(b[i] for b in bs), 2) for i in range(3)] + [round(max(b[i] for b in bs), 2) for i in range(3, 6)]
res['group_bbox'] = {k: gb(v) for k, v in G.items()}
json.dump(res, open(sys.argv[2], 'w'), indent=1)
