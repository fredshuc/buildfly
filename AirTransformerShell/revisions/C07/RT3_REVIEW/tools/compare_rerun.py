"""Usage: python compare_rerun.py <C07 dir after rerun> <dir with the delivered JSON/CSV copies> <out.json>
Compare delivered and rerun C07 evidence files, ignoring SHA-256 fields (STEP headers carry timestamps)."""
import json,sys
W,R,outp=sys.argv[1].rstrip('/')+'/',sys.argv[2].rstrip('/')+'/',sys.argv[3]
def strip(x):
    if isinstance(x,dict):return {k:strip(v) for k,v in x.items() if 'sha256' not in k}
    if isinstance(x,list):return [strip(v) for v in x]
    if isinstance(x,float):return round(x,3)
    return x
out={}
for f in ('integration.json','service.json','access_paths.json','seal_stroke.json','motion_shell.json','machine_readback.json','port_reconciliation.json','shell_intersections.json','rt3_contacts.json','rt3_water_access.json'):
    out[f]=strip(json.load(open(W+f)))==strip(json.load(open(R+f)))
for f in ('tie_rods.csv','traps.csv','static_taps.csv'):
    out[f]=open(W+f).read()==open(R+f).read()
print(out);json.dump(out,open(outp,'w'),indent=1)
