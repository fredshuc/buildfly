#!/usr/bin/env bash
# Reproduce C06 RT-2 results. Python 3.12/3.13, CadQuery 2.8.0 (OCP 7.9.3), NumPy, Matplotlib.
# REPO = a repository-layout copy containing AirTransformerShell/revisions/{C04,C06} (C06 *.py from the package)
#        and dampers/c04-d01 (D01_CAD_REVIEW_PACKAGE.zip extracted). HYD = extracted C04_HYD_R1 directory.
# HXSTEP = M101_D952_P254_220_39x6_C04.step. HXSOLIDS = C04 RT1 results/hx_single_core_solids.json.
set -euo pipefail
T=$(cd "$(dirname "$0")" && pwd); OUT=${OUT:-$T/../results}; C06=$REPO/AirTransformerShell/revisions/C06
(cd "$C06" && python build_c06.py --out "$C06" && python integrate.py "$HXSTEP" "$HYD" "$REPO/dampers/c04-d01" && python verify_motion.py "$REPO/dampers/c04-d01")
cd "$OUT"
python "$T/c06_checks.py" "$C06" "$HXSTEP" c06_checks.json
python "$T/panel_cheek.py" "$C06" panel_cheek.json
python "$T/drive_through_panel.py" "$C06" "$REPO/dampers/c04-d01" drive_panel.json
python "$T/c06_screens.py" c06_checks.json c06_screens.json
python "$T/figure_c06.py" "$C06" "$HXSOLIDS" c06_screens.json "$T/../fig_c06.png"
