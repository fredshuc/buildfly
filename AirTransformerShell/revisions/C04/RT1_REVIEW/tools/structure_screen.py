"""Closed-form structural screens for C04 (SI). Inputs from C04 build geometry and the HX/damper mass estimates
produced by masses.py and damper_mass.py (run from the results directory). Screens only; no code check."""
import json,math
E=200e9;nu=.3;g=9.81
def rhs(b,t):
    A=b*b-(b-2*t)**2;I=(b**4-(b-2*t)**4)/12;return A,I
out={}
# HX on four 40x40x3 risers, L=0.996 m; beam 50x50x3 on top; HX mass band
A,I=rhs(.040,.003);L=.996
for m in (80,110):
    k_ff=4*12*E*I/L**3;k_cant=4*3*E*I/L**3
    # rocking about Y: two riser lines 0.160 m apart (x centres 295 and 455)
    kax=E*A/L;kth=4*kax*(0.080)**2
    h=(575+1150-1100)/1000 # HX CG above riser tops: local CG z575 at global 1725, riser top 1100
    Jcg=m*(1.25**2+.22**2)/12
    f=lambda k,mm:math.sqrt(k/mm)/(2*math.pi)
    fs_ff=f(k_ff,m);fs_c=f(k_cant,m);fr=math.sqrt(kth/(m*h*h+Jcg))/(2*math.pi)
    comb=lambda a,b:1/math.sqrt(1/a**2+1/b**2)
    out[f'hx_support_m{m}']=dict(riser_A_mm2=round(A*1e6),riser_I_mm4=round(I*1e12),sway_k_fixed_N_per_mm=round(k_ff/1e3),sway_k_pinned_top_N_per_mm=round(k_cant/1e3),
      f_sway_fixed_Hz=round(fs_ff,1),f_sway_pinned_Hz=round(fs_c,1),f_rocking_X_Hz=round(fr,1),f_combined_fixed_Hz=round(comb(fs_ff,fr),1),f_combined_pinned_Hz=round(comb(fs_c,fr),1),
      cg_above_riser_top_m=h,euler_load_per_riser_kN=round(math.pi**2*E*I/L**2/1e3,1))
# corner posts 50x50x3, 2.446 m, cantilever from base, no top Y members and no end base cross members
A2,I2=rhs(.050,.003);L2=2.446
out['posts']=dict(I_mm4=round(I2*1e12),k_cantilever_each_N_per_mm=round(3*E*I2/L2**3/1e3,2),k_four_N_per_mm=round(4*3*E*I2/L2**3/1e3,1),
  note='bare-frame racking stiffness if skins are not designed as shear diaphragms')
# guides: 1.5 mm plate, 612 mm span between cheeks, 17.7 deg from vertical
t=.0015;a=.612;rho_s=7900;D=E*t**3/(12*(1-nu**2));m=rho_s*t
f_ss=math.pi/2/a**2*math.sqrt(D/m);f_cc=f_ss*22.37/9.87
w=m*g*math.sin(math.atan(.32))
d_ss=5*w*a**4/(384*D);d_cc=w*a**4/(384*D)
h=.0366;Vc=math.sqrt(15*E*t**3*h/(1.18*a**4*(1-nu**2)))
out['guides']=dict(f1_simply_supported_Hz=round(f_ss,1),f1_clamped_Hz=round(f_cc,1),selfweight_sag_ss_mm=round(d_ss*1000,2),selfweight_sag_cc_mm=round(d_cc*1000,2),
  sag_per_10Pa_ss_mm=round(5*10*a**4/(384*D)*1000,2),miller_critical_velocity_ms=round(Vc,1),channel_velocity_ms=7.55)
# cassette and front damper overhang on the 2.5 mm flange
dm=json.load(open('damper_mass.json'))
for k in 'PR':dm[k]['product_total_steel_equiv_kg']=round(dm[k]['product_body']+dm[k]['drive_end']+dm[k]['feedback_end'],1)
out['dampers_steel_equivalent_kg']=dm
fp=dm['P']['product_total_steel_equiv_kg'];fr_=dm['R']['product_total_steel_equiv_kg']
out['front_pair_overhang']=dict(mass_kg=round(fp+fr_,1),moment_Nm_at_90mm=round((fp+fr_)*g*.09),note='front P+R damper pair per bed carried by the 2.5 mm DUAL_VALVE_FLANGE of an unsupported cassette')
ms=json.load(open('masses.json'))
out['cassette']=dict(mass_kg=ms['cassette_kg'],cg_z_mm=ms['cassette_cg_z_mm'],support='none modelled; BOTTOM at Z142.5 is 38.5 mm above FLOOR top Z104')
tot=ms['host_kg']+ms['four_cassettes_kg']+2*95+4*fp*.6+4*fr_*.6+60
out['machine_mass_estimate_kg']=dict(value=round(tot),basis='host+4 cassettes (7.9 kg/dm3) + 2x95 kg HX wet + 8 dampers at 0.6 x steel-equivalent + 60 kg valves/piping')
print(json.dumps(out,indent=1));json.dump(out,open('structure_screen.json','w'),indent=1)
