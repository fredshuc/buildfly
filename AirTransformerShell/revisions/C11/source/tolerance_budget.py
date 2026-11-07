"""Expose unclosed tolerance and thermal allocations; do not assign PASS."""
from pathlib import Path
import json,csv
R=Path(__file__).resolve().parents[1]
local=json.loads((R/'evidence/local_calculations.json').read_text())['face_clamps']
edge=local['long_edge_after_H02_clearance']
elastic=max(local['carrier']['deflection_mm'],edge['right_strongback_deflection_mm']+edge['right_2mm_carrier_17_5mm_overhang']['tip_deflection_mm'],local['left_end_support']['plate_500N']['tip_deflection_mm'])
gap_stack=.30+elastic
rows=[
 {'interface':'FACE_GAP','quantity':'HX land flatness','bound_mm':.10,'basis':'Final H02 proposed land PV; owner qualification remains open'},
 {'interface':'FACE_GAP','quantity':'Shell carrier flatness','bound_mm':.10,'basis':'Proposed manufacturing requirement, not measured'},
 {'interface':'FACE_GAP','quantity':'Assembly/hard-stop selection','bound_mm':.10,'basis':'Unadjusted allowance; must be measured and shimmed'},
 {'interface':'FACE_GAP','quantity':'Carrier elastic screening','bound_mm':elastic,'basis':'Maximum of Y-edge screen, right strongback plus carrier overhang, and new left-end bearing extension; HX frame deformation still additional/unqualified'},
 {'interface':'FACE_GAP','quantity':'Unadjusted one-sided sum','bound_mm':gap_stack,'basis':'Exceeds +/-0.25mm qualified installed gap; excludes unqualified HX edge/frame deformation; no automatic tolerance PASS'},
 {'interface':'FACE_GAP','quantity':'Permitted qualified gap half-range','bound_mm':.25,'basis':'4.20..4.70mm around4.45; measured local gap and load proof required'},
 {'interface':'THERMAL_X','quantity':'Relative growth over1040mm','bound_mm':1040*(23e-6*70-12e-6*20),'basis':'Illustrative Al core +70K / steel carrier +20K; thermal field not supplied'},
 {'interface':'THERMAL_X','quantity':'Nominal stated travel','bound_mm':1.5,'basis':'Candidate locator/slide requirement; clamped friction and actual travel not verified'},
 {'interface':'THERMAL_X','quantity':'Datum allowance added to thermal example','bound_mm':.4,'basis':'Sensitivity only, not certified tolerance allocation'},
 {'interface':'THERMAL_X','quantity':'Growth plus datum sensitivity','bound_mm':1040*(23e-6*70-12e-6*20)+.4,'basis':'Exceeds1.5mm; thermal slide design remains HOLD'},
 {'interface':'DAMPER_RELATIVE_FRAME','quantity':'Operational FE change','bound_mm':.1053066,'basis':'Mesh48 linear model relative to gravity-loaded datum; excludes thermal/contact/anchor flexibility'},
 {'interface':'DAMPER_RELATIVE_FRAME','quantity':'D05 Shell allocation','bound_mm':.2,'basis':'Pinned D05 allocation; separate terms must not be silently absorbed'}]
with (R/'C11_TOLERANCE_AND_THERMAL_BUDGET.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(R/'evidence/tolerance_budget.json').write_text(json.dumps({'status':'HOLD_UNCLOSED_GAP_AND_THERMAL_STACK','face_gap_unadjusted_mm':[4.45-gap_stack,4.45+gap_stack],'face_qualified_gap_mm':[4.2,4.7],'required_action':'Define selected/shimmed stop settings and measure every local working gap under approved clamp load; qualify actual HX frame deformation; obtain actual temperature/CTE/CG data and verify friction/sliding. Wider seal thickness alone does not close this budget.','rows':rows},indent=2),encoding='utf-8')
print('Tolerance/thermal budget: explicit HOLD')
