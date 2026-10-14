"""RT01-V2: water shuttled through a direct bed EV at each hot/cold reversal,
and the minimum vessel size for both directions at 0.7 barg precharge.
Isothermal gas; Vw(p) = Vn (1 - p0/p). On reversal a bed changes from one
source to the other, so the pressure at its EV changes by the source static
difference plus the flow-induced change (inlet <-> outlet of the bed)."""
from rt01_common import rows, save_json

ATM = 1.01325

def vw(vn, p0g, pg):
    p0, p = p0g + ATM, pg + ATM
    return max(0.0, vn * (1 - p0 / p))

if __name__ == "__main__":
    out = {"shuttle_L_per_EV_per_reversal": []}
    for vn in (12.0, 8.0):
        for p0g in (1.0, 0.7):
            for base in (1.0, 1.5):
                for dp in (0.2, 0.5, 1.0):        # bar change at the EV on reversal
                    out["shuttle_L_per_EV_per_reversal"].append(dict(
                        Vn_L=vn, precharge_barg=p0g, p_low_barg=base, dp_bar=dp,
                        shuttle_L=round(vw(vn, p0g, base + dp) - vw(vn, p0g, base), 3)))
    # minimum Vn: contraction 0.483 L (+0.2 L seal) at p_min, expansion 0.590 L from p_max to 2.8 barg
    p0g, pmin, pmax, pfin = 0.7, 1.0, 2.0, 2.8
    need = None
    for i in range(10, 200):
        vn = i / 10
        ok_c = vw(vn, p0g, pmin) >= 0.483 + 0.2
        v_hi = vw(vn, p0g, pmax) + 0.590
        ok_x = v_hi < vn and (p0g + ATM) / (1 - v_hi / vn) - ATM <= pfin
        if ok_c and ok_x:
            need = vn; break
    out["min_Vn_L_at_0p7barg_precharge_1to2barg"] = need
    # placement clash volume of the four EVs
    rr = [r for r in rows("C05_CLASH_DISPOSITION.csv") if r["source"].startswith("internal/")]
    ev = [r for r in rr if r["a"].startswith("C05_EV_") or r["b"].startswith("C05_EV_")]
    out["EV_pairs"] = len(ev)
    out["EV_overlap_cm3"] = round(sum(float(r["volume_mm3"]) for r in ev) / 1000, 1)
    out["all_C05_overlap_cm3"] = round(sum(float(r["volume_mm3"]) for r in rr) / 1000, 1)
    save_json("rt01_ev_shuttle.json", out)
    for r in out["shuttle_L_per_EV_per_reversal"]:
        if r["Vn_L"] == 12.0 and r["precharge_barg"] == 1.0:
            print(r)
    print({k: v for k, v in out.items() if k != "shuttle_L_per_EV_per_reversal"})
