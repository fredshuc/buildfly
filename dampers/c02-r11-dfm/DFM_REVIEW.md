# AT-DMP02 C02 R11 damper: DFM review and manufacturing-acceleration plan

**Basis:** red-team pack `AT_DMP02_C02_R11_REDTEAM_CROSS_SECTION_20261012.zip` (10,041,000 bytes, SHA-256 `2b30ed4f…5f2857`); all 30 pack files match `03_FILE_INDEX.csv`. The native R10→R11 delta was re-derived independently and matches the pack: 263 definitions and 2,488 instances, with 5 changed BReps, 10 added and 248 unchanged.
**Review date:** 2026-10-12. **Status of the design:** still `PARTIAL / NOT_FOR_MANUFACTURE`. This review authorizes no build, purchase or test. It recommends the changes and evidence that would let one happen sooner.

Evidence tags: **[V]** verified or computed here from the native CAD; **[S]** stated in the pack; **[C]** a screening calculation made here, with its assumptions given; **[I]** an inference; **[R]** a recommendation.

---

## 0. Conclusion

1. **No production release is possible from R11, and DFM work on the hood (A) or the feedback equaliser (B) cannot change that.** Two whole-machine gates are still open and R11 did not touch either one: G1, the main shaft and gear support, and the seal-seat preload. The project's own record shows that the plain bushings, on clearance alone, already use **2.13 mrad** of tilt against a **1 mrad** screen [S/C]. Further iterations on the bushing layout cannot close G1. A preloaded rolling-bearing cassette, measured on a bench, can.
2. **Several of the A/B holds are misclassified or self-inflicted, and each can be cleared by a specific change rather than another analysis round:**
   - The "decisive" P-root weld clash (2 × 281.92 mm³ per MANUAL state) is with **F620_002, a trial-assembly fixture rib**. It is not a product part. Moving that rib 6 mm clears it with no new interference anywhere [V].
   - The more serious question about the P root went unasked. The root shoe sits on the **host-side face of P107** (X −335…−329, the "mother-plate face X=−335"). The host is not in the model, so the AUTO-state collision check cannot see a clash there [V/I].
   - None of the P-root fillets, and none of the R-foot fillets, reach the minimum length that EN 1993-1-8 allows to carry load. The R-root welds also sit directly behind the R106 gasket land on a 3 mm plate [V].
   - A **bolted, clamped 6–8 mm doubler** under the five existing M8 screws, which already have F602 metal compression limiters, takes the R receiver screen from **200.8 MPa to 31–55 MPa** with no welding on the seal frame [C].
   - The G837 "−9 mm²" is a 3×3 mm corner lying 22.6–26.9 mm from the M5 axis, well outside the roughly 8 mm clamp cone. It can be closed by calculation [V/C].
3. **B (the encoder zero) is a measurement problem, not a design problem.** I re-implemented the project's three-DOF model and reproduced it to every printed digit (0.040443837° and −0.031071726°). In that model, predicted drift scales almost as **1/kt**, the encoder-half grip stiffness. That value is an unmeasured assumption of 1×10⁵ N·mm/rad. The crown rolling-hysteresis arm is the second driver. The geometry of the spherical seat has almost no effect. At kt ≥ 3×10⁵ N·mm/rad and a rolling arm ≤ 0.015 mm, the worst-case drift falls to **0.0083° thermal and 0.0053° residual** [V/C]. A single afternoon torsion test gives kt directly, because kt = ΔT/Δβ under the ±0.30 N·m proof torque.
4. **Two B parts need DFM changes before anyone cuts metal:**
   - The B852 Ø3 m6 press fit into a Ø2.98 bore puts **459–1,070 MPa of hoop tension** into a 2.51 mm wall of HRC 58–60 440C, inside the load-bearing crown. It also grows the crown radius by 2–5 µm against a ±10 µm profile tolerance [C]. The pin carries no load by design, so a slip fit with positive retention is enough.
   - The SR20 seat tolerances are not functional: across the 0.94 mm contact annulus they produce less than 0.4 µm of gap [C].
5. **The fastest credible path** is to stop the 90-minute model-iteration rounds, build instrumented engineering test articles of the current geometry with the DFM corrections below, and measure the roughly six parameters that every open hold depends on. Section 7 sets out the plan with acceptance criteria. As a planning estimate, an A/B local release candidate in 6–8 weeks is plausible. Whole-machine release is gated by G1 and the seal preload, and cannot be dated until the bearing-cassette bench test exists.

**Decisions the project owner needs to make now**, each of which unblocks work:
- D1: obtain the host interface drawing for the P107 back face.
- D2: approve bolted (clamped) receiver roots instead of welds on the seal frames.
- D3: set an explicit angle allocation for the B joint (for example 50% of the 0.04° thermal and 0.03° repeatability ceilings).
- D4: authorize an engineering-test-article build and supplier RFQs. These are not production purchases.

---

## 1. Scope and method

