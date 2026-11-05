"""Usage: python compare_json.py <rerun dir> <committed C04 dir> <out.json>
Leaf-by-leaf numeric comparison of rerun flow_checks.json / selector_results.json against the committed files,
plus the P-vs-R face-field identity test on selector_results.json."""
import json,sys
import numpy as np
def flat(x,p=''):
    if isinstance(x,dict):
        for k,v in x.items():yield from flat(v,p+'/'+str(k))
    elif isinstance(x,list):
        for i,v in enumerate(x):yield from flat(v,p+'/'+str(i))
    else:yield p,x
out={}
for f in ('flow_checks.json','selector_results.json'):
    a=dict(flat(json.load(open(f'{sys.argv[1]}/{f}'))));b=dict(flat(json.load(open(f'{sys.argv[2]}/{f}'))))
    bad=[k for k in set(a)|set(b) if not (k in a and k in b and (a[k]==b[k] or (isinstance(a[k],float) and abs(a[k]-b[k])<=1e-9*max(1,abs(b[k])))))]
    out[f]=dict(leaves=len(b),mismatches=len(bad))
s=json.load(open(f'{sys.argv[2]}/selector_results.json'))
idx={(r['port'],r['flow_m3h'],r['mixing_loss_per_m']):np.array(r['field']) for r in s}
out['P_vs_R_field_max_abs_diff']={str(k):float(abs(idx[('P',4870,k)]-idx[('R',4870,k)]).max()) for k in (1.,4.,10.)}
out['R4870_vs_R2435_field_max_abs_diff']={str(k):float(abs(idx[('R',4870,k)]-idx[('R',2435,k)]).max()) for k in (1.,4.,10.)}
print(json.dumps(out,indent=1));json.dump(out,open(sys.argv[3],'w'),indent=1)
