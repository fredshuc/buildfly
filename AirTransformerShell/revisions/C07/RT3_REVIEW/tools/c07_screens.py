"""Closed-form screens for C07 (SI/mm). Usage: python c07_screens.py <c07_checks.json> <out.json>
(1) tie-rod preload band vs ordinary M8 tightening; (2) differential thermal growth of the HX frame inside a
metal-to-metal stop loop of 14 stiff rods; (3) trap seal vs fan shut-off; (4) static side-hole probe in the
supply-side perforation jets; (5) withdrawal clearance budget."""
import json,math,sys
c=json.load(open(sys.argv[1]))
out={}
A_g=37632e-6;n_rod=14;stop_area=14*48  # mm2 per face
Fg=[p*A_g for p in (15e3,60e3)]
out['gasket_force_per_face_N']=[round(f) for f in Fg]
out['rod_share_of_gasket_force_N']=[round(f/n_rod) for f in Fg]
# (1) ordinary torque: F = T/(K d), K = 0.2
tor={T:round(T/(0.2*0.008)) for T in (5,10,25)}
out['M8_preload_from_torque_N']=tor
out['bed_clamp_if_torqued_kN']={T:round(n_rod*F/1e3,1) for T,F in tor.items()}
out['stop_bearing_MPa_if_torqued']={T:round(n_rod*F/stop_area,1) for T,F in tor.items()}
# (2) thermal: HX frame depth 220 mm between the two stop planes; rods 294 mm at cavity temperature
E=200e3;As=36.6;Ag=math.pi*16;L=294
k_rod=E*Ag/L  # N/mm, gross section
th=[]
for alpha,mat in ((12e-6,'steel frame'),(23e-6,'aluminium frame')):
    for dT in (20,40,60):
        d=220*alpha*dT
        F=k_rod*d
        th.append(dict(frame=mat,dT_K=dT,growth_mm=round(d,3),added_force_per_rod_kN=round(F/1e3,2),rod_stress_MPa=round(F/As),
            bed_total_kN=round(n_rod*F/1e3,1),stop_bearing_MPa=round(n_rod*F/stop_area,1)))
out['rod_stiffness_kN_per_mm']=round(k_rod/1e3,1)
out['thermal_stack']=th
out['thermal_note']='Rigid rods with metal stops: the frame growth is forced into rod stretch. Water range 5-80 C (HYD-R2). Compliance (disc springs) of ~0.5-1 kN/mm per rod would keep the added force to ~0.03-0.2 kN.'
# (3) trap seal vs fan shut-off
seal=90;p_seal=seal*9.81
out['trap']=dict(seal_mm=seal,seal_Pa=round(p_seal),duty_Pa=550,shutoff_Pa_typical=[round(1.3*550),round(1.8*550)],
   margin_at_duty=round(p_seal/550,2),margin_at_shutoff=[round(p_seal/(1.3*550),2),round(p_seal/(1.8*550),2)])
# (4) side-hole static probe 4 mm into the HX recess, ~43 mm downstream of the plate (x/d ~2.2)
rho=1.18;vf=4870/3600/0.612;phi=120*math.pi*0.019**2/4/(0.612*0.125)
vj=vf/(0.65*phi);qj=0.5*rho*vj**2
out['static_probe']=dict(hole_jet_velocity_ms=round(vj,2),jet_dynamic_Pa=round(qj,1),hx_dp_assumed_Pa=60,
   bias_if_10_to_30pct_of_jet_q_pct_of_HX_dp=[round(100*.1*qj/60),round(100*.3*qj/60)],
   probe_to_plate_mm=40+4,x_over_d=round(44/19,2))
# (5) withdrawal clearance budget from the checks
tips=c['park_guide_tip_to_HX_face_plane_mm']
out['withdrawal_X_clearance_mm']=dict(park_guide_tips=min(tips.values()),face_gasket=4.2,guide_and_cheek_tips=5.0,lower_tie_rods_below_feet_Z=6.0)
out['installed_height_mm']=c['installed_height']['height_above_floor_mm']
print(json.dumps(out,indent=1));json.dump(out,open(sys.argv[2],'w'),indent=1)
