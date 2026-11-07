"""Verify owner releases and extract a bounded local rebuild cache."""
from pathlib import Path
import json,hashlib,zipfile
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[2];WORK=HERE/'.work'
targets={
 'HX/M101_C08_HORIZONTAL_H01/HX_C08_H01_HYDRONIC_RETURN.zip':'hx',
 'hydronics/H01_HYD_S2/HYD_S2_WATER_DELTA.zip':'hyd',
 'dampers/c09r1-d04/D04_PIN_W2_REVIEW.zip':'d04',
 'AirTransformerShell/revisions/C10/inputs/D03_MOTION_AND_SERVICE.zip':'.',
}
manifest=json.loads((HERE/'INPUTS.json').read_text())
for rel,dest in targets.items():
    p=ROOT/rel
    assert hashlib.sha256(p.read_bytes()).hexdigest()==manifest[rel]['sha256'],rel
    out=(WORK/dest).resolve();out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None
        assert all((out/n).resolve().is_relative_to(out) for n in z.namelist())
        z.extractall(out)
    print('Verified',rel,flush=True)
