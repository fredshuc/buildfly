"""RT01-0: verify the review edition against its own MANIFEST.json (3,326
payloads) without executing any package script."""
import hashlib, json
from rt01_common import PKG, need_pkg, save_json

if __name__ == "__main__":
    need_pkg()
    m = json.loads((PKG / "MANIFEST.json").read_text(encoding="utf-8"))
    bad = []
    for r in m["files"]:
        p = PKG / r["path"]
        if not p.is_file():
            bad.append((r["path"], "MISSING")); continue
        b = p.read_bytes()
        if len(b) != r["bytes"] or hashlib.sha256(b).hexdigest() != r["sha256"]:
            bad.append((r["path"], "MISMATCH"))
    out = dict(payloads=len(m["files"]), mismatches=len(bad), detail=bad[:20])
    save_json("rt01_manifest.json", out); print(out)
