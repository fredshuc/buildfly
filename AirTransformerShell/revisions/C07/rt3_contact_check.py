"""Independent RT3 contact audit. Run beside the C07 STEP with CadQuery 2.8."""
import hashlib, json
from functools import lru_cache
import cadquery as cq
from cad_io import named, bb as shape_bounds
bb=lru_cache(maxsize=30000)(lambda s: tuple(shape_bounds(s)))
from integrate_c07 import HERE, HX, ORIGINS
def paired(a,b,tol=0.0001):
    return all(min(a[k+3],b[k+3])-max(a[k],b[k])>=-tol for k in range(3))
def planar(s,x):
    return [f for f in s.Faces() if f.geomType()=="PLANE" and
            max(abs(bb(f)[j]-x) for j in (0,3))<0.0001]
def areas(aa,bb_faces):
    result={}
    candidates=[(n,b,bb(b)) for n,b in bb_faces]
    for a in aa:
        a_box=bb(a)
        for n,b,b_box in candidates:
            if not paired(a_box,b_box):continue
            v=a.intersect(b).Area()
            if v>0.0001:result[n]=result.get(n,0)+v
    return {n:round(v,5) for n,v in result.items()}
def surfaces(a,b):
    if not paired(bb(a),bb(b)):return 0.0
    return sum(areas(a.Faces(),[(str(i),f) for i,f in enumerate(b.Faces())]).values())
sh=named(HERE/"C07_SHELL.step");hx=named(HX/(HX.name+".step"))
print("eager load",len(sh),len(hx),flush=True)
out={"carrier_steel_equivalent_kg":round(sh["AF_CLAMP_CARRIER"].Volume()*7.85e-6,4),"shell_items":len(sh),"mm_and_mm2":True,"shell_sha256":hashlib.sha256((HERE/"C07_SHELL.step").read_bytes()).hexdigest(),"seats":{},"brace_contacts":{}}
for bed,origin in ORIGINS.items():
    for face,datum,sgn in (("F",265,-1),("R",485,1)):
        pref=bed+face+"_"; force=sh[pref+"CLAMP_CARRIER"];gask=sh[pref+"FACE_GASKET"]; dia=sh[pref+"EPDM_DIAPHRAGM"];collar=sh[pref+"FIXED_COLLAR"]
        hfaces=[(n,f.translate(origin)) for n,s in hx.items() if n.startswith(("POST_","AIR_EDGE_")) and bb(s)[0]<=datum-origin[0]+.001 and bb(s)[3]>=datum-origin[0]-.001 for f in planar(s,datum-origin[0])]
        gf=planar(gask,datum);sf=planar(force,datum)
        seat=areas(gf,hfaces)
        remaining=cq.Compound.makeCompound(gf)
        for label,f in hfaces:
            if label in seat:
                remaining=remaining.cut(f)
        keeper=[]
        for j in range(4):
            guide=sh[pref+"PARK_GUIDE_"+str(j)]
            nut=sh[pref+"PARK_NUT_"+str(j)]
            side_contact=sum(surfaces(guide,sh[pref+n]) for n in ("CHEEK_-307.5","CHEEK_306"))
            released=force.translate((sgn*6,0,0))
            xstop=datum+sgn*32.2
            shoulder=areas(planar(released,xstop),[("shoulder",f) for f in planar(guide,xstop)])
            nuts=bb(nut)
            nutface=nuts[3] if sgn==1 else nuts[0]
            for level in (4.2,6.2):
                target=datum+sgn*(level+6)
                moved_nut=nut.translate((target-nutface,0,0))
                push=areas(planar(released,target),[("push",f) for f in planar(moved_nut,target)])
                if sum(push.values())>1:
                    break
            gap=abs(datum+sgn*level-nutface)
            keeper.append({"guide":j,"weld_face_to_cheek":round(side_contact,4),"installed_push_nut_gap":round(gap,5),
                "released_nut_area":round(sum(push.values()),4),"released_shoulder_area":round(sum(shoulder.values()),4)})
        print("keepers",pref,keeper,flush=True)
        stop=[{"pad_mm2":round(f.Area(),4),"on_hx_mm2":areas([f],hfaces)} for f in sf]
        source={}
        for sign,loc,key,solid in ((1,6.2,"moving_carrier",force),(1,25.5,"fixed_collar",collar)):
            x=datum+sgn*loc
            bead=planar(dia,x); lands=planar(solid,x)
            source[key]={"end_face_mm2":round(sum(f.Area() for f in bead),4),"on_counterpart_mm2":round(sum(areas(bead,[(key,f) for f in lands]).values()),4)}
        sides={}
        for n in (pref+"CHEEK_-307.5",pref+"CHEEK_306",pref+"GUIDE_00",pref+"GUIDE_08"):
            sides[n]=round(surfaces(collar,sh[n]),4)
        out["seats"][pref]={"gasket_mm2":round(sum(f.Area() for f in gf),4),"gasket_lands_mm2":seat,"gasket_area_outside_union":round(remaining.Area(),6),"park":keeper,"hard_stops":stop,"diaphragm":source,"collar_to_duct_mm2":sides}
        print(pref,"gasket, stops",sum(seat.values()),len(stop),sum(sum(y["on_hx_mm2"].values()) for y in stop),source,sides,flush=True)
(HERE/"rt3_contacts.json").write_text(json.dumps(out,indent=2))
targets=[n for n in sh if any(i in n for i in ("RISER_XZ_","CENTRE_BRACE","END_DIAGONAL_","CROSS_RAIL_CLEAT_","HX_TOP_CROSS"))]
boxes={n:bb(s) for n,s in sh.items()}
for n in targets:
    others={k:round(surfaces(sh[n],s),4) for k,s in sh.items() if k!=n and paired(boxes[k],boxes[n])}
    out["brace_contacts"][n]={k:v for k,v in others.items() if v>.001}
    print(n,out["brace_contacts"][n],flush=True)
(HERE/"rt3_contacts.json").write_text(json.dumps(out,indent=2))