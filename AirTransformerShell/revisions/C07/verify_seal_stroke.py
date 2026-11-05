"""Sample the C07 seal release stroke; measure both end contacts of four parking studs."""
import hashlib,json,math
from cad_io import named,bb,clashes
from integrate_c07 import HERE,installed_cores
from build_c07 import face_shape,ring,bellows
def end_faces(shape,x):
    return [f for f in shape.Faces() if all(abs(bb(f)[i]-x)<1e-5 for i in (0,3))]
def area(first,second,x):
    return sum(a.intersect(b).Area() for a in end_faces(first,x) for b in end_faces(second,x))
def main():
    base=named(HERE/"C07_SHELL.step")
    # AF is a representative section. Four full-machine service faces are
    # tested separately by integrate_c07.py service.
    installed={k:v for k,v in base.items() if k.startswith("AF_")}
    stationary={k:v for k,v in installed.items() if not any(q in k for q in
        ("CLAMP_CARRIER","EPDM_DIAPHRAGM","FACE_GASKET","PARK_NUT_","TIE_NUT_","TIE_WASHER_"))}
    fixed={**stationary,**{k:v for k,v in installed_cores().items() if k.startswith("A_")}}
    stages={}
    for stroke in range(7):
        carrier=installed["AF_CLAMP_CARRIER"].translate((-stroke,0,0))
        rubber=face_shape(bellows(stroke),265,-434.4,-1)
        depth=min(6,4.2+stroke)
        gasket=face_shape(ring(4.2+stroke-depth,644,1032,622,1008,depth),265,-434.4,-1)
        nuts={"AF_PARK_NUT_"+str(i):installed["AF_PARK_NUT_"+str(i)].translate((-stroke-2.05 if stroke else 0,0,0)) for i in range(4)}
        moving={"carrier":carrier,"secondary_bellows":rubber,"face_gasket":gasket,**nuts}
        entry={"positive_intersections":clashes(moving,fixed)+clashes(moving,moving,True)}
        if stroke==6:
            entry["positive_stop_mm2"]=[round(area(carrier,stationary["AF_PARK_GUIDE_"+str(i)],265-32.2),3) for i in range(4)]
            entry["opposed_push_nut_mm2"]=[round(area(carrier,nuts["AF_PARK_NUT_"+str(i)],265-12.2),3) for i in range(4)]
        stages[stroke]=entry
    result={"shell_sha256":hashlib.sha256((HERE/"C07_SHELL.step").read_bytes()).hexdigest(),"face":"AF","stroke_samples_mm":stages,"operating_push_nut_axial_daylight_mm":2.05,
       "operating_stop_sleeve_axial_daylight_mm":6,"service_guide_bore_diameter_mm":9.3,
       "straight_meridians_mm":{"Y":23.154961,"Z":20.608279},
       "scope":"Seven nominal poses. Corner strain, pressure reversal, adhesion, wear and tolerances require a specimen test."}
    (HERE/"seal_stroke.json").write_text(json.dumps(result,indent=2))
    print(json.dumps(stages),flush=True)
    assert all(not s["positive_intersections"] for s in stages.values())
    assert all(a>0 for a in stages[6]["positive_stop_mm2"]+stages[6]["opposed_push_nut_mm2"])
if __name__=="__main__":
    main()
