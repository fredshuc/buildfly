"""Shell C03. Run with CadQuery 2.8, matplotlib and Python 3.12.
Inputs: unpacked shell C02 deliverables/native and HX C04 interface package.
Usage: python build_ducts.py PATH_TO_C02_DELIVERABLES PATH_TO_HX_C04
Units mm. Product flow P and regeneration R are interlocked alternatives.
"""
from pathlib import Path
import csv, hashlib, json, math, sys
import cadquery as cq
from itertools import combinations

OUT=Path(__file__).resolve().parent
shell,hx=map(Path,sys.argv[1:3])
native=shell/'native'
index={r['name']:r for r in json.loads((native/'ASSEMBLY.json').read_bytes())}
placement=json.loads((hx/'INTERFACES_AND_PLACEMENTS.json').read_bytes())['placement']
ports=list(csv.DictReader((shell/'tables/PORTS.csv').open(encoding='utf-8-sig')))
COL={'shell':(.63,.68,.73),'duct':(.43,.64,.69),'P':(.10,.56,.73),'R':(.91,.49,.13),'seal':(.18,.25,.30),'drive':(.58,.42,.69),'core':(.73,.58,.36),'water':(.28,.51,.76)}
parts={}; volumes={}; stations=[]; new=set(); extras=set()
def put(name,shape,group,changed=False,reference=False):
    assert name not in parts and shape.isValid(),name
    parts[name]=(shape,group)
    if changed:new.add(name)
    if reference:extras.add(name)
def box(x,y,z,l,w,h):
    return cq.Solid.makeBox(l,w,h,cq.Vector(x,y,z))
def cylinder(x,y,z,l,r):
    return cq.Solid.makeCylinder(r,l,cq.Vector(x,y,z),cq.Vector(1,0,0))
def ring(x,l,y,z,w,h,rim):
    return box(x,y-rim,z-rim,l,w+2*rim,h+2*rim).cut(box(x-1,y,z,l+2,w,h))
def original(name):
    return cq.Shape.importBrep(str(native/index[name]['brep']))
def wire(s):
    x,lo,hi,b,t=s
    return cq.Wire.makePolygon([cq.Vector(x,y,z) for y,z in [(lo,b),(hi,b),(hi,t),(lo,t),(lo,b)]])
def loft(a,b):return cq.Solid.makeLoft([wire(a),wire(b)],ruled=True)
def bands(s):
    x,l,r,b,t=s
    return [(x,l-1.5,l,b,t),(x,r,r+1.5,b,t),(x,l-1.5,r+1.5,b-1.5,b),(x,l-1.5,r+1.5,t,t+1.5)]
def segment(name,a,b,g):
    volumes[name]=loft(a,b)
    for tag,sa,sb in zip(('LEFT','RIGHT','FLOOR','ROOF'),bands(a),bands(b)):
        put(name+'_'+tag,loft(sa,sb),g,True)
    for end,s in zip(('start','end'),(a,b)):
        stations.append(dict(segment=name,end=end,x=s[0],y_min=s[1],y_max=s[2],z_min=s[3],z_max=s[4],area_m2=(s[2]-s[1])*(s[4]-s[3])/1e6))
def bounds(s):
    b=s.BoundingBox()
    return (b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax)
def overlap(a,b):
    return all(min(a[k+3],b[k+3])-max(a[k],b[k])>1e-5 for k in range(3))
for n,r in index.items():
    if r['kind']=='DESIGN_PART':
        if 'WATER_GLAND_PANEL' in n or 'HX_APERTURE' in n or 'HX_SEAL' in n or n.startswith(('B_CROSS_SUPPORT','B_POD_BOTTOM_C')):continue
        put(n,original(n),'shell')
    elif n.endswith(('_DAMPER','_DRIVE')) or (n[2:5] in ('VL_','VU_') and n.endswith(('_ACTUATOR','_BODY'))):
        put(n,original(n),('drive' if not n.endswith('_DAMPER') else n.split('_')[2]),reference=True)
for k in (0,1):
    put('B_CROSS_SUPPORT_'+str(k),original('A_CROSS_SUPPORT_'+str(k)).translate((0,840,0)),'shell',True)
