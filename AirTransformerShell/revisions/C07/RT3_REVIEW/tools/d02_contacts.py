"""Usage: python d02_contacts.py <repo root> <out.json>
Planar contact area between each D02 *_SHOE and the D01 P101/R101 (or mirrored) metal end frames in the installed
STEPs; plus the shoe-boss width vs the 3 mm flange and the in-plane margin of each contact patch to the flange faces."""
import sys,json,csv
from pathlib import Path
root,outp=Path(sys.argv[1]),sys.argv[2]
sys.path.insert(0,str(root/"AirTransformerShell/revisions/C07"))
from cad_io import named,leaves,bb,overlaps
d02=named(root/"dampers/c06-d02/cad/D02_DAMPER_SUPPORTS.step")
shoes={n:s for n,s in d02.items() if n.endswith("_SHOE")}
pts={r["shoe"]:r for r in csv.DictReader(open(root/"dampers/c06-d02/evidence/D02_BEARING_POINTS.csv",encoding="utf-8-sig"))}
frames={}
for n,s in leaves(root/"dampers/c04-d01/cad/D01_EIGHT_DAMPERS_INSTALLED.step"):
    if "/HOST/" in n:continue
    leaf=n.split("/")
    if any(t in n for t in ("P101","R101")):frames["/".join(leaf[-3:])]=s
res={};tol=1e-3
for sn,s in shoes.items():
    sb=bb(s);best=(0,None)
    for fn,f in frames.items():
        fb=bb(f)
        if not all(min(sb[k+3],fb[k+3])-max(sb[k],fb[k])>=-tol for k in range(3)):continue
        top=[fc for fc in s.Faces() if abs(bb(fc)[2]-bb(fc)[5])<1e-6]
        bot=[fc for fc in f.Faces() if abs(bb(fc)[2]-bb(fc)[5])<1e-6]
        a=sum(x.intersect(y).Area() for x in top for y in bot if abs(bb(x)[2]-bb(y)[2])<1e-4)
        if a>best[0]:best=(a,fn,fb)
    a,fn,fb=best
    res[sn]=dict(contact_mm2=round(a,2),frame=fn,frame_x_thickness_mm=round(fb[3]-fb[0],3) if fb else None,
                 listed_mm2=float(pts[sn]["metal_contact_mm2"]) if sn in pts else None)
vals=[v["contact_mm2"] for v in res.values()]
summary=dict(shoes=len(res),min_mm2=min(vals),max_mm2=max(vals),n_below_listed=sum(1 for v in res.values() if v["listed_mm2"] and v["contact_mm2"]<v["listed_mm2"]-0.5))
json.dump(dict(summary=summary,shoes=res),open(outp,'w'),indent=1);print(summary)
