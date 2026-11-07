"""Read-only C10 interface inventory for C11; scratch outputs are not releases."""
from common import *
out=WORK
out.mkdir(exist_ok=True)
shell={r['name']:s for r,s in baseline(groups={'SHELL'})}
report={}
for n,s in shell.items():
    b=bb(s)
    report[n]={'bbox':b,'volume_mm3':s.Volume(),'solids':len(s.Solids())}
(out/'shell_inventory.json').write_text(json.dumps(report,indent=2))
print('Shell inventory',len(shell),flush=True)
hx={}
for n,s in leaves(HX/'H01_FOUR_HX_INSTALLED.step'):
    if any(t in n for t in ('AIR_EDGE','FRAME','POST','FOOT','C05','SEAL','LAND','CARRIER','VENT','DRAIN')):
        hx[n]={'bbox':bb(s),'volume_mm3':s.Volume()}
(out/'hx_interfaces.json').write_text(json.dumps(hx,indent=2))
print('HX interface inventory',len(hx),flush=True)
