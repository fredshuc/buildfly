"""Check all owner segmented rotation bounds against C07 installed shell, supports, water and both cores."""
from pathlib import Path
import sys, json, hashlib
import numpy as np
out = Path(__file__).resolve().parent
source = Path(sys.argv[1]).resolve() / "source"
sys.path.insert(0, str(source))
import bootstrap
from native import load, bb, box
from build import CFG, product_placement, place_bound, swept_test_bounds
# Use the exact moving-part selection and continuous bounds from the owner.
owner = (source / "check_motion_interfaces.py").read_text(encoding="utf-8")
exec(owner[owner.index("_,products=load()"):owner.index("hits=[];candidates=0")])
from cad_io import leaves
from integrate_c07 import D02, merged_water, installed_cores
shell=list(leaves(out/"C07_SHELL.step"))
shell.extend(leaves(D02/"cad/D02_DAMPER_SUPPORTS.step"))
shell.extend(merged_water().items())
shell.extend(installed_cores().items())
bounds=np.array([bb(s) for _,s in shell])
hits=[]; candidates=0
assert len(moving)==600 and len(shell)>1700
for m in moving:
    b=m["bounds"]
    mask=np.all(np.minimum(bounds[:,3:],b[3:])-np.maximum(bounds[:,:3],b[:3])>1e-5, axis=1)
    for i in np.flatnonzero(mask):
        candidates+=1
        vol=shell[i][1].intersect(box(b)).Volume()
        if vol>0.001: hits.append([m["valve"],m["part"],shell[i][0],vol])
report=dict(shell_sha256=hashlib.sha256((out/"C07_SHELL.step").read_bytes()).hexdigest(),segment_bounds=len(moving),stationary_occurrences=len(shell),candidates=candidates,intersections=hits)
(out/"motion_shell.json").write_text(json.dumps(report,indent=2))
print(report)
