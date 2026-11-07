"""Check the assembled reference overlay against every owner occurrence."""
from common import *
from verify import bb
from collections import Counter,defaultdict
sources={'HYD_S2_AND_H01_SERVICE':HYD/'S2_SERVICE.step','HYD_OUTBOARD':HYD/'S2_OUTBOARD_SERVICE.step',
         'D04_SERVICE':D04/'cad/D04_LOCAL_SERVICE.step','D03_MOTION_SERVICE':WORK/'D03_MOTION_AND_SERVICE.step',
         'W2_CROWN':HYD/'W2_ADDITIONAL_INSULATION.step'}
def signature(p,s):return (p.split('/')[-1],tuple(round(x,4) for x in bb(s)))
got=defaultdict(Counter)
path=CAD/'C10_SERVICE_AND_THERMAL_REFERENCE.step'
for p,s in leaves(path):
    group=next(g for g in sources if g in p.split('/'));got[group][signature(p,s)]+=1
checks={}
for group,src in sources.items():
    want=Counter(signature(p,s) for p,s in leaves(src))
    checks[group]={'expected_occurrences':sum(want.values()),'exported_occurrences':sum(got[group].values()),'same_named_world_bounds':want==got[group]}
report={'sha256':sha(path),'groups':checks,'pass':all(r['same_named_world_bounds'] for r in checks.values())}
dump(E/'service_overlay_readback.json',report);print(json.dumps(report,indent=2),flush=True)