- **Inputs** [V]: pack index (30/30 SHA-256), `R11_FULL_ENGINEERING.zip` (native BRep and placements for R9/R10/R11, STEP, evidence, source), drawings (6/31/12 pages), BOM (263 lines), and the signed L1/L2 records R5, R7, R10, R11.
- **Tools** (all in `tools/`, rerun with `tools/run_all.sh <pack.zip>`; output reproduces byte for byte):
  - `native.py` is an OCP-only loader that does not import project code.
  - `check_a_root.py` covers the A-root geometry: weld-bead reconstruction, the fixture-shift study, host-side occupancy, weld eligibility, gasket-land overlap and G837 support.
  - `b_equaliser_sensitivity.py`, `b_driver_sweep.py` and `b_measurement_grid.py` re-implement the R11 B control model with unchanged constitutive laws and with the sphere radius, crown radius, rolling arm and kt exposed as parameters.
  - `dfm_calcs.py` holds the closed-form screens.
  - `bom_routing.py` classifies process routes and tolerance tokens.
  - `native_delta.py` audits the R10→R11 delta.
- **Out of scope:** new product CAD, FE models, the supplier quotes themselves, and any physical test. Where a proposal needs CAD, the review states the constraints the CAD must meet. It does not draw the CAD.

---

## 2. Findings, ranked

