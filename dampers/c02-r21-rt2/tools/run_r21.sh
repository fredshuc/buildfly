#!/usr/bin/env bash
# Reproduce the RT-2 results from the two R21 delivery zips. The package is read as data; no project script is run.
# Usage: tools/run_r21.sh <AT_DMP_R21_RT2_COMPLETE_PART_1_OF_2.zip> <..._PART_2_OF_2.zip> [work dir] [results dir]
# Runtime on one core: about 20 min, most of it in the film-gap distance sweep.
set -euo pipefail
Z1=$(realpath "$1"); Z2=$(realpath "$2"); WORK=$(realpath -m "${3:-./_work_r21}"); HERE=$(cd "$(dirname "$0")" && pwd)
OUT=$(realpath -m "${4:-$HERE/../results}")
mkdir -p "$WORK" "$OUT"; unzip -q -o "$Z1" -d "$WORK"; unzip -q -o "$Z2" -d "$WORK"
PY=${PYTHON:-python3}
$PY -I - "$WORK" <<'PYEOF'
import json, hashlib, os, sys
root = sys.argv[1]; m = json.load(open(os.path.join(root, 'MANIFEST_SHA256.json'))); bad = 0
for e in m:
    p = os.path.join(root, e['path'])
    if not os.path.exists(p) or hashlib.sha256(open(p, 'rb').read()).hexdigest() != e['sha256']: bad += 1; print('BAD', e['path'])
print(f"manifest: {len(m)} entries, {bad} mismatches"); sys.exit(1 if bad else 0)
PYEOF
D="$WORK/R21_WORK/deliverables"; N="$D/native"
$PY -I "$HERE/r21_check.py" "$N" "$OUT/results_r21_check.json" >/dev/null
$PY -I "$HERE/r21_bom_audit.py" "$D" "$OUT/results_r21_bom_audit.json" >/dev/null
$PY -I "$HERE/r21_fastener_map.py" "$D/tables" "$OUT/results_r21_fastener_map.csv" >/dev/null
$PY -I "$HERE/r21_film_keeper.py" "$N" "$OUT/results_r21_film_keeper.json" >/dev/null
$PY -I "$HERE/r21_film_raised_screws.py" "$N" "$OUT/results_r21_film_keeper.json" >/dev/null
$PY -I "$HERE/r21_film_gap.py" "$N" "$OUT/results_r21_film_keeper.json" >/dev/null
$PY -I "$HERE/r21_film_screw_protrusion.py" "$N" "$OUT/results_r21_film_keeper.json" "$OUT/results_r21_film_screw_protrusion.json" >/dev/null
$PY -I "$HERE/r21_film_screw_extension.py" "$N" "$OUT/results_r21_film_keeper.json" "$OUT/results_r21_film_screw_extension.json" 2.0 >/dev/null
$PY -I "$HERE/r21_film_screw_extension.py" "$N" "$OUT/results_r21_film_keeper.json" "$OUT/results_r21_film_screw_extension_4mm.json" 4.0 >/dev/null
$PY -I "$HERE/r21_root_contacts.py" "$N" "$OUT/results_r21_root_contacts.json" >/dev/null
$PY -I "$HERE/r21_yorder.py" "$N" P > "$OUT/results_r21_driveline_order_P.txt"
$PY -I "$HERE/r21_yorder.py" "$N" R > "$OUT/results_r21_driveline_order_R.txt"
$PY -I "$HERE/r21_stop_gear_budget.py" "$D" "$OUT/results_r21_stop_gear_budget.json" >/dev/null
echo "results written to $OUT"
