"""Summarize numerical evidence; retain assumptions and missing acceptance data."""
from pathlib import Path
import json,csv,math
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
def table(p,rows):
    with (R/p).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def run():
    a=read('evidence/frame_screen_mesh24.json');b=read('evidence/frame_screen_mesh48.json');calc=read('evidence/local_calculations.json')
    conv=[];weld=[];anchors=[];load=[]
    for case,r in b['cases'].items():
        old=a['cases'][case]
        stress=r['worst_member']['von_mises_screen_MPa']
        peak=max(v['max_local_stress_MPa'] for v in r['weld_transfer'].values())
        oldpeak=max(v['max_local_stress_MPa'] for v in old['weld_transfer'].values())
        conv.append({'case':case,'mesh24_displacement_mm':old['max_translation_mm'],'mesh48_displacement_mm':r['max_translation_mm'],'displacement_change_percent':100*(r['max_translation_mm']/old['max_translation_mm']-1),'mesh24_web_peak_MPa':oldpeak,'mesh48_web_peak_MPa':peak,'web_peak_change_percent':100*(peak/oldpeak-1),'interpretation':'Global displacement stable; local end stress not demonstrated converged; no fabrication release'})
        load.append({'case':case,'core_mass_cap_each_kg':250,'other_host_mass_cap_kg':1000,'actuator_mass_each_kg':10,'mesh':48,'max_displacement_mm':r['max_translation_mm'],'max_member_stress_MPa':stress,'max_web_stress_MPa':peak,'status':'Conditional linear elastic screening; not measured performance'})
        for web,d in r['weld_transfer'].items():
            for end in ['POST','SISTER']:
                weld.append({'case':case,'web':web,'joint_end':end,'throat_mm':3,'effective_length_mm':257,'area_mm2':771,'force_X_N':d['force_sum_XYZ_N'][0],'force_Y_N':d['force_sum_XYZ_N'][1],'force_Z_N':d['force_sum_XYZ_N'][2],'local_equivalent_stress_screen_MPa':d['max_local_stress_MPa'],'parent_yield_MPa':235,'stress_ratio':d['max_local_stress_MPa']/235,'parent_shear_yield_capacity_N':771*235/math.sqrt(3),'parent_axial_yield_capacity_N':771*235,'released_capacity_N':'','status':'CJP qualification required; parent capacities conditional; local stress mesh sensitivity remains'})
        for v in r['anchors']:
            fx,fy,fz=v['reaction_to_frame_N']
            anchors.append({'case':case,'X_mm':v['X_mm'],'Y_mm':v['Y_mm'],'compression_N':fz,'uplift_N':max(0,-fz),'horizontal_resultant_N':math.hypot(fx,fy),'moment_basis':'Translations fixed, rotations free at foot centre Z82; no selected substrate/anchor','status':'DEMAND_ONLY'})
    table('C11_STRUCTURAL_CONVERGENCE.csv',conv);table('C11_A_POST_WELD_CAPACITY.csv',weld);table('C11_MAIN_BASE_ANCHOR_DEMANDS.csv',anchors);table('C11_STRUCTURAL_LOAD_CASES.csv',load)
    hx=next((R/'.work/h02').rglob('AIR_RESISTANCE_SCENARIOS_NOT_MEASURED.csv'))
    rows=[]
    for r in csv.DictReader(hx.open()):
        if abs(float(r['Q_m3h'])-4870)>.01 and abs(float(r['Q_m3h'])-2435)>.01:continue
        for exponent in ['1p7','2p2']:
            dp=float(r['Pa_n'+exponent])
            for factor in [0,.5,1.]:
                # One optional plate compared with ONE of two equal reference
                # core losses; this is a sensitivity search, not a hole pattern.
                plate=dp*.5*factor
                rows.append({'Q_m3h':r['Q_m3h'],'face_velocity_m_s':float(r['Q_m3h'])/3600/.612,'two_core_scenario_at4870_Pa':r['two_core_reference_Pa'],'exponent':exponent.replace('p','.'),'two_core_scenario_Pa':dp,'plate_factor_of_one_core':factor,'plate_scenario_Pa':plate,'known_scenario_subtotal_Pa':dp+plate,'collector_and_plenum_Pa':'','duct_damper_filter_Pa':'','fan_available_static_Pa':'','fan_margin_Pa':'','status':'UNMEASURED_SCENARIO; total and fan margin unknown; P4870 unchanged'})
    table('C11_PRESSURE_DROP_BUDGET.csv',rows)
    maxrel=max(max(v['loaded_datum_change_relative_to_damper_mm'].values()) for v in b['cases'].values() if 'loaded_datum_change_relative_to_damper_mm' in v)
    tol=read('evidence/tolerance_budget.json');gap_half=(tol['face_gap_unadjusted_mm'][1]-tol['face_gap_unadjusted_mm'][0])/2
    text=f'''# C11 engineering evidence and limits

This is a review candidate, not a fabrication, pressure-test or operating release. Units are mm, N and MPa unless stated otherwise. Numerical checks do not establish physical test results.

## Structure and load paths

The main frame model includes six columns, crossmembers, HX supports, actual end offsets and a separate sister member linked by finite web springs. It does not credit sheet skin as a diaphragm. Four cores use 250 kg each, additional host mass uses 1,000 kg, and four actuators use 10 kg each. The CAD mass audit provides conservative density bounds, not certified masses or centres of gravity. Equipment eccentricities and the assumed host load distribution remain limitations.

Cases cover gravity, opposed +/-1,000 Pa core pressure and 60 Nm actuator torque in S1/S2, 500 N downward plus 300 N horizontal maintenance and 75 Nm torque, and a conservative vertical 2g case retaining wet mass. Lateral transport, lifting and forklift handling are not released. The water island carries its own gravity to the six-foot extension skid and floor; its weight is not fictitiously applied at the A-post.

At mesh 48 the maximum frame displacement is {max(r['max_translation_mm'] for r in b['cases'].values()):.4f} mm and maximum member stress is {max(r['worst_member']['von_mises_screen_MPa'] for r in b['cases'].values()):.2f} MPa. The largest operational change between an HX support datum and its damper datum, relative to the gravity-loaded state, is {maxrel:.4f} mm against the D05 Shell allocation of 0.20 mm. These results depend on rigid frame joints, assumed wall thicknesses, pinned floor translations and the prescribed load distribution. They do not include thermal movement, contact slip, anchor compliance, nonlinear/local buckling or weld defects.

The 24/48 web mesh comparison uses the same current load caps and effective web lengths. Global displacement changes are small, but local web end stress increases by approximately 6%; local peak convergence is therefore OPEN. See C11_STRUCTURAL_CONVERGENCE.csv. The unit cantilever verification is embedded in each frame JSON.

Eight joints now have actual single-bevel full-penetration geometry, 3 mm effective throat, 269 mm gross length and 257 mm effective length. This is not a claim for an undersized structural fillet. C11_A_POST_WELD_CAPACITY.csv couples each joint to frame transfer force and local stress. Parent-metal capacity is conditional on matching weld quality demonstrated on the actual 3 mm T-joint. No released capacity is assigned before WPS/coupon/root-fusion qualification. Post and sister geometry remain unchanged; inspect flush finish +0/-0.1 mm near insulation.

The six water-skid feet use four M12 bolts each, top plates and RHS rails with direct floor-pad bearing. The calculated metal-only vertical stiffness screen is {calc['water_skid']['metal_only_kz_lower_screen_N_mm']:.0f} N/mm per foot. It excludes floor/grout compliance. The owner maximum 993.59 N vertical reaction is screened at 1,000 N. Main-frame anchor demands are tabulated separately; anchor selection, substrate, edge distances, uplift and slip acceptance remain OPEN. Near floor pads have two anchor holes; far pads have four. M10 bridges are alignment/lateral connections, not a substitute for floor bearing.

## Seals and retention

The four frozen core positions are retained. Selected R10480S face strips are 6.35 +/-0.10 mm free, installed at 4.45 mm nominal with 4.20..4.70 mm acceptance gap, giving 24.8..34.9% working compression. The 12 mm seal lies on the owner's 20 mm land. Hard stops and bearing pads define position independently of seal thickness. Typical supplier curves are not batch maxima: <=0.080 MPa over the required compression/conditioning range is a procurement acceptance requirement. Maximum gasket force is 3,171.84 N/core. Twenty M5 clamps at 0.5 Nm can generate up to 10,000 N total preload, closed through the metal stops and support structure. HX has not released this force capacity; its 1,000 N fixture limit is not permission to apply this preload. The clamp load and thermal sliding solution are HOLD items. Clearance to the H02 collector uses upper-corner long ties at the left and bottom-land clamps100mm inboard at the right, leaving a635mm left HX edge span. The Shell carrier now has continuous left bearing and an RHS50x30x3 right strongback; the separate HX uplift/frame proof remains HOLD. The isolated20x8mm edge-rail screen fails the gap criterion and cannot be substituted for an accepted coupled-frame model.

Pocket seals use 4.76 +/-0.10 mm sponge at 3.50 mm nominal installed gap. The front closure remains a real Shell part, independent of the removable seat. The issued crown and upper B vent conflict with this joint. Do not remove the wall, cut copper or silently waive soft interference. Resolve flange/seat/crown/service geometry jointly and repeat air/vapour checks.

Four skin glands use a 2 mm DOWSIL 7091 split lip around the insulation jacket, a renewed splice and a perimeter bond. The 6 mm metal guard protects/retains the lip; it does not transmit an assumed uniform 50 kPa gasket compression. The guard screen is 100 N at a 66 mm span over the 9 mm ligament: 122.22 MPa and 0.296 mm. The 5 mm backer is screened at a 1,000 N blind-thread proof load. Required adhesion coupons, edge-peel, jacket compatibility, movement cycling and 1.5 mm skin/edge-weld proof remain unperformed. Each guard now uses removable M4x16 screws with3.5mm engagement in blind4mm taps, leaving1mm closed backer wall. Fully extract screws, move guards radially before outboard withdrawal. The material-specific curve and bonding assumptions are in evidence/local_calculations.json.

## Drainage and distribution

Four independent D18/ID16 traps connect to the final H02 condensate spigots through replaceable flexible sleeves. Effective water head is 164 mm, comprising 101.94 mm for 1,000 Pa and a 50 mm startup/evaporation allowance with a small residual. The calculated pressure screen is 1,118.34 Pa; actual fan shutoff/fault pressure must be supplied before operation. The inlet fall is 200 mm. Each trap has a cleanout, downstream vent and visible air gap before its own receptor. Pressure-water vent/drain outlets remain separate. Coupler clamp hardware, receptor/support qualification, complete service clearance, wet-bay collection and all penetration vapour seals remain unfinished.

The installed distribution configuration is an open removable frame; no unvalidated perforated plate is installed. Clear nominal face area remains 0.612 m2. Rated P remains 4,870 m3/h (2.2104 m/s), with R=2,435 m3/h as a comparison. C11_PRESSURE_DROP_BUDGET.csv retains all three unmeasured HX resistance scenarios and optional plate losses of 0.5..1 times one core loss. H02 collector, plenum, duct/filter/damper losses and the fan curve are unknown; a complete pressure budget or fan margin cannot be reported as passed. The straight extraction route requires lower Pin-seat removal and a supported bridge/trolley; that predecessor sequence and temporary support are not yet qualified.

## Tolerance and thermal allocations

C11_TOLERANCE_AND_THERMAL_BUDGET.csv explicitly records an unadjusted face-gap stack of+/-{gap_half:.5f}mm against the proposed+/-0.25mm qualification range, before unqualified HX-frame deformation. An illustrative aluminium-core+70K / steel-carrier+20K case plus0.4mm datum allowance gives1.8248mm over1040mm, exceeding the stated1.5mm candidate travel. Both remain HOLD pending selected/shimmed stops, actual temperatures and verified clamped sliding.

## Evidence classification

STEP entities establish candidate geometry. Exact Boolean intersections establish only the reported geometric scope and 0.001 mm3 threshold; they do not establish mechanical clearance under tolerances. Calculations establish conditional screening results. Material, welding, dry assembly, wind, leak, condensate carryover, first fill and running tests have not been performed. Detailed drawings and profiles are REVIEW/HOLD until the acceptance matrix is closed.
'''
    text=text.replace('Fully extract screws, move guards radially before outboard withdrawal.', 'The tested proposal fully extracts the screws, moves the guards radially 90 mm and then outwards 20 mm. It is NOT ACCEPTED: lower guards collide with local H02 drain adapters/mount bolts; upper guards have unresolved lip contact. Qualify actual predecessor removals or revise guard segmentation before claiming replacement access.')
    text=text.replace('10,000 N total preload, closed through the metal stops and support structure.', '10,000 N total bolt preload. This is not a demonstrated toe or seal reaction: jaw contact, sleeve/stop seating and frame stiffness determine the force split. Measured contact loads and cold/hot gap evidence are required.')
    text=text.replace('Each trap has a cleanout,', 'Atmospheric branches use a radius 9.15 mm fishmouth over the D18 outlet, giving a nominal 0.15 mm weld root gap, and a D16.2 opening. The earlier equal-radius cut silently removed no material; all four corrected joints have explicit material-removal and exported-geometry checks. Welding and bore-finish qualification remain open. Each trap has a cleanout,')
    text=text.replace('Clearance to the H02 collector uses upper-corner long ties at the left and bottom-land clamps100mm inboard at the right, leaving a635mm left HX edge span.', 'All clamps now react at the bottom steel frame. Upper-corner long ties were rejected by the full damper sweep. The two left end stations use a 39 mm wide, 3.5 mm flush jaw at X=-410/Y-min-10 and an 8 mm flush jaw at X=-418/Y-max+10. Eight bearing extensions have 8 mm shelves, two 3 mm gussets each and 30x16x3 mm mounting plates welded to the unchanged Shell RHS. The right clamps remain 100 mm inboard. The left HX edge is conservatively screened over 652 mm.')
    end=calc['face_clamps']['left_end_support'];thin=calc['face_clamps']['jaw_net_sections']['left_YMIN_3p5mm_net_at_D10']
    text=text.replace('The isolated20x8mm edge-rail screen fails the gap criterion and cannot be substituted for an accepted coupled-frame model.', f"The isolated 20x8 mm edge-rail screen fails the gap criterion and cannot replace an accepted coupled-frame model. The new thin-jaw beam screen is {thin['stress_MPa']:.2f} MPa at 500 N. The shelf screen, without gusset stiffness credit, is {end['plate_1500N_proof']['stress_MPa']:.2f} MPa at the separate 1,500 N bracket proof load; the mount perimeter-weld equivalent stress is {end['mount_perimeter_weld']['equivalent_stress_MPa']:.2f} MPa. These are conditional screens. Actual RHS wall/corner fit, local wall bending, weld access/WPS, collector clearance under tolerances and complete bracket proof remain OPEN. Do not apply the 1,500 N bracket test through the 500 N jaw.")
    (R/'ENGINEERING_REVIEW_EN.md').write_text(text,encoding='utf-8')
    print('Engineering tables and review written')
if __name__=='__main__':run()
