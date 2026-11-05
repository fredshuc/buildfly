"""Independent stepwise HX withdrawal sweep for C07 (exact solids at each 25 mm step).
Usage: python c07_sweep.py <repo root> <delivered C07_SHELL.step> <out.json>
Service state per the handoff: upper panel, lap, strap, forks, X pins, probes, hose tail/collar, tie nuts and
washers removed; carriers, gaskets and diaphragms released 6 mm; park nuts advanced 8.05 mm; 11 rods parked
280 mm toward -X; two spools and four loose collars per bed removed; D02 and retained water included.
D01 is screened by bounding box only, as in the delivered check. Also reports the minimum stepwise distance
from the moving frame plates to the outboard park-guide studs."""
import sys,json,math
from pathlib import Path
root,shellstep,outp=Path(sys.argv[1]),sys.argv[2],sys.argv[3]
C07=root/"AirTransformerShell/revisions/C07";sys.path.insert(0,str(C07));sys.path.insert(0,str(root/"AirTransformerShell/revisions/C04"))
import cadquery as cq
from cad_io import named,bb,leaves,overlaps
from build_c07 import face_shape,ring,bellows
from integrate_c07 import installed_cores,merged_water,D01,D02
shell=named(shellstep);core=installed_cores();water=merged_water();d02=named(D02/"cad/D02_DAMPER_SUPPORTS.step")
d01b=[bb(s) for n,s in leaves(D01/"cad/D01_EIGHT_DAMPERS_INSTALLED.step") if "/HOST/" not in n]
R={}
for bed,sign in (("A",-1),("B",1)):
    cy={"A":-434.4,"B":845.6}[bed]
    svc=dict(shell)
    for face,datum,sgn in (("F",265,-1),("R",485,1)):
        p=bed+face+"_"
        svc[p+"CLAMP_CARRIER"]=shell[p+"CLAMP_CARRIER"].translate((6*sgn,0,0))
        svc[p+"EPDM_DIAPHRAGM"]=face_shape(bellows(6),datum,cy,sgn)
        svc[p+"FACE_GASKET"]=face_shape(ring(4.2,644,1032,622,1008,6),datum,cy,sgn)
        for k in range(4):svc[p+"PARK_NUT_"+str(k)]=shell[p+"PARK_NUT_"+str(k)].translate((8.05*sgn,0,0))
    for n in list(svc):
        if n.startswith(bed+"_TIE_") and not any(t in n for t in ("NUT","WASHER")) and int(n.rsplit("_",1)[1]) not in (8,10,12):
            svc[n]=svc[n].translate((-280,0,0))
    for n in [n for n in svc if n.startswith(bed) and any(t in n for t in ("_PANEL_UPPER","_PANEL_LAP","_SIDE_BRACE","_TOP_FORK_","_X_PIN_","_DP_LANCE_","_HX_HOSE_TAIL","_HX_HOSE_COLLAR","_TIE_NUT_","_TIE_WASHER_"))]:del svc[n]
    fixed={**svc,**d02,**{n:s for n,s in water.items() if not (n.startswith(bed+"_") and n.endswith(("_DETACHABLE_SPOOL","_UNION_632","_UNION_780")))},
           **{n:s for n,s in core.items() if not n.startswith(bed+"_")}}
    FB={n:bb(s) for n,s in fixed.items()}
    mov=[(n,s,bb(s)) for n,s in core.items() if n.startswith(bed+"_")]
    hits={};d01hits=0;step=25
    for d in range(step,900+step,step):
        off=(0,sign*d,0)
        for n,s,b in mov:
            q=[b[0],b[1]+off[1],b[2],b[3],b[4]+off[1],b[5]]
            for k,fb in FB.items():
                if k in hits or not overlaps(q,fb):continue
                v=s.translate(cq.Vector(*off)).intersect(fixed[k]).Volume()
                if v>1e-3:hits[k]=[d,n,round(v,3)]
            if d==900:
                d01hits+=sum(1 for b2 in d01b if overlaps([b[0],min(b[1],b[1]+off[1]),b[2],b[3],max(b[4],b[4]+off[1]),b[5]],b2))
    # minimum distance moving frame plates <-> outboard park-guide studs over the stroke
    plates=[(n,s) for n,s,b in mov if round(b[3]-b[0],3)==8]
    studs=[svc[bed+f+"_PARK_GUIDE_"+str(k)] for f in ("F","R") for k in range(4)]
    dmin=min(cq.Shape.distance(s.translate(cq.Vector(0,sign*d,0)),t) for d in range(0,901,50) for n,s in plates for t in studs)
    R[bed]=dict(step_mm=step,travel_mm=900*sign,first_intersections=hits,D01_swept_bbox_candidates=d01hits,
        min_distance_frame_plates_to_park_guides_over_stroke_mm=round(dmin,3))
    print(bed,R[bed],flush=True)
json.dump(R,open(outp,'w'),indent=1)
