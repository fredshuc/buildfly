"""D03 four-core C08 installation. Machine coordinates in mm, angles about global +Y."""
from geometry import *
from read_selector import prepare
import math
from itertools import product
from OCP.BRepAdaptor import BRepAdaptor_Surface

IDS=[(bed,level) for bed in "AB" for level in ("LOWER","UPPER")]
def axis(level):
    return (610.,342.) if level=="LOWER" else (-500.,1385.)
def rotate(s,level,deg):
    x,z=axis(level)
    return s.rotate((x,0,z),(x,1,z),deg) if deg else s
def block(x0,x1,y0,y1,z0,z1):
    return cq.Solid.makeBox(x1-x0,y1-y0,z1-z0,cq.Vector(x0,y0,z0))
def ycyl(x,z,lo,hi,r):
    return cq.Solid.makeCylinder(r,hi-lo,cq.Vector(x,lo,z),cq.Vector(0,1,0))
def zcyl(x,y,z1,z2,r):
    return cq.Solid.makeCylinder(r,z2-z1,cq.Vector(x,y,z1))
def hex_nut_y(x,z,y0,y1,af,bore):
    poly=cq.Wire.makePolygon([cq.Vector(x+af/math.sqrt(3)*math.cos(i*math.pi/3),y0,
          z+af/math.sqrt(3)*math.sin(i*math.pi/3)) for i in range(6)],close=True)
    return cq.Solid.extrudeLinear(poly,[],cq.Vector(0,y1-y0,0)).cut(ycyl(x,z,y0-1,y1+1,bore))
def source_parts():
    prepare()
    folder=WORK/"selector"; data=json.loads((folder/"index.json").read_text())
    sets={}
    for bed,level in IDS:
        name=bed+"_"+level
        sets[name]={n:cq.Shape.importBrep(str(folder/f)).translate((110 if level=="LOWER" else 0,0,0))
                    for n,(f,b,g) in data["rows"].items() if name in n}
    return sets

def motion(n):
    return any(n.startswith(t) for t in ("DAMPER_BLADE_","DAMPER_ROOT_SLEEVE_","DAMPER_SHAFT_",
               "DAMPER_ROOT_PIN_","D03_COUPLING_","D03_ACT_OUTPUT_","D03_STOP_ARM_"))

