"""RT01-C: census of the C04/C05 pair records (R02/R03): old-WATER exclusion,
pair classes by object kind and host group, and the recurrence statistics."""
import collections, json
from rt01_common import jload, rows, design, save_json

if __name__ == "__main__":
    host = {str(h["index"]): h for h in jload("internal/HOST_CONTEXT.json")}
    kind = {o["id"]: o["kind"] for o in design()["occurrences"]}
    rr = rows("C05_CLASH_DISPOSITION.csv")
    c04h = [r for r in rr if r["source"] == "C04/internal/HOST_INTERSECTIONS.json"]
    water_idx = {k for k, h in host.items() if h["group"] == "WATER"}
    out = dict(
        host_occurrences=len(host),
        water_group=len(water_idx),
        water_group_retained=sum(host[k]["context_retained"] for k in water_idx),
        c04_host_pairs=len(c04h),
        c04_host_pairs_on_WATER=sum(r["host_index"] in water_idx for r in c04h),
        c04_host_pairs_on_unretained=sum(not host.get(r["host_index"], {}).get("context_retained", True) for r in c04h),
        c05_followup=dict(collections.Counter(r["C05_followup"] for r in rr if r["source"].startswith("C04"))))
    c05 = [r for r in rr if r["source"].startswith("internal/")]
    cls = collections.Counter(); vol = collections.Counter()
    for r in c05:
        a = kind.get(r["a"], "?"); b = kind.get(r["b"], "HOST:" + str(host.get(r["host_index"], {}).get("group"))) if r["scope"] == "HOST" else kind.get(r["b"], "?")
        grp = ("ROUTING(pipe/connector/header involved)" if {"PIPE_SPOOL", "CUSTOM_CONNECTOR", "CUSTOM_HEADER", "CUSTOM_ADAPTER", "SEAL"} & {a, b.split(':')[0]}
               else "PLACEMENT(commodity/support vs host/each other)")
        cls[grp] += 1; vol[grp] += float(r["volume_mm3"])
    out["c05_pairs"] = len(c05)
    out["c05_root_groups"] = {k: dict(pairs=v, vol_cm3=round(vol[k] / 1000, 1)) for k, v in cls.items()}
    small = sum(float(r["volume_mm3"]) < 10 for r in c05)
    out["c05_pairs_below_10mm3"] = small
    print(json.dumps(out, indent=1))
    save_json("rt01_clash_census.json", out)
