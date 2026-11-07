"""Screen the recovered S0 water island against both reviewed C09 assemblies."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np

root = Path(sys.argv[1])
owner = root / 'C08_HYD_SERIES_S0'
sys.path.insert(0, str(owner / 'source'))
from cad_io import leaves, bb

records = {}
def load(path, expected=None):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if expected is not None:
        assert expected == digest, path
    records[path.name] = digest
    return [(name, solid, bb(solid)) for name, solid in leaves(path)]

def closest(left, right):
    bounds = np.array([b for _, _, b in right])
    best = float('inf')
    witness = None
    for lname, lsolid, lb in left:
        lb = np.array(lb)
        delta = np.maximum(np.maximum(lb[:3] - bounds[:, 3:], bounds[:, :3] - lb[3:]), 0)
        lower = np.linalg.norm(delta, axis=1)
        for i in np.argsort(lower):
            if lower[i] >= best:
                break
            rname, rsolid, _ = right[i]
            distance = lsolid.distance(rsolid)
            if distance < best:
                best, witness = distance, (lname, rname)
    return {'minimum_mm': round(best, 4), 'witness': witness}

sha = json.loads((owner/'SHA256.json').read_text())
water = {}
for key, fname, count in [('water', 'C08_WATER_ISLAND_P0.step', 28),
                           ('tools', 'C08_WATER_SERVICE_P0.step', 22)]:
    water[key] = load(owner/fname, sha[fname])
    assert len(water[key]) == count
c09 = root/'AirTransformerShell/revisions/C09'
checks = {}
def screen(group, items, expected_count):
    assert len(items) == expected_count, (group, len(items))
    checks[group] = {key: closest(v, items) for key, v in water.items()}
    print(group, {k: v['minimum_mm'] for k,v in checks[group].items()}, flush=True)
for state in ['S1', 'S2']:
    file = f'C09_INSTALLED_{state}.step'
    expected = json.loads((c09/f'evidence/readback_{state}.json').read_text())
    assembly = load(c09/'cad'/file, expected['sha256'])
    screen(state, assembly, 2920)
    del assembly
envelopes = load(root/'d03/cad/D03_MOTION_AND_SERVICE.step')
for group, count in [('MOTION',46),('SERVICE',36)]:
    tags = {f'{bed}_{level}_{group}' for bed in 'AB' for level in ('LOWER','UPPER')}
    selected = [item for item in envelopes if tags.intersection(item[0].split('/'))]
    screen(group, selected, count)
print(json.dumps({'sha256':records,'checks':checks},indent=2))