def manufacture_interfaces(bed,level,parts):
    x,z=axis(level);sgn=-1 if bed=="A" else 1;side=bed+"_"+level
    def ref(prefix):
        k=next(k for k in parts if k.startswith(prefix))
        return bb(parts.pop(k))
    # Preserve the parent's actual purchasing envelopes. Shaft, pin and frame
    # members are imported solids. OEM internals remain supplier-controlled.
    for end in ("INNER","OUTER"):
        b=ref("REF_"+end+"_BEARING")
        parts["D03_"+end+"_BEARING_INTERFACE_"+side]=ycyl(x,z,b[1],b[4],27.5).cut(ycyl(x,z,b[1]-1,b[4]+1,15.))
        if end=="INNER":
            receiver=next(k for k in parts if k.startswith("M203_INNER_FLANGE"))
            parts[receiver]=parts[receiver].cut(ycyl(x,z,b[1]-.1,b[4]+.1,27.6))
    cb=ref("REF_AIR_DIRECT_COUPLING"); ab=ref("REF_AIR_LOCAL_ACTUATOR")
    near=cb[4] if sgn==-1 else cb[1]
    far=cb[1] if sgn==-1 else cb[4]
    shaft_end=near
    if level=="LOWER":
        # Move the OUTER bearing off the seal and onto an actual dry-side
        # carrier. The old ring becomes a static shaft-seal carrier only.
        key="D03_OUTER_BEARING_INTERFACE_"+side
        parts["D03_SEAL_BACKING_"+side]=parts.pop(key)
        def ys(a,b):return sorted((sgn*a,sgn*b))
        lo,hi=ys(862,876)
        parts[key]=ycyl(x,z,lo,hi,27.5).cut(ycyl(x,z,lo-1,hi+1,15))
        carrier=block(x-52,x+52,lo,hi,z-40,z+40).cut(ycyl(x,z,lo-1,hi+1,27.5))
        # Integral axial shoulder on motor-facing side; wet-side retainer ring.
        c,d=ys(876,878)
        carrier=carrier.fuse(ycyl(x,z,c,d,31).cut(ycyl(x,z,c-1,d+1,24)))
        c,d=ys(860,862)
        ret=ycyl(x,z,c,d,36).cut(ycyl(x,z,c-1,d+1,24))
        for i in range(3):
            px=x+32*math.cos(i*2*math.pi/3);pz=z+32*math.sin(i*2*math.pi/3)
            a,b=ys(859,873);ret=ret.cut(ycyl(px,pz,a,b,2.2));carrier=carrier.cut(ycyl(px,pz,a,b,2))
            a,b=ys(860,871);c,d=ys(857,860)
            parts[f"D03_RETAINER_M4_{side}_{i}"]=ycyl(px,pz,a,b,2).fuse(ycyl(px,pz,c,d,3.5))
        for n in list(parts):
            if n.startswith(("M203_ACT_SPACERS","M203_ACT_M6")):del parts[n]
        for i,(dx,dz) in enumerate(product((-40,40),(-20,20))):
            px,pz=x+dx,z+dz
            carrier=carrier.cut(ycyl(px,pz,lo-1,hi+1,3.3))
            for j,(v,w) in enumerate(((853,862),(876,904))):
                a,b=ys(v,w)
                parts[f"D03_CARRIER_SPACER_{side}_{i}_{j}"]=ycyl(px,pz,a,b,7).cut(ycyl(px,pz,a-1,b+1,3.3))
            a,b=ys(853,918)
            parts[f"D03_DRIVE_STUD_{side}_{i}"]=ycyl(px,pz,a,b,3)
            a,b=ys(909,910)
            parts[f"D03_DRIVE_WASHER_{side}_{i}"]=ycyl(px,pz,a,b,6).cut(ycyl(px,pz,a-1,b+1,3.2))
            a,b=ys(910,915)
            parts[f"D03_DRIVE_NUT_{side}_{i}"]=hex_nut_y(px,pz,a,b,10,3)
        parts["D03_BEARING_CARRIER_"+side]=carrier
        parts["D03_BEARING_RETAINER_"+side]=ret
        # A positive bearing seat transfers actuator gravity at mid-body.
        # Machined cartridge on RHS; OEM must approve the housing bearing area.
        a,b=ys(946,974)
        saddle=block(x-20,x+20,a,b,z-63,z-48).cut(ycyl(x,z,a-1,b+1,55))
        parts["D03_WEIGHT_SADDLE_"+side]=saddle
        a,b=ys(862,982)
        arm=block(x-20,x+20,a,b,z-83,z-63).cut(block(x-17,x+17,a-1,b+1,z-80,z-66))
        parts["D03_WEIGHT_ARM_"+side]=arm
        a,b=ys(862,876)
        parts["D03_WEIGHT_WEB_"+side]=block(x-20,x+20,a,b,z-63,z-40)
        near,far=sgn*883,sgn*904
        cb[1],cb[4]=ys(883,904);ab[1],ab[4]=ys(904,1014)
    def dshaft(u,v):
        y0,y1=sorted((u,v))
        return ycyl(x,z,y0,y1,12).cut(block(x+9,x+14,y0-1,y1+1,z-13,z+13))
    stub=dshaft(sgn*879 if level=="LOWER" else near,near+sgn*10)
    shaft=next(n for n in parts if n.startswith("DAMPER_SHAFT"))
    if level=="LOWER":
        stub=stub.fuse(ycyl(x,z,*sorted((shaft_end,sgn*879)),15))
        a,b=ys(879.5,882.5)
        arm=ycyl(x,z,a,b,17).fuse(block(x-3,x+3,a,b,z-32,z-14))
        parts["D03_STOP_ARM_"+side]=arm.cut(dshaft(a-1,b+1)).clean()
        for i,(angle,tangent) in enumerate(((0.,6.),(77.701928604,-6.))):
            c,s=math.cos(math.radians(angle)),math.sin(math.radians(angle))
            px=x+c*tangent-s*30;pz=z-s*tangent-c*30
            a,b=ys(870,883.5)
            pin=ycyl(px,pz,a,b,3)
            ck="D03_BEARING_CARRIER_"+side
            parts[ck]=parts[ck].cut(pin)
            parts[f"D03_STOP_PIN_{side}_{i}"]=pin
    parts[shaft]=parts[shaft].fuse(stub).clean()
    parts["D03_ACT_OUTPUT_"+side]=dshaft(far,far-sgn*10)
    lo,hi=sorted((near,far-sgn*1.))
    parts["D03_COUPLING_"+side]=ycyl(x,z,lo,hi,20).cut(dshaft(lo-1,hi+1))
    # Closed occupied equipment envelope at the registered supplier datum,
    # including the actual four mounting clearances and head recesses.
    lo,hi=ab[1],ab[4]
    housing=ycyl(x,z,lo,hi,55)
    for dx,dz in product((-40,40),(-20,20)):
        housing=housing.cut(ycyl(x+dx,z+dz,lo-1,hi+1,3.5))
        a,b=sorted((far+sgn*5, far+sgn*(hi-lo+1)))
        housing=housing.cut(ycyl(x+dx,z+dz,a,b,9))
    parts["D03_ACTUATOR_INTERFACE_"+side]=housing
    # A removable feedback hood over the original outboard shaft flag. Its open
    # mouth faces away from the extraction direction. Two tapped blocks are
    # welded to the inside of the existing actuator bracket.
    flag=bb(next(s for n,s in parts.items() if n.startswith("DAMPER_BLADE") and n.endswith("_3_O")))
    lift=1 if level=="LOWER" else -1
    outer=839.5*sgn
    inner=flag[4]+3 if sgn==-1 else flag[1]-3
    ya,yb=sorted((outer,inner))
    def zz(a,b):return sorted((z+lift*a,z+lift*b))
    hood=block(x-49,x+49,ya,yb,*zz(49,51))
    for dx in (-49,47):
        hood=hood.fuse(block(x+dx,x+dx+2,ya,yb,*zz(-18,49)))
    # Open-side U-slot clears both the shaft and its end gland while lifting.
    flag_out=flag[1] if sgn<0 else flag[4]
    a,b=sorted((flag_out+sgn*2,flag_out+sgn*4))
    cap=block(x-47,x+47,a,b,*zz(-18,49)).cut(ycyl(x,z,a-1,b+1,35),
              block(x-35,x+35,a-1,b+1,*zz(-20,0)))
    # Open-ended notches slide past the stationary cover lugs on withdrawal.
    for dx in (-22,22):
        cap=cap.cut(block(x+dx-5.5,x+dx+5.5,a-1,b+1,*zz(-19,49)))
    hood=hood.fuse(cap).clean()
    yy=outer-sgn*4
    for i,dx in enumerate((-22,22)):
        a,b=sorted((outer,outer-sgn*9))
        zp=zz(41,49); hole=zcyl(x+dx,yy,z-60,z+60,2)
        lug=block(x+dx-5,x+dx+5,a,b,*zp)
        # Rear-mount ear on the inboard surface of the split-blank backer.
        # It stands clear of the travelling hood and reaches the solid side land.
        lug=lug.cut(hole).clean()
        parts[f"D03_GUARD_LUG_{side}_{i}"]=lug
        hood=hood.cut(zcyl(x+dx,yy,z-60,z+60,2.25))
        stem=zcyl(x+dx,yy,*zz(42,51),2)
        head=zcyl(x+dx,yy,*zz(51,54),3.5)
        parts[f"D03_GUARD_M4_{side}_{i}"]=stem.fuse(head)
    # Common +X anchor avoids the upper front corner post at X=-560.
    a,b=sorted((sgn*843.5,sgn*845.5))
    bridge=block(x-27,x+83,a,b,*zz(39,51))
    a,b=sorted((outer,sgn*843.5))
    for dx in (-22,22):
        bridge=bridge.fuse(block(x+dx-5,x+dx+5,a,b,*zz(41,49)))
    parts["D03_GUARD_BRIDGE_"+side]=bridge.clean()
    parts["D03_FEEDBACK_HOOD_"+side]=hood
    return sgn,lift

