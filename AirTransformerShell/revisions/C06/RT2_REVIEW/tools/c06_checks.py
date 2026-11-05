"""Independent C06 checks (mm). Usage:
  python c06_checks.py <repo-layout C06 dir> <M101 single-core STEP> <out.json>
Rebuilds the C06 shell solids by executing build_c06.py up to its export stage (no files written),
places the detailed M101 C04 core at both beds, and reports: HX static fit, HX withdrawal sweeps
(+-Y side, +Z roof) with stated removal sets, drip-tray removability, seal-carrier and guide-tip
clearances to the HX frame, cassette-to-structure contacts, drain-outlet elevations, and the gasket
area. Read-only on inputs."""
import sys,json,math
from pathlib import Path
import cadquery as cq
c06,hxstep,outp=Path(sys.argv[1]),sys.argv[2],sys.argv[3]
src=(c06/'build_c06.py').read_text()
src=src.split('def make_assembly')[0]
argv=sys.argv;sys.argv=[str(c06/'build_c06.py'),'--out',__import__('tempfile').mkdtemp()]
ns={'__file__':str(c06/'build_c06.py'),'__name__':'c06'}
exec(compile(src,'build_c06.py','exec'),ns);sys.argv=argv
rows,cat=ns['rows'],ns['categories'];centres=ns['centres']
print('shell solids',len(rows),flush=True)
def bb(s):b=s.BoundingBox();return (b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax)
def ov(a,b,t=1e-6):return all(min(a[k+3],b[k+3])-max(a[k],b[k])>t for k in range(3))
def gap(a,b):return math.sqrt(sum(max(0,max(a[k],b[k])-min(a[k+3],b[k+3]))**2 for k in range(3)))
RB={n:bb(s) for n,s in rows.items()}
hx=cq.importers.importStep(hxstep).val().Solids()
T={'A':(265,centres['A']-367.775,1150),'B':(265,centres['B']-367.775,1150)}
R={'shell_solids':len(rows),'hx_translation':T}
cores={bed:[s.translate(cq.Vector(*t)) for s in hx] for bed,t in T.items()}
CB={bed:[bb(s) for s in p] for bed,p in cores.items()}
def hits(parts,pbs,names,off=(0,0,0)):
    env=[min(b[k] for b in pbs)+off[k%3] if k<3 else max(b[k] for b in pbs)+off[k%3] for k in range(6)]
    out={}
    for n in names:
        if not ov(RB[n],env):continue
        for i,pb in enumerate(pbs):
            q=tuple(pb[k]+off[k%3] for k in range(6))
            if ov(RB[n],q):
                v=parts[i].translate(cq.Vector(*off)).intersect(rows[n]).Volume()
                if v>1e-3:out[n]=round(v,2);break
    return out
# 1 static
R['static_hx_clashes']={bed:hits(cores[bed],CB[bed],list(rows)) for bed in T}
# 2 sweeps
def sweep(bed,vec,dmax,step,removed):
    names=[n for n in rows if n not in removed];first={}
    d=step
    while d<=dmax+1e-9:
        off=tuple(v*d for v in vec)
        for n,v in hits(cores[bed],CB[bed],[n for n in names if n not in first],off).items():first[n]=[d,v]
        d+=step
    return first
side={'A':['A_SIDE_PANEL','A_SIDE_BRACE'],'B':['B_SIDE_PANEL','B_SIDE_BRACE']}
forks=lambda bed:[n for n in rows if n.startswith(bed+'_TOP_FORK')]
tray=lambda bed:[n for n in rows if n.startswith(bed+'_HX_TRAY') or n.startswith(bed+'_TRAY_BAR') or n.startswith(bed+'_PAN_PAD')]
sw={}
for bed,vec in (('A',(0,-1,0)),('B',(0,1,0))):
    sw[bed+'_side_panel_and_brace_removed']=sweep(bed,vec,900,25,side[bed])
    sw[bed+'_plus_forks_removed']=sweep(bed,vec,900,25,side[bed]+forks(bed))
    sw[bed+'_plus_forks_and_tray_removed']=sweep(bed,vec,900,25,side[bed]+forks(bed)+tray(bed))
    sw[bed+'_+Z_roof_topcross_forks_removed']=sweep(bed,(0,0,1),1300,50,['ROOF','HX_TOP_CROSS']+forks(bed))
    print(bed,{k:list(v)[:6] for k,v in sw.items() if k.startswith(bed)},flush=True)
