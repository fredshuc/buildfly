"""C07 shell. Run with CadQuery 2.8 from the repository layout, in mm.
Unchanged named shapes come from the released C06 STEP. Owner modules remain separate.
"""
from pathlib import Path
import csv, math, json, sys
import cadquery as cq
from cad_io import named, bb, clashes

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
C06=HERE.parent/"C06"
D02=ROOT/"dampers"/"c06-d02"
sys.path.insert(0,str(HERE.parent/"C04"))
from design import guide, Z0, BAND, T
from network import diam
from itertools import pairwise
V=cq.Vector
def box(x,y,z,dx,dy,dz):
    return cq.Solid.makeBox(dx,dy,dz,V(x,y,z))
def cyl(point,axis,r,length):
    return cq.Solid.makeCylinder(r,length,V(*point),V(*axis))
def xhole(u,y,z,r,length):
    return cyl((u,y,z),(1,0,0),r,length)
def zhole(x,y,z,r,length):
    return cyl((x,y,z),(0,0,1),r,length)
def yhole(x,y,z,r,length):
    return cyl((x,y,z),(0,1,0),r,length)
def ring(u,width,height,iw,ih,depth):
    return box(u,-width/2,1704-height/2,depth,width,height).cut(
        box(u-1,-iw/2,1704-ih/2,depth+2,iw,ih))
