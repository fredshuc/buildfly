"""Generate the tabular machine interface and traceable field handoff."""
from check import *
from OCP.BRepAdaptor import BRepAdaptor_Surface


def faces_touch(a,b):
    area=0.
    for f in a.Faces():
        for g in b.Faces():
            if f.geomType()==g.geomType() and gap(bb(f),bb(g))<1e-5:
                area+=sum(h.Area() for h in f.intersect(g).Faces())
    return area


def registers():
    sels=assembly();host,_=load_host(sels)
    for bed in "AB":rail_fix(bed,sels[bed+"_LOWER"],host)
    theta=end_angle(sels["A_LOWER"])
    rs=[];axes=[]
    for tag,g in sels.items():
        level=tag.split("_")[1]
        b=bb(next(v for n,v in g.items() if n.startswith("DAMPER_SHAFT_")))
        x,z=axis(level)
        axes.append(dict(selector=tag,axis_X_mm=x,axis_Z_mm=z,axis_unit="0,1,0",
                         shaft_Y_min_mm=round(b[1],4),shaft_Y_max_mm=round(b[4],4),
                         drive_side="-Y" if tag.startswith("A") else "+Y",P_angle_deg=0,R_angle_deg=round(theta,6)))
        for mode,angle,pbit,rbit,enable in (("P",0,1,0,"after both beds proved"),("MIDDLE",theta/2,0,0,"OFF"),
                                            ("R",theta,0,1,"after both beds proved"),("OVERTRAVEL",80,0,1,"LOCKOUT")):
            rs.append(dict(selector=tag,state=mode,shaft_deg=round(angle,6),
                LS_P_expected=pbit,LS_R_expected=rbit,
                feedback_note="target envelope only; mechanical stop must prevent this position" if mode=="OVERTRAVEL"
                    else "nominal at this pose; OEM switching tolerance to validate",
                shut_port=(("Rin" if level=="LOWER" else "Rout") if mode=="P" else
                          ("Pout" if level=="LOWER" else "Pin") if mode=="R" else "no confirmed seal"),
                fan_permission=enable))
    table(E/"D03_END_FEEDBACK.csv",rs)
    table(E/"D03_AXES.csv",axes)
    transitions=[]
    for old,new in (("S1","S2"),("S2","S1")):
        for phase,fans,position,proof in [
            ("RUN_OLD","per mode",old,"four valve endpoints, measured seat proof"),
            ("UNLOAD","command both fans down",old,"hold all four actuators"),
            ("ZERO_FLOW","OFF",old,"fan stop/speed and safe differential pressure confirmed independently"),
            ("TRANSFER","OFF","INTERMEDIATE","move upper/lower as paired selectors; either bed may lag; no fan enable"),
            ("PROVE_NEW","OFF",new,"each target sensor active, opposite inactive, shaft angle in commissioned window; water changeover acknowledged"),
            ("RUN_NEW","ramp to required duties",new,"all four selectors proved; fault/timeout/disagreement or lost proof trips both fans")]:
            p=("A=P,B=R" if position=="S1" else "A=R,B=P" if position=="S2" else "P and R can communicate on either bed")
            transitions.append(dict(transition=old+"->"+new,phase=phase,fan_command=fans,bed_status=p,proof=proof))
    table(E/"D03_CHANGEOVER.csv",transitions)
    rows=[];fits=[]
    def joint(bed,member,receiver,s,t):
        area=faces_touch(s,t);assert area>5,(member,receiver,area)
        rows.append(dict(bed=bed,member=member,receiver=receiver,nominal_contact_mm2=round(area,4)))
    for bed in "AB":
        tag=bed+"_LOWER";g=sels[tag];sgn=-1 if bed=="A" else 1
        chain=["D03_ACTUATOR_INTERFACE_","D03_WEIGHT_SADDLE_","D03_WEIGHT_ARM_","D03_WEIGHT_WEB_","D03_BEARING_CARRIER_"]
        for l,r in zip(chain,chain[1:]):joint(bed,l+tag,r+tag,g[l+tag],g[r+tag])
        for i in range(4):
            s="D03_CARRIER_SPACER_"+tag+"_"+str(i)+"_0"
            root="DAMPER_ACT_BRACKET_"+tag+"_O"
            joint(bed,chain[-1]+tag,s,g[chain[-1]+tag],g[s])
            joint(bed,s,root,g[s],g[root])
        rail=f"F_DAMPER_RAIL_{825*sgn}_O"
        joint(bed,root,rail,g[root],host[rail])
        for x in (-600,1020):
            post=f"F_POST_{x}_{825*sgn}_O"
            joint(bed,rail,post,host[rail],host[post])
        sleeve=next(s for n,s in g.items() if n.startswith("DAMPER_ROOT_SLEEVE"))
        for pos in ("SLOPED","DEEP"):
            name=f"DAMPER_SEAT_{tag}_{pos}_O"
            fits.append(dict(bed=bed,component="root sleeve vs metal seat "+pos,
                        measurement=witness(sleeve,g[name])))
    table(E/"D03_ACTUATOR_LOAD_PATH.csv",rows);save_json(E/"D03_RUNNING_CLEARANCES.json",fits)
    guard_mounts=[]
    for tag,g in sels.items():
        bed,level=tag.split("_");n="M401_DAMPER_BACKER_"+bed+"_"+level[0]+"_O"
        area=faces_touch(g["D03_GUARD_BRIDGE_"+tag],host[n])
        assert area>20,(tag,n,area)
        guard_mounts.append(dict(selector=tag,receiver=n,contact_mm2=round(area,4)))
    table(E/"D03_GUARD_MOUNTS.csv",guard_mounts)
    requirements=[]
    for bed,sgn in (("A",-1),("B",1)):
        for x in (575.,645.):
            for z,diam,meaning in ((313.,9.,"bracket pre-existing foot bore"),(310.,9.,"upper wall of retained RHS"),
               (230.,14.2,"bottom wall, insert crush sleeve from below")):
                requirements.append(dict(bed=bed,component=meaning,X=x,Y=sgn*833.5,Z=z,diameter_mm=diam,axis="Z"))
    table(E/"D03_RAIL_DRILLING.csv",requirements)
    p,ref=cache(OLD,"old")
    names=[n for n in ref if n.startswith(("AIR_PORT_LAND","AIR_PROCESS_IN_WRAP","AIR_PROCESS_IN_FLOOR","ROOF_FLANGE"))]
    table(E/"D03_EXTERNAL_PORT_REFERENCES.csv",[dict(name=n,source="521 original sheet metal; retain at machine datum",bounds_xyz_mm=ref[n][1]) for n in names])


