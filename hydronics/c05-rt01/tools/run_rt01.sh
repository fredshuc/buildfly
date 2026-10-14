#!/usr/bin/env bash
# Reproduce hydronics/c05-rt01/results from the split review package.
# usage: tools/run_rt01.sh <dir containing AT_HYD3_RT01_ENGLISH_MANUAL_REVIEW_20261014.zip.001/.002> [workdir]
set -euo pipefail
SRC=$(cd "$1" && pwd); WORK=${2:-$(mktemp -d)}; mkdir -p "$WORK"; WORK=$(cd "$WORK" && pwd)
HERE=$(cd "$(dirname "$0")" && pwd)
NAME=AT_HYD3_RT01_ENGLISH_MANUAL_REVIEW_20261014.zip
cat "$SRC/$NAME.001" "$SRC/$NAME.002" > "$WORK/$NAME"
echo "0e931351b87aeabf54ee12f92433c28dfd499534a339a304bea17c69134647af  $WORK/$NAME" | sha256sum -c -
mkdir -p "$WORK/pkg" && (cd "$WORK/pkg" && unzip -q -o "../$NAME")
export HYD3_PKG="$WORK/pkg"
cd "$HERE"
for t in rt01_manifest rt01_workload rt01_miter_pieces rt01_hydraulics rt01_elbow_fit rt01_ev rt01_ev_shuttle rt01_tr01 \
         rt01_flex rt01_threaded_makeup rt01_clash_census rt01_pockets; do
  echo "== $t"; python3 "$t.py" > /dev/null
done
# geometry (OCP Booleans): ~5 min, ~3 min, ~40 min on one core
python3 rt01_cad_elbows.py > /dev/null
python3 rt01_export_step.py > /dev/null 2>&1
python3 rt01_step_readback.py > /dev/null 2>&1
python3 rt01_insulation_envelope.py > /dev/null
echo "results written to $(cd .. && pwd)/results"
