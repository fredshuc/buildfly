# AT-DMP02 C02 R16: RT-1 independent review (integration and manufacturability)

**Object reviewed:** `AT_DMP02_C02_R16_FULL_INTEGRATION_RT1_20261012.zip` (26,361,962 bytes, SHA-256 `cbfe74c5…086c8a`), with all 209 manifest entries verified, and the 14-page guide `AT_DMP_R16_RT1_INTEGRATION_REVIEW_EN.pdf`.
**Date:** 2026-10-12. **Status:** the complete C02 remains `PARTIAL / NOT_FOR_MANUFACTURE`. Nothing here authorizes ordering, machining an unissued part, or testing; L1 owns acceptance.

Evidence tags:
- **[V]** reproduced or computed here from the R16 native BRep and transforms, using OCP only.
- **[S]** taken from the package.
- **[C]** a screening calculation made here, with its assumptions stated.
- **[R]** a recommendation.

Each finding below gives the exact PN/instance, source, counterexample, affected use, smallest change and acceptance evidence. Findings are classed as **must-fix (first prototype)**, **controlled-test conditional**, or **P2**.

---

## 0. Conclusion

Two of the four decision-changing R16 findings have a **verified smallest fix that uses only parts already released in SP03, with no new PN**. A third needs one L1 orientation decision, and the evidence favours a single rig pose. The fourth (the P root weld against F620) disappears into the wet-support design if its keep-outs are respected; the P host boundary itself remains open.

1. **P stop (Q2).** Re-phase the stop arm D886 on P2 by +90° about the P2 axis, so the arm points +Y_rig at valve 0°.
   - Result [V]: zero overlap at every 15° step from 0° to 90°. The arm contacts TF900 at exactly 0° and 90° (0.000 mm), with 10.0 mm clearance throughout the travel. **TF900 is unchanged.**
   - Rework: one keyway in a released 0.95 kg part.
2. **Front guard and posts (Q1).** Translate G901 and the two wet-end TF909 posts by −45.5 mm in world Y. Shorten the two G900 side guards by 45.5 mm and add two M8 holes to the TF903 deck.
   - Result [V]: zero wet-side intersections at 0/45/90° in both P and R.
   - Clearances: 5.0 mm to the STD03C stud tips, 5.5 mm to the BK2 wet hub, 3.0 mm radial at the shaft ports.
   - The valid shift window is 45.0–48 mm.
3. **P orientation and wet support (Q3, and the R part of Q1).** In both configurations the wet valve has **no modelled load path**: the fixture feet F622 sit at Z = 1160 on a bench (F640) that is not in either configuration. The R rig floor is at Z = 744, and the P rig lies on its side with its feet on a vertical plane at X = −1278 [V].
   - Recommendation [R]: for the P1 dry-chain programme, rotate the P valve 90° about its shaft axis. P and R then share **one horizontal rig pose and one rig-mounted wet support** (a "wet bay"). That retires all F620/F621/F622 conflicts, including the two 281.92 mm³ weld hits, and reuses the R14 horizontal-gravity rows unchanged.
   - Cost: P is not exercised in its installed gravity direction. The rotor centre of gravity lies on the shaft axis, so gravity torque about the shaft is 0. Only the direction of the 60.7 N radial weight per rotor changes [V].
   - If L1 needs the installed orientation, the side-lying rig must have outriggers or anchors. Its current centre of gravity is 14.7 mm inside the tipping edge, which gives about 69 N·m of restoring moment against a 200 N·m static fault reaction [C].
4. **The largest schedule lever is outside every R16 blocker (Q7).** The P1 kit needs 208 PN / about 2,200 pieces, and existing releases cover 335.
   - 41 PN (315 pieces) can be released now. These are the wet-valve shells, flanges, seat beams, gaskets, PTFE, compression limiters and the A705–A710 feedback frame. Their BReps are **byte-identical from R11 to R16**, none of the R16 conflicts touch them, and none are released.
   - Alongside them, 50 commodity hardware PN (1,038 pieces) can be authorized. That keeps the factory's roughly 1-week cycle busy while L1 decides items 1–3.

**Still open, and not changed by this review:** G1 closure, the mapping from the 1000 N proxy to seal function, the 1800 N per-head guard band, the P host interface, and qualified maintenance load transfer. These are measurement and definition tasks (Q5, Q6). No further model iteration closes them.

