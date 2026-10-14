"""RT01-R07: independent read-back of HYD3_C05_S1/S2 AP242: solid count and
volumes vs the native occurrence table (356 physical + state indicators)."""
import sys, json
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
from rt01_common import ENG, design, save_json
from rt01_occ import volume

if __name__ == "__main__":
    nat = design()["occurrences"]
    vnat = sorted(o["volume_mm3"] for o in nat)
    out = {}
    for st in ("S1", "S2"):
        r = STEPControl_Reader()
        assert r.ReadFile(str(ENG / f"cad/HYD3_C05_{st}_AP242.step")) == IFSelect_RetDone
        r.TransferRoots(); s = r.OneShape()
        e = TopExp_Explorer(s, TopAbs_SOLID); vols = []
        while e.More():
            vols.append(volume(e.Current())); e.Next()
        vols.sort()
        # greedy match of each native occurrence volume to a STEP solid volume
        pool = list(vols); unmatched = []
        for v in vnat:
            j = min(range(len(pool)), key=lambda i: abs(pool[i] - v))
            if abs(pool[j] - v) <= 1e-4 * max(v, 1):
                pool.pop(j)
            else:
                unmatched.append(v)
        out[st] = dict(solids=len(vols), total_volume_mm3=sum(vols), native_total_mm3=sum(vnat),
                       native_unmatched=len(unmatched), extra_step_solids=len(pool),
                       extra_volumes_mm3=[round(x, 1) for x in pool][:10])
        print(st, out[st], flush=True)
    save_json("rt01_step_readback.json", out)
