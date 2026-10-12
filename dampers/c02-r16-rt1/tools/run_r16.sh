#!/usr/bin/env bash
# Reproduce the RT-1 results from the R16 package zip. The package is treated as data; no project script is run.
# Usage: tools/run_r16.sh <AT_DMP02_C02_R16_FULL_INTEGRATION_RT1_20261012.zip> [work dir]
set -euo pipefail
ZIP=$(realpath "$1"); WORK=$(realpath -m "${2:-./_work_r16}"); HERE=$(cd "$(dirname "$0")" && pwd); OUT="$HERE/../results"
mkdir -p "$WORK" "$OUT"; unzip -q -o "$ZIP" -d "$WORK"
PY=${PYTHON:-python3}
$PY -I - "$WORK" <<'PYEOF'
import json, hashlib, os, sys
root = sys.argv[1]; m = json.load(open(os.path.join(root, 'MANIFEST.json'))); bad = 0
for e in m:
    p = os.path.join(root, e['path'])
    if not os.path.exists(p) or hashlib.sha256(open(p, 'rb').read()).hexdigest() != e['sha256']: bad += 1; print('BAD', e['path'])
print(f"manifest: {len(m)} entries, {bad} mismatches"); sys.exit(1 if bad else 0)
PYEOF
D="$WORK/R16_WORK/deliverables"
$PY -I "$HERE/r16_eco_check.py" "$D/native" "$OUT/results_r16_eco.json" >/dev/null
$PY -I "$HERE/r16_mass.py" "$D/native" "$OUT/results_r16_mass.json" >/dev/null
$PY -I "$HERE/r16_release_waves.py" "$D/tables" "$OUT/results_r16_release_waves.csv" "$OUT/results_r16_release_waves_summary.json"
echo "results written to $OUT"
