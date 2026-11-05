"""CAD in mm. Usage: python build_c04.py [path to shell C02 deliverables/native].
Terraced distribution: identical paired manifolds, repeated as four cassettes.
"""
from design import *
from network import diam
import cadquery as cq
import numpy as np
import json,sys,hashlib
from pathlib import Path
from itertools import combinations
OUT=Path(__file__).parent
colors={'air':(.30,.61,.65),'screen':(.76,.54,.23),'shell':(.66,.71,.76),'core':(.74,.55,.32),'P':(.11,.52,.70),'R':(.89,.44,.15),'water':(.37,.48,.71)}
def box(x,y,z,dx,dy,dz):return cq.Solid.makeBox(dx,dy,dz,cq.Vector(x,y,z))
def cylinder(x,y,z,r,l):return cq.Solid.makeCylinder(r,l,cq.Vector(x,y,z),cq.Vector(1,0,0))
def poly(points,y,depth):
    w=cq.Wire.makePolygon([cq.Vector(x,y,z) for x,z in points],close=True)
    return cq.Solid.extrudeLinear(w,[],cq.Vector(0,depth,0))
def offset(points,d):
    a=np.array(points);t=np.diff(a,axis=0);t/=np.linalg.norm(t,axis=1)[:,None]
    n=np.c_[-t[:,1],t[:,0]]
    mid=(n[:-1]+n[1:])/(1+(n[:-1]*n[1:]).sum(axis=1))[:,None]
    q=a+d*np.vstack((n[0],mid,n[-1]))
    q[-1]+=(THROAT-q[-1,1])/t[-1,1]*t[-1]
    return [tuple(v) for v in q]
def aperture_plate(x,y,z,w,h,th,cuts):
    sh=box(x,y,z,th,w,h)
    return sh.cut(*cuts)
def strip(z,d):
    edges=[(0,z+.75),(0,z+BAND-.75)]
    face=cq.Wire.makePolygon([cq.Vector(12,y,h) for y,h in [(-306,edges[0][1]),(306,edges[0][1]),(306,edges[1][1]),(-306,edges[1][1])]],close=True)
    holes=[cq.Wire.makeCircle(d/2,cq.Vector(12,(j-11.5)*25,z+12.5+25*k),cq.Vector(1,0,0)) for j in range(24) for k in range(5)]
    return cq.Solid.extrudeLinear(face,holes,cq.Vector(1.5,0,0))
def flange_cuts(x):
    cuts=[]
    for lo,h in PORTS.values():
        cuts.append(box(x-1,-315,lo,5,630,h))
        ow,oh=706,h+76
        nx,ny=math.ceil((ow-38)/70),math.ceil((oh-38)/70)
        uv=[(-334+i*668/nx,z) for i in range(nx+1) for z in (lo-19,lo+h+19)]
        uv += [(y,lo-19+(oh-38)*i/ny) for y in (-334,334) for i in range(1,ny)]
        cuts += [cylinder(x-1,y,z,4.5,5) for y,z in uv]
    return cuts
import math
proto={}
def add(n,s,c):
    assert s.isValid() and len(s.Solids())==1,n
    proto[n]=(s,c)
for i in range(9):
    p=guide(i)
    add('GUIDE_%02d'%i,poly(offset(p,-T/2)+offset(p,T/2)[::-1],-306,W),'air')
bounds_profile=offset(guide(0),-T/2)+offset(guide(8),T/2)[::-1]
for y in (-307.5,306):
    add('CHEEK_'+str(y),poly(bounds_profile,y,T),'air')
