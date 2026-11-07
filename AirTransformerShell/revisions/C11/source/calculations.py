"""Reproducible local calculations, N/mm/MPa. No test results are fabricated.

Supplier curves are typical, digitised approximately, and cannot establish a
batch maximum. The procurement acceptance envelope is a DESIGN REQUIREMENT.
"""
from pathlib import Path
import math,json,csv
HERE=Path(__file__).resolve().parents[1]
E=HERE/'evidence';E.mkdir(exist_ok=True)
ES=200000.;GS=ES/2.6;FY=235.;FU=360.;GAMMA=1.25
CURVE=[(10,2.8),(15,3.5),(20,4.3),(25,5.5),(30,6.7),(35,7.7),(40,9.6)]
def pressure(strain):
    assert 10<=strain<=40
    for (a,p),(b,q) in zip(CURVE,CURVE[1:]):
        if a<=strain<=b:return (p+(q-p)*(strain-a)/(b-a))*6.894757/1000
def compression(free,gap):return 100*(1-gap/free)
def write_csv(name,rows):
    with (HERE/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def cantilever(P,L,b,t):
    I=b*t**3/12
    return {'force_N':P,'span_mm':L,'width_mm':b,'thickness_mm':t,
            'stress_MPa':6*P*L/(b*t*t),'tip_deflection_mm':P*L**3/(3*ES*I)}
def run():
    report={'status':'LOCAL_DESIGN_CALCULATIONS_NOT_MANUFACTURING_OR_TEST_RELEASE',
      'units':'N mm MPa; room-temperature S235 screening E200GPa fy235 fu360; material certificate and service derating required',
      'sources':[
       {'title':'Saint-Gobain Norseal R10480S TDS','url':'https://www.tapesolutions.saint-gobain.com/en-us/files/2751/download','scope':'typical25% CFD35kPa; closed-cell silicone; not a batch guarantee'},
       {'title':'Stockwell closed-cell silicone sponge compression curves','url':'https://www.stockwell.com/data-sheets/cfd-curves-silicone-sponges.pdf','scope':'R10480S legacy illustrative curve; approximate digitisation; psi converted using6.894757kPa/psi'},
       {'title':'DOWSIL7091 product','url':'https://www.dow.com/en-us/pdp.dowsil-7091-adhesive-sealant.02436621h.html','scope':'material identity and general service properties; does not certify actual jacket adhesion'},
       {'title':'SCI P362','url':'https://steelconstruction.info/images/6/6a/SCI_P362.pdf','scope':'CJP parent-metal resistance conditional on suitable matching qualified weld; no sub3mm EC3 fillet claim'},
       {'title':'JRC steel design worked examples','url':'https://publications.jrc.ec.europa.eu/repository/bitstream/JRC96658/jrc_steel_report_2015_07_22.pdf','scope':'weld/steel calculation method; no project certification'}],
      'curve_strain_percent_pressure_psi':CURVE,
      'gasket_procurement':'Selected thickness +/-0.10mm is a required batch selection, not standard supplier stock tolerance. Require pressure <=0.080MPa throughout20..35% compression after thermal/wet conditioning. Obtain supplier approval for knife-cut12/10mm strips on carrier liner and bonded scarf; no unsupported narrow die-cut claim.',
      'pressure_design_envelope_Pa':[-1000,1000],
      'pressure_status':'provisional design upper bound; actual fan shutoff and fault differential must be supplied; no operation above envelope'}
    seal=[]
    for name,free,gap,gmin,gmax,area in [('FACE',6.35,4.45,4.20,4.70,1032*644-1008*620),
        ('POCKET_A',4.76,3.5,3.35,3.65,22.5*26.5-2.5*6.5),
        ('POCKET_B',4.76,3.5,3.35,3.65,51.5*26.5-31.5*6.5)]:
        cmin=compression(free-.10,gmax);cmax=compression(free+.10,gmin)
        seal.append({'seal':name,'free_mm':free,'selected_thickness_tolerance_mm':.10,'nominal_gap_mm':gap,'gap_min_mm':gmin,'gap_max_mm':gmax,
         'compression_min_percent':cmin,'compression_max_percent':cmax,'area_mm2':area,
         'typical_force_min_N':area*pressure(cmin),'typical_force_max_N':area*pressure(cmax),
         'required_batch_pressure_max_MPa':.080,'design_reaction_max_N':area*.080,
         'acceptance':'force curve/batch and leakage test OPEN; Pocket also has unresolved crown interference' if 'POCKET' in name else 'HX allowable force OPEN;1000N fixture limit is not service capacity'})
    report['seals']=seal;write_csv('C11_SEAL_COMPRESSION_CALC.csv',seal)
    report['face_gap_budget']={'nominal_mm':4.45,'total_half_range_mm':.25,
      'components_full_range_mm':{'HX_land_peak_to_valley':.10,'Shell_bed_peak_to_valley':.10,'stop_height':.10,'assembly_and_thermal_parallelism':.10,'elastic_change':.10},
      'acceptance':'Measure actual opposed gap at20 stations with core on fixed support datums. Reject outside4.20..4.70 at qualified cold/hot state. Tolerances are worst-case additive, not RSS.'}
    jaws={'left_YMIN_3p5mm_net_at_D10':cantilever(500,15,39-10,3.5),'XMAX_net_at_D5.5':cantilever(500,45,24-5.5,8),'Y_edge_net_at_D10_countersink_conservative':cantilever(500,27,24-10,8)}
    jaw=max(jaws.values(),key=lambda x:x['stress_MPa'])
    # Carrier + welded18mm skirt: true centroid and parallel-axis terms.
    A1,A2=42*2,2*18;y1,y2=19,9;cy=(A1*y1+A2*y2)/(A1+A2)
    I=42*2**3/12+A1*(y1-cy)**2+2*18**3/12+A2*(y2-cy)**2
    w=.080*12;L=180
    carrier={'line_load_N_mm':w,'span_mm':L,'I_mm4':I,'centroid_from_skirt_bottom_mm':cy,
      'deflection_mm':5*w*L**4/(384*ES*I),'stress_MPa':w*L*L/8*max(cy,20-cy)/I,
      'rail_notch_local_deflection_mm':5*w*41**4/(384*ES*(42*2**3/12)),
      'scope':'Simply-supported span under maximum accepted batch pressure; continuous skirt seam and rail backing at notches required. Does not prove the complete HX frame.'}
    report['face_clamps']={'count_per_core':20,'torque_Nm':.5,'K_range':[.2,.3],'preload_min_N':.5/(.3*.005),'preload_max_N':500,
      'M5_tensile_area_mm2':14.2,'max_tensile_stress_MPa':500/14.2,'jaw':jaw,'jaw_net_sections':jaws,'carrier':carrier,
      'total_max_preload_N':10000,'total_min_preload_N':20*.5/(.3*.005),'gasket_design_max_N':seal[0]['design_reaction_max_N'],
      'preload_interpretation':'Bolt preload is an upper-bound fastener demand, not a proved toe reaction. Sleeve/stop/frame contact stiffness and jaw seating determine force split. Demonstrate measured contact force and full seal compression; the20-bolt sum alone is not acceptance.',
      'M5_actual_thread_engagement_mm':7.55,'M5_left_YMIN_engagement_mm':6.05,'M5_sleeve_thread_shear_at1500N_MPa':1500/(math.pi*4.2*6.05*.5),
      'remaining_stop_reaction_max_N':10000-seal[0]['design_reaction_max_N'],
      'frame_local_bearing_MPa':500/(12*3),'bearing_basis':'Conservative500N on actual12x3mm positive-stop contact; local frame bending and force split still require owner acceptance','thermal_X_requirement_mm':1066*12e-6*75,
      'available_X_slide_each_direction_mm':1.5,
      'status':'LOCAL_JAW_CARRIER_SCREEN_ONLY; HX frame force/thermal sliding and loaded datum acceptance OPEN. M5 standoff1.5kN proof and representative clamp-loop test required.'}
    edge_span=652-17
    strongI=(30*50**3-24*44**3)/12
    proof=1500.;a=3.;horizontal_effective=24.;vertical_effective=10.;weld_area=2*a*(horizontal_effective+vertical_effective)
    weld_I=2*a*horizontal_effective*8**2+2*a*vertical_effective**3/12
    weld_sigma=proof*29/(weld_I/8);weld_tau=proof/weld_area
    gusset_root_force=proof/2*math.sqrt(1+(26/12)**2)
    report['face_clamps']['left_end_support']={'quantity':8,'station_17':'X-410,Ymin-10;39mm-wide3.5mm flush jaw;M5x12;6.05mm engagement','station_19':'X-418,Ymax+10;8mm flush jaw;7.55mm engagement','sleeve_length_mm':12.45,'load_path':'Bottom Y-end frame -> jaw/short M5 sleeve and positive stop -> carrier ->8mm shelf/two3mm gussets ->30x16x3 mount -> unchanged Shell RHS side; no load through fins/copper/skin','plate_500N':cantilever(500,26,30,8),'plate_1500N_proof':cantilever(1500,26,30,8),'plate_basis':'Conservative ungusseted shelf screen; no stiffness credit taken for gussets','mount_perimeter_weld':{'throat_mm':a,'horizontal_effective_mm':horizontal_effective,'vertical_effective_mm':vertical_effective,'proof_vertical_N':proof,'proof_eccentricity_mm':29,'area_mm2':weld_area,'I_mm4':weld_I,'normal_stress_MPa':weld_sigma,'shear_stress_MPa':weld_tau,'equivalent_stress_MPa':math.sqrt(weld_sigma**2+3*weld_tau**2)},'gusset_root_screen':{'two_gussets':True,'triangle_mm':[26,12,3],'effective_root_each_side_mm':6,'double_sided_throat_mm':3,'force_per_gusset_N':gusset_root_force,'equivalent_traction_MPa':gusset_root_force/(2*3*6)},'qualification':'Actual25mm RHS wall/corner fit, a3 weld access/procedure, local wall bending and complete bracket1.5kN proof OPEN. Test bracket/sleeve separately from500N jaw. Thin jaw plate/contact behaviour and actual collector clearance require loaded/tolerance qualification. Upper long ties are rejected, not installed.'}
    report['face_clamps']['long_edge_after_H02_clearance']={'span_mm':edge_span,'left_HX_edge_span_mm':652,'unreinforced_carrier_rejected_deflection_mm':5*w*edge_span**4/(384*ES*I),'unreinforced_carrier_rejected_stress_MPa':w*edge_span**2/8*max(cy,20-cy)/I,'right_RHS50x30x3_I_mm4':strongI,'right_strongback_deflection_mm':5*w*edge_span**4/(384*ES*strongI),'right_strongback_stress_MPa':w*edge_span**2/8*25/strongI,'right_2mm_carrier_17_5mm_overhang':cantilever(w,17.5,1,2),'left_bearing':'Continuous nominal1.55mm ground strip plus8mm gusseted bearing extensions at two Y-end clamps; fixed core planes unchanged','isolated_HX_20x8_rail_screen_deflection_mm':5*w*652**4/(384*ES*(20*8**3/12)),'status':'Shell carrier reinforced; HX HOLD: left edge is restrained through Y-end frame, conservatively screened over652mm. Isolated20x8 rail does not qualify. Actual coupled core frame stiffness or joint HX collector/hold-down revision required before manufacture; do not apply20x500N.'}
    guard=cantilever(100,66,9,6)
    panel_area=257.654896*144
    bond_area=257.654896*144-(257.654896-24)*(144-24)
    report['glands']={'material':'DOWSIL7091 cured silicone,2mm lip/membrane;12mm jacket axial lap;0.4mm slit with renewed20x1.5mm splice',
      'guard':guard,'guard_displacement_limit_mm':.5,
      'pressure_force_upper_bound_N':panel_area*.001,'minimum_skin_bond_area_mm2':bond_area-6*math.pi*6**2,
      'average_pressure_bond_stress_MPa':panel_area*.001/(bond_area-6*math.pi*6**2),
      'design_bond_allowable_MPa':.05,'coupon_requirement_MPa':.25,
      'screw_max_preload_N':375,'screw_proof_N':1000,'M4_tensile_stress_at_proof_MPa':1000/8.78,
      'blind_thread_engagement_mm':3.5,'tap_depth_mm':4,'closed_backer_wall_mm':1,'thread_tip_clearance_mm':.5,
      'thread_shear_area_screen_mm2':math.pi*3.3*3.5*.5,'thread_shear_at_proof_MPa':1000/(math.pi*3.3*3.5*.5),
      'backer_local_stop_bearing_MPa':375/(math.pi*(6**2-2.25**2)),
      'backer_12mm_strip_cantilever_proof':cantilever(1000,6,12,5),
      'skin_punching_shear_at_proof_MPa':1000/(math.pi*12*1.5),
      'load_path':'guard ->3mm washer/M4x16 removable screw ->3.5mm blind thread in5mm backer;2mm metal stop excludes seal preload. Backer bears against skin and is continuously edge-fused. Pressure reaction is bonded, not applied as fictitious50kPa compression on guard.',
      'qualification':'Average adhesion/shear screening does not prove edge peel or cyclic movement. Actual jacket/paint coupons, +/-4mm axial and +/-1mm radial movement,1000N blind-thread proof, wet ageing and leak/spray test remain OPEN.'}
    a,Lw=3,257
    report['A_post_welds']={'number':8,'joint':'CJP single-bevel T-butt,3mm web,0.5mm root face and gap,45deg bevel; matching consumable',
      'effective_throat_mm':a,'gross_length_mm':269,'end_exclusion_each_mm':6,'effective_length_mm':Lw,
      'area_each_mm2':a*Lw,'parent_shear_yield_capacity_each_N':a*Lw*FY/math.sqrt(3),
      'parent_axial_yield_capacity_each_N':a*Lw*FY,
      'web_shear_spring_each_patch_N_mm':GS*3*269/(19+2*3),
      'web_extension_spring_each_patch_N_mm':ES*3*269/(19+2*3),
      'web_stress_method':'Use actual transfer force from frame model divided by3*257; combine normal and shear by von Mises. Spring includes conservative6mm equivalent weld length in addition to19mm clear web.',
      'capacity_status':'CONDITIONAL on demonstrated full root fusion and matching parent-strength weld. Unqualified joint has no released capacity; eight locations alone are insufficient.',
      'fabrication':'Weld webs before pipe/insulation installation. Removable copper root backing from open channel ends; alternate short backsteps on opposing sides. Grind outer X faces flush+0/-0.1. Qualify actual3mm T coupon with macro/root-fusion and bend examination;100%VT and applicable surface examination. Do not call this a sub3mm structural fillet.'}
    plate=cantilever(1000,40,40,8);kplate=1000/plate['tip_deflection_mm'];kweb=ES*2*5*40/80
    kz=1/(1/kplate+1/kweb)
    report['water_skid']={'input':'inputs/C11_HYD_T01_R1_CANDIDATE.zip/load_cases.csv','vertical_foot_design_N':1000,
      'owner_max_foot_N':993.5920990154216,'owner_service_horizontal_per_foot_N':50,'top_plate_screen':plate,
      'metal_only_kz_lower_screen_N_mm':kz,'local_settlement_at1000N_mm':1000/kz,
      'model':'Conservative40mm effective plate strip cantilever40mm; two5mm RHS walls of40mm bearing length compress over80mm. Floor/grout/anchor compliance excluded. Full floor-pad bearing required.',
      'M12_preload_range_N':[20000,25000],'M12_fasteners_per_foot':4,'M12_proof_stress_screen_MPa':25000/84.3,
      'bolt_pattern_mm':[90,60],'owner_slot_pattern_mm':[80,60],'outward_slot_offset_mm':5,'remaining_owner_slot_adjustment_each_direction_mm':[5,15],
      'custom_top_washer':{'dimensions_X_Y_Z_mm':[24,36,18],'bore_mm':13,'slot_bridge_span_mm':14,'net_width_mm':11,'full_preload_N':25000,'stress_MPa':6*(25000*14/4)/(11*18**2),'deflection_mm':25000*14**3/(48*ES*(11*18**3/12)),'allowable_screen_MPa':FY/GAMMA,'riser_side_clearance_mm':3,'basis':'Simply supported washer net strip across14mm slot, central full25kN bolt preload. Actual contact/edge bearing and batch certificate still required.'},
      'minimum_friction_design_requirement':.15,'foot_slip_resistance_at_min_preload_N':4*20000*.15,
      'M10_bridge_preload_range_N':[4800,6000],'bridge_slip_resistance_at_min_preload_N':2*4800*.15,
      'bridge_horizontal_design_N':300,'bridge_plate_horizontal_stress_MPa':300/(100*8),
      'bridge_root_a3_effective88mm_shear_capacity_N':3*88*FU/(math.sqrt(3)*.8*GAMMA),
      'bridge_vertical_500N_accidental_case':cantilever(500,45,100,8),
      'weld_top_plate_capacity_two128mm_a3_N':2*128*3*FU/(math.sqrt(3)*.8*GAMMA),
      'floor_pressure_1000N_MPa':1000/(160*140),
      'ground_anchor_status':'Demand only; no selected anchor or concrete/substrate data. No lifting/forklift or unrestrained transport release. All6 owner2g vertical reactions remain compressive; lateral transport not specified.',
      'shim_settlement_requirement_mm':.10,
      'qualification':'Friction coefficient>=0.15 after actual coating/conditioning required; otherwise design positive shear keys. Owner must recalculate six-foot reactions using measured ground stiffness/settlement. Bolt length changes with0..5mm owner shim.'}
    report['distribution']={'open_area_m2':.612,'design_dp_Pa':1000,'plate_pressure_force_N':612,
      'retention_factor':2,'reaction_per_lock_N':612,'M5_lock_stress_MPa':612/14.2,'cassette_3mm_punch_shear_MPa':612/(math.pi*5.5*3),
      'runner_I_mm4':(10*10**3-6*6**3)/12,
      'runner_midspan_612N_plate_case_deflection_mm':5*(612/2/1040)*305**4/(384*ES*((10*10**3-6*6**3)/12)),
      'status':'OPEN_FRAME installed; optional plate stiffness/rail deflection must be accepted before fitting a plate.1000Pa is an upper envelope, not a measured plate loss. Service bridge/trolley must be locked and loaded before cassette release.'}
    report['condensate']={'rho_kg_m3':1000,'g_m_s2':9.81,'dp_bound_Pa':1000,'minimum_static_head_mm':1000/(1000*9.81)*1000,
      'startup_evaporation_allowance_mm':50,'selected_effective_head_mm':164,
      'pressure_capacity_screen_Pa':(164-50)/1000*1000*9.81,
      'scope':'Four independent traps upstream of any common tundish; pressure-water relief kept separate. Priming, visible air gap, cleanout and negative-pressure inlet fall are required. This sizing alone is not a completed drain assembly.'}
    beamI=(20*40**3-14*34**3)/12
    postI=(40**4-30**4)/12
    report['condensate']['support']={'per_trap_vertical_proof_N':300,'two_trap_combined_N':600,'RHS40x20x3_I_mm4':beamI,'RHS_span_max_mm':405,'RHS_stress_MPa':300*405*20/beamI,'RHS_deflection_mm':300*405**3/(3*ES*beamI),'root_bridge_one_trap':cantilever(300,60,40,8),'root_bridge_two_traps':cantilever(600,60,40,8),'post_lateral_force_screen_N':300,'post_lever_mm':1100,'post_stress_MPa':300*1100*20/postI,'post_deflection_mm':300*1100**3/(3*ES*postI),'anchor_couple_demand_N':300*1100/90,'status':'Conditional screen; floor/substrate and dissimilar weld qualification OPEN. Hose must qualify relative motion; stiffness does not by itself prove zero HX nozzle reaction. Receptor collar now represented.'}
    (E/'local_calculations.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({'face_max_reaction_N':seal[0]['design_reaction_max_N'],'guard':guard,'carrier':carrier,'base_metal_kz_N_mm':kz},indent=2))
if __name__=='__main__':run()