| ID | Pri | Area | Finding | Tag | Action |
|---|---|---|---|---|---|
| DFM-01 | Critical (schedule) | A / P root | The P a4 fillet clash (281.92 mm³ ×2, MANUAL only) is with **F620_002, a trial-assembly fixture rib** (scope FIXTURE; note: "installation / hole-position fixture only"). Shifting the rib −6 mm in Y clears it with a 1.34 mm gap; −15 mm leaves a 10.3 mm gap and stays inside the P107 border. No other body is hit for shifts up to 25 mm. | V | Reclassify the RT-05 P clash from a product blocker to a fixture ECO. Note that weld *access* needs more than clearance (DFM-02). |
| DFM-02 | Critical | A / host interface | The P root shoe and fillets occupy X −335…−329, the **host side of P107** ("mother-plate face X=−335"; "do not drill through to the machine-side mother plate"). In AUTO the only bodies in that zone are the two shoes, at 1,560 mm³ each, because the host is not modelled. If the host plate backs P107 over Y −71…−55, the root is a hard clash once installed. | V + I | **D1:** obtain the host interface drawing ("see interface drawing" is cited but not in the pack). No further P-root design until it is in hand. |
| DFM-03 | Critical | A / weld design | Under EN 1993-1-8 §4.5.2(2), welds with l_eff ≥ max(30 mm, 6a) are the only ones that may carry load. P back fillet l_eff = 18 mm, P end fillets 2 mm, R foot fillets 20 mm and 3 mm: **none qualify**. Only the 148 mm G842 edges and the frame welds do. The fillets are also over-sized for thin plate: a3 on 3 mm R107 and a2 on 2 mm G830 give a/t = 1.0, against common practice of ≤ 0.7. P-root elastic weld-group screen under a 250 N lateral load: **129 MPa** from Mz, because the lever is only the 10 mm shoe/P107 overlap. | V / C | Do not repair by longer welds on the seal frames. Re-root by bolting (DFM-04, §3.2). |
| DFM-04 | Critical | A / R receiver and seal | All R-root weld footprint (1,800 mm²: two feet plus G842) lies **directly behind the R106 static-gasket land** on the opposite face of the 3 mm R107. The project screen is 200.8 MPa against a 160 MPa limit. A **clamped doubler** (Y −90…−55, X −200…36, five Ø9 holes) under the five existing STD01B M8×25 screws, which have F602 Ø16/Ø8.5×2 metal compression limiters, gives **55 MPa at 6 mm or 31 MPa at 8 mm** on the net section. The bolt-load increment is ≤ 0.79 kN per bolt and R107 is only clamped. | V / C | **D2:** adopt it. Weld or bolt the beams to the doubler on the bench, machine the face after welding, and fit M8×30 or M8×35 screws. |
| DFM-05 | High | A / G837 | The −9 mm² per pad is the 148 window corner cutting a 3×3 mm corner from each pad. It lies 22.6–26.9 mm from the M5 axis, against a clamp-cone radius of about 8.3 mm. It is a 1.5% area loss outside the clamped zone. | V / C | Close RT-06 by this calculation, with no geometry change. Record a G837 bearing pressure from the AM load set. |
| DFM-06 | High | A / G830 frame | "Post-weld flatness 0.15" on a 2 mm, 200×200 frame welded on two edges with a2 fillets. ISO 13920 class E, the tightest class, allows **1.0 mm** for 120–400 mm, so the requirement is 6.7× tighter. | S / C | Screw the frame to machined beam faces (M4, no weld), or make it from ≥ 4 mm and machine it after welding. |
| DFM-07 | High | B / B852 | A Ø3 m6 pin pressed into a Ø2.98 bore **coaxial with the R4 crown**, wall 2.51 mm, HRC 58–60. With the bore assumed H7: contact pressure 347–809 MPa, **bore hoop tension 459–1,070 MPa**, crown radius growth 2.2–5.2 µm against a ±10 µm profile tolerance. The pin's own note says it is not load-bearing. | C | Replace with a Ø3 H7/h6 slip fit plus a retaining feature, or an ISO 8752 spring pin in a standard Ø3 bore. Wire-EDM the bore in the same setup as the crown. |
| DFM-08 | High | B / zero drift | In the reproduced model, drift is governed by **kt**: 1e5 → 3e5 → 1e6 N·mm/rad gives 0.0404 → 0.0129 → 0.0038°. The **rolling arm** is next: 0.030 → 0.005 mm gives 0.0404 → 0.0165°. Sphere radius has **no effect** (R30 = R20) or a slightly adverse one (SR9: 0.0428°). Seat friction is minor. | V / C | Measure kt and the rolling arm (E3). **D3:** set the joint allocation. Stop parametric redesign of B until those numbers exist. |
| DFM-09 | Medium | B / seat tolerances | The SR20 bridge dimple is 0.5 mm deep. The contact annulus is Ø7–Ø8.89, only 0.94 mm wide; it is effectively a cone of about 78.5°. Over that annulus, the specified radius mismatch of 0.01–0.04 mm leaves a 0.09–0.38 µm gap, which is below the Ra. | C | Relax SR to ±0.05 and control the annulus axial position and flatness instead. A DIN 6319-C/D pair (Ø12/Ø6.4, SR9) is a catalogue option with a +0.0024° model penalty. |
| DFM-10 | Medium | B / crown contact | p0 is 936 MPa (project) or **974 MPa** with both springs at their individual maxima, against an estimated first-yield p0 of about 1,950 MPa for 17-4PH H900. The static margin is about 2. A 1 mrad axial misalignment gives 10.5 µm against 3.7 µm of elastic approach, so the line contact relies on self-alignment through the spherical seats. | C | Wire-EDM the 2.5D bridge outline from hardened 440C, with skim passes and polishing to remove recast at the crown. Use a blue-check contact pattern of ≥ 80% length as the acceptance test. |
| DFM-11 | Medium | Drawings | (a) Two general-tolerance regimes in one booklet: R9 pages use machined ±0.10 and laser ±0.20; R11 pages use **±0.05 and ±0.10**. (b) No ISO 2553 weld symbols and no WPS/WPQR reference. (c) The **0.01 mm** P/R111 shim has a group tolerance of ±0.015, which is larger than the nominal. (d) The G837 pocket "inside corner R ≤ 0.1" cannot be milled; R ≤ 0.51 is compatible with the 0.2 block chamfer. (e) In the G840 relief pockets, an R3 cutter corner leaves 0.17 mm of the 1 mm clearance. (f) Custom washers (HW_R8_HOOD_W5, thickness ±0.02) are specified where ISO 7089 exists. | V | Issue a drawing standard (§6) before any RFQ for make-parts. |
| DFM-12 | Medium | Configuration | Unrelated parts share PN prefixes: **G840** (side-panel weld-nut block, 40 instances) and the R11 G840P1/P2/R1/R2 beams; **A704** (input bracket post) and A704R8 (feedback jaw). **P107 is a component of two weldments**: the F600P trial fixture and R11_HOOD_P_ROOT. | V | Renumber the R11 beams. Decide whether P107 ships with the valve or belongs to the host, and which weld sequence applies. |
| DFM-13 | Critical (whole machine) | G1 support | From the project's own R7 numbers: the D547 bushing's radial clearance of 0.0505 mm gives a 4c/95 tilt of **2.13 mrad** before any load. Meeting 1 mrad would need c ≤ 0.024 mm on Ø30, with 80 K thermal swings. | S / C | Stop iterating the bushing layout. Use a preloaded rolling-bearing cassette with line-bored centres (D546 already moves in this direction) and run a bench tilt test (E6). |
| DFM-14 | Medium | A / beams | The G840P weak axis (10 mm deep in Y) carries the largest root moment, Mz/2 = 29.6 N·m: 68 MPa and a 7–15 mrad rotation bound. The beams are milled L-sections from a 206×21.5×26 envelope, about 58% stock removal. | C | Use a laser-cut and press-braked 3–4 mm angle or an EN 10056-1 L30×30×3 (I ≈ 1.4×10⁴ mm⁴, 6.5× the weak-axis stiffness). |
| DFM-15 | High (schedule) | Purchased | 72 purchased PNs, 1,743 instances. The critical items: KHK SSG3-55F30B (status unclear), Valpes actuators (CAD and stop/fault data missing), Baumer encoder and coupling (exact revision), SCHNORR 001500A and 002700A (batch curves), mayr 490.715, HBK T210, R+W BK2, SKF 6005. | S | **D4:** issue RFQs and written-confirmation requests now (§5.2). |
| DFM-16 | Low | J408 | A 0.5 mm 100Cr6 HRC 55–60 washer, Ra0.4, parallel within 0.01 (48 pcs), sitting in an A4/304L assembly. It is a corrosion and heat-treat-flatness risk. | S / I | Specify a hardened martensitic stainless or a catalogue hardened stainless washer. |

---

## 3. A: hood receiver

### 3.1 The P-root "decisive blocker" is a fixture interference [V]
`check_a_root.py` rebuilds the six P-root a4 fillets exactly as the R11 audit does (throat 4, leg 4√2) and intersects them with every MANUAL-state body. The only hits are `P_ROOT_1_BACK_a4` and `P_ROOT_2_BACK_a4` against **F620_002**, at 281.9217895 mm³ each. That matches `R11_P_ROOT_WELD_AUDIT.json` exactly, and the pack's own decision key already calls it `..._MANUAL_FIXTURE_INTERFERENCE_HOLD`. F620 is defined as follows:

