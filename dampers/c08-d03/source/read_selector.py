"""Restore every DAMPER-group member of the same parent used by shell2."""
from geometry import *
import re
PARENT=Path(os.environ.get("M2_FULL_STEP",Path.home()/"Documents/Codex/2026-09-25/airtransformer-m4-in1/work/m2_in2_g0_work/inputs/R1/outputs/V050_SM_M2_IN1_R1_SOR_CANDIDATE.step"))
PARENT_SHA="1876d5f244933f145d9a5f1e9adaafca5ed9a168663eca60e45121cb4b0fc53a"

def prepare():
    out=WORK/"selector"
    out.mkdir(parents=True,exist_ok=True)
    idx=out/"index.json"
    bundle=ROOT/"inputs/M2_SELECTOR_SOURCE.zip"
    if bundle.exists():
        with zipfile.ZipFile(bundle) as z:
            index=json.loads(z.read("index.json"))
            assert index["sha"]==PARENT_SHA and len(index["rows"])==114
            files={r[0] for r in index["rows"].values()}|{"index.json"}
            assert set(z.namelist())==files
            for f in files:
                data=z.read(f)
                if f!="index.json":assert hashlib.sha256(data).hexdigest()==index["files"][f]
                (out/f).write_bytes(data)
        return
    sha=hashlib.sha256(PARENT.read_bytes()).hexdigest()
    assert sha==PARENT_SHA
    if idx.exists() and json.loads(idx.read_text()).get("schema")==2 and json.loads(idx.read_text())["sha"]==sha:return
    rows={}
    for key,s in leaves(PARENT):
        seq=key.split("/")
        n=seq[-2]
        if "ASM_DAMPER_O" not in seq and not re.search(r"REF_(AIR_LOCAL_ACTUATOR|AIR_DIRECT_COUPLING|INNER_BEARING|OUTER_BEARING)|M203_(ACT_SPACERS|ACT_M6|INNER_M6)",n):continue
        if n in rows:raise ValueError(key)
        f=f"{len(rows)}.brep";s.exportBrep(str(out/f))
        rows[n]=[f,bb(s),seq[-4]]
    assert len(rows)>60, len(rows)
    save_json(idx,dict(sha=sha,schema=2,rows=rows))
if __name__=="__main__": prepare()
