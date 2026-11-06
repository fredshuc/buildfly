# Independent red-team disposition — C09 four-core horizontal integration

**Accept the shell, D03 dampers and H00 heat exchangers for prototype detailing. Hold sheet cutting, wet operation and manufacture.** C09 provides a usable common assembly for review. The active water hardware remains outside its verified geometry.

## Reviewed models

- Shell SHA-256 `0510824a686d8e31fdfdec5fac91afccdc123aef33dd73eaf5ea49d9018687ab`.
- S1 SHA-256 `0edefa1f0aef8d08c57cf9afe0242397d4281d118d162bec97bc7c46589267c9`; S2 SHA-256 `1ca6f75d8edba4001e765a4b46cef5e7605b702896d0c16d86854d83f0e7ab56`. Each source STEP readback contains 494 shell, 230 damper and 2,196 heat-exchanger occurrences, or 2,920 per configuration. The HX contribution consists of four instances of the same 549-occurrence product.
- The first-pass review remains in `Independent_Review_EN.md`. The airflow and water service statements below apply to this four-core prototype.

## Geometry disposition

| Interface | Final evidence | Remaining closure |
| --- | --- | --- |
| Process discharge and regeneration inlet | The lower Pout seat's near face at X614.5 gives 24.5 mm clearance to the fin end at X590. The final central section register gives at least 135.364 mm of clear height across the sampled Pout/Rin transitions. | Check full-face distribution and pressure loss in both modes, including the last 100 mm of the fin face. The section samples do not measure flow. |
| Four regeneration cheek seams | I independently traced both edges of each cheek on the corrected transition geometry, including X719, 727, 735 and 747. The final shell's 1 mm grid from X631 to 748 gives at least 2.0015 mm of upper engagement and 2.1785 mm of lower engagement across the four edges. The earlier positive gap at X727 and the lower opening near X719 have closed. The regraded floor measures 1.500 mm normal thickness at X655 and X695. | Detail bends, radii, seal or weld continuity, drain opening, trap and cleanout. Include tolerance before flat pattern release. Verify drainage and leakage on the assembly. |
| B-bed feedback hoods and outer skin | The depth-limited skin patch and dry-side pockets clear both static hood positions and both removal paths. The final D03-to-host screens report zero positive-volume intersections over 0.001 mm³. They cover both end states (266 broad-phase pairs per state), the 46 motion envelopes (86 pairs) and 36 service volumes (14 pairs). | Verify minimum tool clearances and cable routes with the purchased parts. The separate D03 80° fault position exceeds the 77.702° nominal end angle. Verify hard stops, angle feedback and fan unload before switching. |
| HX edges and rear-wall crossings | All 108 broad-phase HX-to-shell pairs clear the 0.001 mm³ threshold. The changed/new host-to-host screen reports zero increased intersections in 231 candidate pairs. Four 2 mm rings have 41,741.78 mm² nominal gasket footprint each. On the common A-lower interface I sampled five locations on each side of a gasket ring. H00 and shell material were present 0.01 mm either side of the respective contact planes at all 20 samples. The final model contains 16 split-gland halves for the eight tube crossings. | Verify compressed gasket stroke and clamping load around all four faces, gland retention and split sealing, panel removal, drains and actual leak rate. The H00 wall-crossing centres at X≈−500 and downward-facing terminal centres at X−576 are distinct datums. |

The host clash threshold detects solid overlap. It does not establish minimum running allowance, gas tightness, gasket contact pressure or service clearances after tolerance. The zero increased host result refers to changed and added components versus the historical baseline. It does not certify all historic joints.

## A post at Z600

I cut a 1 mm slice of the actual STEP at a relieved section. Areas are in mm². Centroid coordinates are global mm and second moments are centroidal mm⁴.

| Section | Area | Centroid (X, Y) | Ixx | Iyy | Absolute Ixy | Weak principal I |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| Original 80 × 40 post | 684 | (−600, −825) | 184,292 | 558,532 | 0 | 184,292 |
| Relieved post alone | 570 | (−600, −834.5) | 40,927.5 | 389,470 | 0 | 40,927.5 |
| Final composite section with sister RHS and both connecting webs | 1,140 | (−614.5, −808.7) | 1,131,529 | 674,337 | 426,474 | 419,057 |

The reinforcement restores local weak-axis section inertia if the connected pieces act together. The centroid moves 14.5 mm in −X and 16.3 mm in +Y from its original position. Detail weld shear transfer, section changes at both relieved intervals, load eccentricity, fatigue and handling loads. Check frame stiffness, buckling and actuator reactions before cutting. These are measured section properties, independent of assumed steel grade and load. They do not constitute a frame strength calculation.

## Hydronics and release

The S0 routing record uses two series coils in each bed. Cold water traverses the lower then upper coil. Hot water traverses the upper then lower coil. Obtain joint HX/hydronics sign-off on reverse hot flow and all eight terminals. The older generic W1-supply/W2-return table conflicts with that hot-water route. Nominal 42 mm downward projections from the upper ports encounter the lower-stage tube after 20.15 mm and 26.697 mm. The rear-wall gland openings address tube passage through the air wall; they do not resolve those downstream spool conflicts.

The owner P0 installed and service STEP binaries were unavailable for this review. Historical water geometry supplies layout context only. Require a versioned water overlay with eight port matches, drain and vent provision, wrench and actuator withdrawal checks and signed switching logic before wet operation or freezing penetrations. Verify dry air-path distribution, sealing and damper controls on the prototype before any live two-bed release.
