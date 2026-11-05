"""Independent RT3 checks on the delivered C07 model (mm).
Usage: python c07_checks.py <repo root with C07 inputs prepared> <delivered C07_SHELL.step> <out.json>
Uses the C07 module readers only for file access and the published service-state transforms.
Reports: (1) hard-stop and gasket edge margins on the HX lands, per face;
(2) the locating chain between carrier and HX (what positions the carrier);
(3) clearances around the moving core in the released service state (transfer-rail tolerance);
(4) perforated-plate ligaments and the guide inclination at the C07 plate plane;
(5) end-diagonal and centre-brace buckling screens and installed height on the plinth."""
import sys,json,math
from pathlib import Path
root,shellstep,outp=Path(sys.argv[1]),sys.argv[2],sys.argv[3]
C07=root/"AirTransformerShell/revisions/C07";sys.path.insert(0,str(C07));sys.path.insert(0,str(root/"AirTransformerShell/revisions/C04"))
import cadquery as cq
from cad_io import named,bb
from build_c07 import face_shape,ring,bellows
from integrate_c07 import installed_cores
import design
from network import diam
shell=named(shellstep);core=installed_cores()
print('shell',len(shell),'core',len(core),flush=True)
R={}
def gap(a,b):return math.sqrt(sum(max(0,max(a[k],b[k])-min(a[k+3],b[k+3]))**2 for k in range(3)))
# (1) stops and gasket on lands. Lands = HX frame plates 8 mm thick at the face (X 265-273 front, 477-485 rear).
faces={"AF":(265,-1,"A"),"AR":(485,1,"A"),"BF":(265,-1,"B"),"BR":(485,1,"B")}
marg={}
for f,(datum,sgn,bed) in faces.items():
    lands=[(n,bb(s)) for n,s in core.items() if n.startswith(bed+"_") and round(bb(s)[3]-bb(s)[0],3)==8 and abs((bb(s)[0] if sgn<0 else bb(s)[3])-datum)<1e-3]
    # rectangles in Y-Z of land members at this face
    rects=[(b[1],b[2],b[4],b[5]) for n,b in lands]
    car=shell[f+"_CLAMP_CARRIER"]
    # stop pads: carrier faces lying in the HX face plane
    pads=[]
    for fc in car.Faces():
        b=bb(fc)
        if abs(b[0]-datum)<1e-4 and abs(b[3]-datum)<1e-4:pads.append((b[1],b[2],b[4],b[5]))
    def margin(p):
        # minimum distance from pad rectangle edge to the boundary of the land rectangle that contains it
        best=None
        for r in rects:
            if p[0]>=r[0]-1e-6 and p[1]>=r[1]-1e-6 and p[2]<=r[2]+1e-6 and p[3]<=r[3]+1e-6:
                m=min(p[0]-r[0],p[1]-r[1],r[2]-p[2],r[3]-p[3]);best=m if best is None else max(best,m)
        return best
    g=bb(shell[f+"_FACE_GASKET"])
    gin=(g[1]+11,g[2]+12,g[4]-11,g[5]-12)
    pm=[margin(p) for p in pads]
    # gap from each stop to the gasket outer boundary (in plane)
    def to_gasket(p):
        dy=max(g[1]-p[2],p[0]-g[4],0);dz=max(g[2]-p[3],p[1]-g[5],0)
        inside=p[0]>=g[1] and p[2]<=g[4] and p[1]>=g[2] and p[3]<=g[5]
        if inside:  # pad lies within outer gasket bbox -> distance to gasket band from inside the ring is irrelevant
            return None
        return round(math.hypot(dy,dz),3)
    marg[f]=dict(n_stop_faces=len(pads),stop_min_land_edge_margin_mm=round(min(m for m in pm if m is not None),3),
        stops_not_fully_on_a_land=sum(m is None for m in pm),
        stop_min_gap_to_gasket_mm=round(min(x for x in (to_gasket(p) for p in pads) if x is not None),3),
        gasket_bbox_YZ=[round(v,2) for v in (g[1],g[2],g[4],g[5])],
        land_rects_YZ=[[round(v,2) for v in r] for r in rects])
R['stops_and_gasket']=marg
# (2) locating chain: which parts constrain the AF carrier in Y/Z
car=shell["AF_CLAMP_CARRIER"];cb=bb(car)
touch=[]
for n,s in list(shell.items())+[(k,v) for k,v in core.items() if k.startswith("A_")]:
    if n=="AF_CLAMP_CARRIER":continue
    b=bb(s)
    if gap(b,cb)>1.0:continue
    d=cq.Shape.distance(car,s)
    if d<1.0:touch.append([n,round(d,3)])
R['AF_carrier_neighbours_within_1mm']=sorted(touch,key=lambda x:x[1])
# hole clearances: tie rods (OD8) and park guide studs in carrier bores
R['locating_clearances_mm']=dict(tie_rod_OD=8,carrier_tie_bore=9.2,park_stud_OD=8,park_bore=9.3,
  note='Carrier is located only by tie rods and park studs (cassette-mounted); neither engages the HX.')
