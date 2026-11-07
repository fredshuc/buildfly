"""Prepare pinned C10 owner inputs without changing any released input."""
from pathlib import Path
import hashlib,json,zipfile,os
def extraction_path(path):
    # The pinned HX archive intentionally retains deep original source paths.
    # Extended Windows paths avoid MAX_PATH without renaming owner evidence.
    return '\\\\?\\'+str(path.resolve()) if os.name=='nt' else str(path)
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[2]
manifest=json.loads((HERE.parent/'C10/INPUTS.json').read_text())
for rel,dest in [('HX/M101_C08_HORIZONTAL_H01/HX_C08_H01_HYDRONIC_RETURN.zip','hx'),
                 ('hydronics/H01_HYD_S2/HYD_S2_WATER_DELTA.zip','hyd')]:
    src=ROOT/rel
    assert hashlib.sha256(src.read_bytes()).hexdigest()==manifest[rel]['sha256']
    out=(HERE/'.work'/dest).resolve();out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(src) as z:
        assert all((out/n).resolve().is_relative_to(out) for n in z.namelist())
        assert z.testzip() is None
        z.extractall(extraction_path(out))
    print('Verified and extracted',rel,flush=True)
src=HERE/'inputs/C11_HYD_T01_R1_CANDIDATE.zip'
assert hashlib.sha256(src.read_bytes()).hexdigest()=='d1a7429701c5786df42d720a8baea2a3bb63ee17c70fefd97fd9166c08ed4f9c'
out=(HERE/'.work/hyd_c11').resolve();out.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(src) as z:
    assert all((out/n).resolve().is_relative_to(out) for n in z.namelist())
    assert z.testzip() is None
    z.extractall(extraction_path(out))
print('Verified C11 hydronics candidate d1a74297',flush=True)
src=HERE/'inputs/C11_D05_DAMPERS_REVIEW.zip'
assert hashlib.sha256(src.read_bytes()).hexdigest()=='b91a15555c282efc3cec27fd62bebdd62de2500bc53f32a909605ecaeeddf837'
out=(HERE/'.work/d05').resolve();out.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(src) as z:
    assert all((out/n).resolve().is_relative_to(out) for n in z.namelist())
    assert z.testzip() is None
    z.extractall(extraction_path(out))
print('Verified D05 candidate b91a1555',flush=True)
src=HERE/'inputs/HX_M101_C10_H02_RETURN_20261107.zip'
assert hashlib.sha256(src.read_bytes()).hexdigest()=='b0fbc5cf3bbcbaeeb0dd0e43a6bdb596389bf00abdbcad51519a115a577bda5b'
out=(HERE/'.work/h02').resolve();out.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(src) as z:
    assert all((out/n).resolve().is_relative_to(out) for n in z.namelist())
    assert z.testzip() is None
    z.extractall(extraction_path(out))
print('Verified final H02 review return b0fbc5cf',flush=True)
