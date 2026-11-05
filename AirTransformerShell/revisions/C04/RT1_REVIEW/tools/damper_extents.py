"""Usage: python damper_extents.py <damper_parts_bbox.json> <R21 native dir> <out.json>
Summarise R21 P/R product extents beyond the 706 mm flange, in the R21 test frame
(shaft axis = test Y, flange height = test X, flow depth = test Z), and compare with C04 reservations."""
import json,sys,collections
d=json.load(open(sys.argv[1]));nat=sys.argv[2]
parts={p['pn']:p for p in json.load(open(f'{nat}/R20_PARTS.json'))}
res={}
for tag in 'PR':
    occ={o['occurrence']:o for o in json.load(open(f'{nat}/R20_{tag}_OCCURRENCES.json'))}
    fl=[b for n,b in d[tag] if occ[n]['pn']==tag+'101']
    F=fl[0];depth=round(max(b[5] for b in fl)-min(b[2] for b in fl),2)
    g=collections.defaultdict(list)
    for n,b in d[tag]:
        o=occ[n]
        if o.get('physical_class') in ('DRY_TEST_FACILITY','WET_TEST_SUPPORT') or o.get('scope')=='FIXTURE' or o['pn'].startswith('BUY53'):continue
        g[o['pn']].append(b)
    env={pn:[min(b[i] for b in bs) for i in range(3)]+[max(b[i] for b in bs) for i in range(3,6)] for pn,bs in g.items()}
    nonfast={pn:e for pn,e in env.items() if not pn.startswith(('H14','HW','STD'))}
    drive=sorted(((round(F[1]-e[1]),pn,parts.get(pn,{}).get('name','')) for pn,e in nonfast.items() if e[1]<F[1]-1),reverse=True)
    fb=sorted(((round(e[4]-F[4]),pn,parts.get(pn,{}).get('name','')) for pn,e in nonfast.items() if e[4]>F[4]+1),reverse=True)
    gear=env.get('BUY504')
    res[tag+'_gear_pair_test_bbox']=gear
    res[tag]=dict(flange_test_bbox=F,flange_face_to_face_mm=depth,
      drive_end_beyond_flange_mm=drive[:8],feedback_end_beyond_flange_mm=fb[:4],
      body_height_extent_test_X=[min(e[0] for e in nonfast.values()),max(e[3] for e in nonfast.values())])
c04=dict(bed_pitch_mm=840,flange_width_mm=706,gap_between_A_B_flanges_mm=134,drive_reserve_along_shaft_mm=170,drive_reserve_X_Z_mm=[160,220],rear_side_skin_cutout_X_Z_mm=[161,222])
P=res['P'];need_two_fb=2*P['feedback_end_beyond_flange_mm'][0][0]
res['comparison']=dict(c04=c04,need_gap_two_feedback_ends_mm=need_two_fb,shortfall_mm=need_two_fb-134,
  need_gap_feedback_plus_drive_to_bearing_mm=P['feedback_end_beyond_flange_mm'][0][0]+[x for x in P['drive_end_beyond_flange_mm'] if x[1]=='BUY_R13_7206'][0][0],
  P_gear_pair_height_and_depth_mm=[round(res['P_gear_pair_test_bbox'][3]-res['P_gear_pair_test_bbox'][0]),round(res['P_gear_pair_test_bbox'][5]-res['P_gear_pair_test_bbox'][2])])
print(json.dumps(res,indent=1,ensure_ascii=False));json.dump(res,open(sys.argv[3],'w'),indent=1,ensure_ascii=False)
