"""Bound full single-axis travel of the screens, upper skins and removable tie rods."""
import hashlib,json
import cadquery as cq
from cad_io import bb, overlaps
from integrate_c07 import HERE, installation
from build_c07 import box, xhole
def main():
    shell,supports,hx,water,dampers=installation()
    fixed={**shell,**supports,**hx,**water,**dampers}
    boxes={n:bb(s) for n,s in fixed.items()}
    report={"shell_sha256":hashlib.sha256((HERE/"C07_SHELL.step").read_bytes()).hexdigest(),"strokes_mm":{"screens":800,"rod_park_minus_X":280,"upper_skin_outboard":150},
            "screen_paths":{},"rod_paths":{},"upper_skin_paths":{}}
    def check(shape,ignore):
        a=bb(shape);hits=[]
        for n,b in boxes.items():
            if n in ignore or not overlaps(a,b):continue
            v=shape.intersect(fixed[n]).Volume()
            if v>.001: hits.append((n,round(v,4)))
        return hits
    for bed,sgn in (("A",-1),("B",1)):
        trim={n for n in shell if n.startswith(bed) and any(k in n for k in ("_PANEL_UPPER","_PANEL_LAP","_SIDE_BRACE"))}
        # The upper skin has no drive cut-outs. Its solid rectangular envelope
        # is a conservative continuous sweep after undoing the lap and strap.
        n=bed+"_PANEL_UPPER"
        x0,y0,z0,x1,y1,z1=boxes[n]
        sweep=box(x0,y0+min(sgn*150,0),z0,x1-x0,y1-y0+150,z1-z0)
        report["upper_skin_paths"][bed]=check(sweep,trim)
        for face in ("F","R"):
            prefix=bed+face+"_"
            ignore=trim|{prefix+"SCREEN_ACCESS_LID",prefix+"SCREEN_ACCESS_SEAL"}
            for i in range(8):
                n=prefix+"SCREEN_%02d"%i
                x0,y0,z0,x1,y1,z1=boxes[n]
                sweep=box(x0,y0+min(sgn*800,0),z0,x1-x0,y1-y0+800,z1-z0)
                report["screen_paths"][n]=check(sweep,ignore|{n})
        nuts={n for n in shell if n.startswith(bed) and ("_TIE_NUT_" in n or "_TIE_WASHER_" in n)}
        for j in (*range(8),9,11,13):
            n=bed+"_TIE_"+str(j)
            x0,y0,z0,x1,y1,z1=boxes[n]
            sweep=xhole(x0-280,(y0+y1)/2,(z0+z1)/2,4,x1-x0+280)
            report["rod_paths"][n]=check(sweep,nuts|trim|{n})
    (HERE/"access_paths.json").write_text(json.dumps(report,indent=2))
    for group in ("screen_paths","rod_paths","upper_skin_paths"):
        bad={n:h for n,h in report[group].items() if h}
        print(group,len(report[group]),bad,flush=True)
if __name__=="__main__":
    main()