R['withdrawal_sweeps_first_contact']=sw
# 3 tray removability with the HX in place (A)
trayparts=[rows[n] for n in tray('A')];tb=[bb(s) for s in trayparts]
def tsweep(vec,dmax,step=5):
    first={};d=step
    others=[n for n in rows if n not in tray('A')]
    while d<=dmax+1e-9:
        off=tuple(v*d for v in vec)
        for i,(p,b) in enumerate(zip(trayparts,tb)):
            q=tuple(b[k]+off[k%3] for k in range(6))
            for j,cb in enumerate(CB['A']):
                key='HX_%03d'%j
                if key in first or not ov(cb,q):continue
                v=p.translate(cq.Vector(*off)).intersect(cores['A'][j]).Volume()
                if v>1e-3:first[key]=[d,round(v,2),[round(x,1) for x in cb]]
        if first:break
        d+=step
    return first
R['A_tray_removal_with_HX_in_place']={'-Y':tsweep((0,-1,0),700),'+Y':tsweep((0,1,0),700),'-Z':tsweep((0,0,-1),60)}
print('tray',{k:list(v)[:3] for k,v in R['A_tray_removal_with_HX_in_place'].items()},flush=True)
# 4 clearances of seal carrier, guides and cheeks to the HX frame (bed A, both faces)
frame=[i for i,b in enumerate(CB['A']) if round(b[3]-b[0])==8]
cl={}
for n in [n for n in rows if n.startswith(('AF_','AR_')) and any(k in n for k in ('GUIDE_00','GUIDE_08','GUIDE_04','CHEEK','SLIDING_SEAL_CARRIER','GASKET'))]:
    cand=sorted(frame,key=lambda i:gap(CB['A'][i],RB[n]))[:2]
    cl[n]=round(min(cq.Shape.distance(cores['A'][i],rows[n]) for i in cand),3)
R['A_clearance_to_HX_frame_mm']=cl
cc={}
for f in ('AF','AR'):
    car=rows[f+'_SLIDING_SEAL_CARRIER']
    cc[f]={n:round(cq.Shape.distance(car,rows[n]),3) for n in rows if n.startswith(f+'_CHEEK') or n in (f+'_GUIDE_00',f+'_GUIDE_08')}
R['A_carrier_to_cassette_walls_mm']=cc
# 5 cassette (AF) contacts with structure/host/stand
cas=[n for n in rows if n.startswith('AF_')]
ext=[n for n in rows if not n.startswith(('AF_','AR_','BF_','BR_')) and cat[n] in ('structure','host','stand')]
cont=[]
for a in cas:
    for b in ext:
        if gap(RB[a],RB[b])<0.05 and cq.Shape.distance(rows[a],rows[b])<0.05:
            z=[max(RB[a][2],RB[b][2]),min(RB[a][5],RB[b][5])];cont.append([a,b,[round(v,1) for v in z]])
R['AF_cassette_contacts_with_structure']=cont
R['AF_cassette_highest_structural_contact_z']=max((c[2][1] for c in cont),default=None)
R['AF_cassette_top_z']=max(RB[n][5] for n in cas if cat[n] in ('air','seal','plates','access','gasket'))
# 6 drains
R['drains']={n:[round(v,1) for v in RB[n]] for n in rows if 'DRAIN_STUB' in n or 'TRAY_NOZZLE' in n}
R['floor_top_z']=RB['FLOOR'][5]
# 7 orientation of new restraints
R['restraint_bboxes']={n:[round(v,1) for v in RB[n]] for n in rows if n.startswith(('A_TOP_FORK','A_RISER_BRACE','HX_TOP_CROSS','A_SIDE_BRACE'))}
# 8 gasket area (one face)
g=rows['AF_GASKET_6_FREE'];R['gasket_face_area_mm2']=round(g.Volume()/4.2,1)
json.dump(R,open(outp,'w'),indent=1);print(json.dumps({k:v for k,v in R.items() if k not in ('withdrawal_sweeps_first_contact',)},indent=0)[:6000])
