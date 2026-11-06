# Four-core C09 red-team handoff

**Disposition. Accept the air-side geometry for prototype detailing. Hold cutting, load-bearing release, fan operation and live-water operation.** The independent final review is in `Final_Red_Team_EN.md`. The two installed states contain 2,920 named occurrences each. S1 runs bed A in process and B in regeneration. S2 reverses both beds.

## Files to open

| File or package | Contents |
| --- | --- |
| `C09_CAD_REVIEW.zip` | Extract at the repository root. Includes the two installed STEP files, standalone shell, editable geometry and verification scripts, port evidence, and both independent reviews. |
| `cad/C09_INSTALLED_S1.step`, `cad/C09_INSTALLED_S2.step` | Each contains the 494-member shell, 230 installed D03 damper parts and 2,196 HX occurrences. Open one state at a time. |
| `cad/C09_SHELL.step` | Structure, ducts, rear-wall glands and coil perimeter seals. The D03 seats are available in the installed states. |
| `dampers/c08-d03/D03_DAMPER_REVIEW.zip` | Owner's two installed states, four selectors, motion/service envelopes, source and evidence. Extract its contents into `dampers/c08-d03/` to rebuild C09 from the packaged GitHub branch. |
| `hydronics/four-core-series/C09_HYDRONICS.zip` | Mode-specific eight-port register and independent 94-occurrence historical water-group STEP. Extract at repository root. Use the historical overlay only to compare the original route. |

## Air path, seal and structure

The four HX share the M101 C05 product. Each contains 549 occurrences. The lower and upper beds' stage datums are Z620 and Z955 mm. At the lower selectors the shaft runs along global Y at X610, Z342. The Pout seat starts at X614.5, 24.5 mm beyond the effective fin edge at X590. The outlet roof starts at X616.5. Both rear air ports retain their established position. The S1/S2 selector end angle is 77.702 degrees. Unload both fans before changing state. D03 identifies 80 degrees as a fault position.

The Pout central height ranges from 240.036 to 240.466 mm across nine mapped sections per bed. The smallest sampled Rin height is 135.364 mm. Across four Rin cheek boundaries, final samples at 1 mm spacing give minimum upper/lower edge engagement of 2.0015/2.1785 mm. The independent reviewer measured 1.500 mm normal floor gauge at two stations. The outlet-facing end of the upper splitter rises 17 mm locally to clear the universal core. Two dry-side pockets allow removal of the B feedback hoods without exposing the air passage to an open cutout.

Four continuous face seals have a nominal 2 mm installed thickness. Eight rear-wall split glands follow the four-core H00 tube crossings. The tops of the masks lie 2 mm below their respective core frames. Establish clamp force, gasket stock, compression tolerances, access and tracer-gas leakage before fabrication. The pressure-bearing HX and the valve hardware have separate qualification requirements.

At the A post two local boxed reliefs clear the W1 couplings. A 22 × 60 × 3 mm sister RHS and four connecting webs bridge both reduced sections. The independent Z600 measurement gives a nominal composite weak principal second moment of 419,057 mm⁴ versus 184,292 mm⁴ for the original section. That comparison assumes full shear transfer. Verify welds, eccentric load, local buckling, transport loads and whole-frame behaviour separately.

## Verification boundary

The exported shell SHA-256 is `0510824a686d8e31fdfdec5fac91afccdc123aef33dd73eaf5ea49d9018687ab`. Both installed STEP files were reimported and counted. `evidence/readback_S1.json` and `evidence/readback_S2.json` identify their exact bytes. Six checks use a 0.001 mm³ positive-volume threshold. Both installed damper states, 46 motion and 36 service envelopes, and the physical four-core HX passed their shell checks. For host-to-host joints the reported result is zero introduced or worsened overlaps involving the changed/new members relative to the historical shell. Designed seal and bearing contacts need their own acceptance tests.

The first independent review returned the host for correction. `development_pass1/` contains its geometric evidence. The final independent review covers the corrected products and states its assumptions and remaining gates. Nominal clearance and local sheet engagement do not establish airflow distribution, pressure loss, gasket performance or a load rating.

## Water and prototype gates

Restore the original series direction. Cold operation traverses lower then upper coil. Hot operation traverses upper then lower. The lower W2–upper W1 spool is common to both modes. The cold-supply/hot-return end is lower W1. The hot-supply/cold-return end is upper W2. Each bed retains four two-way selection functions. Each coil carries the full bed flow, nominally 2.0 m³/h. `hydronics/four-core-series/PORTS_BY_MODE.csv` controls the mode assignment.

The L2-E P0 model and service STEP were reported but could not be obtained. Their absence keeps the valve island and first removable spools outside the installed STEP. A rear wall opening and a threaded coupling end are distinct coordinates. At the upper H00 outlets a 42 mm straight projection meets the lower-stage tube after 20.15 mm (W1) and 26.697 mm (W2). A tubewall gland cannot clear that interference. Require the HX and hydronics owners to sign the versioned eight-port geometry and reverse hot flow. Overlay both active valve and tool volumes and demonstrate spool removal, venting and drainability before drilling external water penetrations.

Before cutting, close the post load path and the sheet bend/fastener details, check the tolerance stack, and select the actual actuator. For airflow qualification, instrument both beds and both states including the last 100 mm of the fin face. Measure distribution, pressure loss, seal leakage and condensate drainage. The present return contains CAD and section measurements only.