pan=box(257.5,21.5,101.5,235,817,1.5)
for y in (52.825,692.825):pan=pan.cut(box(264,y-26,100,222,52,5))
put('B_POD_BOTTOM_C',pan,'shell',True)
for bed in ('A','B'):
    tx,ty,tz=placement[bed]['t_mm']
    assert placement[bed]['R']==[[1,0,0],[0,1,0],[0,0,1]]
    cy=ty+367.775
    zbot=tz+54
    lo,hi=(-840,-20) if bed=='A' else (20,840)
    # Interface references from C04 frame rails and fin dimensions.
    put(bed+'_FIN_ACTIVE_REFERENCE',box(tx+31.65,cy-306,zbot,152,612,1000),'core',reference=True)
    gland=box(750,lo,1300,1.5,hi-lo,400)
    for p in [v for v in placement['global_ports'] if v['id'].startswith(bed+'.')]:
        x,y,z=p['xyz_mm']
        put(p['id'].replace('.','_')+'_TO_BULKHEAD_OD85',cylinder(x,y,z,160,42.5),'water',reference=True)
        gland=gland.cut(cylinder(749,y,z,5,55))
    put(bed+'_C04_GLAND_PANEL',gland,'shell',True)
    for face,x0,sign in [('F',2.5,1),('R',747.5,-1)]:
        prefix=bed+'_'+face+'_'
        port=next(p for p in ports if p['id']==prefix+'P')
        yport=float(port['opening_y_mm'])+315
        x1=x0+sign*135
        x2=x1+sign*2
        end=x0+sign*252.5
        yc=(cy+yport)/2
        def station(x,center,w,b,t):return (x,center-w/2,center+w/2,b,t)
        # Two independently walled mouths, then a full-height common diffuser.
        for tag,b,t,bb,tt in [('P',300,645,270,720),('R',940,1120,870,1155)]:
            segment(prefix+tag,station(x0,yport,630,b,t),station(x1,yc,630,bb,tt),tag)
        # Joint at the two mouths: the central web seals the inter-branch void.
        web=box(min(x1,x2),yc-316.5,268.5,2,633,888)
        for b,t in [(270,720),(870,1155)]:web=web.cut(box(min(x1,x2)-1,yc-315,b,4,630,t-b))
        put(prefix+'MERGE_WEB',web,'duct',True)
        segment(prefix+'COMMON',station(x2,yc,630,270,1155),station(end,cy,612,zbot,zbot+1000),'duct')
        ax=min(end,end+2.5*sign)
        aperture=box(ax,lo+1.5,100,2.5,hi-lo-3,1198.5).cut(box(ax-1,cy-306,zbot,5,612,1000))
        put(prefix+'C04_APERTURE',aperture,'duct',True)
        sx=257.5 if face=='F' else 485
        put(prefix+'C04_SEAL',ring(sx,7.5,cy-306,zbot,612,1000,20),'seal',True)
        put(prefix+'HX_SEAT_DATUM',ring(tx if face=='F' else tx+212,8,cy-306,zbot,612,1000,20),'core',reference=True)

def export(name,names):
    assembly=cq.Assembly(name=name)
    for n in sorted(names):
        s,g=parts[n]
        assembly.add(s,name=n,color=cq.Color(*COL[g],.45 if n in extras else 1))
    path=OUT/(name+'.step')
    assembly.save(str(path))
    actual=cq.importers.importStep(str(path)).val()
    expected=sum(len(parts[n][0].Solids()) for n in names)
    assert len(actual.Solids())==expected,(path,expected,len(actual.Solids()))
    return dict(file=path.name,occurrences=len(names),solids=expected,bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
boxes={n:bounds(s) for n,(s,g) in parts.items()}
clashes=[]
for a,b in combinations(parts,2):
    if (a in new or b in new) and overlap(boxes[a],boxes[b]):
        v=parts[a][0].intersect(parts[b][0]).Volume()
        if v>.001:clashes.append([a,b,round(v,3)])
obstructions=[]
for n,air in volumes.items():
    airbounds=bounds(air)
    for part,(shape,group) in parts.items():
        if overlap(airbounds,boxes[part]):
            v=air.intersect(shape).Volume()
            if v>.001:obstructions.append([n,part,round(v,3)])
assert len(ports)==8 and len(volumes)==12
duct={n for n in parts if any(t in n for t in ['_COMMON_','_MERGE_WEB','_C04_APERTURE','_C04_SEAL','_DUAL_PORT_PLATE','_DAMPER','_DRIVE']) or (n in new and any(n.endswith('_'+t) for t in ('LEFT','RIGHT','FLOOR','ROOF')))}
results={'scope':'Changed solids vs installed shell, reference seats, OD85 spools, eight damper and drive reservations and valve bodies/actuators. Airway interiors vs installed geometry. Static check.','clashes_mm3':clashes,'airway_obstructions_mm3':obstructions,'air_sections':stations,'damper_ports':ports}
(OUT/'verification.json').write_text(json.dumps(results,indent=2))
assert not clashes and not obstructions,(clashes,obstructions)
results['STEP_readback']=[export('C03_DUCTS_AND_DAMPERS',duct),export('C03_INSTALLED_LAYOUT',parts)]
(OUT/'verification.json').write_text(json.dumps(results,indent=2))
print(results['STEP_readback'],flush=True)
