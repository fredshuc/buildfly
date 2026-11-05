"""Read the released STEP modules at their installed origins and audit the C07 configuration."""
from pathlib import Path
import csv,json,hashlib,sys
import cadquery as cq
from cad_io import named,leaves,bb,clashes,overlaps
from build_c07 import face_shape,ring,bellows

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
D01=ROOT/"dampers"/"c04-d01"
D02=ROOT/"dampers"/"c06-d02"
C06=HERE.parent/"C06"
HX=ROOT/"HX"/"M101_D952_P254_220_39x6_C05"
HYD=ROOT/"hydronics"/"C06_RT2_HYD_R2"
ORIGINS={"A":(265,-802.175,1150),"B":(265,477.825,1150)}
def merged_water():
    w=named(C06/"C06_WATER_FIT.step")
    delta=named(HYD/"C06_HYD_R2_REPLACEMENTS_AND_TAIL.step")
    assert len(w)==43 and len(delta)==6 and len(w.keys() & delta.keys())==5
    w.update(delta)
    return w
def installed_cores():
    product=named(HX/(HX.name+".step"))
    assert len(product)==549
    return {b+"_"+n:s.translate(t) for b,t in ORIGINS.items() for n,s in product.items()}
def installation():
    shell=named(HERE/"C07_SHELL.step");d02=named(D02/"cad/D02_DAMPER_SUPPORTS.step")
    core=installed_cores();water=merged_water()
    d01={n:s for n,s in leaves(D01/"cad/D01_EIGHT_DAMPERS_INSTALLED.step") if "/HOST/" not in n}
    assert len(d01)==7212 and len(d02)==149 and len(water)==44
    return shell,d02,core,water,d01
def static_checks():
    shell,d02,core,water,d01=installation()
    svc=named(C06/"C06_WATER_SERVICE.step")
    svc.update(named(HYD/"C06_HYD_R2_BLEED_ENVELOPES.step"))
    ht=named(HX/"C05_VENT_SERVICE_LOCAL.step")
    vents={b+"_"+n:s.translate(t) for b,t in ORIGINS.items() for n,s in ht.items()}
    dsvc=named(D01/"cad/D01_SERVICE_ENVELOPES.step")
    actual={n:s for n,s in dsvc.items() if "FULL_ROTATION_BOUND" not in n}
    groups={"shell":shell,"N8":d02,"HX":core,"water":water,"D01":d01,
        "water_service":svc,"HX_vent_service":vents,"damper_service":actual}
    report={"static_parts":{k:len(v) for k,v in groups.items()},"shell_sha256":hashlib.sha256((HERE/"C07_SHELL.step").read_bytes()).hexdigest(),"overlap_threshold_mm3":.001,"checks":{}}
    pairs=[("shell","N8"),("shell","HX"),("shell","water"),("shell","D01"),
       ("N8","HX"),("N8","water"),("N8","D01"),("water","HX"),("water","D01"),
       ("HX","D01"),("water","water"),("shell","water_service"),("water","water_service"),("N8","water_service"),
       ("HX","water_service"),("D01","water_service"),("shell","HX_vent_service"),
       ("N8","HX_vent_service"),("water","HX_vent_service"),("D01","HX_vent_service"),
       ("shell","damper_service"),("N8","damper_service"),("water","damper_service"),("HX","damper_service")]
    for a,b in pairs:
        hits=clashes(groups[a],groups[b],a==b)
        report["checks"][a+"__"+b]=hits
        print(a,b,len(hits),hits[:3],flush=True)
        (HERE/"integration.json").write_text(json.dumps(report,indent=2))
    return report
def port_check():
    def index(file):
        with file.open(encoding="utf-8-sig") as f:
            return {r["port"]:r for r in csv.DictReader(f)}
    hxfile=HX/"C06_INSTALLED_PORT_FUNCTIONS.csv";hydfile=HYD/"PORT_FUNCTION_REGISTER.csv"
    hx=index(hxfile);water=index(hydfile)
    signed=json.loads((HX/"HX_FUNCTION_SIGNOFF.json").read_text())
    assert hashlib.sha256(hxfile.read_bytes()).hexdigest()==signed["table_sha256"]
    assert set(hx)==set(water)=={"A.W1","B.W1","A.W2","B.W2"}
    for port,row in hx.items():
        w=water[port]
        assert [float(row[k]) for k in ("x_mm","y_mm","z_mm")]==[float(w[k]) for k in ("x_mm","y_mm","z_mm")]
        assert row["normal"]==w["face_normal"] and row["connection"]==w["connection"]
        assert [row[k] for k in ("cold_service","hot_service")]==[w[k] for k in ("cold_service","hot_service")]
        assert row["hydronics_selectors"].split("|")==[w["cold_selector"],w["hot_selector"]]
        assert row["flow_relative_to_HX"]=={"-X":"IN","+X":"OUT"}[w["water_vector_at_union"]]
    proof={"HX_authority":signed["disposition"],"HX_table_sha256":signed["table_sha256"],
        "R2_table_sha256":hashlib.sha256(hydfile.read_bytes()).hexdigest(),"matched_ports":sorted(hx),
        "flow":"Cold and hot W1 supply / W2 return","hold":"Purge, pressure-rated vent hardware, relief and regeneration comparison"}
    (HERE/"port_reconciliation.json").write_text(json.dumps(proof,indent=2))
