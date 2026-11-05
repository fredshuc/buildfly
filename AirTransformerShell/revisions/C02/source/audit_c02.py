import bootstrap,json,cadquery as cq,math
from pathlib import Path
from itertools import combinations
R=bootstrap.ROOT;D=R/'deliverables'
rows=json.loads((D/'native/ASSEMBLY.json').read_text(encoding='utf8'))
sh={q['name']:cq.Shape.importBrep(str(D/'native'/q['brep']))for q in rows}
def overlap(a,b):
    return all(min(a[i+3],b[i+3])-max(a[i],b[i])>1e-6 for i in range(3))
def clashes(a,b,same=False):
    out=[]
    pairs=combinations(a,2)if same else((x,y)for x in a for y in b)
    for x,y in pairs:
        if x['name']==y['name']or not overlap(x['bbox_mm'],y['bbox_mm']):continue
        v=sh[x['name']].intersect(sh[y['name']]).Volume()
        if v>.001:out.append(dict(a=x['name'],b=y['name'],mm3=round(v,4)))
    return out
p=[q for q in rows if q['kind'] in ['DESIGN_PART','ROUTING_REFERENCE']]
equip=[q for q in rows if q['kind']in['SUPPLIER_BODY','EQUIPMENT_ENVELOPE'] or q['name'].endswith(('_DAMPER','_DRIVE'))]
hx=[q for q in rows if q['name'].endswith('_HX_C03')]
withdraw=[q for q in rows if q['name'].endswith('_ACTUATOR_WITHDRAWAL')]
ins=[q for q in rows if q['name'].endswith('_INS25')and'HEADER'not in q['name']]
sweep=[q for q in rows if q['name'].endswith('_EXTRACT_SWEEP')]
fixed=[q for q in p if q.get('scope')not in ['FRONT_REMOVE','ADAPTER_REMOVE']]
data=dict(parts=len(p),equipment=len(equip),all_brep_valid=all(s.isValid()for s in sh.values()),physical_pairs=clashes(p,p,True),equipment_metal=clashes(equip,p),equipment_pairs=clashes(equip,equip,True),hx_static=clashes(hx,p),core_removal=clashes(sweep,fixed),actuator_withdrawal=clashes(withdraw,p+equip),insulation_shell=clashes(ins,[q for q in p if q['group']not in ['W1','W2']]),insulation_pair=clashes(ins,ins,True))
# Ignore intended seal-to-core contact at boundaries only (positive volume is still reported).
(D/'evidence/VALIDATION.json').write_text(json.dumps(data,indent=2))
print(json.dumps(data,indent=2),flush=True)