---

## 1. Corrections carried over from L1's disposition of the R11 red-team review

L1's disposition (`reference/AT_DMP_REDTEAM_DISPOSITION_CN.md`) correctly qualified several of my R11 statements. This review applies them:

| R11 statement | Correction accepted |
|---|---|
| EN 1993-1-8 "§4.5.2(2)" minimum fillet length | The clause is **§4.5.1** in the 2005 edition. The L − 2a deduction applies only when craters are not full size. Eurocode is not automatically the governing method for this machine; one must be chosen. |
| P/R111 0.01 mm shim "±0.015 tolerance larger than nominal" | It is a **group-thickness** tolerance, so it was a misreading. |
| B852 interference range | I assumed an H7 bore. The native file gives Ø2.98 with a general ±0.05, so the drawn range was not bounded by my figures. |
| B kt | The model applies kt to both the jaw and the fixed half, and ΔT/Δβ is a system response. L1's split shows the fixed-half kt dominates. Identification needs separated interfaces. |
| "H1 ≈ 50%" (P host clash) | This had no statistical basis and is withdrawn. Only the geometric fact stands. |
| ISO 2768-mK as a blanket default | ISO 2768-2 is withdrawn (now ISO 22081:2021). State the edition explicitly and set general tolerances per process. |
| BOM routing table | It was regex-based (B850 was classed as turned and B851 as milled). It is an entry point for manual grouping, not an RFQ list. |
| 6–8 week schedule and cost multiples | These had no project scheduling basis. Schedules here are arithmetic on the user-stated 1-week factory cycle, with purchased lead times named as the unknown that dominates. |

---

## 2. Reproduction of the R16 decision findings [V]

`tools/r16_eco_check.py` loads `native/R16_PARTS.json` and the `R16_{P,R}_OCCURRENCES.json` transforms. It reproduces the R16 motion convention: rotation about global −Y through P1 (−439,·,1368), P2 (−439,·,1533) and R1 (−82,·,1583), with P2 at −angle.

| R16 claim | This review |
|---|---|
| P: 22 cross-branch pairs per pose | 22 pairs, total 49,997.6 mm³ (G901 with P101/P106/P107/P107B/J401/STD03C; TF909 with P101/P106/P107/P107B) |
| R: 20 cross-branch pairs per pose | 20 pairs, total 39,148.8 mm³ (adds TF903/TF906/TF909/G901 against F621) |
| D886/TF900: 1194.286 mm³ at 45°, 1600.000 mm³ at 90° | 1194.2859 and 1600.0000. **Additional:** 6437.6 at 15°, 5277.3 at 30° and 756.5 at 75°. The 0/45/90 sampling under-reports the interference. |
| P root a4 against F620_002: 281.92 mm³ ×2 | Same; R16 geometry is identical to the R11 audit |
| P rig "down" maps to −X | Confirmed: the TF908 feet lie on the plane X −1278…−1266, and the deck TF903 is vertical |

---

## 3. Answers to the eight RT-1 questions

### Q1. Guard, front posts and R wet support: must-fix before the corresponding assembly
- **Instances:**
  - P: `R16_P_R14_P_G901_001`, and `R16_P_R14_P_TF909_001/003` against P101_001/002, P106_001/002, P107_001, P107B_001, J401_001/003 and STD03C_001…008.
  - R: `R16_R_R14_R_G901_001`, `TF909_001/003`, `TF903_001` and `TF906_001` against R101/R106/R107, J401_005, STD03C_009…012 and F621_001/002.
  - Source: `evidence/R16_{P,R}_CROSS_BRANCH.json`.
- **Counterexample [V]:**
  - G901 sits at world Y −757.5…−754.5 (rig Z −216). That is 3.5 mm wetward of the flange dry edge (Y = −761) and inside the J401 glands (Y −766.5…−726.5).
  - Apart from the Ø30 shafts, nothing on the wet side extends beyond **Y = −795.0** (the STD03C stud tips; the HW_N6 nuts reach −792.6). The BK2 wet hub begins at **Y = −808.5**, which leaves a **13.5 mm free band** for the end wall.
