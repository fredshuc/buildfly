"""Independent DFM geometry checks on the R11 hood receiver root (A branch).
Usage: python -I check_a_root.py <R11_WORK/deliverables/native dir> <out.json>
Reads native BRep + placements only; does not import project code."""
import sys, json, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from native import *
from OCP.gp import gp_Trsf, gp_Vec
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform

N = Native(sys.argv[1]); out = {}
def moved(s, dx, dy, dz):
    t = gp_Trsf(); t.SetTranslation(gp_Vec(dx, dy, dz)); return BRepBuilderAPI_Transform(s, t, True).Shape()
def state_occs(cfg):
    return [o for o in N.O if cfg in o.get('configs', ['AUTO', 'MANUAL'])]

# 1. Rebuild the six P-root a4 fillets exactly as the R11 audit convention (throat a=4, leg 4*sqrt2).
leg = 4 * math.sqrt(2); beads = []
for i, z in enumerate([1268, 1607], 1):
    beads.append((f'P_ROOT_{i}_BACK_a4', prism([(-335, -65, z), (-335 + leg, -65, z), (-335, -65 - leg, z)], (0, 0, 26)), 26.0))
    for end, sgn in [(z, -1), (z + 26, 1)]:
        beads.append((f'P_ROOT_{i}_END_{end}_a4', prism([(-335, -65, end), (-335 + leg, -65, end), (-335, -65, end + sgn * leg)], (0, 10, 0)), 10.0))
manual = [(o, N.world(o)) for o in state_occs('MANUAL')]
auto = [(o, N.world(o)) for o in state_occs('AUTO')]
mb = [(o, s, bbox(s)) for o, s in manual]; ab = [(o, s, bbox(s)) for o, s in auto]
clash = []
for name, s, L in beads:
    b = bbox(s)
    for o, t, tb in mb:
        if overlap_bb(b, tb):
            v = common_vol(s, t)
            if v > 1e-3:
                p = N.pm[o['pn']]
                clash.append(dict(weld=name, obstacle=o['occurrence'], pn=o['pn'], name=p['name'], scope=o['scope'],
                                  configs=o.get('configs'), mm3=v, obstacle_notes=p.get('notes')))
out['p_root_fillet_clash_MANUAL'] = clash
# min distance of each fillet to F620_002 and torch-access gap
f620 = N.world('F620_002'); out['F620_002_bbox'] = bbox(f620)
out['shoe_to_F620_gap_mm'] = dist(N.world('G840P1_001'), f620)

# 2. Fixture relief: shift F620_002 in -Y (away from the shoe) and re-check against all MANUAL bodies + fillets.
shift_rows = []
for s_mm in [0, 5, 6, 8, 10, 15, 20, 25]:
    t = moved(f620, 0, -s_mm, 0); tb = bbox(t); hits = []
    for name, s, L in beads:
        v = common_vol(s, t)
        if v > 1e-3: hits.append((name, round(v, 3)))
    for o, u, ub in mb:
        if o['occurrence'] == 'F620_002' or not overlap_bb(tb, ub): continue
        v = common_vol(t, u)
        if v > 1e-3: hits.append((o['occurrence'], round(v, 3)))
    gap = min(dist(t, s) for _, s, _ in beads)
    shift_rows.append(dict(shift_minus_Y_mm=s_mm, rib_Y=[tb[1], tb[4]], hits=hits, min_gap_to_fillets_mm=gap))
out['F620_002_shift_study'] = shift_rows

# 3. Host side of P107 (X > -335): what product bodies occupy it in AUTO? (host mother plate not modelled)
host_zone = box(-335, -761, 1240, -300, -55, 1661)
occ_host = []
for o, s, b in ab:
    if not overlap_bb(b, bbox(host_zone)): continue
    v = common_vol(s, host_zone)
    if v > 1e-3: occ_host.append(dict(occ=o['occurrence'], pn=o['pn'], mm3=v, bbox=b))
out['AUTO_bodies_in_P107_host_side_zone'] = occ_host
out['P_shoe_overlap_with_P107_footprint_on_host_face_mm2'] = 2 * 10 * 26  # Y -65..-55 x Z 26 per shoe, two shoes

