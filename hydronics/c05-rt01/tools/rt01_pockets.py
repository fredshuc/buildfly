"""RT01-P: air-trap (local high) and undrainable (local low) pockets created
inside each spool by vertical U-jogs. A pocket is a run of non-rising/non-
falling segments whose neighbours both fall (high) or both rise (low), with a
height difference >= 1 OD. Pockets at spool ends are excluded (they belong to
the header/valve node, which has AV/DV taps on headers only)."""
import collections
from rt01_common import design, save_csv

if __name__ == "__main__":
    out = []
    for e, r in design()["pipe_routes"].items():
        z = [p[2] for p in r["points"]]
        # compress consecutive equal z
        zz = [z[0]] + [b for a, b in zip(z, z[1:]) if abs(b - a) > 1e-6]
        hi = lo = 0
        for i in range(1, len(zz) - 1):
            if zz[i] - max(zz[i - 1], zz[i + 1]) >= r["OD_mm"]:
                hi += 1
            if min(zz[i - 1], zz[i + 1]) - zz[i] >= r["OD_mm"]:
                lo += 1
        if hi or lo:
            out.append(dict(edge=e, kind=r["kind"], OD_mm=r["OD_mm"], high_pockets=hi, low_pockets=lo))
    save_csv("rt01_pockets.csv", out)
    c = collections.Counter()
    for o in out:
        c[(o["OD_mm"], "high")] += o["high_pockets"]; c[(o["OD_mm"], "low")] += o["low_pockets"]
    print(len(out), "spools with internal pockets;", dict(c))
    print([ (o["edge"], o["high_pockets"], o["low_pockets"]) for o in out if o["OD_mm"] == 33.7])