def end_angle(parts):
    name=next(n for n in parts if n.startswith("DAMPER_BLADE") and n.endswith("_0_O"))
    s=parts[name]
    edges=[e for e in s.Edges() if 190<e.Length()<215]
    assert len(edges)>=2
    a,b=[v.Center() for v in edges[0].Vertices()]
    return 90.-math.degrees(math.atan2(abs(a.z-b.z),abs(a.x-b.x)))

def export(path,groups):
    a=cq.Assembly(name=path.stem)
    for group,(parts,color) in groups.items():
        sub=cq.Assembly(name=group)
        for n,s in parts.items():sub.add(s,name=n,color=cq.Color(*color))
        a.add(sub)
    a.export(str(path))
    read=list(leaves(path))
    expected={n:s for parts,_ in groups.values() for n,s in parts.items()}
    assert len(read)==len(expected)
    for key,s in read:
        n=next(t for t in reversed(key.split("/")) if t in expected)
        assert s.isValid() and len(s.Solids())==len(expected[n].Solids()),n
        assert max(abs(a-b) for a,b in zip(bb(s),bb(expected[n])))<.001,n
        assert abs(s.Volume()-expected[n].Volume())<max(.01,expected[n].Volume()*1e-8),n
    return len(read)

def rail_fix(bed,parts,host):
    sign=-1 if bed=="A" else 1
    name=f"F_DAMPER_RAIL_{sign*825}_O";rail=host[name];y=sign*833.5
    for i,x in enumerate((575.,645.)):
        rail=rail.cut(zcyl(x,y,229,311,4.5),zcyl(x,y,229,233.01,7.1))
        # Sleeve installs from below the drilled RHS; its top seats on the
        # underside of the top wall and its lower end is flush with the tube.
        parts[f"D03_CRUSH_TUBE_{bed}_{i}"]=zcyl(x,y,230,307,7).cut(zcyl(x,y,229,308,4.3))
        parts[f"D03_BASE_M8_{bed}_{i}"]=zcyl(x,y,219,314.5,4).fuse(
            cq.Workplane("XY",origin=(x,y,314.5)).polygon(6,15.0111).extrude(5.3).val())
        for j,(za,zb,r) in enumerate(((313,314.5,8),(228.5,230,10))):
            parts[f"D03_BASE_WASHER_{bed}_{i}_{j}"]=zcyl(x,y,za,zb,r).cut(zcyl(x,y,za-1,zb+1,4.2))
        parts[f"D03_BASE_NUT_{bed}_{i}"]=cq.Workplane("XY",origin=(x,y,222)).polygon(6,15.0111).extrude(6.5).val().cut(zcyl(x,y,221,230,4))
    host[name]=rail

