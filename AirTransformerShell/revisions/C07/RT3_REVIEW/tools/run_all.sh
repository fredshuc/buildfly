#!/usr/bin/env bash
# RT3 reproduction. Python 3.11+ with CadQuery 2.8.0 (OCP 7.9.3), NumPy, Matplotlib.
# WT  = clean worktree of 2272676750f015f71027b0715c1a8355cf80c4f5 (git worktree add --detach WT 2272676)
# DELIVERED = directory holding C07_CAD_REVIEW_PACKAGE.zip extracted (C07_SHELL.step, C07_INSTALLED_MACHINE.step)
set -euo pipefail
T=$(cd "$(dirname "$0")" && pwd); OUT=${OUT:-$T/../results}; C=$WT/AirTransformerShell/revisions/C07
REF=$(mktemp -d); cp "$C"/*.json "$C"/*.csv "$REF"/          # delivered evidence before rerun
(cd "$WT" && for s in prepare_inputs build_c07 integrate_c07 "integrate_c07 service" verify_access verify_seal_stroke "verify_motion dampers/c04-d01" export_machine; do
  set -- $s; python AirTransformerShell/revisions/C07/$1.py "${@:2}"; done)
(cd "$C" && python rt3_contact_check.py && python rt3_water_access.py)
python "$T/compare_rerun.py" "$C" "$REF" "$OUT/c07_rerun_identity.json"
cd "$OUT"
python "$T/step_compare.py" "$DELIVERED" "$C" C07_SHELL.step && mv step_compare.json c07_step_compare.json
python "$T/c07_checks.py" "$WT" "$DELIVERED/C07_SHELL.step" c07_checks.json
python "$T/c07_sweep.py" "$WT" "$DELIVERED/C07_SHELL.step" c07_sweep.json
python "$T/c07_screens.py" c07_checks.json c07_screens.json
python "$T/damper_cg.py" "$WT" damper_cg.json
python "$T/d02_contacts.py" "$WT" d02_contacts.json
python "$T/figure_c07.py" "$WT" "$DELIVERED/C07_SHELL.step" c07_screens.json "$T/../fig_c07.png"
