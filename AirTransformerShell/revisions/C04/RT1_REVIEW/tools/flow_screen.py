"""Usage: python flow_screen.py <C04 dir> <out.json>
Independent first-principles flow screen for C04 (SI units). No CFD.
Reads C04 design.py and flow_checks.json; writes flow_screen.json.
Quantities: velocities and dynamic heads at each section, loss-coefficient audit,
distribution-authority ratios for P and R, HX regime, perforation-jet length and
an independent path-loss band with stated K ranges."""
import sys,json,math
from pathlib import Path
src=Path(sys.argv[1]);sys.path.insert(0,str(src))
import design as D
fc=json.loads((src/'flow_checks.json').read_text())
rho,nu=1.18,1.55e-5
Q=4870/3600
A={'P_port':.630*.345,'R_port':.630*.180,'box':(D.OUTER+2-(D.FOOT-2))/1000*.716,'throat':D.DEPTH/1000*D.W/1000,
   'channel_total':D.N*D.W/1000*(D.DEPTH/D.N/math.sqrt(1+D.SLOPE**2)-D.T)/1000,'face':D.W*D.H/1e6}
q=lambda v:.5*rho*v*v
sec={k:dict(area_m2=round(a,5),v_ms=round(Q/a,3),q_Pa=round(q(Q/a),2)) for k,a in A.items()}
# perforated plate: model law vs Idelchik thin sharp-edged plate (Diagram 8-6), referenced to face velocity
vf=Q/A['face']
def phi(d):return 120*math.pi*(d/1000)**2/4/(D.W*D.BAND/1e6)
def model_one(d,cd=.65):return q(vf/(cd*phi(d)))
def idel(d):
    f=phi(d);z=(.707*math.sqrt(1-f)+1-f)**2/f**2;return z*q(vf)
plates=[dict(d_mm=d,phi=round(phi(d),4),model_Pa=round(model_one(d),2),idelchik_Pa=round(idel(d),2)) for d in fc['diameter_mm']]
# balancing differential across bands (two plates per path)
bal=dict(model_shortest_minus_longest_Pa=round(2*(model_one(18.1)-model_one(20.0)),2),idelchik_shortest_minus_longest_Pa=round(2*(idel(18.1)-idel(20.0)),2))
# channel friction: Blasius vs assumed 0.03
vc=sec['channel_total']['v_ms'];cp=(D.DEPTH/D.N/math.sqrt(1+D.SLOPE**2)-D.T)/1000;dh=2*D.W/1000*cp/(D.W/1000+cp)
Re=vc*dh/nu;fb=.316*Re**-.25
L=fc['length_m']
fric=dict(Re=round(Re),dh_mm=round(dh*1000,1),f_blasius=round(fb,4),f_model=.03,
  longest_minus_shortest_two_sides_Pa_model=round(2*.03*(L[-1]-L[0])/dh*q(vc),2),
  longest_minus_shortest_two_sides_Pa_blasius=round(2*fb*(L[-1]-L[0])/dh*q(vc),2))
# independent path-loss band at 4870 m3/h; K referenced to the named section
qP,qR,qc,qt=q(Q/A['P_port']),q(Q/A['R_port']),q(vc),q(Q/A['throat'])
terms=[ # name, section, K_low, K_high, basis
 ('port jet into box and 90 deg turn (supply)','port',1.0,1.5,'sudden expansion + sharp turn, Idelchik 4-1/6-7 class'),
 ('box to throat','throat',.05,.15,'mild contraction'),
 ('channel entry at guide leading edges','channel',.2,.4,'thin-edge inlet'),
 ('72 deg turn and 3.4:1 expansion into band (supply)','channel',.5,1.0,'Borda-Carnot (1-1/3.41)^2=0.50 plus turn'),
 ('band to slot contraction and turn (collector)','channel',.5,.8,'sharp contraction with turn'),
 ('slot exit into box (collector)','channel',1.0,1.0,'free discharge into plenum'),
 ('box to port (collector)','port',.5,1.0,'contraction + turn'),
]
qs={'port':None,'channel':qc,'throat':qt}
def band(tag):
    qp=qP if tag=='P' else qR
    lo=hi=0;rows=[]
    for n,s,a,b,basis in terms:
        qq=qp if s=='port' else qs[s];rows.append(dict(term=n,K=[a,b],ref=s,Pa=[round(a*qq,1),round(b*qq,1)],basis=basis));lo+=a*qq;hi+=b*qq
    fr=2*fb*(sum(L)/len(L))/dh*qc;pl=2*sum(idel(d) for d in fc['diameter_mm'])/8
    lo+=fr+pl+60;hi+=fr+pl+60
    return dict(terms=rows,friction_two_sides_Pa=round(fr,1),plates_two_Pa=round(pl,1),hx_assumed_Pa=60,total_Pa=[round(lo),round(hi)])
