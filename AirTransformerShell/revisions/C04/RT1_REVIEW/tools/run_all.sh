#!/usr/bin/env bash
# Reproduce C04 RT-1 results. Python 3.12/3.13, CadQuery 2.8 (OCP 7.8/7.9), NumPy, SciPy, Matplotlib.
# Inputs (extract each into its own empty directory, outside the repository):
#   C02=<AT_SHELL2_2V_C02_CAD_20261104.zip extracted>/deliverables
#   HX=<buildfly_HX_import_20261105.zip extracted>/HX/M101_D952_P254_220_39x6_C04
#   DMP=<both AT_DMP_R21_RT2 parts extracted into one folder>/R21_WORK/deliverables
#   C04=<repo>/AirTransformerShell/revisions/C04 ; WORK=<scratch dir with copies of the C04 *.py>
set -euo pipefail
T=$(cd "$(dirname "$0")" && pwd); OUT=${OUT:-$T/../results}
cd "$WORK" && python network.py >/dev/null && python selector_flow.py >/dev/null && python build_c04.py "$C02/native"
python "$T/compare_json.py" "$WORK" "$C04" "$OUT/rerun_identity.json"
python "$T/step_compare.py" "$C04_STEP_DIR" "$WORK" C04_TAPER_CASSETTE.step C04_INSTALLED.step   # C04_STEP_DIR = C04_CAD.zip extracted
cd "$OUT"
python "$T/hx_probe.py" "$HX/M101_D952_P254_220_39x6_C04.step" hx_single_core_solids.json
python "$T/hx_feature_probe.py" "$HX/M101_D952_P254_220_39x6_C04.step" > hx_feature_probe.txt
python "$T/c04_install_checks.py" "$C04" "$C02/native" "$HX/M101_D952_P254_220_39x6_C04.step" install_checks.json
python "$T/valves.py" "$C02/native"
python "$T/masses.py" "$C04" "$C02/native"
python "$T/damper_env.py" "$DMP/step" P R
python "$T/damper_extents.py" damper_parts_bbox.json "$DMP/native" damper_extents.json
python "$T/damper_mass.py" "$DMP/step"
python "$T/flow_screen.py" "$C04" flow_screen.json
python "$T/structure_screen.py"
python "$T/figure_interfaces.py" "$T/../fig_interfaces.png"
