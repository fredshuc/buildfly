"""Independent maintenance mock-up. Keep the water trees, vents and headers fixed."""
import json
import hashlib
import cadquery as cq
from cad_io import bb, named, leaves, overlaps
from integrate_c07 import HERE, D01, D02, merged_water, installed_cores
from build_c07 import box, xhole

def main():
    shell=named(HERE/"C07_SHELL.step")
    cores=installed_cores()
    water=merged_water()
    supports=named(D02/"cad/D02_DAMPER_SUPPORTS.step")
    fixed={**shell,**cores,**water,**supports}
    assert len(fixed)==sum(map(len,(shell,cores,water,supports)))
    bounds={name:bb(shape) for name,shape in fixed.items()}
    result={"shell_sha256":hashlib.sha256((HERE/"C07_SHELL.step").read_bytes()).hexdigest(),"beds":{}}
    all_paths=[]
    def contacts(shape,omit,extra=()):
        a=bb(shape);hits=[]
        for n,b in bounds.items():
            if n in omit or not overlaps(a,b):continue
            v=shape.intersect(fixed[n]).Volume()
            if v>.001: hits.append((n,round(v,5)))
        for n,part in extra:
            if overlaps(a,bb(part)):
                v=shape.intersect(part).Volume()
                if v>.001:hits.append((n,round(v,5)))
        return hits
    for bed,sign,order in (("A",-1,("W2","W1")),("B",1,("W1","W2"))):
        datum=bed+"_GLAND_RT1"
        plate=shell[datum]
        plate_x=bb(plate)[0]
        profile=[f for f in plate.Faces() if max(abs(bb(f)[j]-plate_x) for j in (0,3))<.0001]
        assert len(profile)==1
        endplate=plate.translate((60,0,0))
        proj=cq.Solid.extrudeLinear(profile[0].outerWire(),profile[0].innerWires(),cq.Vector(62,0,0))
        pulls={n for n in shell if n.startswith(bed) and any(k in n for k in ("_PANEL_UPPER","_PANEL_LAP","_SIDE_BRACE"))}
        pulls.add(datum)
        found=contacts(proj,pulls)
        all_paths.append((bed+"_gland",proj))
        print(bed,"gland",found,flush=True)
        rows=[]
        for tag in order:
            names=[n for n in water if n.startswith(bed+"_"+tag+"_") and ("DETACHABLE_SPOOL" in n or "_UNION_" in n)]
            assert len(names)==3,names
            pulls.update(names)
            row={"port":bed+"."+tag,"travel_y_mm":sign*930,"parts":{}}
            for n in names:
                x0,y0,z0,x1,y1,z1=bounds[n]
                r=(z1-z0)/2;y=(y0+y1)/2;z=(z0+z1)/2
                assert abs((y1-y0)/2-r)<.0001
                end=y+sign*930
                # Translating a filled X-cylinder in Y creates a YZ stadium.
                # Filling the union and spool bores makes this conservative.
                path=box(x0,min(y,end),z0,x1-x0,930,z1-z0).fuse(
                     xhole(x0,y,z,r,x1-x0),xhole(x0,end,z,r,x1-x0)).clean()
                hits=contacts(path,pulls,[(bed+"_parked_gland",endplate)])
                row["parts"][n]={"x_mm":(x0,x1),"diameter_mm":2*r,"hits":hits}
                all_paths.append((n,path))
            rows.append(row)
            print(bed,tag,rows[-1],flush=True)
        result["beds"][bed]={"gland_x_start_mm":list((bb(plate)[0],bb(plate)[3])),"gland_x_park_mm":list((bb(endplate)[0],bb(endplate)[3])),"gland_hits":found,"spool_rows":rows}
    result["fixed_counts_without_d01"]={"shell":len(shell),"HX":len(cores),"water":len(water),"D02":len(supports)}
    (HERE/"rt3_water_access.json").write_text(json.dumps(result,indent=2))
    damper={n:bb(s) for n,s in leaves(D01/"cad/D01_EIGHT_DAMPERS_INSTALLED.step") if "/HOST/" not in n}
    result["D01_occurrences"]=len(damper)
    path_boxes=[(p,bb(s)) for p,s in all_paths]
    result["D01_bbox_candidates"]=[(p,n) for p,a in path_boxes for n,b in damper.items() if overlaps(a,b)]
    print("D01 candidates",len(damper),len(result["D01_bbox_candidates"]),flush=True)
    (HERE/"rt3_water_access.json").write_text(json.dumps(result,indent=2))
if __name__=="__main__":
    main()