paths={'P_4870':band('P'),'R_4870':band('R')}
r=paths['R_4870'];hx_half=60*.5**1.15
paths['R_2435_laminar_HX']=dict(total_Pa=[round((r['total_Pa'][0]-60)/4+hx_half),round((r['total_Pa'][1]-60)/4+hx_half)],hx_Pa=round(hx_half,1),note='HX taken as dp~Q^1.15 (laminar fin channels), other terms ~Q^2')
# distribution authority: branch resistance (both sides + HX) over port dynamic head
br=fc['branch_and_screens_Pa_at_equal_flow'];brm=sum(br)/len(br)+60
auth={}
for tag,qp in (('P',qP),('R',qR)):
    M=brm/qp
    auth[tag]=dict(branch_Pa=round(brm,1),q_port_Pa=round(qp,1),M=round(M,2),
       band_flow_deviation_pct_for_c=[round(50*c/M,1) for c in (.3,.5,1.0)],c_values=[.3,.5,1.0],
       note='dQ/Q = 0.5*c*q_port/dp_branch; c = fraction of port dynamic head surviving as throat total-pressure spread')
auth['R_2435_laminar_HX']=dict(M=round((brm-60)/4+hx_half,1)/(qR/4),note='HX laminar improves R authority slightly at half flow')
# box geometry for jet development
Dbox=(D.OUTER+2-(D.FOOT-2))/1000
geo=dict(box_depth_m=round(Dbox,4),P_port_top_to_throat_m=round((D.THROAT-535)/1000,3),R_port_top_to_throat_m=round((D.THROAT-845)/1000,3),
  L_over_D_P=round((D.THROAT-535)/1000/Dbox,2),L_over_D_R=round((D.THROAT-845)/1000/Dbox,2))
# HX regime (fin gap from 2.0 mm pitch, 0.133 mm fin from STEP; coating thickness unknown -> two cases)
hx=[]
for coat in (0.0,.15):
    gap=2.0-.133-2*coat;sig=(25.4-9.52-2*coat)/25.4*gap/2.0
    vmax=vf/sig;vg=vf*2.0/gap;Reg=vg*2*gap/1000/nu
    hx.append(dict(coating_mm_per_side=coat,fin_gap_mm=round(gap,3),sigma_min=round(sig,3),v_max_ms=round(vmax,2),Re_gap=round(Reg),
      plate_friction_Pa=round(96/Reg*.152/(2*gap/1000)*q(vg),1),tube_rows_form_Pa=[round(6*.3*q(vmax),1),round(6*.5*q(vmax),1)]))
jets=dict(plate_to_fin_mm=12+31.65,x_over_d=[round((12+31.65)/d,2) for d in (18.1,20.0)],hole_pitch_mm=25,hole_jet_v_ms=round(vf/(.65*phi(19)),2))
# cross-leak tolerance: moisture carry-over from R into P outlet
def leak(dx_allow_gkg,xR_minus_xP,dp=300,cd=.6):
    eps=dx_allow_gkg/xR_minus_xP;Ql=eps*Q;Aleak=Ql/(cd*math.sqrt(2*dp/rho))
    return dict(allowed_fraction_pct=round(100*eps,2),allowed_m3h=round(Ql*3600,1),equiv_leak_area_mm2_at_dp=round(Aleak*1e6),dp_Pa=dp,
      mean_gap_mm_over_R_damper_seal_lines=round(Aleak*1e6/(2*630+2*180+630),3))
leakage=[leak(.2,30),leak(.5,30)]
# switching carry-over volume per bed (two boxes + two guide stacks + HX void)
box_v=Dbox*.716*(D.THROAT-144)/1000
stack=0
for i in range(8):
    a=D.guide(i);b=D.guide(i+1);poly=a+b[::-1]
    s=sum(x1*z2-x2*z1 for (x1,z1),(x2,z2) in zip(poly,poly[1:]+poly[:1]))/2
    stack+=abs(s)/1e6*D.W/1000
vol=2*box_v+2*stack+.152*.612*1.0*.85
carry=dict(bed_air_volume_m3=round(vol,3),flush_time_s_at_P=round(vol/Q,2),water_g_if_R_at_30gkg_over_P_2gkg=round(vol*rho*(30-2),1))
# coil bypass through an uncompressed seat: 652 x 1040 seal outline per face, uniform mean gap
def seat(gap_mm,dp=150,cd=.6):
    A=2*(652+1040)*gap_mm/1e6;Ql=cd*A*math.sqrt(2*dp/rho)
    return dict(mean_gap_mm=gap_mm,dp_Pa=dp,leak_m3h_per_face=round(Ql*3600,1),fraction_of_P_pct=round(100*Ql/Q,2))
seats=[seat(.1),seat(.2),seat(.5)]
out=dict(seat_leak_per_face=seats,sections_at_4870=sec,plates=plates,balancing=bal,friction=fric,independent_paths=paths,authority=auth,box_geometry=geo,hx_regime=hx,perforation_jets=jets,cross_leak_tolerance=leakage,switch_carryover=carry,
  model_reported=dict(P_mix4_Pa=324.83,R_mix4_Pa=275.92,R2435_mix4_Pa=68.98))
print(json.dumps(out,indent=1));json.dump(out,open(sys.argv[2],'w'),indent=1)
