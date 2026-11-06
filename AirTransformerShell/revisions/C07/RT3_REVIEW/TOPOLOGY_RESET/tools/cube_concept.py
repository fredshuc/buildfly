"""Cube Z-flow topology concept for the two-bed module (mm). Usage:
  python cube_concept.py <M101 C05 single-core STEP> <out dir> [D=700] [pitch=800] [--step]
Per bed: vertical M101 C05 core; front plenum = wedge open at the top (process in / regeneration out),
rear plenum = wedge open at the bottom (process out / regeneration in). Each sloped wall meets the coil frame
land at the end of the 1000 mm active height. Damper positions follow the 4-bed diverter corner: at each plenum
the two independent dampers sit on the two faces meeting at the outer corner (slope and roof at the top,
slope and floor at the bottom). Top: P in on the front slope, R out on the roof (rooftop extraction fan).
Bottom: P out on the floor, R in on the rear slope. The dihedral between the two damper planes is 90-atan(D/H).
Builds the reference solids, places the detailed core twice, checks intersections and clearances,
writes CUBE_CONCEPT.step and cube_concept.json. Concept geometry only: no sheet-metal detail."""
import sys,json,math
from pathlib import Path
import cadquery as cq
hxstep,out=sys.argv[1],Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
args=[a for a in sys.argv[3:] if not a.startswith('--')];WRITE_STEP='--step' in sys.argv
D=float(args[0]) if args else 700.;PITCH=float(args[1]) if len(args)>1 else 800.
T=2.0;W=612.;ZB=300.;H=1000.;ZT=ZB+H          # active face Z300-1300
HX0=(0.,0.,ZB-54.)                              # core local Z54 = active bottom
V=cq.Vector
def box(x,y,z,dx,dy,dz):return cq.Solid.makeBox(dx,dy,dz,V(x,y,z))
def xz(poly,y,dy):
    w=cq.Wire.makePolygon([V(x,y,z) for x,z in poly],close=True);return cq.Solid.extrudeLinear(w,[],V(0,dy,0))
parts={};cat={}
def put(n,s,c):
    assert s.isValid(),n;parts[n]=s;cat[n]=c
core=cq.importers.importStep(hxstep).val().Solids()
cores={}
beds={"A":-PITCH/2,"B":PITCH/2}
for bed,cy in beds.items():
    ty=cy-367.775
    for i,s in enumerate(core):cores[f"{bed}_HX_{i:03d}"]=s.translate(V(HX0[0],ty+HX0[1],HX0[2]))
    y0=cy-W/2
    # front wedge: air volume bounded by the slope from (-D,ZT) to (0,ZB); wall is the sheet under that line
    put(bed+"_FRONT_SLOPE",xz([(-D,ZT),(0,ZB),(0,ZB-T*1.25),(-D-T*0.8,ZT)],y0-T,W+2*T),"air")
    put(bed+"_REAR_SLOPE",xz([(220,ZT),(220+D,ZB),(220+D+T*0.8,ZB),(220,ZT+T*1.25)],y0-T,W+2*T),"air")
    for side,yy in (("L",y0-T),("R",y0+W)):
        put(f"{bed}_FRONT_CHEEK_{side}",xz([(-D,ZT),(0,ZB),(0,ZT)],yy,T),"air")
        put(f"{bed}_REAR_CHEEK_{side}",xz([(220,ZT),(220+D,ZB),(220,ZB)],yy,T),"air")
    # mouths: front top, rear bottom. Dampers laid flat: P (421 x 706) and R (256 x 706) flanges, 180 deep.
    # corner dampers. Oriented 180 mm bodies outside the plenum, flange edge on the corner line.
    def on_slope(corner,phi,L):
        b=cq.Solid.makeBox(L,706,180,V(0,-353,-180))      # local x along the slope from the corner, z outward
        return b.rotate(V(0,0,0),V(0,1,0),phi).translate(V(corner[0],cy,corner[1]))
    phi_top=math.degrees(math.atan2(H,D))                  # front slope from the top corner, down and inward
    put(bed+"_FP_DAMPER_RESERVE",on_slope((-D,ZT),phi_top,421),"damper")       # P in, on the front slope
    put(bed+"_FR_DAMPER_RESERVE",box(-D,cy-353,ZT,256,706,180),"damper")      # R out, on the roof
    put(bed+"_RP_DAMPER_RESERVE",box(220+D-421,cy-353,ZB-180,421,706,180),"damper")  # P out, on the floor
    put(bed+"_RR_DAMPER_RESERVE",on_slope((220+D,ZB),phi_top-180,256),"damper")      # R in, on the rear slope
    # water bay reserve in the top-rear dead triangle (above the rear slope, behind the core terminal pipes)
    put(bed+"_WATER_BAY_RESERVE",box(640,cy-353,ZT-300,260,706,500),"water")
    # core supports under the frame shoes, beside the rear mouth
    for x in (20,160):put(f"{bed}_CORE_STAND_{x}",box(x,ty,100,40,720,ZB-54-100),"structure")