- **Smallest change (ECO-A) [V]:**
  - Translate G901 and the two wet-end TF909 posts by **−45.5 mm** in world Y (rig assembly Z −216 → −170.5).
  - Shorten G900 ×2 at the wet end by 45.5 mm and re-drill their post holes. (The only residual hit after moving the plate is a 3 × 3 mm strip, 2,025 mm³, of G901 against G900.)
  - Drill **two new Ø9 holes in TF903** for the relocated posts.
  - Shortening and re-drilling G903 likewise is optional neatness; it only touches.
  - No new PN, and all parts are already released in SP03.
- **Result [V]:**
  - 0 wet intersections at 0/45/90° in both P and R.
  - Gap from G901 to wet non-shaft material 5.0 mm, to the BK2 hub 5.5 mm, to the shafts 3.0 mm radial through the existing Ø36 ports.
  - Window: at a 40 mm shift G901 still touches the stud tips (14.1 mm³ each); at 48 mm the BK2 gap falls to 3.0 mm.
- **Condition to record:**
  - The stud protrusion depends on the installed preload stack. Acceptance: the measured stud tip is ≥ 3 mm from G901 after assembly.
  - G901 must be removed before any gland service; it is a contact guard, not a gland boundary.
- **R wet support:**
  - Trimming the dry end of the two F621 fixture ribs to Y ≥ −715 removes all four F621 conflicts (TF903, TF906, TF909, G901) [V].
  - **This is not a fix for the integrated configuration.** F621 stands on F622 feet at Z = 1160, and the bench beneath them is absent from the R configuration, so the R valve has no load path into the rig. Use the trim only for an unloaded bench fit-up. Solve the integrated support with Q3.

### Q2. P stop direction: must-fix before motion
- **Instances:** `R16_P_R14_P_D886_001` (on P2) against `R16_P_R14_P_TF900_001`. Source: `evidence/R16_P_DRY_MOTION.json`, D886/TF900 part notes.
- **Root cause [S/V]:**
  - D886 is drawn for a counter-clockwise (CCW) sweep. At 0° the arm lies along +X_rig with its lower face (Y = −10) resting on the TF900 start post (X 55…85, Y −75…−10). At 90° it lies along +Y_rig with its left face (X = −10) against the end-post head (X −40…−10, Y 50…80).
  - P2 turns clockwise (CW), so it drives the arm straight into the start post: 6,438 mm³ at 15°.
  - A sweep toward −Y_rig is impossible with this arm in any case: the 80 mm arm exceeds the 75 mm distance to the TF900 base.
- **Smallest change (ECO-C) [V]:**
  - **Re-phase D886 by +90° about P2**, so the arm points +Y_rig at valve 0° and +X_rig at valve −90°.
  - Motion check from 0° to 90° in 15° steps against every non-P2 body, including the P1 group rotating +angle: **no overlap at any step**. Gap to TF900 is 0.000 mm at both ends (positive stops) and 10.0 mm during travel.
  - The stop roles swap: the end-post head becomes the closed stop and the start post the open stop. The contact radius stays about 65–70 mm, so the 200 N·m / 3,333 N static screen in the D886 note is unchanged.
- **Implementation:** cut a keyway in D886 **angularly under the arm root**, i.e. in phase with the arm instead of 90° behind it.
  - If D886 is already machined, wire-EDM or slot a second keyway; the old keyway stays empty, and the hub wall is 15 mm.
  - Otherwise issue D886 rev B.
  - The spindle D870, the key D884, the gear mesh phase and P1/D885 are all untouched. The leaf zero is still set by clamping the BK2 with the leaf closed and D886 resting on its closed stop.
- **Condition [C]:** the closed stop is now the TF900 end post, about 140 mm of cantilever with a 30 × 36 section. At 200 N·m (≈3.1 kN at 65 mm), the screen gives ≈0.17 mm deflection (≈0.15°) and 80 MPa. At 78 N·m it is ≈0.06°. The start post is about 10× stiffer.
  - If L1's closed-position budget is tighter than ≈0.06° at working torque, add a bolt-on brace to the end post. This is a TF900 rework, not a new design.
- **Acceptance:** an indexed 0→90° check at ≤ 5° steps or a swept-volume check, using the actual parts unloaded; final stop angles gauged to ±0.1° (TF900 note); bounded input via the existing mayr chain.

