"""Audit the final 1 mm trim against the preserved 40 mm jaw iteration."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
 old=R/'evidence/development/pre_jaw_edge_clearance_fix/shell_index_previous.json'
 current=R/'.work/shell/index.json'
 a={r['name']:r for r in json.loads(old.read_text())}
 b={r['name']:r for r in json.loads(current.read_text())}
 assert a.keys()==b.keys()
 expected={f'C11_{bed}_{level}_FACE_CLAMP_17' for bed in 'AB' for level in ['LOWER','UPPER']}
 changes=[]
 for name,x in a.items():
  y=b[name];dv=x['volume_mm3']-y['volume_mm3'];db=max(abs(u-v) for u,v in zip(x['bbox'],y['bbox']))
  if abs(dv)>max(.001,abs(x['volume_mm3'])*1e-9) or db>1e-5:
   assert name in expected,(name,dv,db)
   assert abs(dv-77)<.001 and abs(y['bbox'][3]+391)<1e-5,(name,dv,y['bbox'])
   changes.append({'part':name,'removed_volume_mm3':dv,'old_bbox':x['bbox'],'new_bbox':y['bbox']})
 assert {r['part'] for r in changes}==expected
 result={'status':'PASS_ONLY_FOUR_1MM_JAW_EDGE_TRIMS','old_shell_index_sha256':sha(old),'shell_index_sha256':sha(current),'changed_parts':changes,'unchanged_part_signatures':len(b)-4,'scope':'Name/volume/bounds delta against the preserved iteration; final installed clearance, full integration, motion and independent rebuild remain separate required evidence.'}
 (R/'evidence/jaw_edge_trim_delta.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
 print(result['status'],len(b)-4,flush=True)
if __name__=='__main__':run()
