"""Independent Boolean checks of minimal ECO candidates on the R16 integrated P/R configurations.
Usage: python -I r16_eco_check.py <R16_WORK/deliverables/native> <out.json>
Conventions reproduced from R16 r16_check.py: rotation about global -Y through P1 (-439,*,1368), P2 (-439,*,1533),
R1 (-82,*,1583); P2 turns by -angle, P1/R1 by +angle. Discrete poses only."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r16_native import R16
from native import bbox, volume, common_vol, dist, box, overlap_bb
from OCP.gp import gp_Trsf, gp_Ax1, gp_Pnt, gp_Dir, gp_Vec
from OCP.TopLoc import TopLoc_Location
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut

NAT, OUT = sys.argv[1], sys.argv[2]
AXES = {'P1': (-439, 1368), 'P2': (-439, 1533), 'R1': (-82, 1583)}
ROT = {'D870','D871','D872','D873','D894','D884','D885','D886','D887','D888','D521_R14','D530','D892','D896','H14_PIN5',
       'H14_SPLIT','BUY504','BUY_R13_BK2','BUY520','BUY521','BUY531','HW_R13_M4TIP','H14_M8X25','H14_W8','H14_M6X20'}
def rotating(q):
    if q['pn'] == 'H14_W8': return abs(q['rig_local_origin'][2] - 177) < 1e-6
    return q['pn'] in ROT
def group(q, cfg):
    if q['source'] == 'R12' and q.get('moving'): return q['moving']
    if q['source'] == 'R14' and rotating(q): return 'R1' if cfg == 'R' else ('P1' if q['rig_local_origin'][0] > 82.5 else 'P2')
    return None
def rot(key, angle_deg):
    x, z = AXES[key]; a = angle_deg * (-1 if key == 'P2' else 1)
    t = gp_Trsf(); t.SetRotation(gp_Ax1(gp_Pnt(x, 0, z), gp_Dir(0, -1, 0)), math.radians(a)); return t
def trans(dx, dy, dz):
    t = gp_Trsf(); t.SetTranslation(gp_Vec(dx, dy, dz)); return t
def place(N, q, angle, pre=None, post=None):
    g = N.trsf(q)
    if pre is not None: g = pre.Multiplied(g)          # world-frame edit applied before motion
    k = group(q, N.cfg)
    if k and angle: g = rot(k, angle).Multiplied(g)
    if post is not None: g = post.Multiplied(g)
    return N.local(q['pn']).Moved(TopLoc_Location(g))
def world_all(N, angle, edits=None):
    edits = edits or {}; W = {}
    for q in N.O:
        e = edits.get(q['occurrence'], {})
        s = place(N, q, angle, pre=e.get('pre'))
        if 'cut' in e: op = BRepAlgoAPI_Cut(s, e['cut']); op.Build(); s = op.Shape()
        W[q['occurrence']] = s
    return W
def hits_of(N, W, targets, angle, exclude_same_group=True):
    BB = {k: bbox(s) for k, s in W.items()}; out = []
    for t in targets:
        qt = N.om[t]; gt = group(qt, N.cfg)
        for q in N.O:
            k = q['occurrence']
            if k == t: continue
            if exclude_same_group and gt and group(q, N.cfg) == gt: continue
            if not overlap_bb(BB[t], BB[k]): continue
            v = common_vol(W[t], W[k])
            if v > 1e-3: out.append(dict(a=t, b=k, pn=[qt['pn'], q['pn']], mm3=round(v, 4), angle=angle))
    return out
res = {}

# --- 1. Baseline reproduction of the decision-changing hits
for cfg in ['P', 'R']:
    N = R16(NAT, cfg); W = world_all(N, 0)
    tg = [q['occurrence'] for q in N.O if q['pn'] in ('G901', 'TF909', 'TF903', 'TF906')]
    h = [x for x in hits_of(N, W, tg, 0) if N.om[x['b']]['source'] == 'R12']
    res[f'{cfg}_baseline_cross_hits_guard_frame'] = dict(count=len(h), total_mm3=round(sum(x['mm3'] for x in h), 3),
                                                       pairs=sorted({tuple(x['pn']) for x in h}))

# --- 2. ECO-A: move G901 and the two wet-end TF909 posts dryward (world -Y) by d; G900/G903 unchanged
eco_a = {}
for cfg in ['P', 'R']:
    N = R16(NAT, cfg)
    wet_end_posts = [q['occurrence'] for q in N.O if q['pn'] == 'TF909' and bbox(N.world(q))[4] > -760]
    g901 = [q['occurrence'] for q in N.O if q['pn'] == 'G901']
    rows = []
    for d in [40.0, 45.5, 48.0]:
        edits = {k: {'pre': trans(0, -d, 0)} for k in g901 + wet_end_posts}
        allh = []
        for ang in [0, 45, 90]:
            W = world_all(N, ang, edits)
            allh += hits_of(N, W, g901 + wet_end_posts, ang)
        W0 = world_all(N, 0, edits)
        wet = [q['occurrence'] for q in N.O if q['source'] == 'R12' and q['pn'] != 'B200_R13']
        gw = min(dist(W0[g901[0]], W0[k]) for k in wet if overlap_bb([*(x - 30 for x in bbox(W0[g901[0]])[:3]), *(x + 30 for x in bbox(W0[g901[0]])[3:])], bbox(W0[k])))
        bk = [q['occurrence'] for q in N.O if q['pn'] == 'BUY_R13_BK2']
        gb = min(dist(W0[g901[0]], W0[k]) for k in bk)
        shafts = [q['occurrence'] for q in N.O if q['pn'] == 'B200_R13']
        gs = min(dist(W0[g901[0]], W0[k]) for k in shafts)
        rows.append(dict(shift_mm=d, posts=wet_end_posts, hits=allh, n_hits=len(allh), gap_G901_to_wet_nonshaft_mm=round(gw, 3),
                         gap_G901_to_BK2_mm=round(gb, 3), gap_G901_to_wet_shaft_mm=round(gs, 3), G901_Y=[round(bbox(W0[g901[0]])[1], 2), round(bbox(W0[g901[0]])[4], 2)]))
    eco_a[cfg] = rows
res['ECO_A_guard_relocation'] = eco_a

# --- 3. ECO-B (R): trim dry end of fixture ribs F621 to Y >= -715
N = R16(NAT, 'R')
f621 = [q['occurrence'] for q in N.O if q['pn'] == 'F621']
edits = {k: {'cut': box(-1e4, -2000, -1e4, 1e4, -715, 1e4)} for k in f621}
W = world_all(N, 0, edits)
res['ECO_B_R_F621_trim'] = dict(trim_to_Y=-715, hits_after=hits_of(N, W, f621, 0, exclude_same_group=False))

# --- 4. ECO-C (P): re-index stop arm D886 on P2 by r degrees about the P2 axis, sweep P2 0..-90
N = R16(NAT, 'P'); d886 = [q['occurrence'] for q in N.O if q['pn'] == 'D886'][0]
def idx(r):
    t = gp_Trsf(); x, z = AXES['P2']; t.SetRotation(gp_Ax1(gp_Pnt(x, 0, z), gp_Dir(0, -1, 0)), math.radians(r)); return t
stop = {}
for r in [0, -90, 90]:
    rows = []
    for ang in [0, 15, 30, 45, 60, 75, 90]:
        W = world_all(N, ang, {d886: {'pre': idx(r)}})
        h = hits_of(N, W, [d886], ang)
        tf = [q['occurrence'] for q in N.O if q['pn'] == 'TF900'][0]
        rows.append(dict(angle=ang, hits=[(x['b'], x['pn'][1], x['mm3']) for x in h], gap_to_TF900_mm=round(dist(W[d886], W[tf]), 4)))
    stop[f'reindex_{r:+d}deg'] = rows
res['ECO_C_P_stop_reindex'] = stop
# arm direction check: world direction of D886 arm tip relative to P2 axis at P2 angle 0 for each index
for r in [0, -90, 90]:
    s = place(N, N.om[d886], 0, pre=idx(r)); b = bbox(s)
    res['ECO_C_P_stop_reindex'][f'reindex_{r:+d}deg_bbox_at_0'] = [round(x, 1) for x in b]
json.dump(res, open(OUT, 'w'), indent=1, default=float)
print(json.dumps({k: v for k, v in res.items() if not k.startswith('ECO_A')}, indent=1, default=float)[:6000])
for cfg, rows in eco_a.items():
    for r in rows: print('ECO_A', cfg, r['shift_mm'], 'hits', r['n_hits'], [ (h['b'], h['mm3'], h['angle']) for h in r['hits']][:6], 'gapwet', r['gap_G901_to_wet_nonshaft_mm'], 'gapBK2', r['gap_G901_to_BK2_mm'], 'gapshaft', r['gap_G901_to_wet_shaft_mm'], r['G901_Y'])