### Q3. P support orientation and wet support: must-fix before supporting or load transfer (L1 decision)
- **Facts [V]:**
  - The P rig frame (TF903 deck X −606…−594, legs TF907 along X, feet TF908 at X −1278) is a box lying on its side.
  - Masses from volume × density, with purchased proxies as upper bounds: rig drive 203.7 kg (≤ 38 kg proxy), rig frame 277.8 kg, P wet valve 64.8 kg, R wet valve 39.3 kg.
  - Rotor B200_R13: 6.19 kg, with its centre of gravity **on** the shaft axis.
  - Pressure load at 1,500 / 2,000 Pa over the 630 × 345 opening is 326 / 435 N [C].
- **Option O1 (recommended for the P1 dry-chain, torque, stop and coupling programme):** rotate the P valve 90° about its shaft axis, with P107 facing down and both shafts horizontal at equal height. Use the rig in the **same horizontal pose as R** (feet on the floor at Z = 744).
  - The R14 horizontal-gravity rows and the floor/anchor design apply unchanged, and one rig pose serves both valves.
  - Gravity deviation from the installed pose: the shaft gravity torque is 0 in both poses. The 60.7 N radial weight per rotor changes direction, not magnitude. Its friction-torque contribution, ≈ μWr ≈ 0.15 × 60.7 N × 0.015 m ≈ 0.14 N·m, is ≤ 0.2% of 78 N·m [C].
  - What O1 does **not** represent: the installed gravity direction for the feedback branches (B zero drift belongs to the B01 station) and seal-track sag under rotor weight.
- **Option O2 (installed-orientation fidelity):** keep the side-lying rig.
  - Add two outrigger RHS with feet under the drive side, extending the footprint ≥ 300 mm beyond X = −594 (restoring ≈ 1.46 kN·m against 200 N·m), plus floor anchors.
  - Re-run the 44 R14 rows with gravity in the deck plane.
  - Carry P107 on a vertical "mother-plate simulator" tied to the rig frame.
- **Wet support for either option: a rig-mounted "wet bay"** [R]. A frame extension bolted to the rig frame (two RHS legs to the floor, rails, a receiver table) carries P107 or R107 on its border. It replaces F600P/F620/F621/F622/F623 and the missing bench in the integrated configuration. Design requirements:
  - *Heights:* R107 underside 60 mm above the deck top; P (O1) shaft 104 mm above the P107 back face, against 95 mm for R, so one table works with a 9 mm riser difference.
  - *Keep-outs:* the six P root fillets with ≥ 20 mm torch corridor (equivalent to the F620 ≥ 15 mm shift, 10.3 mm gap); the R G843 boss line and M8 screw heads (Y −82…−66 on the five-bolt row); the relocated G901 plane; the flow window and leaf sweep.
  - *Alignment:* the wet and dry halves share one frame, with four-point shims at the table. Measure the BK2 rim/face offsets after clamping, cold and hot.
  - *Loads:* valve weight 65 / 39 kg; static fault reaction 200 N·m through the table bolts; pressure 0.33–0.44 kN.
- **Acceptance:** wet-bay drawing with the keep-outs Boolean-checked against the full configuration; anchor and tipping calculation; unloaded fit-up with measured BK2 offsets inside the coupling supplier's simultaneous-misalignment data for the exact variant.

### Q4. P host / F620 weld and R G843: must-fix before installed root acceptance, not before loose-part fabrication
- **P root [V/S]:** the two back fillets `P_ROOT_1/2_BACK_a4` still hit `F620_002` (281.9218 mm³ each); `evidence/R16_P_ROOT_WELDS.json`.
  - Under Q3 the integrated rig does not use F620, so the conflict is retired *if* the wet bay respects the keep-out above. The R11 shift study (geometry unchanged) shows a −15 mm support edge gives a 10.3 mm gap.
  - The **host** boundary at X ≥ −335 behind P107 is not closed by any rig work. Only the host interface drawing, or a host-simulator coupon built to it, closes it. Keep installed-root acceptance as its own gate, separate from the rig programme. The hood loose parts A01/A02 are unaffected.
