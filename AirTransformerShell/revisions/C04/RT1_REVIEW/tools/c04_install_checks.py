"""Independent C04 installation checks.
Usage: python c04_install_checks.py <C04 source dir> <C02 deliverables/native> <HX single-core STEP> <out.json>
Rebuilds the C04 installed solids from the unmodified C04 build script (export stage skipped),
places the detailed M101 C04 single-core STEP at the documented A/B transforms, and reports
clashes, clearances, sweeps and valve/actuator interfaces. Read-only on inputs."""
import sys,json,math,itertools,time
from pathlib import Path
import cadquery as cq
src,native,hxstep,outp=sys.argv[1:5]
code=Path(src,'build_c04.py').read_text()
code=code.split('errors=check(installed)')[0]
sys.path.insert(0,src)
sys.argv=[str(Path(src,'build_c04.py')),native]
ns={'__file__':str(Path(src,'build_c04.py')),'__name__':'c04'}
exec(compile(code,'build_c04.py','exec'),ns)
inst=ns['installed']
print('installed host+cassette solids',len(inst),flush=True)
def bb(s):
    b=s.BoundingBox();return (b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax)
def overlap(a,b,tol=0.0):
    return all(min(a[k+3],b[k+3])-max(a[k],b[k])>tol for k in range(3))
hx=cq.importers.importStep(hxstep).val().Solids()
T={'A':(265,-802.175,1150),'B':(265,37.825,1150)}
R={}
# 1. Static clash of the detailed HX against all installed solids, except the HX stand-ins
skip=('FIN_VOLUME_REF','HX_FRAME_REF')
for bed,t in T.items():
    parts=[s.translate(cq.Vector(*t)) for s in hx]
    hb=[bb(s) for s in parts]
    env=(min(b[0] for b in hb),min(b[1] for b in hb),min(b[2] for b in hb),max(b[3] for b in hb),max(b[4] for b in hb),max(b[5] for b in hb))
    R[bed+'_hx_envelope']=[round(v,2) for v in env]
    clashes=[];touch=[]
    for n,(s,c) in inst.items():
        if any(k in n for k in skip):continue
        sb=bb(s)
        if not overlap(sb,env,-0.01):continue
        for i,(p,pb) in enumerate(zip(parts,hb)):
            if overlap(sb,pb,1e-6):
                v=p.intersect(s).Volume()
                if v>1e-3:clashes.append((n,i,round(v,3)))
            elif overlap(sb,pb,-0.01):touch.append(n)
    R[bed+'_hx_clashes_mm3']=clashes
    R[bed+'_hx_face_contacts']=sorted(set(touch))
    print(bed,'clashes',len(clashes),'contacts',sorted(set(touch)),flush=True)
    R[bed+'_parts']=parts
# 2. Minimum distances from HX envelope solids to named host items
def mindist(parts,s):
    return min(p.distance(s) if hasattr(p,'distance') else 0 for p in parts)
names=lambda pat:[n for n in inst if pat in n]
dist={}
for bed in T:
    parts=R[bed+'_parts']
    hb=[bb(p) for p in parts]
    for n in names('ROOF')+names(bed+'W1_RESERVE')+names(bed+'W2_RESERVE')+names(bed+'_WATER_GLAND')+names('SIDE_')+[k for k in names(bed+'_V') ]+names(bed+'_BEAM'):
        s=inst[n][0];sb=bb(s)
        # nearest candidate parts by bbox gap
        def gap(b):return math.sqrt(sum(max(0,max(b[k],sb[k])-min(b[k+3],sb[k+3]))**2 for k in range(3)))
        cand=sorted(range(len(parts)),key=lambda i:gap(hb[i]))[:3]
        dist[bed+':'+n]=dict(bbox_gap=round(min(gap(hb[i]) for i in cand),2),exact=round(min(cq.Shape.distance(parts[i],s) for i in cand),2) if gap(hb[cand[0]])<200 else None)
