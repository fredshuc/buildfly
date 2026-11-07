# C10 — Red-team review of the integrated sheet-metal structure

C10 integrates the H01 horizontal heat exchangers, D04 dampers and HYD-S2 water circuit into the four-core AirTransformer assembly. This review should determine whether the revised sheet-metal interfaces are ready for the next prototype-detailing stage and identify what must be resolved before fabrication or wet operation.

**Status: geometry review candidate; manufacturing release is not granted.** The recorded geometric checks pass within the scope below. They do not establish structural capacity, leak tightness, thermal performance, pressure ratings or airflow uniformity.

| Review reference | Value |
|---|---|
| Repository / branch | `fredshuc/buildfly` / `codex/c10-four-core-prototype` |
| Reviewed CAD and evidence commit | [`a42fdb87a09ce56a657d70e35181e55a0f6dfd9c`](https://github.com/fredshuc/buildfly/commit/a42fdb87a09ce56a657d70e35181e55a0f6dfd9c) |
| Input-collection parent | `918a444cfa939311676e108b373b2fcbeafe76f6` |
| Structure baseline | C09R1, as supplied in the D04 installed models |
| Units / placement | Millimetres; shared global assembly coordinates |
| Operating states | S1: A process / B regeneration. S2: A regeneration / B process. |

**HYD-S2 names the water-circuit revision; it does not mean operating state S2.** This English README is a documentation supplement to the issued C10 package. The existing CAD, validation records and ZIP are unchanged; this supplemental README is supplied alongside that ZIP.

## 1. Files to open

1. Open [C10_INSTALLED_S1.step](cad/C10_INSTALLED_S1.step) and [C10_INSTALLED_S2.step](cad/C10_INSTALLED_S2.step) separately. They represent alternative operating states, not two assemblies to combine.
2. Open [C10_CHANGED_SHEET_AND_GLANDS.step](cad/C10_CHANGED_SHEET_AND_GLANDS.step) to isolate the 75 changed/new occurrences. Use [C10_SHELL.step](cad/C10_SHELL.step) for their structural context.
3. Review the STEP-derived sections in [C10_STRUCTURE_REVIEW.png](C10_STRUCTURE_REVIEW.png).
4. Overlay [C10_SERVICE_AND_THERMAL_REFERENCE.step](cad/C10_SERVICE_AND_THERMAL_REFERENCE.step) in the same global coordinates. Its motion, tool, removal and insulation references must not be counted as installed hardware. Inspect envelopes according to their intended service sequence.
5. Read [VALIDATION_SUMMARY.json](VALIDATION_SUMMARY.json), then the detailed evidence linked in section 4. Use [CHANGED_PARTS.csv](CHANGED_PARTS.csv) and [shell_changes.json](evidence/shell_changes.json) to identify exact part names and bounds.

Each installed state contains **3,116 occurrences**. Occurrences include repeated instances, seals and simplified hardware; this count is not a procurement BOM.

| Assembly group | Occurrences per state |
|---|---:|
| Shell, frame, retention and seal components | 560 |
| D04 damper components | 244 |
| Four H01 heat exchangers | 2,204 |
| Eight removable first-spool assemblies | 72 |
| HYD-S2 water rack | 36 |

## 2. Incorporated owner updates

| Input | Incorporated interface and retained intent | Source |
|---|---|---|
| H01 heat exchangers | Four placements of one unhanded core; eight horizontal water faces at X = -787.5; removable first spools of 77.5 mm to the rack interface at X = -865; wet-bay insulation and tool/removal envelopes | [H01 archive](../../../HX/M101_C08_HORIZONTAL_H01/HX_C08_H01_HYDRONIC_RETURN.zip) |
| D04 dampers | C09R1 upper Pin-seat/gasket relief, R20.5; local seal continuity, retainers and hardware; 244 damper occurrences in each state | [D04 archive](../../../dampers/c09r1-d04/D04_PIN_W2_REVIEW.zip) |
| HYD-S2 water circuit | Revised FS/Q placement, three external bridge pipes per bed, water rack, service envelopes and upper W2 insulation/host-space request | [HYD-S2 archive](../../../hydronics/H01_HYD_S2/HYD_S2_WATER_DELTA.zip) |
| D03 motion/service basis | 46 motion and 36 service envelopes retained as the D04 motion baseline | [D03 archive](inputs/D03_MOTION_AND_SERVICE.zip) |

[INPUTS.json](INPUTS.json) pins all four source archives by SHA-256. The owner components retain their supplied geometry and placements. C10 replaces the earlier H00 core/water references in the coordinated installed assembly; reviewers should not overlay those older installed components on top of H01/HYD-S2.

The cold-water series path remains lower-core W1 to W2, through FS/Q, then upper-core W1 to W2. Hot flow reverses and enters upper-core W2. The common return controls, four selector valves per bed and series architecture are retained. Owner flow/pressure-drop figures remain design inputs, not measurements made by this shell revision.

## 3. Sheet-metal changes to challenge

### A. Eight outer-skin penetrations and four split gland assemblies

- Outer-skin openings at approximately X = -650 follow H01: W1 diameter 120 mm and W2 diameter 94 mm. Centres follow the pipe crossing at the skin, not the remote threaded-face coordinates. The eight inner-wall diameter 45 mm passages and D04 upper W2 interfaces are retained.
- Each bed/level receives one two-hole gland assembly: two 1.5 mm steel retainer halves, a 0.3 mm split, a flexible boot represented at 2 mm installed thickness, and six M4 studs/nuts. Fixing positions are in [GLAND_FIXINGS.csv](GLAND_FIXINGS.csv).
- The flexible boot follows the supplied wet-bay insulation contour. Its intended load path is through the outer skin and insulation seal, without clamping the copper pipe. Material, compression, bonding, service-slit closure, torque and stud strength remain to be specified/validated.
- Final steel-retainer openings are diameter 126/100 mm. They permit the checked 12 mm axial withdrawal in the -X direction after nut removal, with studs and the corresponding wet-bay insulation present. Final upward/downward removal around installed pipework still requires a dry assembly trial.
- An earlier smaller retainer opening produced approximately 6.187 mm³ of interference during withdrawal. That development failure is retained under [development_pass1](evidence/development_pass1/); the final release check is in [detail_measurements.json](evidence/detail_measurements.json).

Review assembly order, hand/tool access, replaceability of the consumable boot, vapour sealing and whether real tolerance/thermal movement can load the pipe or tear the seal.

### B. Two raised upper-W2 insulation pockets

- The supplied additional insulation reaches Z = 1164.85; the requested installation-space envelope reaches Z = 1166.85. C10 raises the local inlet-floor/wrap corner with a 1.5 mm roof whose underside is Z = 1168.5 and top is Z = 1170.
- Rear returns occupy X = -584 to -582.5. Inboard returns terminate at A: Y = -744 and B: Y = 120. The retained upper Pin seat provides the front closure; the new roof and inboard return meet that existing component.
- Exported face-contact areas with the seat are 33.75 mm² at the A roof, 77.25 mm² at the B roof, and 37.5 mm² at each inboard return. These are geometric contact measurements, not weld areas qualified for strength. Rear returns do not meet the seat and are excluded from that particular contact criterion.
- The A post, sister RHS reinforcement and four connecting webs remain intact. The minimum measured separation from the additional insulation to the A post is 2.0 mm; minimum separation to changed shell geometry is 3.65 mm, at the B pocket roof.

Review continuous closure, weld/seal accessibility, tolerance accumulation and condensation at the locally reduced insulation near the post. Nominal clearance and touching CAD faces do not prove an airtight or vapour-tight assembly.

### C. Upper-plenum roof and inner cheek

- The terminal core-face region gains approximately 60 mm of roof height relative to the earlier profile. The rear inlet interface, feedback-cover recess and final outlet datum are retained.
- New roof segments use 1.5 mm thickness normal to the sheet. The inner cheek is extended to follow the new roof; the existing outer cheek is retained.
- The minimum sampled roof-underside height above the fin top over the terminal 100 mm is 99.180 mm at the central section. Maximum sampled signed roof-to-inner-cheek shortfall is 0.043402 mm. These are nominal model measurements, not fabrication tolerances or proof of a sealed joint.
- Bend radii, bend allowances/K factors, flat patterns and weld-distortion allowances remain fabrication-detail work. Added plenum depth is an airflow-improvement candidate; no CFD, coated-core pressure-drop test or flow-uniformity result is claimed.

Review the retained transitions and outlet, access to the new joints, manufacturability and whether the actual resistance distribution supports the intended airflow improvement in both operating states.

## 4. Verification evidence and its limits

| Check | Recorded outcome | Evidence / interpretation |
|---|---|---|
| Exported S1/S2 readback | 3,116 occurrences per state; zero invalid parts | [S1](evidence/verify_S1.json), [S2](evidence/verify_S2.json). All occurrences are included; exact repeated local topology is validated once and reused for rigid instances. |
| Retained component comparisons | Named placements agree with source models within recorded limits | Retained shell/D04 checks compare volume and bounds; H01, rack and spool checks compare names and global bounds. These checks are not an independent redesign or certification of owner components. |
| Installed cross-group intersections | No hits above 0.001 mm³ | All ten pairings among shell, dampers, complete HX group, rack and first spools are screened. Conservative bounds select candidates; exact solid intersections decide them. |
| Changed-shell self/context intersections | No increases reported | Changed/new parts are checked against the shell. Existing pair overlaps are compared to the parent; an increase above 0.01 mm³ is reported. This does not certify every inherited shell joint or every internal owner-assembly contact. |
| Motion, service and thermal references | No hits above the stated threshold against changed shell geometry | D03 motion/service, D04 local service, H01 service, HYD-S2 service/outboard, requested host space and additional insulation. D04 is also checked against the added insulation. Full maintenance procedures still require review. |
| Roof thickness, pocket contacts, retainer release | PASS within the individual criteria | [Detail measurements](evidence/detail_measurements.json), [measurement source](source/measure_detail.py). The retainer check is the initial axial release, not the complete removal sequence. |
| Reference-overlay export | All 328 named occurrences match source world bounds | [Overlay readback](evidence/service_overlay_readback.json): 226 combined HYD/H01 service, 4 outboard, 14 D04, 82 D03 and 2 W2 crown references. |

The positive-volume intersection threshold is a numerical screening rule, **not a minimum allowable mechanical clearance**. Zero hits does not close tolerance, thermal-growth, vibration, accessibility or safety questions. Review the executable criteria in [verify.py](source/verify.py), including exclusions and baseline comparisons, before relying on its `pass` flag.

## 5. Requested red-team findings

Please distinguish newly introduced defects from inherited unresolved items, and give each finding a reproducible location and a disposition. Suggested identifiers below are review topics, not findings already established by this README.

| Topic | Questions / evidence required for closure |
|---|---|
| RT-C10-01 — Glands and service | Can each retainer and boot be installed and fully removed in the real sequence? Are tool access, split sealing, preload, stud pull resistance and pipe isolation adequate? Verify with tolerances and a dry assembly. |
| RT-C10-02 — Pocket closure and cold surfaces | Are all pocket/seat seams accessible and continuously sealable? Does insulation remain effective at the A post under the lowest water temperature and highest design dew point? Specify leak and condensation tests. |
| RT-C10-03 — Plenum and airflow | Do both duties achieve the required flow distribution with measured coated-core resistance? Check the terminal 100 mm, outlet transition and feedback-cover interface. Nominal depth alone is insufficient. |
| RT-C10-04 — Sheet manufacture | Resolve bends/flat patterns, seam sequence, material choices, tolerances and distortion. Check that fabrication details preserve valve motion, service space and sealing. |
| RT-C10-05 — Structural load paths | Review the retained A-post reinforcement and [A_POST_WELD_REGISTER.csv](A_POST_WELD_REGISTER.csv). Define loads, weld sizing/procedure, frame stiffness, handling and fatigue requirements. The register locates interfaces; it supplies no rated capacity. |
| RT-C10-06 — Water-rack support | Complete the independent load-bearing rack support and pipe clamps. Demonstrate that component/pipe weight and operating loads do not transfer into HX nozzles, seals or thin skin, and preserve service envelopes. |
| RT-C10-07 — Inherited damper/HX gates | Revisit D03 lower-shaft 1.0 mm end clearance and upper-sweep thermal/tolerance margin, D04 consumable-seal retention, full-core extraction, HX face-seal compression, condensate drainage and trap details. |
| RT-C10-08 — Water-system commissioning | Obtain owner signoff for actual connection stacks, component pressure/temperature ratings, anti-pullout, isolation/relief and reverse hot-flow operation. Confirm test prerequisites before wet operation. |

For each finding, return:

- **ID, severity and disposition:** fabrication/operation blocker, prototype prerequisite, or improvement; include whether it is new or inherited.
- **Location:** S1/S2 or both, exact component names, global coordinates and a marked section/screenshot where helpful.
- **Evidence and failure mechanism:** measured clearance/interference, assembly step, load assumption or test condition; separate observation from inference.
- **Required change and closure evidence:** proposed correction, responsible discipline, and the calculation, measurement or test needed to close it.

Conclude with separate dispositions for geometric integration, prototype detailing, fabrication readiness and wet-operation readiness. List unresolved blockers explicitly. Do not treat the current geometry PASS as approval for the latter stages.

## 6. Package integrity and reproduction

The issued [C10_REVIEW_PACKAGE.zip](C10_REVIEW_PACKAGE.zip) is self-contained with repository-relative paths. It includes the owner input archives, editable Python sources, STEP models, interface tables, diagram and recorded checks. [MANIFEST_SHA256.json](MANIFEST_SHA256.json) covers its 37 payload members; the manifest is the 38th ZIP member. [PACKAGE_RECEIPT.json](PACKAGE_RECEIPT.json) identifies the archive itself. This supplemental README is outside that issued archive/manifest.

| Artifact | SHA-256 |
|---|---|
| Issued ZIP, 52,565,707 bytes | `ec2bdaca80646c54479c436cfc3cdf311a1521b589d9341a45811f5a3d72b6ff` |
| Installed S1 | `55f43f07d34ba2ec186b634673f06bc3efdf6dfdc911c11433e07fd720a67f09` |
| Installed S2 | `5e547cd158b5c6d3692a940d672a6aa8a1ae074655237abf4ff09e1fbfe0ecff` |
| Shell | `bc7b82ca5a851cf371baa1f6a4760e7a52b8f0d221b1d975f098e56fd74ff1b3` |

Verify the issued archive before rebuilding. Rebuild in a separate extracted copy or worktree because generation overwrites local CAD/evidence and a new package may have different byte hashes.

Dependencies: Python 3.12, CadQuery 2.8, OCP 7.9 and NumPy; Matplotlib is required for the figure. If dependencies are outside the Python environment, set `CADQUERY_LIBDIRS` to their directories using the operating system's path separator. From `AirTransformerShell/revisions/C10`, run:

```text
python source/prepare.py
python source/build.py
python source/verify.py S1
python source/verify.py S2
python source/measure_detail.py
python source/verify_service.py
python source/draw.py
python source/package.py
```

On restricted Windows systems where Python's WMI metadata query stalls, `C10_NO_WMI=1` enables the process-local metadata fallback used during this build. It does not change machine settings. Runtime libraries and the regenerable `.work/` cache are intentionally excluded from the repository.
