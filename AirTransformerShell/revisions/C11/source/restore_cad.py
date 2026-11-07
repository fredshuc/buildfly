"""Restore byte-identical large STEP outputs from repository gzip copies."""
from pathlib import Path
import json,gzip,hashlib,shutil
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    manifest=R/'cad/COMPRESSED_STEP_MANIFEST.json'
    if not manifest.exists():print('No compressed CAD manifest; use existing STEP outputs.');return
    for r in json.loads(manifest.read_text()):
        src=R/'cad'/r['compressed'];dst=R/'cad'/r['step']
        assert sha(src)==r['gzip_sha256'],src
        if dst.exists():
            assert sha(dst)==r['step_sha256'],f'Existing STEP differs; preserve it and resolve before restoring: {dst}'
        else:
            with gzip.open(src,'rb') as a,dst.open('xb') as b:shutil.copyfileobj(a,b)
            assert sha(dst)==r['step_sha256']
        print('Verified',dst.name,flush=True)
if __name__=='__main__':run()