# 4. Weld lengths vs EN 1993-1-8 4.5.2(2): l_eff = L - 2a (craters) must be >= max(30, 6a)
def elig(L, a): leff = L - 2 * a; need = max(30.0, 6 * a); return dict(L=L, a=a, l_eff=leff, required=need, load_bearing=leff >= need)
out['weld_length_check'] = {
    'P_root_back_a4_26': elig(26, 4), 'P_root_end_a4_10': elig(10, 4),
    'R_foot_long_a3_26': elig(26, 3), 'R_foot_short_a3_9': elig(9, 3),
    'G842_long_edge_a3_148': elig(148, 3), 'G830_to_beam_a2_206': elig(206, 2)}

# 5. P107 blind M8 holes (valve side, depth 10.5, 1.5 mm web at host face X=-335): distance to nearest fillet.
p107 = N.pm['P107']; o107 = N.om['P107_001']
holes = []
for f in p107['features']:
    if f['type'] != 'blind_thread': continue
    Y = o107['o'][1] + f['x']; Z = o107['o'][2] + f['y']
    holes.append((Y, Z))
near = []
for (Y, Z) in holes:
    if Y < -100: continue
    # tap-drill dia 6.8; hole bottom web from X=-336.5 to -335
    web = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(-347, Y, Z), gp_Dir(1, 0, 0)), 3.4, 10.5).Shape()
    d = min(dist(web, s) for _, s, _ in beads)
    if d < 20: near.append(dict(hole_Y=Y, hole_Z=Z, min_dist_bead_to_blind_hole_mm=d))
out['P107_blind_M8_near_root_welds'] = near

# 6. R root: weld/feet footprint on R107 bottom vs R106 gasket land on R107 top face (same 3 mm plate).
r106 = N.world('R106_001')
gasket_land = []
for occ in ['G840R1_001', 'G840R2_001', 'G842_001']:
    s = N.world(occ); b = bbox(s)
    # contact strip projected onto the R106 gasket layer on the opposite (Z=1491) face of R107
    proj = box(b[0], max(b[1], -64), 1491.0, b[3], min(b[4], -55), 1491.1)
    a = common_vol(proj, r106) / 0.1 if overlap_bb(bbox(proj), bbox(r106)) else 0.0
    gasket_land.append(dict(occ=occ, contact_footprint_mm2=(b[3] - b[0]) * (min(b[4], -55) - max(b[1], -64)),
                            area_directly_behind_R106_gasket_mm2=a))
out['R_root_behind_gasket_land'] = gasket_land
out['R107_thickness_mm'] = 3; out['R_weld_throat_mm'] = 3

# 7. R M8 row and G842 coverage
o = N.om['R107_001']; rows = []
for f in N.pm['R107']['features']:
    if f['type'] == 'hole':
        Y = o['o'][1] + f['x']; X = o['o'][0] - f['y']
        if Y > -100: rows.append((round(X, 2), round(Y, 2), f['d']))
out['R107_holes_feedback_side'] = sorted(rows)
g = bbox(N.world('G842_001')); out['G842_bbox'] = g
out['G842_gap_to_M8_row_centre_mm'] = g[1] - (-74)

# 8. G837 support loss geometry on G830 (window-corner notch) and distance to the M5 hood screw axis
loss = []
for tag, frame in [('P', 'G830P_001'), ('R', 'G830R_001')]:
    fr = N.world(frame); fb = bbox(fr)
    for oo in N.occs('G837'):
        s = N.world(oo); b = bbox(s)
        if not overlap_bb([b[0]-1, b[1]-1, b[2]-1, b[3]+1, b[4]+1, b[5]+1], fb): continue
        slab = box(b[0], fb[1], b[2], b[3], fb[4], b[5])
        sup = common_vol(slab, fr) / (fb[4] - fb[1])
        loss.append(dict(frame=frame, pad=oo['occurrence'], pad_footprint_bbox=[b[0], b[2], b[3], b[5]], supported_mm2_full_footprint=sup))
out['G837_support_on_G830'] = loss
# hood screws: G836 block centres
out['G836_centres'] = {oo['occurrence']: [round((bbox(N.world(oo))[i] + bbox(N.world(oo))[i+3]) / 2, 2) for i in range(3)] for oo in N.occs('G836')}

# 9. A709 corner shape (for corner-relief options on the 148 window)
a709 = N.pm['A709']; out['A709_features'] = [f for f in a709['features'] if f['type'] not in ('hole',)][:8]
json.dump(out, open(sys.argv[2], 'w'), indent=1, default=float)
print(json.dumps(out, indent=1, default=float)[:12000])
