"""Shared loaders for the RT-01 review of AT-HYD3-MFG-C05 R1.

All tools are read-only on the delivered package. Set HYD3_PKG to the folder
where the reassembled AT_HYD3_RT01_ENGLISH_MANUAL_REVIEW_20261014.zip was
extracted (the folder that contains 00_START_HERE.html).
"""
from pathlib import Path
import json, csv, os, math

PKG = Path(os.environ.get("HYD3_PKG", "")).expanduser()
ENG = PKG / "engineering"
OUT = Path(__file__).resolve().parents[1] / "results"


def need_pkg():
    if not (ENG / "cad" / "C05_NATIVE_DESIGN.json").is_file():
        raise SystemExit("Set HYD3_PKG to the extracted RT01 review package root")


def jload(rel):
    return json.loads((ENG / rel).read_text(encoding="utf-8-sig"))


def rows(rel):
    with (ENG / rel).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def save_json(name, obj):
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(json.dumps(obj, indent=1, default=float), encoding="utf-8")


def save_csv(name, rr):
    OUT.mkdir(exist_ok=True)
    keys = list(dict.fromkeys(k for r in rr for k in r))
    with (OUT / name).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rr)


def design():
    need_pkg()
    return jload("cad/C05_NATIVE_DESIGN.json")


def graph():
    return jload("functional_baseline/C05_FLOW_GRAPH.json")


def headers():
    return {h["node"]: h for h in jload("internal/C05_HEADER_DEFINITIONS.json")}


def connections():
    return {c["port"]: c for c in jload("internal/C05_INSTALLED_CONNECTIONS.json")}


def unit(v):
    n = math.sqrt(sum(x * x for x in v))
    return [x / n for x in v]


def sub(a, b):
    return [x - y for x, y in zip(a, b)]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))
