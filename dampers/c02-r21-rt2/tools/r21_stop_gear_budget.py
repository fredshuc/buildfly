"""RT2-04: closed-position error budget at the blade edge and gear-pair (G1) face-load screen, from the package's own
R18 stop screens and R14 two-plane surrogate rows. Linear scaling with torque (gravity terms neglected: conservative
for the torque-driven terms, stated). Nothing here is a new spring assumption: support stiffnesses are the two R14 bounds.
Topology (native R20 P, verified by r21_yorder.py): input -> BUY521 (160 Nm) -> BUY520 (110 Nm) -> D885 -> P1 D870 ->
BUY504 mesh -> P2 D870 -> D886 (outboard of the Y-1081 bearing) -> TF900.  P2 leaf sees the stop; P1 leaf also sees the mesh.
Usage: python -I r21_stop_gear_budget.py <deliverables dir> <out.json>"""
import sys, json, math
D, OUT = sys.argv[1], sys.argv[2]
s18 = json.load(open(f"{D}/history/R18/evidence/R18_STOP_TO_SEAL_MAP.json"))
r14 = json.load(open(f"{D}/history/R14/evidence/R14_TWO_PLANE_DEFLECTION_SENSITIVITY.json"))
RP, B, ALPHA, CG, R_EDGE = 82.5, 30.0, math.radians(20), 20.0, 77.0   # pitch radius, face, pressure angle, c_gamma N/(mm.um), blade edge radius
T_REF = 200.0
T_CASES = {'normal_78': 78.0, 'BUY520_static_max_120': 120.0, 'BUY520_dynamic_peak_150': 150.0, 'BUY521_dynamic_peak_195': 195.0}
KHK_SURFACE_NM = 423.0                                       # BUY504 notes: tooth-surface reference torque (supplier basis unconfirmed)
w_cat = KHK_SURFACE_NM * 1000 / RP / B                       # implied uniform line load at that rating, N/mm
def row(case, kb):
    return next(r for r in r14['rows'] if r['case'] == case and r['pose'] == 'bench' and r['bearing_k'] == kb)
out = dict(inputs=dict(r_pitch=RP, face=B, alpha_deg=20, c_gamma=CG, blade_edge_r=R_EDGE, khk_surface_Nm=KHK_SURFACE_NM,
                       implied_catalogue_line_load_N_per_mm=round(w_cat, 1)), cases={})
for kb in (25000, 100000):
    jam, s90 = row('P_driven_jam', kb), row('P_stop90', kb)
    pl = {q['plane']: q for q in s90['planes']}
    # stop normal is world X = line of centres (R18 actual_contact_normal) -> stop force lies in the separating plane (P_stop90)
    dev, inc = abs(pl['Y']['relative_angle_mrad']), abs(pl['X']['relative_angle_mrad'])   # Y = tangential plane, X = separating plane
    fma_hi = B * (dev * math.cos(ALPHA) + inc * math.sin(ALPHA))      # um (mrad * mm = um), components adding
    fma_lo = B * abs(dev * math.cos(ALPHA) - inc * math.sin(ALPHA))   # components opposing
    dt, dr = pl['Y']['relative_at_gear_mm'], pl['X']['relative_at_gear_mm']
    phase_mrad = abs(dt + dr * math.tan(ALPHA)) / RP * 1000           # extra P1 rotation to keep flank contact
    for name, T in T_CASES.items():
        f = T / T_REF; Ft = T * 1000 / RP
        res = {}
        for lo_hi, fma in (('lo', fma_lo * f), ('hi', fma_hi * f)):
            xc = math.sqrt(2 * Ft * B / (CG * fma)) if fma > 0 else math.inf
            if xc >= B: w = Ft / B + CG * fma / 2; KH = 1 + CG * fma * B / (2 * Ft)
            else: w = math.sqrt(2 * Ft * CG * fma / B); KH = math.sqrt(2 * fma * CG * B / Ft)
            res[lo_hi] = dict(f_ma_um=round(fma, 1), loaded_width_mm=round(min(xc, B), 1), K_Hbeta=round(KH, 2),
                              peak_line_load_N_mm=round(w, 1), contact_stress_ratio_vs_catalogue=round(math.sqrt(w / w_cat), 2))
        stop_edge = {str(r['contact_radius_mm']): round(r['blade_edge_displacement_mm'] * f, 3) for r in s18['rows'] if r['T_Nm'] == 200}
        out['cases'][f'k{kb}_{name}'] = dict(T_Nm=T, Ft_N=round(Ft), mesh=res,
            P2_edge_from_stop_mm_by_contact_radius=stop_edge,
            P1_extra_edge_from_mesh_shift_mm=round(phase_mrad * f * R_EDGE / 1000, 3),
            P1_extra_angle_deg=round(math.degrees(phase_mrad * f / 1000), 3))
for k, v in out['cases'].items(): print(k, json.dumps(v))
json.dump(out, open(OUT, 'w'), indent=1)
