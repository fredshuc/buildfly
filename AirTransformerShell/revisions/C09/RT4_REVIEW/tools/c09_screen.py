"""Independent RT4 screen of a C09 installed STEP.
Usage: python -I c09_screen.py <C09_INSTALLED_Sx.step> <out.json>
Reads every leaf, groups by first path field below the root, and runs bbox-filtered
positive-volume intersection on every cross-group pair (SHELL x DAMPERS, SHELL x HX,
DAMPERS x HX) and every intra-DAMPERS pair. Threshold 0.001 mm^3 (same as owner)."""
import sys, json, time, collections, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xcaf_leaves import leaves, bbox, overlap
TOL = 1e-3
t0 = time.time()
L = leaves(sys.argv[1])
def grp(p):
    f = p.split('/')
    for k in ('SHELL', 'DAMPERS', 'HEAT_EXCHANGERS'):
        if any(x.startswith(k) for x in f): return k
    return f[1] if len(f) > 1 else f[0]
G = collections.defaultdict(list)
for p, s in L: G[grp(p)].append((p, s, bbox(s)))
inv = {k: len(v) for k, v in G.items()}
print('leaves', len(L), inv, round(time.time()-t0, 1), flush=True)
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
# HX: merge per core to cut pair count (bbox per occurrence still used)
for a, b, same in (('DAMPERS', 'HEAT_EXCHANGERS', False), ('SHELL', 'HEAT_EXCHANGERS', False),
                   ('SHELL', 'DAMPERS', False), ('DAMPERS', 'DAMPERS', True)):
    r = screen(G[a], G[b], same); res[a + '_x_' + b] = r
    print(a, b, r['candidate_pairs'], len(r['overlaps']), round(time.time()-t0, 1), flush=True)
# group bounding boxes
def gb(lst):
    bs = [x[2] for x in lst]; return [round(min(b[i] for b in bs), 2) for i in range(3)] + [round(max(b[i] for b in bs), 2) for i in range(3, 6)]
res['group_bbox'] = {k: gb(v) for k, v in G.items()}
json.dump(res, open(sys.argv[2], 'w'), indent=1)
