"""Four-core topology with one horizontal M101 C05 coil per bed (mm). Usage:
  python cube_horizontal.py <M101 C05 single-core STEP> <out dir> [D=500] [pitch=800]
Same airflow as the four-core outdoor reference (V050): P in through a VERTICAL damper on the upper plenum's front
end wall (flow +X), down through the coil, out through a VERTICAL damper on the lower plenum's rear end wall (+X).
R in through a damper on the lower plenum's floor slope next to the rear corner (flow +Z, from a bottom hopper),
up through the coil, out through a damper on the roof slope next to the front corner (+Z, rooftop fan).
Both plenums are wedges that close onto the coil frame land (apex gap 0). Hydronic pack in the front-bottom
quadrant; the coil terminal pipes point down into it. The core is rotated (no mirror): global X = 1054 - lz,
Y = cy + 367.775 - ly, Z = Zc + 220 - lx (ports at the front end, pointing down)."""
import sys,json,math
from pathlib import Path
import cadquery as cq
hxstep,out=sys.argv[1],Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
D=float(sys.argv[3]) if len(sys.argv)>3 else 500.;PITCH=float(sys.argv[4]) if len(sys.argv)>4 else 800.
V=cq.Vector;T=2.;W=612.;L=1000.
def box(x,y,z,dx,dy,dz):return cq.Solid.makeBox(dx,dy,dz,V(x,y,z))
def xz(poly,y,dy):
    w=cq.Wire.makePolygon([V(x,y,z) for x,z in poly],close=True);return cq.Solid.extrudeLinear(w,[],V(0,dy,0))
# vertical budget: R damper body below the rear floor corner, plus a 120 mm intake passage above a 60 mm base
th=math.atan2(D,L);c,s=math.cos(th),math.sin(th)
Zc=60+120+180*c+256*0+D+0.0      # coil bottom face (lower plenum apex at the front)
Zc=math.ceil(Zc/10)*10
Ztop_face=Zc+220
XF,XR=-10.,L+10.                 # plenum end walls on the frame lands
parts={}
def put(n,sh):
    assert sh.isValid(),n;parts[n]=sh
core=cq.importers.importStep(hxstep).val().Solids()
cores={}
beds={"A":-PITCH/2,"B":PITCH/2}
def on_slope(corner,u_dir,n_dir,Lf,cy):
    # damper body: length Lf along u_dir from the corner (in X-Z), 706 wide in Y, 180 along n_dir (outward)
    p0=V(corner[0],cy-353,corner[1]);u=V(u_dir[0],0,u_dir[1]);n=V(n_dir[0],0,n_dir[1])
    pts=[p0,p0+u*Lf,p0+u*Lf+n*180,p0+n*180]
    w=cq.Wire.makePolygon(pts,close=True);return cq.Solid.extrudeLinear(w,[],V(0,706,0))
for bed,cy in beds.items():
    for i,sh in enumerate(core):
        cores[f"{bed}_HX_{i:03d}"]=sh.rotate(V(0,0,0),V(1,0,-1),180).translate(V(1054,cy+367.775,Zc+220))
    y0=cy-W/2
    put(bed+"_ROOF_SLOPE",xz([(XF,Ztop_face+D),(XR,Ztop_face),(XR,Ztop_face+T),(XF,Ztop_face+D+T)],y0-T,W+2*T))
    put(bed+"_FLOOR_SLOPE",xz([(XF,Zc),(XR,Zc-D),(XR,Zc-D-T),(XF,Zc-T)],y0-T,W+2*T))
    put(bed+"_FRONT_END_WALL",box(XF-T,y0-T,Ztop_face,T,W+2*T,D))
    put(bed+"_REAR_END_WALL",box(XR,y0-T,Zc-D,T,W+2*T,D))
    for side,yy in (("L",y0-T),("R",y0+W)):
        put(f"{bed}_UPPER_CHEEK_{side}",xz([(XF,Ztop_face),(XF,Ztop_face+D),(XR,Ztop_face)],yy,T))
        put(f"{bed}_LOWER_CHEEK_{side}",xz([(XF,Zc),(XR,Zc),(XR,Zc-D)],yy,T))
    # dampers: P vertical on end walls at the wide ends; R on the slopes beside those corners
    put(bed+"_P_IN_DAMPER",box(XF-T-180,cy-353,Ztop_face+D-421,180,706,421))
    put(bed+"_P_OUT_DAMPER",box(XR+T,cy-353,Zc-D,180,706,421))
    put(bed+"_R_OUT_DAMPER",on_slope((XF,Ztop_face+D+T),(c,-s),(s,c),256,cy))           # above the roof, near the front corner
    put(bed+"_R_IN_DAMPER",on_slope((XR,Zc-D-T),(-c,s),(-s,-c),256,cy))               # below the floor, near the rear corner
    # hydronic pack reserve: front-bottom quadrant below the lower plenum's apex
    put(bed+"_HYDRONIC_RESERVE",box(-200,cy-380,80,520,760,Zc-0.32*D-80-150))
    # coil side rails (support under the frame side members, outside the plenum width)
    for hand in (-1,1):put(f"{bed}_COIL_RAIL_{hand}",box(-20,cy+hand*355-15,Zc-40,1080,30,40))