def package():
    import shutil
    out=ROOT/"inputs";out.mkdir(exist_ok=True)
    if (out/"FOUR_HX_INSTALLED.step").resolve()!=HX.resolve():
        shutil.copyfile(HX,out/"FOUR_HX_INSTALLED.step")
    ix=json.loads((WORK/"selector/index.json").read_text())
    files=sorted({f for f,_,_ in ix["rows"].values()})
    ix["files"]={f:hashlib.sha256((WORK/"selector"/f).read_bytes()).hexdigest() for f in files}
    with zipfile.ZipFile(out/"M2_SELECTOR_SOURCE.zip","w",zipfile.ZIP_DEFLATED) as z:
        z.writestr("index.json",json.dumps(ix))
        for f in files:z.write(WORK/"selector"/f,f)
    result=json.loads((E/"D03_RUN.json").read_text())
    assert all(result[k]==0 for k in ("static_rigid_hits","motion_hits","motion_unresolved","service_hits","cross_sweep_hits")),result
    assert not result["hx"]["confirmed_hx_clashes"] and not result["hx"]["unresolved"]
    for n,h in result["cad_sha256"].items():assert hashlib.sha256((ROOT/"cad"/n).read_bytes()).hexdigest()==h
    paths=[ROOT/"README_CN.md",ROOT/"run.ps1",ROOT/".gitignore"]
    for folder in ("cad","evidence","source","inputs"):
        paths += [p for p in (ROOT/folder).iterdir() if p.is_file()]
    hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
    with zipfile.ZipFile(ROOT/"D03_DAMPER_REVIEW.zip","w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for n in hashes:z.write(ROOT/n,n)
        z.writestr("SHA256.json",json.dumps(hashes,indent=2))
    with zipfile.ZipFile(ROOT/"D03_DAMPER_REVIEW.zip") as z:
        assert z.testzip() is None and all(hashlib.sha256(z.read(n)).hexdigest()==h for n,h in hashes.items())
    print("Package verified",len(hashes),"files")


if __name__=="__main__":
    registers()
    if "--package" in sys.argv:package()
