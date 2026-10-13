"""Independent interference and motion check of the R20/R21 P and R cold-test configurations (OCP only).
Usage: python -I r21_check.py <R21_WORK/deliverables/native> <out.json> [step_deg]
Conventions (from R17 r17_check.py, verified against R20 placements): rotation about global -Y through
P1 (83,*,1583), P2 (-82,*,1583), R1 (-82,*,1583); P2 turns -angle. Rotating dry set as R17; H14_W8 rotates
only for the captive output washer (world Y -1149.1..-1147.5). Wet/wet (R12/R12) pairs are inherited, not rechecked."""
import sys, os, json, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from native import bbox, common_vol, dist, overlap_bb
from OCP.TopoDS import TopoDS_Shape
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Builder
from OCP.gp import gp_Trsf, gp_Ax1, gp_Pnt, gp_Dir
from OCP.TopLoc import TopLoc_Location
import io
NAT, OUT = sys.argv[1], sys.argv[2]; STEP = float(sys.argv[3]) if len(sys.argv) > 3 else 2.5
PARTS = {p['pn']: p for p in json.load(open(f"{NAT}/R20_PARTS.json"))}
AX = {'P1': (83.0, 1583.0), 'P2': (-82.0, 1583.0), 'R1': (-82.0, 1583.0)}
ROT = {'D870','D871','D872','D873','D894','D884','D885','D886','D887','D888','D521_R14','D530','D892','D896','H14_PIN5',
       'H14_SPLIT','BUY504','BUY_R13_BK2','BUY520','BUY521','BUY531','HW_R13_M4TIP','H14_M8X25','H14_W8','H14_M6X20'}
cache = {}
def local(pn):
    if pn not in cache:
        s = TopoDS_Shape(); BRepTools.Read_s(s, io.BytesIO(PARTS[pn]['brep'].encode()), BRep_Builder()); cache[pn] = s
    return cache[pn]
def trsf(o):
    u, v, n, p = o['u'], o['v'], o['n'], o['o']; g = gp_Trsf()
    g.SetValues(u[0], v[0], n[0], p[0], u[1], v[1], n[1], p[1], u[2], v[2], n[2], p[2]); return g
def rot(key, ang):
    x, z = AX[key]; a = ang * (-1 if key == 'P2' else 1); t = gp_Trsf()
    t.SetRotation(gp_Ax1(gp_Pnt(x, 0, z), gp_Dir(0, -1, 0)), math.radians(a)); return t
res = {}
for cfg in ['P', 'R']:
    t0 = time.time(); O = json.load(open(f"{NAT}/R20_{cfg}_OCCURRENCES.json"))
    W0 = {o['occurrence']: local(o['pn']).Moved(TopLoc_Location(trsf(o))) for o in O}
    B0 = {k: bbox(s) for k, s in W0.items()}
    def group(o):
        if o['source'] == 'R12' and o.get('moving'): return o['moving']
        if o['source'] == 'R14' and o['pn'] in ROT:
            if o['pn'] == 'H14_W8' and abs(B0[o['occurrence']][4] - (-1147.5)) > 0.01: return None
            if cfg == 'R': return 'R1'
            b = B0[o['occurrence']]; return 'P1' if (b[0] + b[3]) / 2 > 0.5 else 'P2'
        return None
    G = {o['occurrence']: group(o) for o in O}
    om = {o['occurrence']: o for o in O}
    # 1. static pairs at 0 deg: every non-R12 body vs every other body (skip R12/R12)
    static_hits = []; tested = 0; keys = list(W0)
    for i, a in enumerate(keys):
        for c in keys[i + 1:]:
            if om[a]['source'] == 'R12' and om[c]['source'] == 'R12': continue
            if not overlap_bb(B0[a], B0[c]): continue
            tested += 1; v = common_vol(W0[a], W0[c])
            if v > 1e-3: static_hits.append(dict(a=a, b=c, pn=[om[a]['pn'], om[c]['pn']], src=[om[a]['source'], om[c]['source']], mm3=round(v, 4)))
    # 2. motion: moving bodies vs all bodies of another group (skip R12/R12)
    movers = [k for k in keys if G[k]]
    angles = sorted(set([round(x * STEP, 4) for x in range(int(90 / STEP) + 1)] + [0.1, 1.0, 89.0, 89.9]))
    motion = []
    stop = None
    for ang in angles:
        W = {}
        for k in keys:
            W[k] = W0[k] if not G[k] or ang == 0 else local(om[k]['pn']).Moved(TopLoc_Location(rot(G[k], ang).Multiplied(trsf(om[k]))))
        B = {k: (bbox(W[k]) if G[k] else B0[k]) for k in keys}
        hits = []
        for a in movers:
            for c in keys:
                if c == a or G[c] == G[a]: continue
                if G[c] and c < a: continue
                if om[a]['source'] == 'R12' and om[c]['source'] == 'R12': continue
                if not overlap_bb(B[a], B[c]): continue
                v = common_vol(W[a], W[c])
                if v > 1e-3: hits.append(dict(a=a, b=c, pn=[om[a]['pn'], om[c]['pn']], mm3=round(v, 4)))
        rec = dict(angle=ang, hits=hits)
        if cfg == 'P':
            d = [k for k in keys if om[k]['pn'] == 'D886'][0]; t = [k for k in keys if om[k]['pn'] == 'TF900'][0]
            rec['D886_TF900_gap_mm'] = round(dist(W[d], W[t]), 4)
        motion.append(rec)
    res[cfg] = dict(instances=len(O), static_pairs_tested=tested, static_hits=static_hits,
                    motion=[dict(angle=m['angle'], n_hits=len(m['hits']), hits=m['hits'], **({'D886_TF900_gap_mm': m['D886_TF900_gap_mm']} if 'D886_TF900_gap_mm' in m else {})) for m in motion],
                    seconds=round(time.time() - t0, 1))
    print(cfg, 'static tested', tested, 'static hits', len(static_hits), 'motion positions', len(motion),
          'max motion hits', max(len(m['hits']) for m in motion), flush=True)
json.dump(res, open(OUT, 'w'), indent=1)