R['min_distance_mm']=dist
print(json.dumps(dist,indent=0),flush=True)
# 3. Extraction sweeps: translate the full HX by steps and record first obstructing host solid
removable_default=('_HX_FRAME_REF','FIN_VOLUME_REF')
def sweep(bed,vec,dmax,step,remove):
    parts=R[bed+'_parts'];first={};base=[bb(p) for p in parts]
    host={n:(s,bb(s)) for n,(s,c) in inst.items() if not any(k in n for k in removable_default+remove)}
    d=step
    while d<=dmax+1e-9:
        off=[v*d for v in vec]
        mb=[(b[0]+off[0],b[1]+off[1],b[2]+off[2],b[3]+off[0],b[4]+off[1],b[5]+off[2]) for b in base]
        env=(min(b[0] for b in mb),min(b[1] for b in mb),min(b[2] for b in mb),max(b[3] for b in mb),max(b[4] for b in mb),max(b[5] for b in mb))
        for n,(s,sb) in host.items():
            if n in first or not overlap(sb,env,1e-6):continue
            for i,pb in enumerate(mb):
                if overlap(sb,pb,1e-6):
                    v=parts[i].translate(cq.Vector(*off)).intersect(s).Volume()
                    if v>1e-3:first[n]=(d,i,round(v,1));break
        d+=step
    return dict(sorted(first.items(),key=lambda x:x[1]))
sw={}
yA=(0,-1,0);yB=(0,1,0)
sw['A_-Y_side_skin_removed']=sweep('A',yA,900,25,('SIDE_-852',))
sw['B_+Y_side_skin_removed']=sweep('B',yB,900,25,('SIDE_850',))
sw['A_+Z_roof_removed']=sweep('A',(0,0,1),1300,50,('ROOF',))
sw['B_+Z_roof_removed']=sweep('B',(0,0,1),1300,50,('ROOF',))
sw['A_-X_front_skin_removed']=sweep('A',(-1,0,0),900,50,('FRONT_SKIN',))
R['sweeps_first_contact_mm']=sw
print(json.dumps(sw,indent=0),flush=True)
for bed in T:R.pop(bed+'_parts')
# 4. C02 valve references and withdrawal zones in C04 (+1000 Z) against roof and ports
vz={}
roof=inst['ROOF'][0]
for bed in 'AB':
    for k in ('VL','VU'):
        for item in ('BODY','ACTUATOR','ACTUATOR_WITHDRAWAL'):
            s=cq.Shape.importBrep(str(Path(native,f'{bed}_{k}_{item}.brep'))).translate((0,0,1000))
            b=bb(s);v=s.intersect(roof).Volume() if b[5]>2550 else 0.0
            vz[f'{bed}_{k}_{item}']=dict(zmax=round(b[5],2),y=[round(b[1],2),round(b[4],2)],roof_intersection_mm3=round(v,1))
R['valves_c04']=vz
# 5. Port axis to valve AB face offsets (C02 WATER_INTERFACES +1000 Z) using C04 HX functions
wi=json.load(open(Path(native).parent/'tables'/'WATER_INTERFACES.json'))
ports={'A.W1':(615,-75.325,2370),'A.W2':(615,-225.325,2370),'B.W1':(615,764.675,2370),'B.W2':(615,614.675,2370)}
func={'W1':'CS/HR','W2':'CR/HS'}
valvefunc={'VL':'CS/HR','VU':'CR/HS'}
links=[]
for row in wi:
    if not row['id'].endswith('.AB'):continue
    v=row['id'].split('.')[0];bed=v[0];vk=v[2:]
    face=row['body_face_mm'];face=[face[0],face[1],face[2]+1000]
    correct=[p for p in ports if p[0]==bed and func[p[2:]]==valvefunc[vk]][0]
    p=ports[correct]
    links.append(dict(valve=v,valve_function=valvefunc[vk],c02_table_target=row['network'],required_target=correct,
        table_target_ok=row['network']==correct,AB_face_C04=[round(c,3) for c in face],dX=round(face[0]-p[0],2),dY=round(face[1]-p[1],2),dZ=round(face[2]-p[2],2)))
R['valve_links']=links
print(json.dumps(links,indent=0))
json.dump(R,open(outp,'w'),indent=1)
