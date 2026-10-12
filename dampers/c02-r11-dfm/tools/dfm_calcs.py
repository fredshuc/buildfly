"""Closed-form DFM screening calculations for the C02 R11 review (units: N, mm, MPa).
Inputs: R11_A_ROOT_CONTROLS.json (project load rows). Usage: python -I dfm_calcs.py <evidence dir> <out.json>
All results are screening estimates with stated assumptions, not qualification."""
import sys, json, math
A = {a['tag']: a for a in json.load(open(f"{sys.argv[1]}/R11_A_ROOT_CONTROLS.json"))}
out = {}

# 1. P root weld group (as designed): two roots at Z=1281 and 1620 (339 mm apart), each: back fillet 26 mm
# along Z at y=-65, two end fillets 10 mm along Y (y=-65..-55) at z=+-13; throat a=4 (leg 5.657).
# Split: Fz shared equally; Mx -> +-Fy couple over 339 mm; My -> +-Fx couple over 339 mm; Mz carried locally
# by each root (both roots lie on one Z line, so Mz cannot be split into a couple). Elastic line-weld model.
a = 4.0; Lb, Le = 26.0, 10.0
ybar = (Lb * -65 + 2 * Le * -60) / (Lb + 2 * Le)
I_z = Lb * a * (-65 - ybar) ** 2 + 2 * a * (((-55 - ybar) ** 3 - (-65 - ybar) ** 3) / 3)
Aw = a * (Lb + 2 * Le); cmax = max(abs(-55 - ybar), abs(-65 - ybar))
rows = []
for r in A['P']['AM']:
    F, M = r['force_N'], r['root_moment_Nmm']
    fz = F[2] / 2; fy = M[0] / 339.0; fx = abs(M[1]) / 339.0; mz = abs(M[2]) / 2
    sig_M = mz * cmax / I_z; sig_N = fx / Aw; tau = math.hypot(fy, fz) / Aw
    rows.append(dict(case=r['case'], root_Mz_Nmm=mz, normal_from_Mz_MPa=sig_M, normal_from_Fx_MPa=sig_N, shear_MPa=tau,
                     von_mises_like_MPa=math.sqrt((sig_M + sig_N) ** 2 + 3 * tau ** 2)))
out['P_root_weld_group'] = dict(assumptions='rigid frame; Mz shared equally by the two roots; throat-plane stresses; craters ignored',
                                weld_area_mm2_per_root=Aw, I_z_mm4=I_z, lever_y_mm=cmax, rows=rows,
                                max_MPa=max(x['von_mises_like_MPa'] for x in rows),
                                note='Lever for Mz is limited by the 10 mm shoe/P107 overlap (Y -65..-55).')

# 2. G840P beam weak-axis screen for the same root moment Mz/2 (beam 10 mm deep in Y, 26 mm in Z, 206 mm long)
E304 = 193000.0; b, h, L = 26.0, 10.0, 206.0
I_weak = b * h ** 3 / 12; I_strong = h * b ** 3 / 12; mz = max(x['root_Mz_Nmm'] for x in rows)
out['G840P_beam_screen'] = dict(I_weak_mm4=I_weak, I_strong_mm4=I_strong, root_moment_Nmm=mz,
    bending_MPa=mz / (I_weak / (h / 2)),
    rotation_mrad_bounds=[1e3 * mz * L / (2 * E304 * I_weak), 1e3 * mz * L / (E304 * I_weak)],
    note='bounds: moment introduced uniformly along the frame weld (lower) or at the free end (upper)')
# standard angle alternative EN 10056-1 L30x30x3 (I about leg-parallel centroidal axes ~1.40e4 mm4, catalogue value)
out['G840P_beam_screen']['L30x30x3_I_mm4_catalogue'] = 1.40e4

# 3. R receiver: project strip screen vs clamped (bolted, not welded) full-depth doubler under existing M8 row.
MxR = max(abs(r['root_moment_Nmm'][0]) for r in A['R']['AM'])
proj = 6 * MxR / (210 * 3 ** 2)
alt = []
for t in [6.0, 8.0, 10.0]:
    bx, holes = 236.0, 5 * 9.0
    sig_gross = 6 * MxR / (bx * t ** 2); sig_net = 6 * MxR / ((bx - holes) * t ** 2)
    alt.append(dict(t_mm=t, doubler_X=[-200, 36], doubler_Y=[-90, -55], sigma_gross_MPa=sig_gross, sigma_net_MPa=sig_net,
                    bolt_increment_N_pivot_at_feet_edge=MxR / (5 * 19.0), bolt_increment_N_pivot_at_far_edge=MxR / (5 * 16.0),
                    M8_screw_length_change_mm=+t))
out['R_receiver'] = dict(max_Mx_Nmm=MxR, project_R107_strip_MPa=proj, clamped_doubler_options=alt,
    assumptions='doubler carries full moment between beam feet and bolt line; R107 only clamped; prying neglected (bolt line 16-19 mm from both edges); five existing STD01B M8 at X=-191,-136.5,-82,-27.5,27, Y=-74 with F602 metal compression limiters')

