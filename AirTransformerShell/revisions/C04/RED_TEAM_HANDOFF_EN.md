# AirTransformer two-bed machine | Red-team handoff

**Decision requested:** Is the C04 air-path geometry suitable to build for a cold-flow test, and which interfaces must change before the integrated machine can be released? Issue a separate verdict for each module and for the assembled machine.

Review baseline: 5 November 2026, buildfly commit [4d87530](https://github.com/fredshuc/buildfly/commit/4d8753023487dc0c1a13efb420595c1f1d9e8b01). Dimensions are in mm. X runs through the coil thickness, +X points towards the water connections, Y runs across the two beds, and Z is vertical. P denotes process air and R denotes regeneration air. Each bed contains one vertical heat exchanger (HX). In a settled state both ends of a bed select the same air circuit. The beds exchange duties.

## Files to open

| Module | Controlled input | What the evidence covers |
|---|---|---|
| Shell, ducts and frame | [C04 cross-section](https://github.com/fredshuc/buildfly/blob/4d8753023487dc0c1a13efb420595c1f1d9e8b01/AirTransformerShell/revisions/C04/C04_section.png) and [two assembly STEPs](https://github.com/fredshuc/buildfly/blob/4d8753023487dc0c1a13efb420595c1f1d9e8b01/AirTransformerShell/revisions/C04/C04_CAD.zip) | The installed model contains both beds, simplified HX seats and active volumes, and reserved equipment space. The saved interference list is empty at a 0.001 mm³ threshold. STEP readback counted 28 solids in one cassette and 188 in the installed assembly. |
| M101 heat exchanger | [C04 single-core STEP, two-core STEP, interface report and import package](https://github.com/fredshuc/buildfly/tree/4d8753023487dc0c1a13efb420595c1f1d9e8b01/HX/M101_D952_P254_220_39x6_C04) | One product definition, 39 parallel circuits with six passes each. Both instances use the same orientation. Use the single-core STEP for installation checks and the shell transforms below. Qualify any supplier alternative separately before changing this baseline. |
| Air dampers | [AT-DMP02 C02 R21 source packages](https://github.com/fredshuc/buildfly/tree/4d8753023487dc0c1a13efb420595c1f1d9e8b01/dampers/c02-r21) and [RT-2 findings](https://github.com/fredshuc/buildfly/blob/4d8753023487dc0c1a13efb420595c1f1d9e8b01/dampers/c02-r21-rt2/RT2_REVIEW.md) | RT-2 reported no motion interference at 41 rotor positions in its P and R cold-test configurations. Shell C04 represents eight damper bodies and eight drives by envelopes. Installed motion, sealing and tool access need a separate check. |
| Water changeover | [Hydronics RT01 review package](https://github.com/fredshuc/buildfly/tree/4d8753023487dc0c1a13efb420595c1f1d9e8b01/hydronics/RT01_review) and [C02 valve interface table](https://github.com/fredshuc/buildfly/blob/4d8753023487dc0c1a13efb420595c1f1d9e8b01/AirTransformerShell/revisions/C02/deliverables/tables/WATER_INTERFACES.json) | Four three-way selector valves. RT01 is a reference for the water circuit. The C04 shell includes translated valve references and four pipe penetrations. Branch routing, header continuity, union removal and the switching sequence require integrated evidence. |

## Installation datums to verify first

The HX interface file contains original global port positions at Z1370. Shell C04 raises both coils by **1000**. Use the HX **local** port coordinates with the shell translations in this table. Applying the old global coordinates would place all four penetrations a metre too low. [HX interface source](https://github.com/fredshuc/buildfly/blob/4d8753023487dc0c1a13efb420595c1f1d9e8b01/HX/M101_D952_P254_220_39x6_C04/INTERFACES_AND_PLACEMENTS.json)

| Bed | Single-core translation (X, Y, Z), identity rotation | W1 installed face centre (X, Y, Z) | W2 installed face centre (X, Y, Z) |
|---|---|---|---|
| A | (265, −802.175, 1150) | (615, −75.325, 2370) | (615, −225.325, 2370) |
| B | (265, 37.825, 1150) | (615, 764.675, 2370) | (615, 614.675, 2370) |

All four Rp 1¼ female connections point towards +X. The X750 bulkhead lies 135 mm beyond each connection face. A Ø85 insulated pipe centred in a Ø110 hole has 12.5 mm nominal radial clearance. On each bed, W1 connects to cold supply or hot return, and W2 connects to cold return or hot supply. Thus cold operation flows W1 → W2 and hot operation flows W2 → W1. Trace those four duties to the actual valve ports.

The main shell occupies X −131.1 to +1312, Y −852 to +852 and Z 0 to 2552. External drives and damper bodies extend beyond this envelope. Relative to shell C03, the roof rose by 800, the front extended by 79.1, and the HX and valve references rose by 1000. Review lifting, lateral stiffness, anchorage and service height against these installed datums.

## Air distribution and fan duty

Each side of each bed has a full-width selector box below the coil. Its 612 × 320 throat feeds eight inclined channels. Each channel turns towards a distinct 612 × 125 strip on the 612 × 1000 active face, spanning Z1204–2204. The opposite cassette collects from the same eight strips. Reversing flow exchanges the two functions. Path lengths range from about 0.19 to 1.11 m. Each strip has a 120-hole balancing plate, with candidate hole diameters increasing from 18.1 mm at the shortest path to 20.0 mm at the longest. Both end strips therefore have defined routes. The engineering question is how much air each receives with real valve wakes, edge leakage and a wet coil.

| Quantity | C04 result | Interpretation for review |
|---|---|---|
| Process design point | 4870 m³/h through one active bed, mean face velocity 2.21 m/s | Use the per-bed flow for the active P route. Establish the R operating point independently. |
| Two cassettes and their balancing plates | About 149 Pa at equal band flow | Component estimate. It is already included in the path totals below. |
| Example P / R internal path totals | 325 / 276 Pa at the same 4870 m³/h | Includes both selector boxes and an assumed 60 Pa HX loss. Damper blades and external duct losses are additional. The equal-flow R case is a comparison. |
| Sensitivity to selector losses | P 238–499 Pa, R 226–376 Pa at 4870 m³/h | The assumed mixing-loss coefficient spans 1–10 m⁻¹. Establish installed fan duty using measured losses and the applicable fan curve. |
| Face distribution under imposed pressure bias | 48 model cases, local/mean velocity 0.860–1.137, worst coefficient of variation (CV) 7.23% | These are pressure-network predictions. Reverse symmetry is imposed. Independent variation in local coil loading, separation and individual perforation jets needs testing. |

[Pressure-network inputs and results](https://github.com/fredshuc/buildfly/tree/4d8753023487dc0c1a13efb420595c1f1d9e8b01/AirTransformerShell/revisions/C04) · [Recorded geometry checks](https://github.com/fredshuc/buildfly/blob/4d8753023487dc0c1a13efb420595c1f1d9e8b01/AirTransformerShell/revisions/C04/fit.json)

## Independent checks and closeout evidence

| Priority / owner | Check | Evidence required for a verdict |
|---|---|---|
| 1 · Air path and fan | Test A/P, A/R, B/P and B/R at their assigned flows. Exercise both intended flow directions with production-representative dampers and dry and wet core conditions. Check the first and last bands, corners and the inactive air path. | Record total flow, fan speed, air density, total pressure loss, HX pressure drop and 8 × 12 equal-area face readings. Use patch averages between plate and fins. Proposed gate: every patch 0.80–1.20 of its measured face mean and CV ≤10%, while the fan meets the specified duty. Record bypass and cross-leakage separately. |
| 1 · HX and shell | Install the detailed single-core STEP twice. Check all feet, ports, unions, frame rails, seal lands and roof clearances. Sweep the actual coil extraction path with the stated removal sequence. | Datum overlay, clash volumes and minimum clearances with tolerances and insulation. Identify removable panels, required lift and the first obstructing part. |
| 1 · Water changeover and controls | Trace cold and hot paths on each bed. Examine transition states, delayed or failed valve feedback and temporary hot-to-cold connection. Use actual port functions, actuator timing and confirmed fail positions. | Marked schematic, four-valve state table, transition timing diagram, and a bench check of isolation, continuity and pressure drop. Confirm the means of releasing and withdrawing all four upper connections. |
| 2 · Dampers | Fit actual R21 P and R configurations at all eight interfaces. P opening 630 × 345, R opening 630 × 180, flange width 706, reserved body depth 180. Check handedness, blade sweep, shafts, drives, wiring, wet drainage and access. | Worst installed clearance over the full stroke and an isolation test with the opposite circuit closed. Cross-reference applicable RT-2 stop/gear, feedback and film-retention findings. |
| 2 · Structure and sheet metal | Check the raised core load path to the base, roof and post stability, vibration of long guides, filter/plate access, seal compression and condensate retention. | Load cases and reactions, critical deflection against seal allowance, feasible bend and fastening details, and an assembly/removal sequence. Weight optimization is deferred. |

**Reproduction.** From the [shell C04 directory](https://github.com/fredshuc/buildfly/tree/4d8753023487dc0c1a13efb420595c1f1d9e8b01/AirTransformerShell/revisions/C04), run `python network.py`, `python selector_flow.py`, `python build_c04.py <C02-deliverables/native>`, then `python render.py`. Use Python 3.12, CadQuery 2.8, NumPy, SciPy and Matplotlib. Obtain the native valve input from the [C02 CAD package](https://github.com/fredshuc/buildfly/blob/4d8753023487dc0c1a13efb420595c1f1d9e8b01/AirTransformerShell/revisions/C02/packages/AT_SHELL2_2V_C02_CAD_20261104.zip). Compare the imported solids, transforms and physical interfaces as well as the scalar results.

**Requested return.** Give one disposition per module and one for cold-flow build readiness: accept, accept with named conditions, or revise. For each blocker, identify the affected file, part and operating state, give the measured or calculated result against its criterion, and name the smallest correction and the evidence needed to close it. Record separately what still gates manufacture.
