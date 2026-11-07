# C09 and recovered S0 water geometry
Prototype detailing, 6 November 2026. The air-side review applies to commit 71d9ef9. This supplement adds the original L2-E S0 package from 9bd5e96 and independently measures the distance between its external parts and the C09/D03 geometry. The geometry revisions remain under their original owners.

| Reference | Count | Minimum to 28 water solids, mm | Minimum to 22 tool/service volumes, mm |
| --- | ---: | ---: | ---: |
| C09 installed S1 | 2920 | 84.20 | 84.20 |
| C09 installed S2 | 2920 | 84.20 | 84.20 |
| D03 motion | 46 | 344.788 | 326.785 |
| D03 service | 36 | 395.670 | 373.659 |

The rear skin is the nearest installed part. The calculation uses global STEP placements and exact BRep distances after bounding-box screening. The JSON records input hashes and closest named pairs. The candidate external island can stay at its present location for detailed routing. Water island footprint, support loads and access on site still require checking.

Eight first spools from the coils to the rack boundary are missing. Upper-stage downward ports encounter the lower tube at approximately 20.15 and 26.697 mm for the W1 and W2 projections at OD42. Develop and verify a removable first section for each terminal. Preserve cold lower-to-upper and hot upper-to-lower series flow. Four water-model internal intersections at FS/Q remain in the owner report. The external clearance measurements do not resolve these connections. The C09 fabrication hold remains in effect, including post load transfer, bends, seams, gaskets, tool access and tolerances.

## Reproduce
From a directory containing the branch checkout, extract the C09 CAD review archive into an input directory, the D03 damper archive into its d03 subdirectory, and C08_HYD_SERIES_S0.zip into the input directory. Run python verify_overlay.py INPUT_DIR in a CadQuery/OCP environment. clearances.json records the closest pairs, in millimetres.