for i,d in enumerate(diam):add('BALANCE_BAND_%02d'%i,strip(Z0+i*BAND,d),'screen')
# The whole 320 mm throat ends in a selector below the lowest face strip.
inside=FOOT-2
outside=OUTER+2
add('SELECT_INNER',box(inside-1.5,-358,144,1.5,716,THROAT-144),'air')
add('DUAL_VALVE_FLANGE',aperture_plate(outside,-358,144,716,THROAT-144,2.5,flange_cuts(outside)),'air')
for y in (-359.5,358):add('BOX_CHEEK_'+str(y),box(inside-1.5,y,144,outside-inside+4,1.5,THROAT-144),'air')
add('BOTTOM',box(inside-1.5,-359.5,142.5,outside-inside+4,719,1.5),'air')
# Throat plate is flush below the guide feet; selector touches each channel.
cap=box(inside,-358,THROAT-1.5,outside-inside,716,1.5)
add('THROAT_PLATE',cap.cut(box(FOOT,-306,THROAT-2,DEPTH,W,3)),'air')
for tag,(z,h) in PORTS.items():
    add('RESERVE_'+tag,box(outside+2.5,-353,z-38,180,706,h+76),tag)
# Core-seat perimeter gasket outside airway and flush against HX frame.
# Put lip on the outside of cheek/outer-wall ends to leave the active window clear.
seal=box(0,-326,Z0-20,5,652,1040).cut(box(-1,-307.5,Z0-.75,8,615,1001.5))
add('SEAT_RETURN',seal,'air')
def bbox(s):
    b=s.BoundingBox()
    return (b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax)
def check(p):
    bb={n:bbox(s) for n,(s,c) in p.items()};bad=[]
    for a,b in combinations(p,2):
        if all(min(bb[a][k+3],bb[b][k+3])-max(bb[a][k],bb[b][k])>1e-5 for k in range(3)):
            vol=p[a][0].intersect(p[b][0]).Volume()
            if vol>.001:bad.append((a,b,round(vol,3)))
    return bad
clash=check(proto);assert not clash,clash
def make_assembly(name,rows):
    a=cq.Assembly(name=name)
    for n,(s,c) in rows.items():
        a.add(s,name=n,color=cq.Color(*colors[c],.40 if 'RESERVE' in n else 1.))
    return a
full=cq.Assembly(name='AT_SHELL_C04')
cs=make_assembly('TAPER_CASSETTE',proto)
# Rotate around Z for the -X face (all local Y coordinates are symmetric).
for bed,cy in CENTRES.items():
    for face,x,ang in [('F',265,180),('R',485,0)]:
        loc=cq.Location(cq.Vector(x,cy,0),cq.Vector(0,0,1),ang)
        full.add(cs,name=bed+'_'+face,loc=loc)
layout={}
def place(n,s,c='shell'):layout[n]=(s,c)
front=265-outside-2.5
rear=1312.
left,right=-852.,852.
# Boundary skins: openings at front terminal and rear extension of each valve.
for label,x in [('FRONT',front-2),('BACK',rear-2)]:
    cuts=[]
    for cy in CENTRES.values():
        if label=='FRONT':
            # Single removable valve-flange panel occupies this opening.
            cuts.append(box(x-1,cy-360,142,5,720,THROAT-142+2))
        else:
            cuts.extend(box(x-1,cy-315,z,5,630,h) for z,h in PORTS.values())
    place(label+'_SKIN',aperture_plate(x,left,104,right-left,2446,2,cuts))
for y in (left,right-2):
    side=box(front,y,104,rear-2-front,2,2446)
    for z,h in PORTS.values():
        side=side.cut(box(485+outside+3,y-1,z+h/2-111,161,5,222))
    place('SIDE_'+str(y),side)
place('ROOF',box(front-2,left,2550,rear-front+2,right-left,2))
place('FLOOR',box(front-2,left,102,rear-front+2,right-left,2))
def rhs(x,y,z,dx,dy,dz,axis):
    dims=[dx,dy,dz];pos=[x+3,y+3,z+3];size=[v-6 for v in dims];pos[axis]-=4;size[axis]=dims[axis]+2
    return box(x,y,z,*dims).cut(box(*pos,*size))
for y in (-850,800):
    place('BASE_SILL_'+str(y),rhs(front,y,52,rear-2-front,50,50,0))
    for x in (front,rear-52):
        place('FOOT_'+str((x,y)),box(x,y,0,50,50,52))
        place('POST_'+str((x,y)),rhs(x,y,104,50,50,2446,2))
