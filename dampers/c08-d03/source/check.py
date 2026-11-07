from envelopes import *
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GeomAbs import GeomAbs_Circle
from itertools import combinations

E=ROOT/"evidence"
LIMIT=.001
def gap(a,b):
    return math.sqrt(sum(max(0,a[i]-b[i+3],b[i]-a[i+3])**2 for i in range(3)))
def overlap(a,b):
    return all(min(a[i+3],b[i+3])-max(a[i],b[i])>1e-5 for i in range(3))
def vol(a,b):
    return sum(abs(v.Volume()) for v in a.intersect(b).Solids())
def witness(a,b):
    d=BRepExtrema_DistShapeShape(a.wrapped,b.wrapped);d.Perform()
    assert d.IsDone()
    pts=[d.PointOnShape1(1),d.PointOnShape2(1)]
    return round(d.Value(),6),[[round(f(),4) for f in (p.X,p.Y,p.Z)] for p in pts]

def load_host(selectors):
    # This iteration has no C08 host. Only a deliberately supplied successor
    # can enable full overlay; never look up the missing historical artefact.
    explicit=os.getenv("C08_STEP")
    official=Path(explicit) if explicit else None
    idx,rows=cache(official or OLD,"c08" if official else "old")
    assert len(rows)==521
    owned={k for g in selectors.values() for k in g}
    shapes={}
    for n,(f,b) in rows.items():
        if n in owned:continue
        if not official and n.startswith(("M401_DAMPER_BLANK_","M401_DAMPER_BACKER_")) and "_L_" in n:
            shapes[n]=cq.Shape.importBrep(str(idx/f)).translate((110,0,0))
            continue  # D03 proposes relocating the local guard backers with its station
        if not official and not (n.startswith(("F_","ROOF_FLANGE","AIR_PORT_LAND")) or b[2]>600.):
            continue  # no invented C08 sheet metal in a provisional assembly
        shapes[n]=cq.Shape.importBrep(str(idx/f))
    if official:
        for bed,level in IDS:
            group=selectors[bed+"_"+level]
            for n in group.keys() & rows.keys():
                # Verify installed geometry at the archived S1 pose. B's
                # moving members are normalised to P in the product dictionary.
                original=cq.Shape.importBrep(str(idx/rows[n][0]))
                prod=group[n]
                if bed=="B" and motion(n):prod=rotate(prod,level,end_angle(selectors["A_LOWER"]))
                assert max(abs(a-b) for a,b in zip(bb(prod),bb(original)))<.02, n
    return shapes,official

def envelopes_and_static(selectors,host,theta):
    groups={}; local={}; allparts=dict(host)
    for tag,g in selectors.items():
        level=tag.split("_")[1]
        env={n:sweep(s,n,level,theta) for n,s in g.items() if motion(n)}
        groups[tag+"_MOTION"]=(env,(.96,.57,.13,.32));local.update(env);allparts.update(g)
        serv=services(g,tag[0],level)
        groups[tag+"_SERVICE"]=(serv,(.06,.64,.7,.28))
    return groups,local,allparts

