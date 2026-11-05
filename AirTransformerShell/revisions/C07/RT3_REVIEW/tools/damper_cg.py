"""Usage: python damper_cg.py <repo root> <out.json>
Independent steel-equivalent CG of the installed D01 AFP and AFR product occurrences (excluding the obsolete HOST),
compared with the D02 bearing points; derives the tipping-limit actuator mass about the drive-side bearing line
for an actuator centred in the D01 reserve and at its outboard face."""
import sys,json,csv
from pathlib import Path
root,outp=Path(sys.argv[1]),sys.argv[2]
sys.path.insert(0,str(root/"AirTransformerShell/revisions/C07"))
from cad_io import leaves
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
pts=list(csv.DictReader(open(root/"dampers/c06-d02/evidence/D02_BEARING_POINTS.csv",encoding="utf-8-sig")))
res={}
acc={k:[0,0,0,0] for k in ("AFP","AFR")}
for n,s in leaves(root/"dampers/c04-d01/cad/D01_EIGHT_DAMPERS_INSTALLED.step"):
    if "/HOST/" in n:continue
    for k in acc:
        if "/"+k+"/" in "/"+n+"/" or n.split("/")[1:2]==[k]:
            g=GProp_GProps();BRepGProp.VolumeProperties_s(s.wrapped,g);v=abs(g.Mass());c=g.CentreOfMass()
            a=acc[k];a[0]+=v;a[1]+=v*c.X();a[2]+=v*c.Y();a[3]+=v*c.Z()
reserve={"AFP":(-1315.9,-1565.9),"AFR":(-1315.9,-1565.9)}
for k,(v,x,y,z) in acc.items():
    m=v*7.85e-6;cg=(x/v,y/v,z/v)
    p=[r for r in pts if r["valve"]==k];ys=sorted({float(r["y"]) for r in p});xs=sorted({float(r["x"]) for r in p})
    drive_line=ys[0]  # bed A drives are toward -Y
    arm_w=cg[1]-drive_line
    lim={}
    for label,ya in (("reserve_centre",sum(reserve[k])/2),("reserve_outboard_face",reserve[k][1])):
        lim[label]=round(m*arm_w/(drive_line-ya),2)
    res[k]=dict(steel_equivalent_kg=round(m,2),cg_mm=[round(c,1) for c in cg],bearing_y_mm=ys,bearing_x_mm=xs,
        drive_side_pair_fraction=round((ys[1]-cg[1])/(ys[1]-ys[0]),4),inner_pair_fraction=round((cg[0]-xs[0])/(xs[1]-xs[0]),4) if xs else None,
        tipping_limit_actuator_kg_no_inset=lim)
print(json.dumps(res,indent=1));json.dump(res,open(outp,'w'),indent=1)