- PN "P trial-assembly upright rib", scope FIXTURE, configuration MANUAL only.
- It is welded into F600P, the independent trial-assembly fixture weldment.
- Its notes say it is an installation and hole-position fixture only, and that its stiffening of the receiver frame must not be used to prove installed sealing or load performance.

Results of shifting the F620_002 rib (Y −74…−66) in −Y, re-checked against the fillets and every MANUAL body:

| Shift (mm) | 0 | 5 | 6 | 8 | 10 | 15 | 20 |
|---|---|---|---|---|---|---|---|
| Fillet hits | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| Min gap to fillets (mm) | 0 | 0.34 | 1.34 | 3.34 | 5.34 | 10.34 | 15.34 |
| Other new hits | – | none | none | none | none | none | none |

Clearance is not access. The shoe sits 1.0 mm above the rib, so a GTAW torch (gas cup about Ø12) cannot reach the back-fillet root at 45° until the rib is at least about 15–20 mm away. A 15 mm shift keeps the rib on the P107 border (Y −93…−55) and out of the flow window. **This is a fixture-only change** [R], but see 3.2 before relying on any welded P root.

### 3.2 The real P-root question: what is behind P107 once installed? [V/I]
- The P107 notes say: "keep mother-plate face X=−335"; "M8 blind holes from the valve side, 1.5 mm remaining at the back; do not drill through to the machine-side mother plate". P107 has **no through holes**, so it must be fixed to the host by some means other than its own fasteners.
- The R11 root shoe occupies X −335…−329 over Y −65…−55, which is inside the P107 outline, on the host face.
- In AUTO, the only bodies in the zone X −335…−300 behind P107 are the two shoes (1,560 mm³ each). **The host is not modelled**, so "product delta 0/0/0/0" cannot cover this interface. In MANUAL, the fixture rib that stands in for the host support is exactly what the weld hits.

**Competing hypotheses.**
- H1: the host mother plate backs P107 across its border. In that case the shoe and its welds are a hard clash once installed, and P107 may itself be welded to the host, which turns the R11_HOOD_P_ROOT weld kit into a field-weld or sequence problem.
- H0: the host plate stops below Y ≈ −71, so the band is free.
- Evidence for H1: the wording above, the absence of through holes, and the fixture mimicking a back support.
- Evidence for H0: L1 told L2 to "check the P107/R107 outer edges first", which may mean someone already knew the band was free.
- **I rate H1 at about 50%.** The discriminator is the host interface drawing, or a 10-minute measurement on the machine.

**Options once D1 is known** [R]:
- **P-a (only if H0 holds and the free band is ≥ 25 mm):** keep a welded shoe, done in the shop before P107 is installed, with the fixture rib moved ≥ 15 mm. The weld-length problem remains: the shoe must overlap ≥ 30 mm + 2a, which the M8 blind-hole webs at Y −74 (1.5 mm) make awkward. **Not preferred.**
- **P-b (works under either hypothesis):** a bolted bracket on the P107 **top edge face** (Y = −55, 12 mm wide), using 2 × M5 or M6 blind tapped holes per root at X = −341 (6 mm from both faces). Put the holes between the existing M8 blind holes (Z = 1259, 1322.8, 1386.7 … 1642), keeping clear of ±10 mm around each. For example Z ≈ 1305 and 1340 for one root and 1560 and 1600 for the other, which keeps ≥ 18 mm between hole axes and ≥ 8 mm of wall. The edge zone between the G836 blocks (Z 1297–1604) is free of product bodies in both states [V]. The weakness is that the 12 mm edge again limits the lever for Mz: the bolt tension estimate is about 3–4 kN per root, which is acceptable for A4-80 M6 with 9 mm engagement (thread shear ≈ 34 MPa), but the rotational stiffness must be verified by E5.
- **P-c (best stiffness, needs L1 scope approval):** carry the beams to the upstream receiver P107B as well, with a slotted Y-bearing support so thermal growth is free. Mz is then a couple over about 196 mm: roughly 150 N per end instead of 29.6 N·m on a 10 mm lever.

### 3.3 Weld details as drawn cannot be credited [V/C]
| Joint | L (mm) | a | l_eff = L − 2a | Required, max(30, 6a) | Load-bearing? |
|---|---|---|---|---|---|
| P root back | 26 | 4 | 18 | 30 | no |
| P root ends | 10 | 4 | 2 | 30 | no |
| R foot long | 26 | 3 | 20 | 30 | no |
| R foot short | 9 | 3 | 3 | 30 | no |
| G842 long edge | 148 | 3 | 142 | 30 | yes |
| G830–beam | 206 | 2 | 202 | 30 | yes |

P-root weld group, elastic line-weld screen: A_w = 184 mm² and I_z = 1,797 mm⁴ per root, lever 7.8 mm. Case P-AM-0/180 gives **128.8 MPa** in the throat plane from the local Mz. Every other component of the load is below 2 MPa. The welds are not overloaded, but the detail is code-ineligible and set by geometry: it has a 10 mm lever. Over-throating on thin plate (a = t on R107 and G830) increases the risk of burn-through and distortion on exactly the faces that need to stay flat.

