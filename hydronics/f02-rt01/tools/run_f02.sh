#!/usr/bin/env bash
# usage: tools/run_f02.sh <HYD3_F02_Water_Only_Interfaces_20261017.stp> <extracted C05 RT01 package dir> [workdir]
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
