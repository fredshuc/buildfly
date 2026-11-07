"""Non-mutating ShapeFix probe of invalid installed H02 valve occurrences."""
from common import *
from OCP.ShapeFix import ShapeFix_Shape
def run():
    folder=WORK/'installed_S1';src=folder/'index.json'
    if not src.exists():src=folder/'partial.json'
    data=json.loads(src.read_text());rows=[r for r in data['parts'] if not r.get('valid',True) and r['name'].startswith('A_LOWER__')]
    report=[];shapes={}
    for r in rows:
        s=cq.Shape.importBrep(str(folder/r['file']));f=ShapeFix_Shape(s.wrapped);f.SetPrecision(1e-6);f.SetMaxTolerance(.01);f.Perform();q=cq.Shape.cast(f.Shape())
        one={'part':r['name'],'installed_valid':s.isValid(),'probe_valid':q.isValid(),'volume_delta_mm3':q.Volume()-s.Volume(),'bbox_max_delta_mm':max(abs(a-b) for a,b in zip(bb(s),bb(q))),'status':'DIAGNOSTIC_ONLY_NOT_APPLIED_TO_INSTALLED_CAD'}
        report.append(one);shapes[r['name']]=q;print(one,flush=True)
    if shapes:
        path=WORK/'INVALID_REPAIR_PROBE.step';save(shapes,path)
        reread=named(path)
        for r in report:r['probe_STEP_roundtrip_valid']=reread[r['part']].isValid()
    dump(E/'invalid_solid_diagnostic.json',{'source_assembly_sha256':data['sha256'],'scope':'A lower canonical invalid valve occurrences available at probe time. Any repair requires complete exported-assembly revalidation; this probe does not alter pinned owners or installed STEP.','parts':report})
if __name__=='__main__':run()