### 3.4 R receiver: stop welding on the seal frame [V/C]
- **Geometry [V].** The R107 feedback-side M8 row is at Y = −74 and X = −191, −136.5, −82, −27.5, 27. The STD01B M8×25 screws have their heads below R107, with Ø16 washers, and F602 metal compression limiters sit in the gasket layer at every bolt. Under R107, between Y −91.5 and −55, the only bodies are those screw heads and washers plus the R11 feet and G842. R113 ends at Y = −91.5 and R112 at Y = −93.
- **Proposal [R].** A doubler "G842-B" (1.4307 plate, 6–8 mm, X −200…36, Y −90…−55, five Ø9 holes on the existing pattern) clamped under the existing screws, lengthened by the doubler thickness to standard M8×30 or M8×35. The beams are welded to the doubler on the bench or bolted to it (M5 into an 8 mm doubler, or through-bolts), and the doubler face is machined after welding. **No welding on R107**, and the hood support becomes a removable, testable sub-assembly. That also closes the gap the brief notes about "replacing the fixed support itself".
- **Screen [C], for the worst project row R-AM-270, |Mx| = 63.27 N·m:**
  - Doubler net-section bending: 55.2 MPa at 6 mm, 31.1 MPa at 8 mm, 19.9 MPa at 10 mm. The project's R107 strip screen was 200.8 MPa.
  - Bolt-load increment as a couple about either doubler edge (16–19 mm lever): 0.67–0.79 kN per bolt. Because F602 makes the joint metal-to-metal, gasket strain is fixed while the joint stays closed. **The acceptance criterion is therefore non-separation:** verified M8 preload ≥ 3× the increment. The pack does not state the M8 tightening specification, so it must be checked.
- **Seal interaction [I].** Every hood load into R107, welded or bolted, ends at this M8 clamp row; there is no other path. The clamped doubler does not add a path. It replaces weld heat and distortion behind the gasket land with a stiff, removable part. RT-08 (indirect seal effect) is still owed a measurement (E5), not a model.

### 3.5 G837 −9 mm² is closed by geometry [V/C]
The window corner (X −368…−365, Z 1294…1297 for G837_001, and equivalent at all eight pads) removes 9.0 mm² of 601.24 mm², which is 1.50%. The M5 hood screw axis is at (−349, 1278). The lost area lies 22.6–26.9 mm from that axis. A VDI-2230-style clamp cone for the M5 head (d_w 8.5, clamped length about 7 mm) has an outer radius of about 8.3 mm, so the lost corner is about 2.7× outside the clamped zone. Pad bearing and joint stiffness are unchanged to first order. **Recommendation:** close RT-06 with this record and no geometry change. Window corner fills are not viable anyway, because A709 is a sharp 140×140 square with a 4 mm gap and a fill would eat the A709 corner clearance.

### 3.6 Frame and beam manufacturability [S/C]
- G830 is a 2 mm frame with 148 windows, 26 mm side strips and a 17 mm web (P). It is welded to the beams with a2 fillets on two edges and must be flat within 0.15 after welding. That is not achievable reliably: ISO 13920 class E gives 1.0 mm. Screw G830 to machined beam faces, for example 4 × M4 per beam into the 10 mm beam depth, or thicken to ≥ 4 mm and machine after welding.
- The beams are milled from a 206×21.5×26 envelope with four relief pockets each. Pocket inside corners must be ≤ R1.5 (0.79 mm of the 1 mm clearance remains at R1.5; 0.17 mm at R3). Alternatively, enlarge each relief by 2 mm. A formed angle is cheaper and 6.5× stiffer about the axis that carries the largest moment.
- G837 pocket "R ≤ 0.1": R ≤ 0.51 still clears the G836 block, which has 12.00 −0.02/−0.05 and a 0.2 chamfer in a 12.10 +0.05/0 pocket. A 0.3 chamfer allows R ≤ 0.68, which a Ø1.2 cutter can machine at 1 mm depth.

---

## 4. B: feedback equaliser

### 4.1 What actually drives the encoder-zero result [V/C]
`b_equaliser_sensitivity.py` re-implements `r11_controls.py`. The constitutive laws, histories, solver and retry seeds are unchanged; only the parameters are exposed. It reproduces the project's figures: pure HEAT 0.015839056°, post-proof COOL 0.040443837°, residual −0.031071726°, proof peak 0.193281956°. Varying one parameter at a time on MAX_UNEQUAL with seat μ = 0.12:

| Parameter | Value | Thermal/cool (°) | Residual (°) |
|---|---|---|---|
| Baseline (arm 0.030, kt 1e5, SR20, R4) | – | 0.0404 | −0.0311 |
| Rolling arm | 0.005 mm | 0.0165 | −0.0071 |
| kt | 3e5 | 0.0129 | −0.0099 |
| kt | 1e6 | 0.0038 | −0.0029 |
| Crown radius | 2 mm | 0.0334 | −0.0289 |
| Crown radius | 8 mm | 0.0561 | −0.0360 |
| Sphere radius | 30 mm | 0.0404 | −0.0311 |
| Sphere radius | 9 mm (DIN 6319) | 0.0428 | −0.0335 |
| Seat μ | 0.05 | 0.0431 | −0.0338 |

