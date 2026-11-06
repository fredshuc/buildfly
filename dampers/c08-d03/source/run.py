from check import *


def hx_screen(shapes,selectors,theta):
    # The released shared STEP has 549 leaves in each of four placements.
    # Distances between disjoint global bounding boxes are rigorous lower bounds.
    hx=[]
    for key,s in leaves(HX):
        hx.append((key,s,bb(s)))
    assert len(hx)==2196
    nearest={}; intersections=[]; unresolved=[]
    for group,items in shapes.items():
        value=1e6;best=None
        for n,s in items.items():
            b=bb(s)
            for low,key,t in sorted(((gap(b,b2),k,obj) for k,obj,b2 in hx),key=lambda a:a[0]):
                if low>max(value,.001):break
                d,pts=witness(s,t)
                if d<value:value=d;best=[n,key,d,pts]
                if d>.0001 or not group.endswith("_MOTION") or vol(s,t)<=LIMIT:continue
                tag=next(tag for tag,g in selectors.items() if n in g)
                level=tag.split("_")[1];rotor=selectors[tag][n]
                states=[]
                for a in np.linspace(0,theta,81):
                    p=rotate(rotor,level,float(a));v=vol(p,t) if overlap(bb(p),bb(t)) else 0.
                    if v>LIMIT:states.append([round(float(a),5),round(v,5)])
                if states:
                    first=states[0][0];lo=max(0,first-theta/80);hi=first
                    for _ in range(9):
                        mid=(lo+hi)/2
                        if vol(rotate(rotor,level,mid),t)>LIMIT:hi=mid
                        else:lo=mid
                    mx=max(states,key=lambda v:v[1])
                    intersections.append(dict(rotor=n,obstruction=key,first_sample_deg=first,
                        entry_bracket_deg=[round(lo,4),round(hi,4)],last_sample_deg=states[-1][0],
                        max_sample_deg=mx[0],max_sample_volume_mm3=mx[1],
                        witness=witness(rotate(rotor,level,mx[0]),t)[1]))
                else:unresolved.append([n,key,"conservative overlap; 81 exact poses clear"])
        nearest[group]=best
    return dict(minimum=nearest,confirmed_hx_clashes=intersections,unresolved=unresolved)


def main():
    for d in (E,ROOT/"cad",WORK):d.mkdir(exist_ok=True,parents=True)
    sets=assembly();theta=end_angle(sets["A_LOWER"])
    host,source=load_host(sets)
    for bed in "AB":rail_fix(bed,sets[bed+"_LOWER"],host)
    print("Install:",len(host),"host parts; official C08:",source,flush=True)
    holes_and_seats(sets)
    data={t:route_check(g,t,theta) for t,g in sets.items()}
    for t,rows in data.items():
        assert [(r['DEEP']['centreline_blocked'],r['SLOPED']['centreline_blocked']) for r in rows[:3]]==[(False,True),(False,False),(True,False)]
        assert rows[-1]["DEEP"]["steel_overlap_mm3"]>990
        assert abs(rows[0]["LS_P_gap_mm"]-1.5)<.001 and abs(rows[2]["LS_R_gap_mm"]-1.5)<.001
    save_json(E/"D03_ENDPOINT_CHECKS.json",data)
    groups,rot,allparts=envelopes_and_static(sets,host,theta)
    print("Continuous external check",flush=True)
    mot=motion_check(sets,rot,allparts,theta)
    cross=[]
    for (a,g),(b,h) in combinations(sets.items(),2):
        for n in g.keys() & rot.keys():
            for k in h.keys() & rot.keys():
                if overlap(bb(rot[n]),bb(rot[k])):
                    v=vol(rot[n],rot[k])
                    if v>LIMIT:cross.append([n,k,v])
    mot["cross_selector_sweeps"]=cross
    save_json(E/"D03_MOTION_CHECKS.json",mot)
    print("Motion",len(mot["hits"]),len(mot["unresolved_intervals"]),len(cross),flush=True)
    serv=service_check(sets,groups,allparts);save_json(E/"D03_SERVICE_CHECKS.json",serv)
    print("Service",serv["hits"][:12],flush=True)
    static=static_check(sets,host)
    elastic=[];hard=[]
    for record in static:
        names=record[:2]
        elastic_joint=(any(n.startswith(("DAMPER_SHAFT_","DAMPER_ROOT_SLEEVE_")) for n in names)
                       and any(n.startswith(("DAMPER_ROOT_LIP_","DAMPER_ROOT_END_SEAL_")) for n in names))
        (elastic if elastic_joint else hard).append(record)
    save_json(E/"D03_STATIC_CHECKS.json",dict(rigid=hard,inherited_seal_interference=elastic))
    print("Static",hard[:15],flush=True)
    interesting={}
    for bed in "AB":
        tag=bed+"_LOWER";g=sets[tag];s=next(s for n,s in g.items() if n.startswith("DAMPER_SHAFT"))
        other=next(s for n,s in sets[("B" if bed=="A" else "A")+"_LOWER"].items() if n.startswith("DAMPER_SHAFT"))
        interesting[tag+"_shaft_to_other_shaft"]=witness(s,other)
        stop=g["D03_STOP_ARM_"+tag]
        for i,deg in enumerate((0,theta)):
            pin=g[f"D03_STOP_PIN_{tag}_{i}"]
            interesting[tag+"_hard_stop_"+str(i)]=witness(rotate(stop,"LOWER",deg),pin)
            assert interesting[tag+"_hard_stop_"+str(i)][0]<.001
        bracket=g["DAMPER_ACT_BRACKET_"+tag+"_O"]
        interesting[tag+"_bracket_to_load_rail"]=witness(bracket,host[f"F_DAMPER_RAIL_{(-825 if bed=='A' else 825)}_O"])
    save_json(E/"D03_CLEARANCE_WITNESSES.json",interesting)
    for state in ("S1","S2"):
        placed={}
        for tag,g in sets.items():
            a=theta if (tag[0]=="B")== (state=="S1") else 0.
            placed[tag]=({n:rotate(s,tag.split("_")[1],a) if motion(n) else s for n,s in g.items()},
                         (.21,.54,.69) if a==0 else (.84,.49,.21))
        placed["SHELL_REFERENCE"]=(host,(.64,.7,.75,.36))
        print(state,export(ROOT/f"cad/D03_INSTALLED_{state}.step",placed),flush=True)
    print("Envelope readback",export(ROOT/"cad/D03_MOTION_AND_SERVICE.step",groups),flush=True)
    hxr=hx_screen({k:g for k,(g,c) in groups.items()},sets,theta)
    save_json(E/"D03_HX_CHECK.json",dict(sha256=hashlib.sha256(HX.read_bytes()).hexdigest(),leaves=2196,**hxr))
    official=bool(source)
    save_json(E/"D03_RUN.json",dict(host="C08" if official else "PARENT_FRAME_ONLY_C08_NOT_AVAILABLE",
       host_sha256=hashlib.sha256((source or OLD).read_bytes()).hexdigest(),source_sha256=json.loads((WORK/"selector/index.json").read_text())["sha"],
       angle_deg=theta,host_parts=len(host),moving_occurrences=len(rot),service_volumes=sum(len(g) for k,(g,c) in groups.items() if k.endswith("_SERVICE")),
       static_rigid_hits=len(hard),motion_hits=len(mot["hits"]),motion_unresolved=len(mot["unresolved_intervals"]),
       service_hits=len(serv["hits"]),cross_sweep_hits=len(cross),hx=hxr,
       cad_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (ROOT/"cad").glob("*.step")}))
    print("Verified STEP exports.",flush=True)


if __name__=="__main__":main()