# 4. B852 press fit: Ø3 m6 (3.002..3.008) into Ø2.98 bore coaxial with the R4 (Ø8) crown; assume bore H7 (2.980..2.990)
E = 200000.0; nu = 0.3; R = 1.49; ro = 4.0
pf = []
for d_int in [3.002 - 2.990, 3.008 - 2.980]:
    dr = d_int / 2
    p = dr * E * (ro ** 2 - R ** 2) / (2 * R * ro ** 2)
    hoop = p * (ro ** 2 + R ** 2) / (ro ** 2 - R ** 2)
    u_o = 2 * p * R ** 2 * ro / (E * (ro ** 2 - R ** 2))
    pf.append(dict(diametral_interference_mm=d_int, contact_pressure_MPa=p, bore_hoop_tension_MPa=hoop, crown_radius_growth_um=1e3 * u_o))
out['B852_press_fit'] = dict(wall_mm=ro - R, rows=pf, crown_profile_tolerance_um=10,
    note='same-material Lame solution, solid pin; 440C HRC58-60 hub; crown OD growth compares with the R4 +-0.01 profile tolerance')

# 5. Crown/flat Hertz line contact, and edge-contact sensitivity
Es = E / (2 * (1 - nu ** 2)); Lc = 10.5
def hertz(Q, Rc): bh = math.sqrt(4 * Q * Rc / (math.pi * Lc * Es)); return 2 * Q / (math.pi * bh * Lc), bh
Qmax = 2 * 569.493466
p0, bh = hertz(Qmax, 4.0); p0_2, _ = hertz(Qmax, 2.0)
approach = (Qmax / (math.pi * Lc * Es)) * (2 * math.log(4 * 4.0 / bh) + 1)
out['crown_contact'] = dict(Q_N=Qmax, p0_R4_MPa=p0, halfwidth_mm=bh, p0_R2_MPa=p0_2, elastic_approach_um=1e3 * approach,
    H900_yield_MPa=1170, line_contact_first_yield_p0_MPa=1.67 * 1170,
    tilt_um_over_length_for_1mrad=1e3 * 1e-3 * Lc,
    note='first yield for line contact at p0 ~ 3.3k = 1.67*sy (Tresca); 17-4PH H900 sy ~1170 MPa (AMS 5643 typical min)')

# 6. Spherical seat: bridge dimple depth/annulus and radius-mismatch gap across the annulus
Rs = 20.0; depth = 0.5; r_out = math.sqrt(Rs ** 2 - (Rs - depth) ** 2); r_in = 3.5
gap = [dR * (r_out ** 2 - r_in ** 2) / (2 * Rs ** 2) for dR in (0.01, 0.04)]
out['sphere_seat'] = dict(dimple_depth_mm=depth, annulus_r_mm=[r_in, r_out], annulus_width_mm=r_out - r_in,
    annulus_area_mm2=math.pi * (r_out ** 2 - r_in ** 2), cone_half_angle_equiv_deg=90 - math.degrees(math.asin(((r_in + r_out) / 2) / Rs)),
    gap_across_annulus_um_for_dR_0p01_0p04=[1e3 * g for g in gap],
    note='specified SR20 +0.02/0 vs -0.01/-0.02 gives <0.5 um gap across the annulus: radius tolerance is not functional; annulus axial position/flatness is')

# 7. G837 pocket internal-corner radius vs G836 block chamfer (12.10+0.05/0 pocket, 12.00-0.02/-0.05 block, chamfer 0.2)
g_min = (12.10 - 12.00) / 2; c = 0.2
out['G837_pocket_corner'] = dict(min_side_clearance_mm=g_min, block_chamfer_mm=c, max_corner_radius_mm=(math.sqrt(2) * (g_min + c / 2)) / (math.sqrt(2) - 1),
    with_chamfer_0p3=(math.sqrt(2) * (g_min + 0.15)) / (math.sqrt(2) - 1), drawing_value='R<=0.1')

# 8. G840 relief pockets: milled internal corner radius r against a sharp G836/G837 corner with 1 mm wall clearance
out['G840_relief_corner'] = [dict(r_mm=r, remaining_clearance_mm=r * (1 - math.sqrt(2)) + math.sqrt(2) * 1.0 if r > 1 else 1.0) for r in (1, 1.5, 2, 2.5, 3, 3.4142)]

# 9. G837 lost support: corner 3x3 at 22.6..26.9 mm from the M5 axis; M5 clamp cone radius estimate
dw, Lk = 8.5, 2 + 4 + 1.0
out['G837_support'] = dict(lost_mm2=9.0, lost_fraction=9.0 / 601.2417, distance_from_screw_axis_mm=[math.hypot(16, 16), math.hypot(19, 19)],
    clamp_cone_outer_radius_mm=(dw + 2 * Lk * math.tan(math.radians(30))) / 2, note='VDI 2230-style cone, tan(phi)~0.6 upper bound; frame 2 + backing 4 + washer 1 mm')

# 10. Main-support context from project numbers (R7): plain-bush clearance vs 1 mrad
c = 0.0505; Lsp = 95.0
out['G1_bush_clearance'] = dict(c_radial_mm=c, span_mm=Lsp, tilt_mrad_project_formula=4 * c / Lsp * 1e3,
    c_needed_for_1mrad_mm=1e-3 * Lsp / 4, note='project formula 4c/95 (R7); clearance alone exceeds the 1 mrad screen before any load')

# 11. Weld flatness requirement vs ISO 13920 class E
out['G830_flatness'] = dict(required_mm=0.15, ISO13920_E_120_400_mm=1.0, ratio=1.0 / 0.15)
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(json.dumps(out, indent=1))