- **R G843 [S/C]:**
  - G843 already implements the clamped, no-weld-on-R107 direction: five integral Ø20 bosses on the existing M8/F602 line and no root weld.
  - Because contact is only at that single boss line, the moment about X is carried by bolt preload over the boss annulus (a lever of about ±10 mm).
  - R01 closure therefore needs (i) the M8 row tightening specification and achieved preload, which is absent from the package, and (ii) a measured AM 250 N test giving boss gap, gasket-land gap at ≤ 50 mm spacing along R107/R101, and return to zero.
  - Manufacturability: the part is cut from a 238 × 47 × 209 mm block, about 92% material removal from 304L with 201 mm tall, 10 mm uprights. It is acceptable for one P1 piece. The P2 alternative is a welded base plus uprights, machined after welding, with no weld on R107.

### Q5. Measured data that closes dry/wet thermal compatibility and the 1000 N mapping: controlled-test conditional
Measure one quantity per interface, and keep force, leakage and contact as separate records:

| Interface | Measurement |
|---|---|
| D874/D875 bearing planes | Two-plane spindle displacement (capacitive or dial) at 38/78 N·m and at a 200 N·m static step. Accept against the 0.10 mm centre-distance and 1 mrad screens. |
| BK2 couplings | Rim and face offsets cold and at the hot state, compared with the supplier's simultaneous-misalignment data for the exact variant |
| J404 fixed-end stack | Axial load–displacement through the PTFE and J404 (stack compliance) |
| Each gland station | Four simultaneous stud forces (instrumented studs or calibrated washers) with measured uncertainty, which defines the guard band below 1,800 N |
| Seal track | Seal compression or gap every ≤ 50 mm, before and after preload, and after a thermal cycle |
| Leakage | Leakage measured separately at 500/1,500 Pa |

### Q6. Continuous supported removal and reinstallation: must-fix before maintenance, not before first assembly
- **Evidence [S]:** `R16_REAR_PLATE_PATH_COUNTEREXAMPLES.json` and `R16_ACTUAL_NUT_TOOL_ACCESS.json`. Every blocker is a **removable dry-rig part**:
  - D875 screws (M5×20 and M10×45);
  - D879 caps and the 7206 bearings;
  - TF900;
  - the D886/D888 arms and D885;
  - the mayr BUY520 with its 8 × M6×20;
  - BK2, D894/D884, D890/D892/D893 ahead of the D873 nuts.
- **Interpretation [R]:** these entries define precedence. No cyclic dependency appears in the supplied counterexamples, so a valid order is likely to exist. What is missing is a **written sequence with a captured load at each step**. Draft order for P:
  1. Isolate, depressurize, cool.
  2. Lock each wet rotor at its BK2 wet hub.
  3. Mayr and M6 screws.
  4. D885, then D886.
  5. TF900 (2 × M12).
  6. D879 caps, M5 and M10 screws.
  7. Withdraw D875 by 85 mm.
  8. D873 nuts, after BK2 and the stop/adapter hubs.
- **Missing hardware:** a wet-rotor lock rated for the 500 N handling perturbation. The 200 N / 50 N spindle cradle does not cover it.
- **Acceptance:** a precedence table derived from these JSON files, each step with a named load path; a dry run on the unloaded rig.

### Q7. Can a shop build each configured PN from the release index? Must-fix before claiming a complete kit
Source: `tables/R16_CONFIGURED_MANUFACTURING_GAPS.csv`. The proposed waves are in `results/results_r16_release_waves.csv` [V].

