# AirTransformer two-bed shell C06 | Red-team handoff

**Decision requested:** accept or return the coupled geometry for prototype detailing. Hold cutting and two-bed manufacture. The C04 single-bed cold-flow recommendation remains conditional on the independent stand and the C04 RT1 test conditions.

## Configuration

C06 combines the C04 tapered eight-channel face distributor, M101 C04 with the RT1 port alignment, eight D01 dampers and a pitch-adapted L2-E C04_HYD_R1 water bay. Bed A is fixed. Translate bed B and its four valves by +440 mm along Y. Bed centres are Y = −434.4 and +845.6 mm. The casing side faces span 2144 mm. The shell STEP including supports spans X −438 to 1312, Y −858 to 1298 and Z 0 to 2552 mm. Allow additional installation space for the dampers, site connections and component removal.

| Interface | C06 geometry |
| --- | --- |
| Damper faces | Front X −129.1, rear X 879.1 mm. Keep 630 × 345 mm process and 630 × 180 mm regeneration net openings. The D01 35 mm adapter includes its gasket. Shorten each rear sleeve by 39 mm. |
| Water unions | All four point along +X at X 615, Z 2370 mm. A supply/return Y −75.325/−225.325 mm. B supply/return Y +1204.675/+1054.675 mm. |
| Water bay | Eight two-way changeover valves. Two DN32 return-meter positions. Four site interfaces at X 1360, Y −733 mm. Elevations and directions are in interfaces.csv. The separate fit STEP contains the C06 routing. |
| Supports and seals | Eight cassette bearers and four damper support portals. Four peripheral seals with retractable carriers, nominal 6.0 mm free and 4.2 mm installed thickness. Geometry defines nominal seats and compression. |
| Flow-test hardware | 32 removable balancing plates, access covers, pressure takeoffs and drainage features. Both modes retain the full-height tapered passages. |

## Verification

The exported shell reads back as 327 solids. The shell self-check found zero intersections above 0.001 mm³. The integration read 7,212 D01 product and interface occurrences after excluding the obsolete host reference, 1,074 solids across two detailed M101 units, and 43 water-bay solids. The static shell–damper, shell–HX, shell–water and checked water service pairs passed. See integration_checks.json for the exact pair inventory.

Eight intersections occur when the four rear dampers are represented by single rectangular full-rotation bounds. The boxes intersect the sleeves and side panels. A second check applies the owner's 600 continuous segmented bounds to all 327 shell occurrences. Nine pairs required solid intersection. All nine passed the 0.001 mm³ threshold. The full boxes remain in the results for traceability. The actuator-selection and single-cover service boxes produced zero shell intersections.

## Open decisions before build

1. Verify foot anchorage, portal stability, flange bearing and joint loads with actual valve masses. Demonstrate independent support under installation and service loads. The model has no structural or weld qualification.
2. Qualify the right-hand hardware, G843 clamp and selected actuator. Repeat the movement and removal checks with purchased actuators and tolerances. Demonstrate the complete HX withdrawal sequence with the water unions disconnected, seal carriers released and removable parts identified. The C04 withdrawal distance has not been requalified on C06.
3. Test seal compression, corner continuity, bypass, drainage and tracer leakage. Retain all eight conditions from C04 RT1 §3. For flow distribution, test regeneration first and map both modes over the entire coil. Compare local/mean velocity to 0.80–1.20. No C06 CFD, fan-duty measurement or face-uniformity result is available.
4. Hydronics owner to accept the longer headers and revised saddle, confirm trapped-volume relief and valve sequencing, and quantify hot/cold carryover before live water operation.

## Reproduction

Use CadQuery 2.8 and the repository layout. Extract the owner packages first. Keep the C04 shell sources in the adjacent C04 directory and the extracted D01 package at dampers/c04-d01. Run build_c06.py, then integrate.py with the detailed M101 STEP, extracted water package directory and D01 directory, in that order. Run verify_motion.py with the D01 directory. Overlay C06_SHEET_METAL.step and C06_WATER_FIT.step at the common origin. In the D01 installed file suppress its HOST reference. C06_WATER_SERVICE.step contains clearance volumes only.