Worst of MAX_UNEQUAL and MIRROR, seat μ = 0.12, over the two **measurable** parameters (thermal/cool and |residual|, in degrees):

| Rolling arm \ kt (N·mm/rad) | 1e5 | 3e5 | 1e6 |
|---|---|---|---|
| 0.030 mm | 0.0404 / 0.0311 | 0.0129 / 0.0099 | 0.0038 / 0.0029 |
| 0.015 mm | 0.0261 / 0.0167 | 0.0083 / 0.0053 | 0.0025 / 0.0016 |
| 0.005 mm | 0.0165 / 0.0071 | 0.0053 / 0.0023 | 0.0016 / 0.0007 |

**Interpretation [I].** The encoder half sees the crown couple C through a Coulomb grip of stiffness kt, so β ≈ C/kt. The model's proof-torque peak is exactly T/kt (0.30 N·m / 1e5 → 0.17°). That gives a free calibration: **the ±0.30 N·m proof step already in the test history measures kt directly.** The value 1×10⁵ is the bottom of the project's sensitivity range; L1's R10 recalculation used 1×10⁶.

I tested one hypothesis that turned out wrong. I expected that replacing the SR20 seat with a smaller standard spherical washer would reduce the friction couple and therefore the drift. It does the opposite: the seat friction helps lock the bridge against the encoder half. DIN 6319 is therefore justified on lead time only, at a +0.0024° model cost.

### 4.2 B parts: manufacturing route and changes [C/R]
- **B850 bridge (440C, HRC 58–60).** The outline, including the R4 crown, is 2.5D along Z, so **wire-EDM it from pre-hardened plate**. Cut the crown and the Ø3 pin bore in one setup: that gives micron-level coaxiality and no heat-treat distortion. Use at least three skim passes, then polish or lap the crown to remove the recast layer, because the crown is the 936–974 MPa contact. Sink-EDM or jig-grind the SR20 dimples. Control the annulus axial position (±0.02) and flatness, and treat SR as ±0.05.
- **B852 pin.** Do not press into the crown (DFM-07). Use either (i) Ø3 H7/h6 with a head on one end and a DIN 6799 retaining washer on the other, or (ii) an ISO 8752 Ø3 spring pin in a standard Ø3 H12 bore. Both need only the axial capture the design asks for, since the ears have 0.5 mm radial free play.
- **B851 seat (440C, Ø12/Ø6.4).** Keep it. If lead time dominates, a DIN 6319-C 6.4 (Ø12, SR9) with a matching concave or conical seat is a catalogue alternative at a small model penalty. Hardened catalogue parts in C45 or stainless are available.
- **A704R8 jaw (17-4PH H900).** Machine in Condition A and age to H900, which shrinks by about 0.05%. **Finish-grind the fulcrum flat after ageing** (flatness 0.01, Ra 0.4). The crown-on-flat p0 of 974 MPa is about half the estimated first-yield p0 for H900 (about 1,950 MPa, Tresca line contact). The open risks are fretting and the rolling-hysteresis arm, not static yield, which is why the rolling arm is measured in E3.
- **HW_R11_GUIDE_M5 (A4-80, 57 mm under head, Ø5h9 × 8.5 guide).** This is a turned special. Check whether an ISO 4762 M5×55 or M5×60 partially threaded screw works with the stack, given the shank tolerance and the guide-overlap margin of 0.5375 mm. If it does not, order the special now, since it is on the critical path.
- **Hard-washer support of 84.6%.** The simple-strip bending is 7.46 MPa against 17-4PH H900 yield above 1,000 MPa, and the average pressure is 12.3 MPa. Close it by calculation; this is not a manufacturing issue.

---

## 5. Whole-machine gates and procurement

### 5.1 G1 main support and seal preload: DFM view [S/C/R]
- **G1.** Plain-bushing clearance alone uses 2.13 mrad against a 1 mrad screen, before load or temperature; the R7 formula is 4c/95 with c = 0.0505. A plain-bushing architecture cannot pass. R7's rolling-bearing candidates were not qualified for installed clearance, ring ΔT, fit loss or axial float. Those are **measurable on a single bench cassette** in less time than one more modelling round. Recommended concept:
  - a preloaded angular-contact or tapered pair, so there is no radial clearance to budget;
  - centres line-bored in one setup in a solid plate pair, which D546 already specifies as 165.000 ± 0.015 and coaxial within 0.010/125;
  - the gear straddled between the bearings rather than overhung.
- **Seal preload (1000 N minimum, 1800 N maximum).** The R5/R7 records show that the window is consumed by thermal drift and measurement uncertainty: 4,250 N/mm stack stiffness means a 0.01 mm gauge resolves 42.5 N. Install with **force-measured preload** (a load cell or calibrated washer during assembly), not by height.