def motion_check(selectors,rot,scene,theta):
    bounds={n:bb(s) for n,s in scene.items()}
    hits=[];near=[];contacts=[];candidates=0;uncertain=[]
    for tag,parts in selectors.items():
        level=tag.split("_")[1]
        for n,shape in parts.items():
            if n not in rot:continue
            env=rot[n]; eb=bb(env)
            radius=max(math.hypot(x-axis(level)[0],z-axis(level)[1]) for x,z in product(
                (eb[0],eb[3]),(eb[2],eb[5])))
            for k,b in bounds.items():
                if k in rot or gap(eb,b)>3:continue
                other=scene[k]; candidates+=1
                if n=="D03_STOP_ARM_"+tag and k.startswith("D03_STOP_PIN_"+tag):
                    # Pin centre in the lug's tangent direction is
                    # 6*cos(delta)+30*sin(delta) at angular separation delta
                    # from its own end. It is >=6 on [0,77.702] (concave;
                    # minima at endpoints); lug half-width 3 + pin radius 3.
                    # Hub-to-pin clearance is hypot(6,30)-17-3 > 10 mm.
                    end=0. if k.endswith("_0") else theta
                    assert witness(rotate(shape,level,end),other)[0]<1e-5
                    assert 6*math.cos(math.radians(theta))+30*math.sin(math.radians(theta))>6
                    contacts.append([n,k,"analytic unilateral end stop; tangent only at its endpoint"]);continue
                if tag in k and (("BEARING" in k and ("SHAFT" in n or "ROOT_SLEEVE" in n))
                            or "ROOT_END_SEAL" in k or "ROOT_LIP" in k or "DAMPER_SEAL_" in k
                            or ("D03_SEAL_BACKING" in k and "SHAFT" in n)
                            or ("D03_ACT_OUTPUT" in n and "D03_ACTUATOR" in k)):
                    contacts.append([n,k,"journal / designed seal or drive interface"]);continue
                lower=env.distance(other)
                if lower>.0005:
                    if lower<3:near.append([n,k,round(lower,5)])
                    continue
                if vol(env,other)<=LIMIT:
                    near.append([n,k,0.]);continue
                # Exact shapes at adaptive angular midpoints. The most any point
                # moves over a half interval is 2*r*sin(delta/4).
                def check_range(a,c,depth=0):
                    mid=(a+c)/2;p=rotate(shape,level,mid);d=p.distance(other)
                    bound=2*radius*math.sin(math.radians(c-a)/4)
                    if d>bound+1e-6:return
                    v=vol(p,other) if d<1e-6 else 0
                    if v>LIMIT:
                        hits.append(dict(moving=n,obstruction=k,deg=round(mid,5),volume_mm3=round(v,5)));return
                    if depth>=9:
                        uncertain.append([n,k,round(a,4),round(c,4)]);return
                    check_range(a,mid,depth+1);check_range(mid,c,depth+1)
                check_range(0,theta)
    return dict(candidates=candidates,hits=hits,unresolved_intervals=uncertain,designed_pairs=contacts,
                certified_near_pairs_mm=sorted(near,key=lambda r:r[2]))

def service_check(selectors,envs,allparts):
    bounds={n:bb(s) for n,s in allparts.items()};hits=[];closest={}
    for tag,g in selectors.items():
        for key,s in envs[tag+"_SERVICE"][0].items():
            box=bb(s);minimum=1e9;best=None
            # Mechanism locked at process and isolated for service.
            for n,b in sorted(bounds.items(),key=lambda it:gap(box,it[1])):
                lo=gap(box,b)
                if lo>min(5.,minimum+1e-5):break
                own=n in g
                if own and key.startswith("HOOD_PULL") and ("HOOD" in n or "_LIMIT_SENSOR_" in n or "GUARD_M4" in n):continue
                if own and key.startswith("ACT_PULL") and ("ACTUATOR_INTERFACE" in n or "ACT_OUTPUT" in n or "ACT_M6" in n):continue
                if own and key.startswith("ACT_PULL") and n.startswith(("D03_DRIVE_NUT","D03_DRIVE_WASHER")):continue
                if own and key.startswith("ACT_SOCKET") and ("ACT_M6" in n):continue
                if own and key.startswith("ACT_SOCKET") and n.startswith(("D03_DRIVE_NUT","D03_DRIVE_STUD","D03_DRIVE_WASHER")):continue
                if own and key.startswith("HOOD_DRIVER") and "GUARD_M4" in n:continue
                if own and key.startswith("BASE_SOCKET") and "D03_BASE_M8" in n:continue
                if own and key.startswith("ACT_PULL") and "D03_COUPLING" in n:continue # engaged D output leaves its matching bore
                other=allparts[n]
                v=vol(s,other) if overlap(box,b) else 0
                if v>LIMIT:hits.append([key,n,round(v,4)])
                d,pts=witness(s,other)
                if d<minimum:minimum,best=d,[n,d,pts]
            closest[key]=best or "all other bounds >5 mm"
    return dict(hits=hits,nearest_within_5_mm=closest)

def static_check(selectors,host):
    hits=[]
    boxes={n:bb(s) for n,s in host.items()}
    boxes.update({n:bb(s) for parts in selectors.values() for n,s in parts.items()})
    for tag,g in selectors.items():
        candidates=dict(host)
        for name,g2 in selectors.items():
            if name!=tag:candidates.update(g2)
        for n,s in g.items():
            b=boxes[n]
            for k,t in candidates.items():
                if overlap(b,boxes[k]):
                    v=vol(s,t)
                    if v>LIMIT:hits.append([n,k,round(v,5)])
        for (n,s),(k,t) in combinations(g.items(),2):
            if overlap(bb(s),bb(t)):
                v=vol(s,t)
                if v>LIMIT:hits.append([n,k,round(v,5)])
    return hits

