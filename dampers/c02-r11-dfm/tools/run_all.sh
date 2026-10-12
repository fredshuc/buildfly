#!/usr/bin/env bash
# Reproduce every number in DFM_REVIEW.md from the R11 red-team pack.
# Usage: tools/run_all.sh <path to AT_DMP02_C02_R11_REDTEAM_CROSS_SECTION_20261012.zip> [work dir]
# The pack is treated as data: it is extracted into a separate work dir and no project script is executed.
set -euo pipefail
PACK_ZIP=$(realpath "$1"); WORK=$(realpath -m "${2:-./_work}"); HERE=$(cd "$(dirname "$0")" && pwd); OUT="$HERE/../results"
mkdir -p "$WORK/pack" "$WORK/full" "$OUT"
unzip -q -o "$PACK_ZIP" -d "$WORK/pack"
( cd "$WORK/pack" && tail -n +2 03_FILE_INDEX.csv | tr -d '\r' | while IFS=, read -r p b h; do
    echo "$h  $p"; done | sha256sum -c --quiet ) && echo "pack index: all SHA-256 OK"
unzip -q -o "$WORK/pack/R11_FULL_ENGINEERING.zip" -d "$WORK/full"
NAT10="$WORK/full/R10_WORK/deliverables/native"; NAT11="$WORK/full/R11_WORK/deliverables/native"; R9EV="$WORK/full/R9_WORK/deliverables/evidence"
PY=${PYTHON:-python3}
$PY -I "$HERE/native_delta.py"  "$NAT10" "$NAT11" "$OUT/results_native_delta.json" >/dev/null
$PY -I "$HERE/check_a_root.py"  "$NAT11" "$OUT/results_a_root.json" >/dev/null
$PY -I "$HERE/dfm_calcs.py"     "$WORK/pack/evidence" "$OUT/results_dfm_calcs.json" >/dev/null
$PY -I "$HERE/bom_routing.py"   "$NAT11" "$WORK/pack/evidence/R11_BOM_FULL.csv" "$OUT/results_bom_routing.json" "$OUT/results_bom_routing.csv" >/dev/null
$PY -I "$HERE/b_equaliser_sensitivity.py" "$R9EV" "$OUT/results_b_sphere_radius.json" >/dev/null
$PY -I "$HERE/b_driver_sweep.py" "$R9EV" "$OUT/results_b_driver_sweep.json" >/dev/null
$PY -I "$HERE/b_measurement_grid.py" "$R9EV" "$OUT/results_b_measurement_grid.json"
echo "results written to $OUT"