### 5.2 Purchased items: actions now (no purchase authority assumed) [S/R]
| Item | Risk | Action |
|---|---|---|
| KHK SSG3-55F30B | The 2025 price list shows "None" for this exact suffix | Written confirmation of the active code, bore/hub tolerance, inspection certificate and lead time. Do not substitute F30A or F45A without an equivalence review. |
| Valpes VSX150.90B.G00 / VRX75.70B.G00 | Placeholder outline only | Request the selected-model CAD, torque/time curves, stop behaviour and fault (stall) torque. These freeze the A701/A702 interface. |
| Baumer EAL580 11197423 + 11053277 coupling | Revision-specific mechanical limits | Request the coupling misalignment, stiffness and torque limits for the exact revision. Supply 2 sets for E3. |
| SCHNORR 001500A (60) and 002700A (144) | Catalogue point force only | Request batch-tagged load and unload force-height curves, hysteresis and relaxation. Order test lots for E2. |
| mayr 490.715 110/160 N·m, HBK T210, R+W BK2, SKF 6005-2RSH, igus XSM | Standard catalogue items | Confirm lead times. Request exact certificates. |
| Rogers HT-870, skived PTFE 0.25 | Material qualification | Request lot certificates and compression-set data. |

---

## 6. Drawing and configuration readiness for RFQ [V/R]
The R11 booklets are design-review documents. A fabricator cannot quote or inspect from them without guessing. The minimum changes:
1. **One general-tolerance standard:** ISO 2768-mK for machined parts and ISO 13920-BF for weldments. Tighten only the features named as critical-to-quality (CTQ). The current R11 default of ±0.05 on every unmarked machined size roughly doubles cost on the 63 milled PNs.
2. **Weld symbols per ISO 2553** on every joint, a WPS reference (304L GTAW/ER308L, qualified per ISO 15614-1), the weld sequence and a distortion allowance. No a/t > 0.7 on thin plate.
3. **Datum reference frames (ISO 5459) and a CTQ list** per part with the inspection method. The STEP-plus-coordinate-table definition is acceptable for CNC and laser work, but each CTQ still needs a toleranced callout.
4. Fix the impossible or ambiguous callouts in DFM-11: the 0.01 mm shim (minimum 0.025, or specify a group-thickness tolerance only), G837 R ≤ 0.1, the G840 relief corners, and custom washers where ISO 7089 exists.
5. **Renumber** the R11 G840 beams and make the A704/A704R8 distinction explicit. Resolve which weldment owns P107.
6. The 61 PNs with ≤ 0.03-class tolerance tokens (see `results/results_bom_routing.json`) should each carry an explicit process note, e.g. grinding, lapping, EDM, or select-fit.

Process-route summary of the R11 database [V], from `bom_routing.py`:

| Route | PNs | Instances | PNs with tight tolerance |
|---|---|---|---|
| Purchased | 72 | 1,743 | 5 |
| Milled / prismatic | 63 | 218 | 18 |
| Sheet (laser, some bending and welding) | 48 | 92 | 2 |
| Turned | 31 | 359 | 21 |
| Seal / gasket / insulation | 18 | 56 | 3 |
| Precision shim | 12 | kit | 12 |
| Weldment | 12 | 5 | – |

---

## 7. Plan to accelerate manufacture

### 7.1 Change the loop, not just the design
Through R11, the record contains **no physical measurement**: no fabricated sample, supplier inspection, rig, or leak test. Every open A/B hold reduces to a handful of interface properties that the model has to assume: kt, the rolling arm, spring-stack curves, weld distortion on 3 mm plate, receiver rotational stiffness, and bearing tilt. The next round should **build to measure**, not iterate the model.

### 7.2 Experiments and gates
| # | Experiment (engineering test article, not product) | Measures | Acceptance (proposed; L1 to confirm) | Unblocks |
|---|---|---|---|---|
| E1 | Host interface: drawing or a site measurement of the region behind P107 | Free band behind P107, Y −100…−55 | Decision between P-a and P-b | DFM-02, D1 |
| E2 | Spring stack: 10 stacks of 001500A 5S×2P, plus 002700A for the seal | Load/unload F–h at 20 °C and at the hot limit; 24 h hold; 3 pre-cycles | Cold window 350–450 N achievable with U(k=2) ≤ 5 N; relaxation recorded | RT-12, RT-03 inputs |
| E3 | B rig: one bridge, jaw and A703 on a Ø30 304L dummy shaft; autocollimator or 0.001° encoder on the encoder half; heater for +80 K on the clamp | (i) kt from the ±0.30 N·m step; (ii) bridge moment–angle loop, giving the rolling arm; (iii) the full COLD→HEAT→±0.03/±0.30→COOL history, 10 cycles | kt ≥ 3×10⁵ N·mm/rad, arm ≤ 0.015 mm, measured β within the D3 allocation (e.g. ≤ 0.02° thermal, ≤ 0.015° residual) | RT-09/10/11 |
| E4 | Weld coupon on 3 mm 304L (only if any weld on R107 survives D2) | Flatness of the gasket land and heat tint | Within the R101 seal-face flatness (0.15/300) | DFM-04 |
| E5 | Hood receiver on the trial fixture (F620 moved), R clamped doubler, P root per D1 | 250 N × 8 directions plus weight; dial indicators at the A709/A710 clearance points and at R107/P107 near the M8 row | Loaded minimum clearance ≥ 1.0 mm; return within 0.02 mm; no joint separation; gasket-land movement within limits | RT-04/05/06/07/08 |
| E6 | G1 bearing-cassette bench: two shafts at 165 mm, the actual KHK pair and preloaded bearings | Shaft tilt and centre change at 78/38 N·m and at 200 N·m jam; ΔT of 40/80 K | ≤ 1 mrad and ≤ 0.10 mm centre change at working load; retained and undamaged at 200 N·m | RT-01/02, whole machine |

