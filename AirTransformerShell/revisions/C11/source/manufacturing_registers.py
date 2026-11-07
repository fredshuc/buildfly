"""Cut/machining registers from final Shell BRep index and design metadata."""
from pathlib import Path
import json,csv,re,hashlib
R=Path(__file__).resolve().parents[1]

def write(name,rows):
    assert rows,name
    with (R/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def run():
    src=R/'.work/shell/index.json';rows=json.loads(src.read_text());rhs=[];caps=[];sleeves=[]
    for r in rows:
        if not r['changed']:continue
        n=r['name'];b=r['bbox'];dim=[round(b[i+3]-b[i],5) for i in range(3)];material=r['material']
        if n.startswith('C11_') and 'RHS' in material:
            axis=max(range(3),key=lambda i:dim[i]);cross=[i for i in range(3) if i!=axis]
            nums=re.findall(r'[0-9]+(?:\.[0-9]+)?',material.split('RHS',1)[1])
            rhs.append({'part':n,'quantity':1,'material_and_section':material,'length_axis':'XYZ'[axis],'cut_length_mm':dim[axis],'cross_axes':''.join('XYZ'[i] for i in cross),'cross_sizes_mm':str([dim[i] for i in cross]),'wall_mm':float(nums[2]) if len(nums)>=3 else 'SEE_SOURCE','end_cut':'Square90deg; welded assembly candidate','notes':'Verify actual stock corner radius/wall and end fit; bearing/weld datum tolerances govern; no manufacture before closure matrix acceptance'})
        if n.startswith('C11_') and ('ENDCAP' in n or n.endswith('_CAP') or '_STRONGBACK_CAP_' in n) and 'plate' in material.lower():
            axis=min(range(3),key=lambda i:dim[i]);cross=[i for i in range(3) if i!=axis]
            caps.append({'part':n,'quantity':1,'material':material,'normal_axis':'XYZ'[axis],'thickness_mm':dim[axis],'profile_axes':''.join('XYZ'[i] for i in cross),'rectangular_profile_mm':str([dim[i] for i in cross]),'tolerance':'Profile+/-0.2mm; deburrR0.5; confirm stock inner corner radius and seal-weld fit','status':'REVIEW_CANDIDATE'})
        if '_FACE_STANDOFF_' in n:
            thin=n.endswith('_17')
            sleeves.append({'part':n,'quantity':1,'axis':'Z','centre_X_mm':round((b[0]+b[3])/2,5),'centre_Y_mm':round((b[1]+b[4])/2,5),'base_Z_mm':round(b[2],5),'length_mm':dim[2],'OD_mm':10,'lower_thread':'M5x0.8;minorD4.2;tap10mm from lower end BEFORE attachment','upper_clearance_D_mm':5.2,'actual_screw_engagement_mm':6.05 if thin else 7.55,'bolt_tip_gap_mm':3.95 if thin else 2.45,'proof_N':1500,'manufacture':'Machined12.45mm spacer. End faces parallel0.05; length+/-0.05. Seal attachment to carrier. Supplier/WPS/proof OPEN. No upper-frame long sleeves remain.'})
    write('C11_RHS_CUT_LIST.csv',rhs);write('C11_CAP_PLATE_CUT_LIST.csv',caps);write('C11_MACHINED_REACTION_SLEEVES.csv',sleeves)
    proof={'source_shell_index_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'RHS_parts':len(rhs),'cap_parts':len(caps),'reaction_sleeves':len(sleeves),'status':'REVIEW_CUT_LISTS_NOT_MATERIAL_OR_PROCESS_RELEASE'}
    (R/'evidence/manufacturing_registers.json').write_text(json.dumps(proof,indent=2),encoding='utf-8');print(proof)

if __name__=='__main__':run()
