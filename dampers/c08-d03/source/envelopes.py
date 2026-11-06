from selector import *
import numpy as np
from scipy.spatial import ConvexHull

def sweep(shape,name,level,angle,split=True):
    x,z=axis(level);b=bb(shape)
    if split and level=="UPPER" and name.startswith("DAMPER_BLADE") and name.endswith("_0_O"):
        cuts=[b[1],b[1]+50,b[4]-50,b[4]]
        solids=[]
        for lo,hi in zip(cuts,cuts[1:]):
            piece=shape.intersect(block(b[0]-1,b[3]+1,lo,hi,b[2]-1,b[5]+1))
            solids.extend(sweep(piece,name,level,angle,False).Solids())
        return cq.Compound.makeCompound(solids)
    arm=name.startswith("D03_STOP_ARM")
    if (not name.startswith("DAMPER_BLADE") and not arm) or name.endswith("_3_O"):
        radius={"DAMPER_ROOT_PIN":16.65,"DAMPER_SHAFT":15.,"DAMPER_ROOT_SLEEVE":16.5,
                "D03_COUPLING":20.,"D03_ACT_OUTPUT":12.}.get(next((k for k in
                   ("DAMPER_ROOT_PIN","DAMPER_SHAFT","DAMPER_ROOT_SLEEVE","D03_COUPLING","D03_ACT_OUTPUT") if name.startswith(k)),""),16.5)
        # Pins may be skew cylinders. Bound them by every extrema corner;
        # the circular shaft/sleeve/hub sizes are from the source cylinders.
        if name.startswith("DAMPER_ROOT_PIN"):
            radius=max(math.hypot(a-x,v-z) for a,v in product((b[0],b[3]),(b[2],b[5])))
        return ycyl(x,z,b[1],b[4],radius)
    polygon=np.array(list(product((-3.,3.),(-32.,-14.)))) if arm else np.array([[v.Center().x-x,v.Center().z-z] for v in shape.Vertices()])
    radius=max(np.linalg.norm(polygon,axis=1))
    slices=[ycyl(x,z,b[1],b[4],17)] if arm else []
    for a,c in zip(np.linspace(0,angle,17)[:-1],np.linspace(0,angle,17)[1:]):
        pts=[]
        pad=radius*(1-math.cos(math.radians(c-a)/2))+1e-5
        for deg in (a,c):
            co,si=math.cos(math.radians(deg)),math.sin(math.radians(deg))
            rotated=polygon@np.array([[co,-si],[si,co]])
            for off in product((-pad,pad),repeat=2):pts.extend(rotated+off)
        pts=np.array(pts);h=ConvexHull(pts)
        w=cq.Wire.makePolygon([cq.Vector(x+pts[i,0],b[1],z+pts[i,1]) for i in h.vertices],close=True)
        slices.append(cq.Solid.extrudeLinear(w,[],cq.Vector(0,b[4]-b[1],0)))
    return cq.Compound.makeCompound(slices)

def services(parts,bed,level):
    side=bed+"_"+level;sgn=-1 if bed=="A" else 1; lift=1 if level=="LOWER" else -1
    x,z=axis(level)
    housing=parts["D03_ACTUATOR_INTERFACE_"+side]
    a=bb(housing);far=a[1] if sgn<0 else a[4]
    near=a[4] if sgn<0 else a[1]
    # Withdraw housing and output spindle together. The translating cylinder
    # is conservative beyond the engaged shaft; retain actual tool bores.
    lo,hi=sorted((near,far+sgn*130))
    swept_body=ycyl(x,z,lo,hi,55)
    for dx,dz in product((-40,40),(-20,20)):
        swept_body=swept_body.cut(ycyl(x+dx,z+dz,lo-1,hi+1,3.5))
    # Only the spindle leaves the housing on the inboard side.
    lo,hi=sorted((near,near-sgn*10))
    nose=ycyl(x,z,lo,hi,12).cut(block(x+9,x+14,lo-1,hi+1,z-13,z+13))
    envelopes={"ACT_PULL_"+side:swept_body.fuse(nose).clean()}
    hood=parts["D03_FEEDBACK_HOOD_"+side]
    hb=bb(hood);za,zb=sorted((z+lift*51,z+lift*141))
    # The hood is open on its trailing edge. Its side walls and U-slot
    # occupy a subset of the original hood below the leading cap. Fill the
    # small mounting bores in the swept region to be conservative.
    crown=block(hb[0],hb[3],hb[1],hb[4],za,zb)
    full=hood.fuse(crown)
    for i,dx in enumerate((-22,22)):
        za,zb=sorted((z+lift*49,z+lift*51))
        full=full.fuse(zcyl(x+dx,sgn*835.5,za,zb,2.25))
    probe_boxes=[]
    for n,s in parts.items():
        if "_LIMIT_SENSOR_" not in n:continue
        b=bb(s)
        probe_boxes.append(block(b[0]-.16,b[3]+.16,b[1],b[4],min(b[2],b[2]+lift*90)-.16,max(b[5],b[5]+lift*90)+.16))
    envelopes["HOOD_PULL_"+side]=cq.Compound.makeCompound([full.clean(),*probe_boxes])
    for i,(dx,dz) in enumerate(product((-40,40),(-20,20))):
        # AF10 thin-wall socket OD16 on a straight extension, enters through
        # the reserved OD18 well. Test one tool at a time.
        lo,hi=sorted((near+sgn*5,far+sgn*65))
        envelopes[f"ACT_SOCKET_{side}_{i}"]=ycyl(x+dx,z+dz,lo,hi,8)
    for i,dx in enumerate((-22,22)):
        lo,hi=sorted((z+lift*54,z+lift*109))
        envelopes[f"HOOD_DRIVER_{side}_{i}"]=zcyl(x+dx,sgn*835.5,lo,hi,4)
    if level=="LOWER":
        for i,xx in enumerate((575.,645.)):
            envelopes[f"BASE_SOCKET_{side}_{i}"]=zcyl(xx,sgn*833.5,175,222,9)
    return envelopes
