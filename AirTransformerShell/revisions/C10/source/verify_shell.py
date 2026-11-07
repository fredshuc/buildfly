"""Fast preflight on the exported shell while the full assembly is composed."""
from verify import *
shell=named(CAD/'C10_SHELL.step');c=json.loads((E/'shell_changes.json').read_text())
delta={n:shell[n] for n in set(c['modified'])|set(c['added'])}
base=cache_host('S1');out={}
print('shell preflight',len(shell),len(delta),flush=True)
for key,p in [('thermal_material',HYD/'W2_ADDITIONAL_INSULATION.step'),('thermal_space',HYD/'W2_HOST_SPACE_REQUEST.step'),('D04_service',D04/'cad/D04_LOCAL_SERVICE.step'),('H01_service',HX/'H01_TOOL_AND_REMOVAL.step'),('D03_motion_service',WORK/'D03_MOTION_AND_SERVICE.step')]:
    out[key]=screen(keyed(delta),keyed(dict(leaves(p))))
    print(key,out[key],flush=True);dump(E/'shell_preflight.json',out)
r=screen(keyed(delta),keyed(shell));increased=[];seen=set()
for n,k,v in r['hits']:
    if n==k or tuple(sorted((n,k))) in seen:continue
    seen.add(tuple(sorted((n,k))))
    old=base['SHELL'][n].intersect(base['SHELL'][k]).Volume() if n in base['SHELL'] and k in base['SHELL'] else 0
    if v>old+.01:increased.append([n,k,v,old])
out['increased_shell']=increased;print('INCREASED SHELL',increased,flush=True)
dump(E/'shell_preflight.json',out)
