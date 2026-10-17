#!/usr/bin/env bash
# usage: tools/run_f02.sh <F02.stp> <extracted C05 RT01 package dir> <workdir> [v0498B.step]
# Expected input SHA-256: f4888a598afdb25b92fe2006c415a064d02447cfd6a4a14bf02e6c29a7e83988
set -euo pipefail
STP=$(realpath "$1"); export HYD3_PKG=$(realpath "$2"); W=${3:-$(mktemp -d)}; mkdir -p "$W"; W=$(realpath "$W")
HERE=$(cd "$(dirname "$0")" && pwd)
sha256sum "$STP"
python3 "$HERE/f02_read.py" "$STP" "$W" > /dev/null 2>&1
python3 "$HERE/f02_lines.py" "$W"
python3 "$HERE/f02_topo2.py" "$W"
python3 "$HERE/f02_host.py" "$W"        # ~15 min: OCP Booleans vs 2,810 host BReps
python3 "$HERE/f02_metrics.py" "$W"
cp "$W"/f02_parts.json "$W"/f02_lines.json "$W"/f02_clash.json "$HERE/../results/"
# v0498B C4 comparison (optional 4th argument: V0498B_VS2D_P0_X800_VS2D_P0_CANDIDATE_C4_ANALYSIS.step,
# SHA-256 f3d1b1ec6820a5d3d5dccfe16867e06fc1023ae5156ca82dae0142246f214a3b)
if [ $# -ge 4 ]; then
  V=$(realpath "$4"); VW="$W/v0498B"; mkdir -p "$VW"
  python3 "$HERE/f02_read.py" "$V" "$VW" > /dev/null 2>&1
  python3 "$HERE/v_pipes.py" "$VW"
  python3 "$HERE/v_host.py" "$VW"        # ~10 min
  python3 "$HERE/trend.py" "$VW/v_pipes.json" "$W/f02_lines.json" "$VW/trend.json"
fi