# (3) service state for bed A (published transforms), clearances around the moving core
svc=dict(shell)
for face,datum,sgn in (("F",265,-1),("R",485,1)):
    p="A"+face+"_"
    svc[p+"CLAMP_CARRIER"]=shell[p+"CLAMP_CARRIER"].translate((6*sgn,0,0))
    svc[p+"EPDM_DIAPHRAGM"]=face_shape(bellows(6),datum,-434.4,sgn)
    svc[p+"FACE_GASKET"]=face_shape(ring(4.2,644,1032,622,1008,6),datum,-434.4,sgn)
for n in list(svc):
    if n.startswith("A_TIE_") and not n.startswith(("A_TIE_NUT","A_TIE_WASHER")) and int(n.rsplit("_",1)[1]) not in (8,10,12):
        svc[n]=svc[n].translate((-280,0,0))
removed=[n for n in svc if n.startswith("A") and any(t in n for t in ("_PANEL_UPPER","_PANEL_LAP","_SIDE_BRACE","_TOP_FORK_","_X_PIN_","_DP_LANCE_","_HX_HOSE_TAIL","_HX_HOSE_COLLAR","_TIE_NUT_","_TIE_WASHER_"))]
for n in removed:del svc[n]
mov={n:s for n,s in core.items() if n.startswith("A_")}
mb={n:bb(s) for n,s in mov.items()};env=[min(b[k] for b in mb.values()) if k<3 else max(b[k] for b in mb.values()) for k in range(6)]
cl=[]
for n,s in svc.items():
    b=bb(s)
    # only parts whose Y range overlaps the core's swept Y range (toward -Y by 900)
    if b[4]<env[1]-900 or b[1]>env[4]:continue
    if gap([b[0],env[1],b[2],b[3],env[4],b[5]],[env[0],env[1],env[2],env[3],env[4],env[5]])>30:continue
    # X/Z clearance in the projection normal to the sweep: distance between X-Z rectangles of nearest core parts
    best=None
    for m,c in mb.items():
        dx=max(c[0]-b[3],b[0]-c[3],0);dz=max(c[2]-b[5],b[2]-c[5],0)
        if dx==0 and dz==0:
            continue
        d=math.hypot(dx,dz)
        if best is None or d<best[0]:best=(d,m,'X' if dx>dz else 'Z')
    if best and best[0]<12:cl.append([n,round(best[0],2),best[2]])
cl=sorted(cl,key=lambda x:x[1])
R['A_service_XZ_projection_clearance_lt_12mm']=cl
import collections
grp=collections.OrderedDict()
for n,d,ax in cl:
    k=(d,ax,''.join(c for c in n.split('_',1)[1] if not c.isdigit()).strip('_()., -'))
    grp.setdefault(k,[]).append(n)
R['A_service_clearance_classes']=[dict(clearance_mm=k[0],axis=k[1],part_type=k[2],count=len(v)) for k,v in grp.items()]
# park-guide stud tips relative to the HX face plane
tips={}
for f,(datum,sgn,bed) in faces.items():
    for k in range(4):
        b=bb(shell[f+"_PARK_GUIDE_"+str(k)])
        tips[f+"_PARK_GUIDE_"+str(k)]=round((datum-b[3]) if sgn<0 else (b[0]-datum),3)
R['park_guide_tip_to_HX_face_plane_mm']=tips
# (4) plate plane
def slope_at(u,i=4):
    pts=design.guide(i)
    for (u0,z0),(u1,z1) in zip(pts,pts[1:]):
        if u0<=u<=u1:return math.degrees(math.atan2(abs(z1-z0),u1-u0))
R['plate_plane']=dict(C04_plate_u_mm=12.75,C07_plate_u_mm=40.0,land_end_u=design.LAND,blend_end_u=design.LAND+design.BLEND,
  guide_inclination_from_horizontal_deg_at_u40=round(slope_at(40),1),at_u12=round(slope_at(12),1),
  plate_to_fin_mm=dict(C04=12+31.65,C07=40+31.65),
  hole_pitch_YZ_mm=[25,21],diameters_mm=list(map(float,diam)),z_ligament_mm=[round(21-float(d),2) for d in diam],y_ligament_mm=[round(25-float(d),2) for d in diam],
  sheet_mm=1.5)
# (5) structure screens
E=200e3
def euler(b,h,L):
    I=b*h**3/12;return round(math.pi**2*E*I/L**2/1e3,2)
ed=bb(shell["END_DIAGONAL_F"]);L=math.hypot(2040,1250)
cb2=bb(shell["SERVICE_CENTRE_BRACE"]);Lc=math.hypot(446,2364)
R['bracing']=dict(end_diagonal=dict(section_mm=[12,40],length_mm=round(L),euler_kN_weak_axis_pinned=euler(40,12,L),bbox=[round(v,1) for v in ed]),
  centre_brace=dict(section_mm=[16,38],length_mm=round(Lc),euler_kN_weak_axis_pinned=euler(38,16,Lc)),
  end_diagonals_direction={"F":"rises toward +Y","R":"rises toward -Y"})
pl=[bb(s) for n,s in shell.items() if n.startswith("PLINTH_")]
R['installed_height']=dict(plinth_count=len(pl),plinth_bottom_z=min(b[2] for b in pl),roof_top_z=max(bb(s)[5] for s in shell.values()),
  height_above_floor_mm=round(max(bb(s)[5] for s in shell.values())-min(b[2] for b in pl),1))
json.dump(R,open(outp,'w'),indent=1);print(json.dumps(R,indent=1)[:7000])