def assembly():
    selectors=source_parts()
    angle=end_angle(selectors["A_LOWER"])
    for bed,level in IDS:
        key=bed+"_"+level
        parts=selectors[key]
        # Historical S1 has A on the slope and B vertical. Normalise ALL
        # rotor members to the process position before applying a common angle.
        assert abs(end_angle(parts)-(angle if bed=="A" else 0))<1e-5
        if bed=="B":
            for n in parts:
                if motion(n):parts[n]=rotate(parts[n],level,-angle)
        if level=="UPPER":
            # Only the outer 50 mm strips reach an HX post during the stroke.
            # Keep the upper hinge, both seats and the middle 550 mm of tip.
            blade=next(n for n in parts if n.startswith("DAMPER_BLADE") and n.endswith("_0_O"))
            s=parts[blade];b=bb(s);cx,cz=axis(level)
            for ya,yb in ((b[1]-1,b[1]+50),(b[4]-50,b[4]+1)):
                cut=block(216,260,ya,yb,-10,10).rotate((0,0,0),(0,1,0),90-angle).translate((cx,0,cz))
                s=s.cut(cut)
            parts[blade]=s.clean()
        sgn,lift=manufacture_interfaces(bed,level,parts)
        flag=next(s for n,s in parts.items() if n.startswith("DAMPER_BLADE") and n.endswith("_4_O"))
        fx=flag.Center()
        x,z=axis(level); radius=math.hypot(fx.x-x,fx.z-z)
        outerface=(bb(flag)[1] if sgn<0 else bb(flag)[4])
        for mode,theta in (("P",0.),("R",angle)):
            c,s=math.cos(math.radians(theta)),math.sin(math.radians(theta))
            dx,dz=(fx.x-x)*37/radius,(fx.z-z)*37/radius
            px,pz=x+c*dx+s*dz,z-s*dx+c*dz
            lo,hi=sorted((outerface+sgn*1.5,outerface+sgn*7))
            probe=ycyl(px,pz,lo,hi,3)
            guard="D03_FEEDBACK_HOOD_"+key
            parts[guard]=parts[guard].cut(ycyl(px,pz,lo-1,hi+1,3.15))
            parts["D03_"+mode+"_LIMIT_SENSOR_"+key]=probe
    return selectors