allb=[ (lambda b:(b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax))(x.BoundingBox()) for x in list(parts.values())+list(cores.values())]
env=dict(x=[round(min(b[0] for b in allb)-20,1),round(max(b[3] for b in allb)+20,1)],y=[-PITCH-10,PITCH+10],z=[0,round(max(b[5] for b in allb)+60,1)])
def bb(s):b=s.BoundingBox();return [b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax]
def ov(a,b):return all(min(a[k+3],b[k+3])-max(a[k],b[k])>1e-6 for k in range(3))
PB={n:bb(s) for n,s in parts.items()};CB={n:bb(s) for n,s in cores.items()}
clash=[]
for n,sh in parts.items():
    for m,cs in cores.items():
        if ov(PB[n],CB[m]):
            v=sh.intersect(cs).Volume()
            if v>1e-3:clash.append([n,m,round(v,2)])
selfc=[]
from itertools import combinations
for a,b in combinations(parts,2):
    if ov(PB[a],PB[b]):
        v=parts[a].intersect(parts[b]).Volume()
        if v>1e-3 and not ('DAMPER' in a+b and ('SLOPE' in a+b or 'WALL' in a+b)):selfc.append([a,b,round(v,1)])
def mind(n,bed):
    cand=sorted((m for m in cores if m.startswith(bed+"_")),key=lambda m:sum(max(0,max(PB[n][k],CB[m][k])-min(PB[n][k+3],CB[m][k+3]))**2 for k in range(3)))[:8]
    return round(min(cq.Shape.distance(parts[n],cores[m]) for m in cand),1)
clear={n:mind(n,n[0]) for n in parts if n[0] in "AB" and any(k in n for k in ("DAMPER","HYDRONIC"))}
# where the coil terminal pipes / unions end up (lowest core Z near the front end)
front=[CB[m] for m in CB if m.startswith("A_") and CB[m][3]<0]
Q=4870/3600
res=dict(orientation="horizontal coil, vertical airflow (four-core topology, one coil per bed)",D_mouth_mm=D,coil_bottom_Z=Zc,coil_top_Z=Ztop_face,
  roof_slope_deg=round(math.degrees(th),1),P_to_R_damper_dihedral_deg=round(90-math.degrees(th),1),
  envelope_mm=env,dimensions_mm={k:round(v[1]-v[0],1) for k,v in env.items()},
  mouth_velocity_process_ms=round(Q/(W/1e3*D/1e3),2),mouth_velocity_regen_2435_ms=round(Q/2/(W/1e3*D/1e3),2),
  core_parts_in_front_of_X0=dict(count=len(front),z_range=[round(min(b[2] for b in front),1),round(max(b[5] for b in front),1)] if front else None,
     x_min=round(min(b[0] for b in front),1) if front else None),
  core_clashes_above_0p001_mm3=clash,skeleton_self_intersections=selfc,min_clearance_to_core_mm=clear)
a=cq.Assembly(name="CUBE_HORIZONTAL_CONCEPT")
for n,sh in parts.items():a.add(sh,name=n)
a.export(str(out/"CUBE_HORIZONTAL_SKELETON.step"))
json.dump(res,open(out/"cube_horizontal.json","w"),indent=1);print(json.dumps(res,indent=1))
