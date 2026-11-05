import os, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for d in [ROOT.parent/'R5_WORK/early_vendor',ROOT.parent/'R5_WORK/runtime_ready']:
    if d.exists(): sys.path.insert(0,str(d))
os.environ.setdefault('MPLBACKEND','Agg')