def wire(u,w,h):
    return cq.Wire.makePolygon([V(u,y,1704+z) for y,z in
        [(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]],close=True)
def bellows(stroke):
    # Bonded closed rectangular convolution. Keep the two end beads at their
    # metal lands in both installed and released representations.
    stations=[(6.2+stroke,637,1029),(9.2+stroke*.8,637,1029),
              (15.5+stroke*.55,645,1032),(22+stroke*.25,632,1024),(25.5,632,1024)]
    if stroke:
        # A collapsing fold develops toward the duct, away from the moving
        # rail. Preserve both straight-side meridian lengths at every stroke.
        neutral=[(6.2,637,1029),(9.2,637,1029),(15.5,645,1032),(22,632,1024),(25.5,632,1024)]
        def meridian(points,axis):
            return sum(math.hypot(b[0]-a[0],(b[axis]-a[axis])/2) for a,b in pairwise(points))
        fold=list(stations[3])
        for axis in (1,2):
            goal=meridian(neutral,axis)
            lo,hi=fold[axis]-32,fold[axis]
            for _ in range(42):
                fold[axis]=(lo+hi)/2
                stations[3]=tuple(fold)
                if meridian(stations,axis)>goal: lo=fold[axis]
                else: hi=fold[axis]
            fold[axis]=(lo+hi)/2
            stations[3]=tuple(fold)
    outer=cq.Solid.makeLoft([wire(u,w,h) for u,w,h in stations],True)
    inner=cq.Solid.makeLoft([wire(u,w-2.4,h-2.4) for u,w,h in stations],True)
    membrane=outer.cut(inner)
    # Integral turned-in attachment flanges give both joints a broad bonded
    # face. The collar and lip extend past the entire elastomer footprint.
    moving=ring(6.2+stroke,637,1029,624,1016,1.2)
    fixed=ring(24.3,636,1028,622,1014,1.2)
    return membrane.fuse(moving,fixed).clean()
def face_shape(shape,datum,cy,sign):
    if sign<0: shape=shape.rotate((0,0,0),(0,0,1),180)
    return shape.translate((datum,cy,0))
def xz(poly,y,dy):
    w=cq.Wire.makePolygon([V(x,y,z) for x,z in poly],close=True)
    return cq.Solid.extrudeLinear(w,[],V(0,dy,0))
def yz(poly,x,dx):
    w=cq.Wire.makePolygon([V(x,y,z) for y,z in poly],close=True)
    return cq.Solid.extrudeLinear(w,[],V(dx,0,0))
def pipe(points,ro,ri):
    # Continuous bore through the rounded junctions. All elbows are routing
    # envelopes pending hose supplier bend-radius and bend-loss data.
    def domain(r):
        spans=[]
        for a,b in pairwise(points):
            d=V(*b)-V(*a)
            spans.append(cq.Solid.makeCylinder(r,d.Length,V(*a),d.normalized()))
        spans.extend(cq.Solid.makeSphere(r,V(*p),angleDegrees1=-90) for p in points[1:-1])
        return spans[0] if len(spans)==1 else spans[0].fuse(*spans[1:]).clean()
    return domain(ro).cut(domain(ri))
def poly_face_offset(points,dis):
    import numpy as np
    a=np.array(points); t=np.diff(a,axis=0);t/=np.linalg.norm(t,axis=1)[:,None]
    n=np.c_[-t[:,1],t[:,0]]
    m=(n[:-1]+n[1:])/(1+(n[:-1]*n[1:]).sum(axis=1))[:,None]
    q=a+dis*np.vstack((n[0],m,n[-1]))
    q[-1]+=(1124-q[-1,1])/t[-1,1]*t[-1]
    return [tuple(p) for p in q]
def face_lift(u,i):
    for (u0,z0),(u1,z1) in pairwise(guide(i)):
        if u0<=u<=u1: return z0+(z1-z0)*(u-u0)/(u1-u0)
    raise ValueError(u)
def clip_plate(i):
    # Keep 120 holes and the C04 hole diameter in each replaceable plate.
    z=face_lift(40,i)+62.5
    outline=cq.Wire.makePolygon([V(39.25,y,z+h) for y,h in
        [(-305.8,-56),(305.8,-56),(305.8,56),(-305.8,56)]],close=True)
    holes=[cq.Wire.makeCircle(float(diam[i])/2,V(39.25,(j-11.5)*25,z+(k-2)*21),V(1,0,0))
           for j in range(24) for k in range(5)]
    return cq.Solid.extrudeLinear(outline,holes,V(1.5,0,0))
def keeper(s,i):
    # Two retainer strips on each guide. Radius clearance for the slide is
    # encoded by the 2.3 mm slot around a 1.5 mm plate.
    zlow=face_lift(40,i)
    for u0,u1 in ((37.5,38.85),(41.15,42.5)):
        z1,z2=face_lift(u0,i),face_lift(u1,i)
        for side in (-1,1):
            if (i==0 and side<0) or (i==8 and side>0): continue
            h=zlow+side*10
            # At u42.5 the guide centre is still inside the strip.
            s=s.fuse(xz([(u0,z1),(u1,z2),(u1,h),(u0,h)],-306,612))
    return s.clean()
def metric_hex(u,y,z,af,length,bore):
    rad=af/math.sqrt(3)
    w=cq.Wire.makePolygon([V(u,y+rad*math.cos(k*math.pi/3),z+rad*math.sin(k*math.pi/3))
                            for k in range(6)],close=True)
    return cq.Solid.extrudeLinear(w,[],V(length,0,0)).cut(xhole(u-1,y,z,bore,length+2))

def build():
    parts=named(C06/"C06_SHEET_METAL.step")
    assert len(parts)==327
    with (D02/"evidence/D02_C06_PADS_TO_SUPPRESS.csv").open(encoding="utf-8-sig") as f:
        oldpads=[r["pad"] for r in csv.DictReader(f)]
    assert len(oldpads)==16
    for n in oldpads: del parts[n]
    for n in list(parts):
        if any(t in n for t in ("_TRAY_BAR_","_PAN_PAD_","_HX_TRAY","_ADJ_",
               "_SLIDING_SEAL_CARRIER","_GASKET_6_FREE","_PLATE_ACCESS","_BALANCE_BAND_")):
            del parts[n]
    def add(n,s):
        assert n not in parts,n
        assert len(s.Solids())==1 and s.isValid(),n
        parts[n]=s
    def part(n,s):
        full=bed+"_"+n
        add(full,s)
    def local(n,s):
        add(prefix+n,face_shape(s,datum,cy,sgn))
    tap_rows=[]; drain_rows=[]; clamp_rows=[]
    plate_proto=[clip_plate(i) for i in range(8)]
    for bed,cy,outer in (("A",-434.4,-1),("B",845.6,1)):
        ty=cy-367.775
        # N10: horizontally split skin. Lower drive apertures stay installed.
        panel=parts.pop(bed+"_SIDE_PANEL")
        b=bb(panel)
        part("PANEL_LOWER",panel.intersect(box(-1700,-2000,0,4000,4000,999.5)))
        part("PANEL_UPPER",panel.intersect(box(-1700,-2000,1000.5,4000,4000,1800)))
        yface=b[1] if outer<0 else b[4]
        ylap=yface-3 if outer<0 else yface+1
        # Removable external lap. Compressible strip closes the 1 mm split.
        part("PANEL_LAP",box(b[0],ylap,989,b[3]-b[0],2,22))
        part("PANEL_LAP_SEAL",box(b[0],yface-1 if outer<0 else yface,989,b[3]-b[0],1,22))
        # N9: pins through the actual two existing slotted top lugs.
        for k,y in enumerate((ty+27.35,ty+707.35)):
            for j in range(2):
                n=bed+"_TOP_FORK_"+str((k,j))
                parts[n]=parts[n].cut(yhole(375,y-16,2266,6.25,32))
            part("X_PIN_"+str(k),yhole(375,y-10,2266,6,20).fuse(yhole(375,y-13,2266,9,3)))
        for k,y in enumerate((ty+15,ty+655)):
            # End faces land directly on the 40 mm posts.
            part("RISER_XZ_"+str(k),xz([(315,195),(435,1034),(435,1074),(315,235)],y-14,28))
        # N4/N6. C05 supplies the pan, its tabs and the short spigot.
        # The entire hose-side fitting is removed for extraction.
        x,y=375,cy+238
        part("HX_HOSE_TAIL",pipe([(x,y,1159),(x,y,74)],11,9))
        part("HX_HOSE_COLLAR",zhole(x,y,1154,14,13).cut(zhole(x,y,1153,11,15)))
        parts["FLOOR"]=parts["FLOOR"].cut(zhole(x,y,99,15,8))
        for name,xd,yd in (("HX",375,cy+238),("F",55,cy+285),("R",695,cy+285)):
            # Separate open discharge per trap. The 210 mm plinth keeps the
            # low point above the installation floor. No cross-bed drain path.
            path=[(xd,yd,74),(xd,yd,-151),(xd+66,yd,-151),(xd+66,yd,-43),(xd+103,yd,-43)]
            part(name+"_TRAP",pipe(path,12,9))
            drain_rows.append((bed,name,xd,yd,74,-151,-43,90))
        for face,datum,sgn in (("F",265,-1),("R",485,1)):
            prefix=bed+face+"_"
            side=outer*sgn
            # Rebuild the two cheek and nine guide tips from the controlled C04
            # curves. A continuous 5 mm stand-off remains at the HX lands.
            tip_cut=box(-1,-410,1120,6,820,1150)
            for i in range(9):
                n="GUIDE_%02d"%i
                q=list(guide(i))
                profile=poly_face_offset(q,-.75)+poly_face_offset(q,.75)[::-1]
                del parts[prefix+n]
                local(n,keeper(xz(profile,-306,612).cut(tip_cut),i))
            cheek_pts=poly_face_offset(guide(0),-.75)+poly_face_offset(guide(8),.75)[::-1]
            cover_slots=[]
            for sy,y0 in ((-1,-307.5),(1,306)):
                suffix="CHEEK_-307.5" if sy<0 else "CHEEK_306"
                cheek=xz(cheek_pts,y0,1.5).cut(tip_cut)
                if sy==side:
                    for i in range(8):
                        z=face_lift(40,i)+62.5
                        cover_slots.append(z)
                        cheek=cheek.cut(box(38.5,-311,z-56.5,3,622,113))
                        cheek=cheek.cut(yhole(49,sy*306-5,z,2.1,10))
                else:
                    for i in (2,5):
                        z=Z0+125*i+62.5
                        cheek=cheek.cut(yhole(35,sy*306-5,z,2.15,10))
                        # Static ports face transverse to flow, inside the HX
                        # recess. The short removable lance clears the sliding screen.
                        ys=sy*299
                        gauge=pipe([(-7,ys,z),(35,ys,z),(35,sy*339,z)],2,1)
                        cap=xhole(-8,ys,z,2,1)
                        gauge=gauge.fuse(cap).cut(zhole(-4,ys,z-3,.8,6))
                        local("DP_LANCE_"+str(i),gauge.clean())
                        tap_rows.append((bed,face,i,datum+sgn*4,cy+sgn*ys,z))
                del parts[prefix+suffix]
                local(suffix,cheek)
            for i,p in enumerate(plate_proto): local("SCREEN_%02d"%i,p)
            # Removable cover and gasket. Around the eight slots the bonded
            # gasket is a real closed loop instead of a blank over the holes.
            y0=307.5 if side>0 else -308.5
            z0=min(cover_slots)-61
            g=box(33.5,y0,z0,21,1,997)
            cover=box(33.5,308.5 if side>0 else -311.5,z0,21,3,997)
            for z in cover_slots:
                g=g.cut(box(38,-312,z-57.5,4,624,115))
                hole=yhole(49,side*306-8,z,2.1,16)
                cover=cover.cut(hole);g=g.cut(hole)
            local("SCREEN_ACCESS_SEAL",g);local("SCREEN_ACCESS_LID",cover)
            # N1-N3. Continuous face plate backs the gasket; the rear box
            # section has two 3 mm walls 20 mm apart. End beads of the
            # flexible sleeve land on the backing plate and fixed collar.
            gasket=ring(0,644,1032,622,1008,4.2)
            local("FACE_GASKET",gasket)
            lip=ring(4.2,770,1156,622,1008,2)
            tube=ring(6.2,770,1156,650,1036,20)
            void=ring(9.2,764,1150,656,1042,14)
            carrier=lip.fuse(tube.cut(void))
            rods=[(offset,z) for offset in (-355,392) for z in (1235,1547,1859,2173)]
            rods += [(offset,z) for offset in (-180,0,180) for z in (1140,2268)]
            for j,(oy,z) in enumerate(rods):
                yy=oy*sgn
                if oy==392:
                    # Integral closed-end lug outside the outer rail.
                    carrier=carrier.fuse(box(4.2, min(380*sgn,405*sgn),z-13,22,25,26))
                carrier=carrier.cut(xhole(3,yy,z,4.6,25))
                local("TIE_NUT_"+str(j),metric_hex(28.2,yy,z,13,6.5,4.0))
                local("TIE_WASHER_"+str(j),xhole(26.2,yy,z,9,2).cut(xhole(25.5,yy,z,4.2,4)))
                if face=="F":
                    part("TIE_"+str(j),xhole(228,cy+oy,z,4,294))
                    clamp_rows.append((bed,j,cy+oy,z,8,294))
            # Four sides carry separate stop lands on the HX frame, outside
            # the continuous gasket. Installed thickness is set by these pads.
            for hand in (-1,1):
                for z in (1235,1547,1859,2173):
                    carrier=carrier.fuse(box(0,hand*324-1.5,z-8,4.2,3,16))
                for yy in (-180,0,180):
                    carrier=carrier.fuse(box(0,yy-8,1704+hand*518-1.5,4.2,16,3))
            # Four M8 guides carry the released ring and keep its face parallel.
            # Turn the thin nut outward until the rail bears on its fixed
            # shoulder, exactly 6 mm away. The stem crosses a screen ligament.
            for k,(hand,z) in enumerate((h,j) for h in (-1,1) for j in (1182,face_lift(40,7))):
                yy=340*hand
                carrier=carrier.cut(xhole(3.0,yy,z,4.65,25),xhole(4.1,yy,z,8.5,2.1))
                base=box(60,307.5 if hand>0 else -353,z-12,4,45.5,24)
                stud=xhole(.15,yy,z,4,59.85)
                stop=xhole(32.2,yy,z,8,3).fuse(xhole(35.2,yy,z,4.5,19.8),xhole(55,yy,z,8,5))
                local("PARK_GUIDE_"+str(k),base.fuse(stud,stop).clean())
                local("PARK_NUT_"+str(k),metric_hex(.15,yy,z,13,4,4.0))
            local("CLAMP_CARRIER",carrier.clean())
            local("EPDM_DIAPHRAGM",bellows(0))
            local("FIXED_COLLAR",ring(25.5,642,1034,615,1001.5,1.5))
            # The R vane trial cassette mounts to blind bosses on both box
            # cheeks. A plug/bolt closes each port in either test condition.
            for hand in (-1,1):
                key=prefix+("BOX_CHEEK_358" if hand>0 else "BOX_CHEEK_-359.5")
                for j,(u,z) in enumerate(((268,707),(327,707),(268,815),(327,815))):
                    worldhole=face_shape(yhole(u,hand*358-5,z,2.65,10),datum,cy,sgn)
                    parts[key]=parts[key].cut(worldhole)
                    ya=359.5 if hand>0 else -367.5
                    boss=yhole(u,ya,z,5.5,8).cut(yhole(u,359 if hand>0 else -365.5,z,2.65,6.5))
                    local("R_VANE_BOSS_"+str((hand,j)),boss)
    # C06_HYD_RT2 valve-tray drain. Bore axis is +X.
    parts["BACK_SKIN"]=parts["BACK_SKIN"].cut(xhole(1308,-700,1068.475,23,8))
    # Triangulate each end above the ducts. Connect to the inside faces of
    # the corner posts, leaving the upper side-panel service bays clear.
    for end,x in (("F",-115),("R",1278)):
        low,high=(1180,2430) if end=="F" else (2430,1180)
        add("END_DIAGONAL_"+end,yz([(-800,low),(1240,high),(1240,high+40),(-800,low+40)],x,12))
    # Roof rail to top cross: side angle brackets joined to both members.
    for j,y in enumerate((-834,1272)):
        add("CROSS_RAIL_CLEAT_"+str(j),box(395,y-8,2485,24,16,25))
    # An installed central X-Z brace remains during either side service.
    add("SERVICE_CENTRE_BRACE",xz([(-91,104),(355,2468),(355,2506),(-91,142)],177,16))
    add("CENTRE_BRACE_FOOT",box(-125,175,104,34,20,38))
    # Under-skid plinth: uprights support each original foot without moving
    # the machine datum. Two transverse feet connect the portal line.
    feet={n:s for n,s in parts.items() if ("FOOT_" in n or "MID_FOOT" in n) and bb(s)[2]<.01}
    for j,(n,s) in enumerate(feet.items()):
        x1,y1,_,x2,y2,_=bb(s)
        add("PLINTH_"+str(j),box(x1,y1,-210,x2-x1,y2-y1,210).cut(
            box(x1+3,y1+3,-211,x2-x1-6,y2-y1-6,212)))
    return parts,clamp_rows,tap_rows,drain_rows

def save_csv(name,columns,values):
    with (HERE/name).open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f);w.writerow(columns);w.writerows(values)
def main():
    parts,rods,taps,drains=build()
    save_csv("tie_rods.csv",["bed","index","global_y_mm","global_z_mm","diameter_mm","length_mm"],rods)
    save_csv("static_taps.csv",["bed","face","band_index","probe_x_mm","probe_y_mm","probe_z_mm"],taps)
    save_csv("traps.csv",["bed","source","x_mm","y_mm","coupling_z_mm","low_axis_z_mm","outlet_axis_z_mm","clear_seal_mm"],drains)
    findings=clashes(parts,parts,True)
    (HERE/"shell_intersections.json").write_text(json.dumps(findings,indent=2))
    print(len(parts),"shell parts;",len(findings),"clashes",findings[:12],flush=True)
    if findings: raise ValueError("Shell interference")
    a=cq.Assembly(name="C07_SHELL")
    for n,s in parts.items(): a.add(s,name=n)
    a.export(str(HERE/"C07_SHELL.step"))
    check=named(HERE/"C07_SHELL.step")
    assert set(check)==set(parts)
    assert all(s.isValid() and len(s.Solids())==1 for s in check.values())
    print("STEP readback",len(check),flush=True)
if __name__=="__main__": main()
