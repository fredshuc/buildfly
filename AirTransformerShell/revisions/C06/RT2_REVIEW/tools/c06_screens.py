"""Closed-form screens for C06 (SI). Usage: python c06_screens.py <c06_checks.json> <out.json>
Gasket clamp reaction and cassette overturning, series leak through the zero-clearance carrier fit,
untrapped drain leakage, trap height available, HX X-direction support frequency, machine envelope."""
import json,math,sys
c=json.load(open(sys.argv[1]));rho=1.18;Q=4870/3600;E=200e9;g=9.81
A=c['gasket_face_area_mm2']/1e6
out={}
# 1 gasket reaction: closed-cell sponge CLD band at ~30 % deflection (ASTM D1056 grades 2A1..2A3 order of magnitude)
cld=[15e3,35e3,60e3]
z_gasket=1704;z_bearer=142.5;lever=(z_gasket-z_bearer)/1000;bearer_gap=(327-116)/1000
out['gasket_clamp']=[dict(CLD_kPa=p/1e3,force_kN_per_face=round(p*A/1e3,2),overturning_kNm=round(p*A*lever/1e3,2),
   bearer_couple_kN=round(p*A*lever/bearer_gap/1e3,1),per_lead_screw_N=round(p*A/8)) for p in cld]
out['gasket_clamp_basis']=dict(gasket_area_m2=A,lever_m=round(lever,3),bearer_spacing_m=bearer_gap,compression_stroke_mm=6.0-4.2,
   note='Only bearer contacts at Z104 found between cassette and structure (c06_checks.json); clamp reacts through cheek lugs into the cassette.')
# 2 series leak: guide/cheek tips flush with HX frame face, carrier window zero-clearance sliding fit on cheeks and guides 0/8
per=2*(615+1001.5)/1000
def series(g1,g2,dp=150,cd=.6):
    geff=1/math.sqrt(1/g1**2+1/g2**2) if g1 and g2 else 0
    Ql=cd*per*geff/1000*math.sqrt(2*dp/rho);return dict(tip_gap_mm=g1,carrier_gap_mm=g2,effective_gap_mm=round(geff,3),leak_m3h_per_face=round(Ql*3600,1),pct_of_P=round(100*Ql/Q,2))
out['carrier_series_leak']=dict(perimeter_m=per,cases=[series(.3,.3),series(.5,.5),series(1,.5)])
# 3 untrapped 20 mm drains
def drain(dp):
    a=math.pi/4*.02**2;Ql=.6*a*math.sqrt(2*dp/rho);return dict(dp_Pa=dp,m3h_each=round(Ql*3600,1),pct_of_P_each=round(100*Ql/Q,2))
out['untrapped_drain']=dict(bore_mm=20,box_drains=4,tray_nozzles=2,cases=[drain(150),drain(300)],
  trap_seal_needed_mm=round(300/9.81,0)*2,stub_outlet_above_ground_mm=c['drains']['AF_DRAIN_STUB'][2],tray_nozzle_outlet_z=c['drains']['A_HX_TRAY_NOZZLE'][2])
# 4 HX X-direction: risers braced only in Y-Z (brace X thickness 30, Y span), forks restrain Y only
b,t=.040,.003;I=(b**4-(b-2*t)**4)/12;L=.996
for m in (80,110):
    out[f'hx_x_sway_m{m}']=dict(f_pinned_Hz=round(math.sqrt(4*3*E*I/L**3/m)/(2*math.pi),1),f_fixed_Hz=round(math.sqrt(4*12*E*I/L**3/m)/(2*math.pi),1))
out['restraint_planes']=dict(riser_brace=c['restraint_bboxes']['A_RISER_BRACE_275'],fork=c['restraint_bboxes']['A_TOP_FORK_(0, 0)'],
  note='Brace is a 30 mm (X) bar spanning Y-Z; forks are 4 mm (Y) plates: both restrain Y only.')
# 5 seal-carrier ring out-of-plane bending between lead screws (screws only at Y +-337, Z 1235/1547/1859/2173)
perim=2*(650+1036)
Ir=18.5*5**3/12  # mm4: 18.5 mm land, 5 mm plate, bending out of plane
spans={'top_bottom_between_side_screws_mm':674,'side_between_screws_mm':312}
ring=[]
for p in cld:
    q=p*A/perim  # N/mm line load
    row=dict(CLD_kPa=p/1e3,line_load_N_per_mm=round(q,3))
    for k,L in spans.items():
        row['deflection_'+k]=round(5*q*L**4/(384*200e3*Ir),2)
    ring.append(row)
out['carrier_ring_bending']=dict(I_mm4=round(Ir,1),compression_stroke_mm=1.8,cases=ring,
  note='Simply supported between screw points; linear estimate. Deflection above ~1.8 mm means the gasket is not compressed there.')
# 6 plate-access slot ligaments in the outboard cheek
pc=json.load(open(sys.argv[1].replace('c06_checks.json','panel_cheek.json')))
out['cheek_slot_ligament']=dict(material_left_in_slot_band_mm3=pc['AF_CHEEK_306_material_in_u10.5_15_mm3'],
  equivalent_total_ligament_height_mm=round(pc['AF_CHEEK_306_material_in_u10.5_15_mm3']/(4.5*1.5),2),
  forward_strip_mm3=pc['AF_CHEEK_306_forward_strip_u0_10.5_mm3'],uncut_inboard_cheek_band_mm3=pc['AF_CHEEK_-307.5_material_in_u10.5_15_mm3'])
print(json.dumps(out,indent=1));json.dump(out,open(sys.argv[2],'w'),indent=1)