# envelope
xmin=-D-T*0.8-10;xmax=220+D+T*0.8+10;ymin=-PITCH-10;ymax=PITCH+10;zmin=0;zmax=max(ZT+180+20,ZB-54+1249+25)
put("BASE",box(xmin,ymin,0,xmax-xmin,ymax-ymin,100),"structure")
put("ROOF",box(xmin,ymin,zmax-T,xmax-xmin,ymax-ymin,T),"structure")
# checks
def bb(s):b=s.BoundingBox();return [b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax]
def ov(a,b):return all(min(a[k+3],b[k+3])-max(a[k],b[k])>1e-6 for k in range(3))
PB={n:bb(s) for n,s in parts.items()};CB={n:bb(s) for n,s in cores.items()}
clash=[]
for n,s in parts.items():
    for m,c in cores.items():
        if ov(PB[n],CB[m]):
            v=s.intersect(c).Volume()
            if v>1e-3:clash.append([n,m,round(v,2)])
def mind(n,prefix):
    cand=sorted((m for m in cores if m.startswith(prefix)),key=lambda m:sum(max(0,max(PB[n][k],CB[m][k])-min(PB[n][k+3],CB[m][k+3]))**2 for k in range(3)))[:8]
    return round(min(cq.Shape.distance(parts[n],cores[m]) for m in cand),2)
clear={n:mind(n,n[0]+"_") for n in parts if n[0] in "AB" and any(k in n for k in ("SLOPE","DAMPER","WATER","STAND"))}
env=dict(x=[round(xmin,1),round(xmax,1)],y=[ymin,ymax],z=[zmin,round(zmax,1)])
dims={k:round(v[1]-v[0],1) for k,v in env.items()}
Q=4870/3600
allb=[bb(x) for x in parts.values()]
over=dict(x=[round(min(b[0] for b in allb),1),round(max(b[3] for b in allb),1)],z=[round(min(b[2] for b in allb),1),round(max(b[5] for b in allb),1)])
res=dict(D_mouth_mm=D,bed_pitch_mm=PITCH,active_face_Z=[ZB,ZT],envelope_mm=env,dimensions_mm=dims,
  damper_layout="corner: top P-in on front slope + R-out on roof; bottom P-out on floor + R-in on rear slope",
  damper_dihedral_deg=round(90-math.degrees(math.atan(D/H)),1),overall_incl_damper_bodies_mm=over,
  damper_to_damper_min_mm={b:round(cq.Shape.distance(parts[b+"_FP_DAMPER_RESERVE"],parts[b+"_FR_DAMPER_RESERVE"]),2) for b in beds},
  slope_from_vertical_deg=round(math.degrees(math.atan(D/H)),1),
  mouth_velocity_process_ms=round(Q/(W/1e3*D/1e3),2),mouth_velocity_regen_2435_ms=round(Q/2/(W/1e3*D/1e3),2),
  core_clashes_above_0p001_mm3=clash,min_clearance_to_core_mm=clear,
  scope="Concept skeleton: plenum walls as single sheets, dampers and water bay as reserve boxes; no seals, frame or fans.")
a=cq.Assembly(name="CUBE_ZFLOW_CONCEPT")
for n,s in parts.items():a.add(s,name=n)
if WRITE_STEP:
    for n,s in cores.items():a.add(s,name=n)
a.export(str(out/("CUBE_CONCEPT_WITH_CORES.step" if WRITE_STEP else "CUBE_CONCEPT_SKELETON.step")))
json.dump(res,open(out/"cube_concept.json","w"),indent=1);print(json.dumps({k:v for k,v in res.items() if k!='min_clearance_to_core_mm'},indent=1));print(clear)