def service_checks():
    shell=named(HERE/"C07_SHELL.step");core=installed_cores();w=merged_water()
    d02=named(D02/"cad/D02_DAMPER_SUPPORTS.step")
    damper_bounds={n:bb(s) for n,s in leaves(D01/"cad/D01_EIGHT_DAMPERS_INSTALLED.step") if "/HOST/" not in n}
    assert len(damper_bounds)==7212
    report={}
    for bed,sign in (("A",-1),("B",1)):
        cy=ORIGINS[bed][1]+367.775
        retained=dict(shell);removed=[]
        def take(n):
            del retained[n];removed.append(n)
        for n in list(retained):
            if not n.startswith(bed): continue
            if any(t in n for t in ("_PANEL_UPPER","_PANEL_LAP","_SIDE_BRACE","_TOP_FORK_","_X_PIN_","_DP_LANCE_","_HX_HOSE_TAIL","_HX_HOSE_COLLAR","_TIE_NUT_","_TIE_WASHER_")): take(n)
            elif n.startswith(bed+"_TIE_") and int(n.rsplit("_",1)[1]) not in (8,10,12):
                retained[n]=retained[n].translate((-280,0,0))
        # Three bottom rods stay seated. Eleven rods park toward the front, beyond the core path.
        for face,datum,sgn in (("F",265,-1),("R",485,1)):
            p=bed+face+"_"
            for k in range(4):
                key=p+"PARK_NUT_"+str(k)
                retained[key]=retained[key].translate((8.05*sgn,0,0))
            retained[p+"CLAMP_CARRIER"]=retained[p+"CLAMP_CARRIER"].translate((6*sgn,0,0))
            retained[p+"EPDM_DIAPHRAGM"]=face_shape(bellows(6),datum,cy,sgn)
            retained[p+"FACE_GASKET"]=face_shape(ring(4.2,644,1032,622,1008,6),datum,cy,sgn)
        changed={n:s for n,s in retained.items() if n.startswith(bed) and ("_PARK_NUT_" in n or any(n.endswith(x) for x in ("CLAMP_CARRIER","EPDM_DIAPHRAGM","FACE_GASKET")))}
        release_pairs=clashes(changed,{n:s for n,s in retained.items() if n not in changed})+clashes(changed,changed,True)
        water_off=[n for n in w if n.startswith(bed+"_") and n.endswith(("_DETACHABLE_SPOOL","_UNION_632","_UNION_780"))]
        assert len(water_off)==6,water_off
        fixed=dict(retained);fixed.update(d02);fixed.update({n:s for n,s in w.items() if n not in water_off})
        fixed.update({n:s for n,s in core.items() if not n.startswith(bed+"_")})
        bound={n:bb(s) for n,s in fixed.items()}
        candidates=[];dh=[];hits=[]
        for n,s in core.items():
            if not n.startswith(bed+"_"):continue
            ax=bb(s);ax[1 if sign==-1 else 4]+=sign*900
            for key,b in damper_bounds.items():
                if overlaps(ax,b):dh.append([n,key])
            for key,b in bound.items():
                if not overlaps(ax,b):continue
                candidates.append([n,key])
                sweep=cq.Solid.makeBox(ax[3]-ax[0],ax[4]-ax[1],ax[5]-ax[2],cq.Vector(*ax[:3]))
                v=sweep.intersect(fixed[key]).Volume()
                if v<=.001: continue
                # Translation along Y preserves both X and Z. Clip the actual
                # HX solid to the obstacle X/Z slab before bounding its sweep.
                cx0,cz0=max(ax[0],b[0]),max(ax[2],b[2])
                cx1,cz1=min(ax[3],b[3]),min(ax[5],b[5])
                slab=cq.Solid.makeBox(cx1-cx0,ax[4]-ax[1]+2,cz1-cz0,cq.Vector(cx0,ax[1]-1,cz0))
                for seg in s.intersect(slab).Solids():
                    small=bb(seg);small[1 if sign==-1 else 4]+=sign*900
                    pathbox=cq.Solid.makeBox(small[3]-small[0],small[4]-small[1],small[5]-small[2],cq.Vector(*small[:3]))
                    v2=pathbox.intersect(fixed[key]).Volume()
                    if v2>.001: hits.append([n,key,round(v2,3)])
        report[bed]={"shell_sha256":hashlib.sha256((HERE/"C07_SHELL.step").read_bytes()).hexdigest(),"water_removals":sorted(water_off),"travel_mm":sign*900,"moving_core_solids":549,"parked_rods":11,"rod_parking_mm_X":-280,"service_removals":removed,
            "released_carrier_intersections":release_pairs,"box_candidates":candidates,
            "unexcluded_swept_box_pairs":hits,"D01_swept_box_candidates":dh}
        print("SERVICE",bed,len(release_pairs),len(candidates),len(hits),len(dh),hits[:6],flush=True)
        (HERE/"service.json").write_text(json.dumps(report,indent=2))
if __name__=="__main__":
    if "service" in sys.argv:service_checks()
    else:
        port_check()
        static_checks()
