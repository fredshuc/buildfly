"""Usage: python cube_screens.py <cube_concept.json> <out.json>
Path-loss band for the cube Z-flow topology versus the C04/C07 selector-box path (RT1 flow_screen basis),
fan-power difference, and the damper end-housing packaging check at the chosen bed pitch."""
import json,sys
c=json.load(open(sys.argv[1]));rho=1.18;Q=4870/3600
q=lambda v:.5*rho*v*v
qP=q(Q/(0.630*0.345));qm=q(c['mouth_velocity_process_ms'])
terms={'P damper in (K 0.3-0.8 on port q)':(0.3*qP,0.8*qP),'damper jet to mouth (K 0.5-1 on port q)':(0.5*qP,1.0*qP),
 'turn from header into coil (K 0.5-1.5 on mouth q)':(0.5*qm,1.5*qm),'coil (assumed)':(60,60),
 'coil exit into collector (K 0.5-1.5 on mouth q)':(0.5*qm,1.5*qm),'collector to mouth (K 0.5-1)':(0.5*qm,1.0*qm),
 'P damper out (K 0.3-0.8 on port q)':(0.3*qP,0.8*qP)}
lo=sum(v[0] for v in terms.values());hi=sum(v[1] for v in terms.values())
c04=(219+2*0.3*qP,278+2*0.8*qP)   # RT1 independent internal band plus the same two dampers
save=(c04[0]-hi,c04[1]-lo)
eta=0.6
out=dict(port_q_Pa=round(qP,1),mouth_q_Pa=round(qm,1),terms={k:[round(a,1),round(b,1)] for k,(a,b) in terms.items()},
  cube_process_path_Pa=[round(lo),round(hi)],selector_box_path_Pa_same_basis=[round(c04[0]),round(c04[1])],
  saving_Pa=[round(max(save[0],0)),round(save[1])],fan_shaft_power_saving_W_at_eta_0p6=[round(max(save[0],0)*Q/eta),round(save[1]*Q/eta)],
  damper_packaging=dict(bed_pitch_mm=c['bed_pitch_mm'],flange_mm=706,gap_between_beds_mm=c['bed_pitch_mm']-706,
     R21_feedback_end_beyond_flange_mm=217,needed_for_two_inboard_feedback_ends_mm=434,
     note='Topology-independent: side-by-side 706 mm dampers with shafts along Y need >=434 mm between beds unless drive and feedback share one end.'))
print(json.dumps(out,indent=1));json.dump(out,open(sys.argv[2],'w'),indent=1)
