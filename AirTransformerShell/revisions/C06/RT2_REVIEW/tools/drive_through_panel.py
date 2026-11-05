"""Usage: python drive_through_panel.py <C06 dir (for integrate.py reader)> <D01 dir> <out.json>
For the rear dampers of bed A (ARP, ARR): X-Z projected extents of every installed D01 leaf lying outboard
of the side-panel plane (Y < -850), compared with the closed side-panel cut-outs, i.e. whether the panel
can be withdrawn along -Y over the installed drive lines."""
import sys,json
from pathlib import Path
c06,d01,outp=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
pre=(c06/'integrate.py').read_text()
ns={};exec(pre[pre.index('import cadquery'):pre.index('parser=argparse')],ns);exec(pre[pre.index('def leaves('):pre.index('def screen(')],ns)
cut={'ARP':[912.65,186.55,1099.55,538.45],'ARR':[912.65,661.55,1099.55,848.45]}
res={k:dict(cutout_XZ=v,parts_outboard=0,beyond_cutout=[]) for k,v in cut.items()}
for n,s in ns['leaves'](d01/'cad/D01_EIGHT_DAMPERS_INSTALLED.step'):
    if '/HOST/' in n or n.rsplit('/',1)[-1].startswith('HOST_'):continue
    for k in cut:
        if '/'+k in n or n.startswith(k) or ('_'+k+'_') in n:
            b=ns['bb'](s)
            if b[1]< -850:
                res[k]['parts_outboard']+=1
                c=cut[k]
                if b[0]<c[0] or b[2]<c[1] or b[3]>c[2] or b[5]>c[3]:
                    res[k]['beyond_cutout'].append([n.rsplit('/',1)[-1],[round(v,1) for v in (b[0],b[1],b[2],b[3],b[4],b[5])]])
for k in res:res[k]['n_beyond']=len(res[k]['beyond_cutout']);res[k]['beyond_cutout']=res[k]['beyond_cutout'][:15]
print(json.dumps(res,indent=1));json.dump(res,open(outp,'w'),indent=1)