for x in (275,435):
    place('BASE_Y_CROSS_'+str(x),rhs(x,-800,52,40,1600,50,1))
for y in (-850,820):
    place('ROOF_RAIL_'+str(y),rhs(front+50,y,2510,rear-52-front-50,30,40,0))
for bed,cy in CENTRES.items():
    ty=cy-367.775
    # Actual C04 mounting pattern with transferred-through holes.
    for j,y in enumerate((ty+15,ty+655)):
        beam=rhs(265,y-25,1100,220,50,50,0)
        holes=[cq.Solid.makeCylinder(8.5,52,cq.Vector(x,y,1099)) for x in (317,437)]
        place(bed+'_BEAM_'+str(j),beam.cut(*holes))
        for x in (275,435):
            place(bed+'_RISER_'+str((j,x)),rhs(x,y-20,104,40,40,996,2))
    place(bed+'_FIN_VOLUME_REF',box(296.65,cy-306,Z0,152,612,1000),'core')
    for face,x in [('F',265),('R',477)]:
        seat=box(x,cy-326,Z0-20,8,652,1040).cut(box(x-1,cy-306,Z0,10,612,1000))
        place(bed+face+'_HX_FRAME_REF',seat,'core')
    gland=box(750,cy-375,2280,2,750,240)
    for id,oy in [('W1',726.85),('W2',576.85)]:
        y=ty+oy
        gland=gland.cut(cylinder(749,y,2370,55,5))
        place(bed+id+'_RESERVE_OD85',cylinder(615,y,2370,42.5,160),'water')
    place(bed+'_WATER_GLAND',gland)
    for tag,(z,h) in PORTS.items():
        x=485+outside+2.5+180
        throat_ext=box(x,cy-316.5,z-1.5,rear-2-x,633,h+3).cut(box(x-1,cy-315,z,rear-x+2,630,h))
        place(bed+tag+'_DISCHARGE_SLEEVE',throat_ext)
        # Drives attach on the bed's outboard side. Shaft bridge to drive is a reservation.
        side=1 if bed=='B' else -1
        y=cy+353 if side==1 else cy-353-170
        for face,xx in [('F',front-164),('R',485+outside+3)]:
            place(bed+face+tag+'_DRIVE_RESERVE',box(xx,y,z+h/2-110,160,170,220),'R')
    if len(sys.argv)>1:
        for k in ('VL','VU'):
            for item in ('BODY','ACTUATOR'):
                n=bed+'_'+k+'_'+item
                s=cq.Shape.importBrep(str(Path(sys.argv[1])/(n+'.brep'))).translate((0,0,1000))
                place(n+'_REFERENCE',s,'water')
full.add(make_assembly('HOST',layout),name='HOST_GEOMETRY')
# Inspect installed host solids against occurrences as well as prototype joints.
installed=dict(layout)
for bed,cy in CENTRES.items():
    for fc,x,ang in [('F',265,180),('R',485,0)]:
        for n,(s,c) in proto.items():
            t=s.rotate((0,0,0),(0,0,1),ang).translate((x,cy,0))
            installed[bed+fc+'_'+n]=(t,c)
errors=check(installed)
(OUT/'fit.json').write_text(json.dumps(dict(installed_clashes=errors),indent=2))
assert not errors,errors
expected_count=sum(len(s.Solids()) for s,c in installed.values())
report={'installed_clashes':errors,'threshold_mm3':.001,'channel_count_per_face':8,'total_channels':32,'damper_count':8,'body_depth_mm':180,'shell_xz':[front-2,rear,0,2552],'guides':{i:guide(i) for i in range(9)},'files':[]}
for name,a,count in [('C04_TAPER_CASSETTE',cs,len(proto)),('C04_INSTALLED',full,expected_count)]:
    path=OUT/(name+'.step');a.save(str(path))
    s=cq.importers.importStep(str(path)).val();got=len(s.Solids());assert got==count,(name,got,count)
    report['files'].append(dict(file=path.name,solids=got,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
(OUT/'fit.json').write_text(json.dumps(report,indent=2))
print(report['files'],flush=True)