def holes_and_seats(selectors):
    rows=[];ap=[];axes=[]
    for tag,g in selectors.items():
        bed,level=tag.split("_");x,z=axis(level)
        axes.append(dict(selector=tag,x_mm=x,y_reference_mm=0,z_mm=z,unit_axis="0,1,0",travel_deg=77.7019286))
        for n,s in g.items():
            if not any(k in n for k in ("ACT_BRACKET","INNER_RECEIVER","INNER_FLANGE","FEEDBACK_HOOD","SEAT_")):continue
            seen=set()
            for e in s.Edges():
                arc=BRepAdaptor_Curve(e.wrapped)
                if arc.GetType()!=GeomAbs_Circle:continue
                c=arc.Circle();p=c.Location();d=c.Axis().Direction()
                key=tuple(round(f(),4) for f in (p.X,p.Y,p.Z))+ (round(c.Radius()*2,4),)
                if key in seen:continue
                seen.add(key);rows.append(dict(selector=tag,part=n,x_mm=key[0],y_mm=key[1],z_mm=key[2],
                    diameter_mm=key[3],normal=[round(d.X(),3),round(d.Y(),3),round(d.Z(),3)],
                    arc_degrees=round(math.degrees(arc.LastParameter()-arc.FirstParameter()),3)))
            if "SEAT_" in n:
                faces=[f for f in s.Faces() if f.innerWires()]
                # Keep both aperture face loops. Coordinates define the sloped
                # window independently of projected rectangle dimensions.
                for i,f in enumerate(faces):
                    for w in f.innerWires():
                        ap.append(dict(selector=tag,port=("Rin" if level=="LOWER" else "Rout") if "SLOPED" in n else ("Pout" if level=="LOWER" else "Pin"),
                            face=i,xyz_mm=[[round(v.Center().x,4),round(v.Center().y,4),round(v.Center().z,4)] for v in w.Vertices()]))
    table(E/"D03_AXES.csv",axes);table(E/"D03_MOUNT_OPENINGS.csv",rows);table(E/"D03_SEAT_APERTURES.csv",ap)

def route_check(g,tag,theta):
    level=tag.split("_")[1];blade=next(s for n,s in g.items() if "BLADE_" in n and n.endswith("_0_O"))
    flags=next(s for n,s in g.items() if "BLADE_" in n and n.endswith("_4_O"))
    results=[]
    for mode,a in (("P",0.),("MID",theta/2),("R",theta),("OVERTRAVEL",80.)):
        plate=rotate(blade,level,a);row=dict(state=mode,deg=a)
        for pos in ("DEEP","SLOPED"):
            seat=next(s for n,s in g.items() if "DAMPER_SEAT_" in n and pos in n)
            seal=next(s for n,s in g.items() if "DAMPER_SEAL_" in n and pos in n)
            f=next(f for f in seat.Faces() if f.innerWires())
            w=f.innerWires()[0]; origin=w.Center(); normal=f.normalAt()
            ray=cq.Edge.makeLine(origin-normal*12,origin+normal*12)
            row[pos]=dict(centreline_blocked=plate.distance(ray)<1e-5,steel_gap_mm=round(plate.distance(seat),5),
                          steel_overlap_mm3=round(vol(plate,seat),5),seal_gap_mm=round(plate.distance(seal),5),
                          seat_witness=witness(plate,seat)[1])
            if (pos=="DEEP" and mode=="R") or (pos=="SLOPED" and mode=="P"):
                aperture=cq.Face.makeFromWires(w)
                blade_face=max(plate.Faces(),key=lambda g:g.Area())
                assert abs(blade_face.normalAt().dot(normal))>.999999
                offset=normal*(origin-blade_face.Center()).dot(normal)
                footprint=blade_face.translate(offset)
                unclosed=aperture.cut(footprint).Area()
                assert unclosed<.002,(tag,mode,unclosed)
                row[pos]["aperture_mm2"]=round(aperture.Area(),4)
                row[pos]["projected_uncovered_mm2"]=round(unclosed,5)
                row[pos]["minimum_edge_overlap_mm"]=round(w.distance(footprint.outerWire()),5)
        for label in ("P","R"):
            sensor=g["D03_"+label+"_LIMIT_SENSOR_"+tag]
            row["LS_"+label+"_gap_mm"]=round(rotate(flags,level,a).distance(sensor),5)
        results.append(row)
    return results
