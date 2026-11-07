"""Historical prototype against the archived 40 mm jaw assembly; not a final check."""
from integrate import *
folder,rows=cache_scene('S1')
out=[]
for bed in 'AB':
 for level in ['LOWER','UPPER']:
  name=f'C11_{bed}_{level}_FACE_CLAMP_17'
  row=next(r for r in rows if r['group']=='SHELL' and r['name']==name)
  old=cq.Shape.importBrep(str(folder/row['file']));b=bb(old)
  new=old.cut(box(-391,b[1]-1,b[2]-1,b[3]+1,b[4]+1,b[5]+1))
  assert new.isValid() and old.Volume()>new.Volume()
  near=[]
  for r in rows:
   if r['group']!='HEAT_EXCHANGERS' or not r['name'].startswith(bed+'_'+level+'__'):continue
   local=r['name'].split('__',1)[1]
   if not (local.startswith(('W1_','W2_','TUBE_','H02_COND_')) or '_LONG_U_' in local or '_RETURN_' in local):continue
   if not overlap(bounds(new),r['bbox'],5):continue
   d=new.distance(cq.Shape.importBrep(str(folder/r['file'])))
   assert d>=.5,(name,r['name'],d)
   near.append({'part':r['name'],'distance_mm':d})
  assert near
  out.append({'jaw':name,'width_mm':39,'checked':near})
dump(E/'development/pre_jaw_edge_clearance_fix/trim_prototype.json',{'source_assembly_sha256':sha(CAD/'C11_INSTALLED_S1.step'),'status':'PASS_PROTOTYPE_ONLY_NOT_FINAL_EXPORT','jaws':out})
print(out,flush=True)
