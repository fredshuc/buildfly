import bootstrap,json,hashlib,shutil,cadquery as cq
from pathlib import Path
R=bootstrap.ROOT;D=R/'deliverables'
# Correct the review projection to the final CAD dimensions.
p=R/'source/render_c02.py';s=p.read_text(encoding='utf8').replace('1314,1704','1364,1704').replace('1314,1752','1364,1752').replace('[(936,760),(1036,1230)]','[(976,760),(1076,1230)]')
p.write_text(s,encoding='utf8')
rows=json.loads((D/'native/ASSEMBLY.json').read_text(encoding='utf8'))
physical=[q for q in rows if q['kind']in['DESIGN_PART','ROUTING_REFERENCE']]
equip=[q for q in rows if q['kind']in['SUPPLIER_BODY','EQUIPMENT_ENVELOPE']]
ins=[q for q in rows if q['name'].endswith('_INS25')or q['name'].endswith('_HEADER_INS25')]
def clash(a,b):
 out=[]
 for x in a:
  for y in b:
   if x['name']==y['name']:continue
   ax=x['bbox_mm'];by=y['bbox_mm']
   if not all(min(ax[i+3],by[i+3])-max(ax[i],by[i])>1e-6 for i in range(3)):continue
   v=cq.Shape.importBrep(str(D/'native'/x['brep'])).intersect(cq.Shape.importBrep(str(D/'native'/y['brep']))).Volume()
   if v>.001:out.append(dict(a=x['name'],b=y['name'],mm3=v))
 return out
extra=dict(insulation_equipment=clash(ins,equip),header_insulation_shell=clash([q for q in ins if'HEADER'in q['name']],physical))
checks=[]
for stem,selected in [
('SHELL',[q for q in rows if q['kind']=='DESIGN_PART' and q['group']!='SEAL']),
('LAYOUT',[q for q in rows if q['kind']in ['DESIGN_PART','ROUTING_REFERENCE'] or(q['kind']!='SPACE_RESERVATION' or q['group']in ['HX','P','R'])]),
('SERVICE',[q for q in rows if q['kind']not in ['DESIGN_PART','ROUTING_REFERENCE']])]:
 f=D/'cad'/('AT_SHELL2_2V_C02_'+stem+'.step');s=cq.importers.importStep(str(f)).val()
 wanted=sum(q['solids']for q in selected);vol=sum(q['volume_mm3']for q in selected)
 expected=[min(q['bbox_mm'][i]for q in selected)for i in range(3)]+[max(q['bbox_mm'][i]for q in selected)for i in range(3,6)]
 bb=s.BoundingBox();actual=[bb.xmin,bb.ymin,bb.zmin,bb.xmax,bb.ymax,bb.zmax]
 checks.append(dict(file=f.name,solid_count=len(s.Solids()),expected_solids=wanted,relative_volume_error=abs(s.Volume()-vol)/vol,max_bbox_error_mm=max(abs(x-y)for x,y in zip(actual,expected)),valid=s.isValid(),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
 assert checks[-1]['solid_count']==wanted and checks[-1]['relative_volume_error']<1e-7 and checks[-1]['max_bbox_error_mm']<1e-4
extra['step_readback']=checks
(D/'evidence/EXTENDED_VALIDATION.json').write_text(json.dumps(extra,indent=2))
(R/'inputs').mkdir(exist_ok=True)
src=R.parent/'L1_E_HYD3_REVIEWS/COR01_VALVE_DATUM_20261018'
if not (R/'inputs/3D-CAD-step-R3025-BL2.stp').exists():shutil.copy2(src/'sources/3D-CAD-step-R3025-BL2.stp',R/'inputs/3D-CAD-step-R3025-BL2.stp')
if not (R/'inputs/COR01_VALVE_DATUM_CN.md').exists():shutil.copy2(src/'L1_COR01_VALVE_DATUM_SOURCE_ADD01_CN.md',R/'inputs/COR01_VALVE_DATUM_CN.md')
# Future rebuild uses the bundled supplier STEP.
p=R/'source/build_c02.py';s=p.read_text(encoding='utf8').replace("ROOT.parent/'L1_E_HYD3_REVIEWS/COR01_VALVE_DATUM_20261018/sources/3D-CAD-step-R3025-BL2.stp'","ROOT/'inputs/3D-CAD-step-R3025-BL2.stp'")
p.write_text(s,encoding='utf8')
# Bootstrap falls back to installed libraries if sibling runtime is absent.
print(json.dumps(extra,indent=2),flush=True)