| Proposed wave | PN | Pieces | Content | Gate |
|---|---|---|---|---|
| Released (no change) | 66 | 200 | R14 rig loose parts, hood A01/A02 | Installation acceptance |
| **ECO on released parts** | 5 | 9 | D886 keyway; G901/TF909 relocation; G900 shortening; TF903 holes | L1 approves ECO-A and ECO-C |
| **W1: release now** | 41 | 315 | P101–P104, P102A–E, P105A/B, P106, P109, P110; R101–R104, R102A/B, R105A, R106, R109, R110, R112, R113; S301A/B/C, S303, S311–S313; F602/F603; STD01PC; A705–A710 | BRep identical R11→R16; no R16 conflict touches them |
| **W1: commodity hardware** | 50 | 1,038 | A4-80 / 8.8 screws, nuts and washers | Authorization only |
| **RFQ now** | 9 | 19 | KHK SSG3-55F30B, NSK 7206 BEAMRSUCNB, R+W BK2 (2 variants), mayr 110/160, HBK T210, Baumer encoder and coupling | Written version, fit and lead-time confirmation; user authorizes any external contact |
| W2: weld spec first | 1 | 3 | B200_R13 rotors | Weld sequence, runout and journal-protection definition |
| W2: after SP04 dimensional first article | 12 | 141 | J401–J408, STD03C/04C/05B, F604 for the remaining five stations | Extend the SP04 scope after its dimensional FAI; preload stays unreleased |
| W2: station consumables | 6 | 429 | BUY548, BUY402, 001500A, hard washers, HW_N6/W6 | Follow the station allocation |
| W3: after B01 data | 8 | 30 | A703P/R, A704R8, B850–B853, guide screws | Installed feedback branches |
| Hold (root/host) | 5 | 5 | P107, G840P1/P2, G843, R107 | Q4 |
| Supersede | 5 | 11 | F620–F623, P107B | Replaced by the wet bay (Q3) |

Two definition gaps remain beyond W1:
- the shell **weldment** definitions (P100F/B, R100F/B/S), covering weld sequence, distortion allowance and post-weld line-boring of the shaft bores, which P102 notes require after assembly;
- the B200_R13 rotor weld specification.

Both are short definition tasks, not design work.

**Schedule arithmetic, not a commitment.** With the user's roughly 1-week factory cycle and decisions on ECO-A, ECO-C, O1/O2 and W1 within about a week, the shop critical path is:
- W1 cut and gasket parts → shell welding → post-weld boring: about 3 cycles.
- Rotor welding, in parallel once the weld spec exists.
- Wet-bay fabrication, in parallel.

The unknown that dominates is the lead time of the nine critical purchased items. That is why the RFQs should go first.

### Q8. Simplifications worth deferring: P2 only
- G843 one-piece from solid → welded base plus uprights, machined after welding.
- G840P milled L-beams → formed angle, once the P root is settled (R11 DFM-14; L1 conditional).
- Motion verification at ≤ 5° steps or by swept volume instead of 0/45/90. This is not a deferral: it is cheap, and it found the 15°/30° overlaps here.
- Do not reopen the released SP01–SP04, A01/A02 or B01 batches for cost or appearance.

---

## 4. Confidence and what would change these conclusions
| Conclusion | Confidence | What would change it |
|---|---|---|
| ECO-C (D886 re-phase) clears the P stop with TF900 unchanged | High for nominal geometry at 15° steps | A continuous or tolerance sweep showing a hit; a closed-stop stiffness budget below ≈0.06° at 78 N·m (then add the TF900 brace) |
| ECO-A (−45.5 mm guard relocation) clears all wet conflicts | High nominal; the 5 mm stud margin is sensitive to the installed stack | Measured stud protrusion after preload; a G901 attachment detail not in the BRep |
| O1 is adequate for dry-chain verification | Medium. The quantities are small, but the choice depends on which outputs L1 wants from the rig. | An L1 requirement for installed-orientation seal or feedback data on this rig, which means choosing O2 |
| W1 parts can be released without rework risk from R16 decisions | High for R16 interactions (BRep identity, no conflicts). Medium overall, because G1 and seal-preload outcomes could still change gland-side interfaces, not shells. | A G1 or seal decision that moves the gland seat on the flange |
| The maintenance route is a sequencing task, not a geometric dead end | Medium; only the supplied counterexamples were examined | A blocker that is not removable, or a cyclic precedence |

## Appendix: files and reproduction
- `RT1_FINDINGS.csv`: one row per finding, in the RT-1 return format.
- `tools/r16_eco_check.py`: baseline reproduction, ECO-A shift study, ECO-B F621 trim, ECO-C D886 re-phase sweep.
- `tools/r16_mass.py`: masses and centres of gravity by group.
- `tools/r16_release_waves.py`: proposed release waves; the classification rules are explicit in the source.
- `tools/run_r16.sh <R16 zip>`: verifies the 209-entry manifest and regenerates `results/`. The package is treated as data and no project script is executed. Output was regenerated byte for byte.
