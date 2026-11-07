# C10 integrated structure — review handoff

C10 integrates the issued H01 horizontal heat exchangers and eight removable first spools, the D04 Pin-seat/gland seals, and the HYD-S2 external rack. It replaces the C09/H00 assembly as the coordinated geometry candidate on this branch. The owner geometry and all four H01 placements are retained.

## Model and results

Open `cad/C10_INSTALLED_S1.step` (A process/B regeneration) or `C10_INSTALLED_S2.step` (opposite states). Each has **3,116 occurrences**: 560 shell/retention/seal items, 244 D04 damper items, 2,204 HX occurrences, 72 first-spool items and 36 water-rack items. The service overlay is a separate reference, not physical installed hardware.

The shell revision changes 9 existing parts and adds 66 occurrences. It implements the eight H01 outer-skin penetrations with four split-retainer pairs and fitted weather/vapour boots; two closed raised corner pockets accommodate the HYD-S2 upper W2 insulation request without cutting the A post. The last part of each upper-plenum roof is raised by approximately 60 mm and the inner cheek is extended to close the roof joint. New roof segments measure 1.500 mm normal gauge. Fold radii and flat patterns remain a fabrication-detail task.

Both exported full models pass the stated >0.001 mm³ positive-volume cross-group screens and the changed-shell motion, service and insulation checks. No new/increased shell-to-shell overlaps were found. The sampled last 100 mm of the fin face has at least **99.180 mm** from the fin top to the roof underside at the central section; this is a geometric measurement, not a measured velocity distribution. The maximum signed inner-cheek shortfall at the sampled roof joints is **0.043402 mm**. See `evidence/verify_S1.json`, `verify_S2.json` and `detail_measurements.json` for all comparisons, exclusions and scope.

## Review priorities and holds

1. Review the local pocket-to-existing-Pin-seat seams and weld/seal accessibility. Positive-volume clearance does not prove leak tightness. Verify the fitted outer boots, service slit, retainer preload and weld-stud pull resistance on actual materials.
2. Assess airflow distribution with measured coated-core resistance and both flow duties, including the terminal 100 mm. This delivery is not CFD, FEA or a flow test. Do not infer pressure loss or uniformity from added depth alone.
3. Retain the D03 lower-shaft end-clearance and upper-sweep thermal/tolerance gates, D04 consumable-seal validation, full HX extraction, HX face-seal compression and condensate/drain/trap detailing.
4. The A post and sister/web reinforcement are unchanged. `A_POST_WELD_REGISTER.csv` locates load-transfer interfaces; welding procedure, seam sizing, frame stiffness, handling loads and fatigue require structural review. The water island still needs its independent load-bearing support/pipe clamps, kept outside the issued service envelopes.
5. HYD-S2 and H01 remain dimensioned interface candidates. Actual connection stack lengths, pressure ratings, anti-pullout, isolation/relief, reverse hot-flow commissioning and cold condensation performance require owner signoff. No sheet cutting, wet-operation or manufacturing release is asserted here.

## Rebuild and package

The self-contained review ZIP has repository-relative paths. Extract at a new root, then run the commands in `README_CN.md` from `AirTransformerShell/revisions/C10`. It includes the three pinned owner archives and the D03 motion/service input; editable C10 source, STEP models, interface tables, figure and verification records are included. Runtime dependencies and scratch logs are excluded. `INPUTS.json` pins the owner ZIPs; `MANIFEST_SHA256.json` covers all package members other than itself. The package can be reviewed without recovering the old chats.