### 7.3 Indicative schedule (planning estimate)
Assumptions: decisions D1–D4 within about 1 week; an in-house or partner shop with laser, CNC, wire-EDM and GTAW; supplier responses within 1–2 weeks. The KHK and Valpes availability is the main schedule risk.

| Week | Work |
|---|---|
| 0–1 | D1–D4. RFQs and confirmation requests out. Drawing standard (§6) issued. F620 fixture ECO. |
| 1–3 | A ECO (clamped R doubler; P root per D1; screwed G830; formed beams). B ECO (pin, seat tolerances, EDM route, jaw grind). Renumbering. |
| 2–5 | Fabricate EVT parts: 2 B rigs, 1 A receiver on the trial fixture, 1 G1 cassette. SCHNORR test lots. |
| 4–7 | Run E2, E3 and E5. Run E6 in parallel. Update only the parameters that were measured, and rerun the existing models once. |
| 8 | Gate review. A/B drawings for release if E3 and E5 pass. Whole-machine release depends on E6 and the seal-preload plan. |

**Fallbacks:**
- If E3 gives kt < 3×10⁵ N·mm/rad, increase the A703 grip preload or length (keyways and cross holes in the shaft remain forbidden), or reallocate the angle budget at D3.
- If E1 confirms H1 and P-b proves too compliant in E5, escalate P-c for scope approval.
- If E6 fails at 200 N·m, revisit the torque-limiter setting with mayr data before changing the structure.

---

## 8. Confidence, and what would change these conclusions
| Conclusion | Confidence | What would change it |
|---|---|---|
| The P weld clash is a fixture interference, and a 6–15 mm rib shift clears it | High (direct Boolean) | A requirement that the bench rib position replicate a host feature exactly |
| The P root may clash with the host | ~50% (H1) | The host interface drawing |
| The root welds are not code-creditable | High for EN 1993-1-8. The project may use another code with a different minimum length, but the 2–3 mm end-weld lengths fail under any common rule. | A different governing code, plus a qualification test |
| The clamped R doubler takes the screen to ≤ 55 MPa | Medium (beam/strip screen, not FE) | An FE or E5 measurement showing local prying or R107 bending at the bolt line above the screen |
| G837 −9 mm² is immaterial | High | Evidence that the pad load path is bearing far from the screw axis, e.g. hood prying in a cold maintenance case |
| B drift is governed by kt and the rolling arm; seat geometry is secondary | High *within the project model*. Moderate for the physical device, because the model omits self-weight, host loads and stack rotational stiffness. | E3 data; a measured stack rotational stiffness that is much lower than the screw-beam proxy |
| The B852 press fit is a fracture and profile risk | High for the stress level. Moderate for actual cracking, which depends on the bore finish and the 440C condition. | A press-fit trial on 10 EDM-cut 440C coupons with dye-penetrant inspection |
| G1 cannot pass with plain bushings | High (the project's own arithmetic) | Evidence that the 4c/95 formula double-counts clearance |

---

## Appendix A: files
- `tools/` contains the scripts listed in §1 and `run_all.sh`. Requirements: Python 3.13, cadquery-ocp 8.0.1.1, numpy and scipy. The scripts read the pack as data; no project script is executed.
- `results/` contains all computed outputs. `results_bom_routing.csv` gives a per-PN route, instance count, status and tight-tolerance tokens.
- `RT_FINDINGS.csv` contains a response to each RT-01…RT-18 question in the pack's finding-form format, plus the DFM-xx items.

## Appendix B: external references used
- EN 1993-1-8:2005 §4.5.2, fillet-weld minimum effective length max(30 mm, 6a), with l_eff = L − 2a, as applied in [Steel Buildings in Europe, worked example](https://infosteel.be/images/Steel-Buildings-in-Europe/SSB05/96).
- ISO 13920 Table 3, class E straightness/flatness: 0.5 / 1 / 1.5 mm for the >30–120 / >120–400 / >400–1000 mm bands. From the [ISO/FDIS 13920 sample](https://cdn.standards.iteh.ai/samples/86032/be6f737b161c483d90b20817060a93db/ISO-FDIS-13920.pdf) and the [ISO 13920:1996 sample](https://cdn.standards.iteh.ai/samples/23313/68ef2052e2324d40b14d2d7c639a8dd7/ISO-13920-1996.pdf).
- DIN 6319-C for d1 = 6.4: outside diameter 12, h 2.3, r1 = 9 (catalogue values: [Ameco](https://eshop.ameco.cz/products/en/3/2619/g1630/65540600), [Misumi](https://uk.misumi-ec.com/vona2/detail/221304378123)). Verify against the standard text before design use.
- The supplier facts (KHK, Valpes, Baumer, SCHNORR, SKF) are taken from the pack's `02_SUPPLIER_BOUNDARIES.csv` and were not re-verified here.
- Material values used in the screens (17-4PH H900 σy ≈ 1,170 MPa; E = 193–200 GPa) are typical handbook minima. Replace them with the certificate values for the material lot actually used.
