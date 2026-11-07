"""RT5 targeted distances on a C10 installed STEP.
Usage: python -I c10_probe.py <C10_INSTALLED_S1.step> <W2_ADDITIONAL_INSULATION.step> <out.json>
(1) upper Pin seat / static gasket / D04 local parts -> upper-core HX leaves (exact BRep distance, 30 mm cap)
(2) additional W2 insulation -> A post, sister RHS, webs and pocket parts
(3) first spools / water rack -> shell and HX (nearest, 30 mm cap)"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xcaf_leaves import leaves, bbox, overlap
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
L = leaves(sys.argv[1]); INS = leaves(sys.argv[2])
def grp(k): return [(p, s, bbox(s)) for p, s in L if k in p.split('/')]
SH, DA, HX, RK, SP = grp('SHELL'), grp('DAMPERS'), grp('HEAT_EXCHANGERS'), grp('WATER_RACK'), grp('FIRST_SPOOLS')
def nearest(A, B, cap=30.0):
    best = (cap, None)
    for pa, sa, ba in A:
        for pb, sb, bb_ in B:
            if not overlap(ba, bb_, g=best[0]): continue
            d = BRepExtrema_DistShapeShape(sa.wrapped, sb.wrapped); d.Perform()
            if d.IsDone() and d.Value() < best[0]:
                q1, q2 = d.PointOnShape1(1), d.PointOnShape2(1)
                best = (d.Value(), [pa.split('/')[-1], '/'.join(pb.split('/')[-2:]), [round(q1.X(), 3), round(q1.Y(), 3), round(q1.Z(), 3)], [round(q2.X(), 3), round(q2.Y(), 3), round(q2.Z(), 3)]])
    return {'min_mm': round(best[0], 4) if best[1] else f'>{cap}', 'detail': best[1]}
out = {}
for bed in 'AB':
    upper = [x for x in HX if f'{bed}_UPPER' in x[0].split('/') and 'FIN' not in x[0].split('/')[-1].upper()]
    for key in (f'DAMPER_SEAT_{bed}_UPPER_DEEP_O', f'DAMPER_STATIC_GASKET_{bed}_UPPER_O'):
        out[f'{key}->HX_{bed}_UPPER'] = nearest([x for x in DA if x[0].split('/')[-1] == key], upper); print(key, out[f'{key}->HX_{bed}_UPPER'], flush=True)
    d04 = [x for x in DA if 'D04' in x[0].split('/')[-1] and f'_{bed}' in x[0].split('/')[-1]]
    out[f'D04_{bed}_local({len(d04)})->HX_{bed}_UPPER'] = nearest(d04, upper); print(bed, 'D04', out[f'D04_{bed}_local({len(d04)})->HX_{bed}_UPPER'], flush=True)
insb = [(p, s, bbox(s)) for p, s in INS]
for key in ('F_POST_-600_-825_O', 'C09_A_POST_SISTER_RHS_22x60x3', 'C09_A_POST_UPPER_FRONT_WEB', 'C09_A_POST_UPPER_REAR_WEB', 'C10_A_W2_POCKET_ROOF', 'C10_B_W2_POCKET_ROOF', 'AIR_PROCESS_IN_FLOOR_A_O', 'AIR_PROCESS_IN_FLOOR_B_O'):
    out[f'insulation->{key}'] = nearest(insb, [x for x in SH if x[0].split('/')[-1] == key], cap=60.0); print(key, out[f'insulation->{key}'], flush=True)
out['insulation->DAMPERS'] = nearest(insb, DA, cap=60.0); print('ins dampers', out['insulation->DAMPERS'], flush=True)
out['first_spools->SHELL'] = nearest(SP, SH); print('spools shell', out['first_spools->SHELL'], flush=True)
out['water_rack->SHELL'] = nearest(RK, SH, cap=60.0); print('rack shell', out['water_rack->SHELL'], flush=True)
out['water_rack->HX'] = nearest(RK, HX, cap=60.0); print('rack hx', out['water_rack->HX'], flush=True)
json.dump(out, open(sys.argv[3], 'w'), indent=1)
