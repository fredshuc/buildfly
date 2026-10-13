# AT-DMP02 C02 R21: RT-2 independent review, focused on manufacturability

Package: `AT_DMP_R21_RT2_COMPLETE_PART_1_OF_2.zip` (SHA-256 `a1a20084…c7b213d`) and `…PART_2_OF_2.zip` (`a3381aff…d5b36`). Both are stored in `dampers/c02-r21/`. The combined 815-entry `MANIFEST_SHA256.json` verifies with 0 mismatches.

Scope: read-only computation on the delivered native BReps, placements and tables. No supplier was contacted, nothing was purchased and nothing physical was done. L1 owns every acceptance. Labels used below: **[V]** computed here and reproducible from `tools/`; **[S]** taken from the package; **[I]** engineering inference; **[R]** recommendation.

## 0. Conclusion

1. **R21 is a sound manufacturing baseline. Proceed with the scoped releases now.**
   - The RT-1 changes L1 adopted are present in the geometry [V]:
     - G901 at Y −803..−800.
     - TF909 at −823..−803.
     - G900 and G903_R18 end at −803 and −800.
     - D886 is re-indexed.
     - The wet bay TF920–927 reaches the Z 744 floor.
     - P is in O1′ with P107B as the lower receiver.
   - Across 41 rotor positions (0–90°) in P and R, the cold-test configurations show:
     - zero motion interference;
     - zero cross-branch overlap;
     - all 213 static overlaps are modelled thread engagements.
   - The net BOM closes row by row (need = issued + unissued on all 220 rows), with no over-credit and no double allocation.
2. **Procurement, not machining, is the critical path.**
   - MAKE: 654 of 732 pieces are already issued (89%).
   - BUY: 32 of 1,530 pieces are issued (2%).
   - Of the 1,301 fastener and small-hardware pieces, 1,141 (88%) map to a named ISO/DIN designation today. Their enquiries can be drafted without further engineering.
   - The other 160 pieces (9 rows) need one L1 decision each (§3, RT2-01).
3. **Four MUST-FIX items have a smallest change I can support with computation:**
   - **RT2-03:** the dry cradle band at Y −818..−808 sits on the BK2 30h7/Ra 0.8 grip zone. This contradicts stage A1 ("no grip on … BK2") and the B202 note "protect polished journals". Each of the two glands per rotor must also cross a band, which is the handoff L1 is worried about.
     - Smallest change: support the finished rotor between centres. This needs two small centres re-cut in the final end faces.
     - Each gland is pre-staged on a Ø29.9 tailstock-quill nose, so no support ever opens while a gland crosses.
     - The same stand is the 0.03 mm runout inspection fixture.
   - **RT2-06:** the governing defect is the Ø5 end hole tangent to the film end (zero ligament), not the frame shadow. The brief's 224.79/435 mm² uses the full 87 mm nominal width as denominator; of the film material actually present in the end strip, 97.2% is already frame-backed.
     - Smallest change: a 46.774 × 7 × 0.8 mm 304 keeper under the existing end screw.
     - It touches only the end STD08B screws and clears every moving body by ≥12.58 mm.
     - It needs the 16 end screws lengthened by ≥2 mm. Otherwise thread protrusion falls to 0.95 mm (1.9 pitches), below the F06 rule of ≥2 pitches.
     - A 2 mm or 4 mm longer screw has no new clash.
   - **RT2-04:** D886 sits on the P2 gear spindle about 45–50 mm outboard of the bearing. The stop reaction therefore loads the KHK gear pair (G1) through spindle tilt.
     - With the package's own R14 surrogate at the soft support bound (25,000/20,000 N/mm), G1 peak line load reaches about 1.0× the catalogue-implied value at the 78 N·m normal closing torque. It reaches 1.08–1.24× at the 120 N·m limiter release.
     - At the stiff bound (100,000 N/mm) it is 0.61–0.78×.
     - So the evidence that permits finite input is three measurements:
       - the in-situ support stiffness, or a loaded contact pattern;
       - calibration of both limiters;
       - the blade-edge closing error of each leaf against its measured seal reserve.
     - Spring assumptions do not substitute for these.
     - A crowned D886 contact at r ≈ 75 mm collapses the 2.6× spread in stop-induced edge error (0.072–0.184 mm at 78 N·m) to about 0.08 mm. D886 is new and unreleased, so this is cheap.
   - **RT2-07:** the feedback root (A703/A704R8/B850–B853/guide screws) forms a geometrically closed contact chain in P and R. The overlaps are threads only. What is missing is a product quantity allocation (B01/E01 specimens cannot count) plus two calculations its own notes require. No geometry is missing.
4. **CONDITIONAL items can be approved with named measurements:**
   - **RT2-01:** approve scoped manufacture.
   - **RT2-02:** proceed to coupons once the bevel-root rule is restated as root face controlled and preparation = t − root.
   - **RT2-05:** approve machining and unloaded mating. Measure pointwise, because the minimum-metal margin is only 0.01 mm.
   - **RT2-08:** qualifiable. I give the arithmetic that turns the trip rule into a loading-rate limit and a mechanical stroke limit.

Confidence:
- High: geometry, motion and BOM verification; the band-on-grip conflict; the film-keeper fit and the thread-protrusion shortfall.
- Medium: the G1 load screen. It inherits the package's linear surrogate, and the catalogue rating basis is unconfirmed.
- Medium-low: the maintenance hand-off sequence (RT2-09). It is a proposal and needs L1 acceptance.

The evidence that would change these conclusions:
- measured support stiffness and seal compression reserve (RT2-04);
- an actual fixture vendor drawing (RT2-03);
- supplier answers on HW_N3/HW_N10/STD08B (RT2-01).

## 1. Corrections from the L1 RT-1 disposition, carried forward

L1's disposition of my RT-1 review (`history/RT1_L1_DISPOSITION/*`) is correct on the following points, and this review applies them:
- **P107 position.** My RT-1 claim that P107 sat on the bottom, 9 mm from R, was wrong for the exact R16 transform. P107B is the P lower receiver at Z 1488/1491, and P107 is 104 mm above the axis. I re-verified both in R20.
- **The "10 mm en-route" D886–TF900 clearance was not a continuous lower bound.** The full-travel minimum near the ends is 0.087 mm at 0.1° and 0.096 mm at 89.9°, with 0 at the end stops. Over 12.5–77.5° the gap is a constant 10.0 mm, set by a rotation-invariant feature pair [V].
- **Status of W1 and the routing table.** W1 (41 PN / 315 pieces) was a work queue, not a release. A regex/kind routing table is not an RFQ list. In this review the fastener map is a draft designation list for L1 to confirm, not a purchase specification.
- **Partial G901 move.** Moving G901 alone left the old G900 overlapping by 2,025 mm³ per side. R17/R18 resolved this by changing G900 [V: G900 ends at −803, no overlap].
- **Maintenance and wet-side loads.** A drafted maintenance order is not a proven acyclic sequence. A 500 N wet-side disturbance is a force, not a lock torque. RT2-09 below is built as a load-carrying hand-off chain for that reason.
- **Code choice.** These earlier corrections still apply: the governing code must be chosen explicitly; the relevant Eurocode clause is EN 1993-1-8 §4.5.1; ISO 2768-2 is withdrawn (now ISO 22081).

## 2. What was checked, and how

| Check | Tool | Result |
|---|---|---|
| Manifest | `run_r21.sh` | 815 entries, 0 mismatches [V] |
| Static overlap at 0°, all pairs except wet/wet R12–R12 (inherited, not re-checked) | `r21_check.py` | P: 1,506 instances, 633 bbox-overlapping pairs tested, 112 overlaps. R: 1,073 instances, 574 pairs, 101 overlaps. All 213 are modelled thread engagements or set screws (list below) [V] |
| Motion at 0, 0.1, 1, 2.5…87.5 (2.5° step), 89, 89.9, 90° (41 positions), with every moving body against every body of another group | `r21_check.py` | 0 overlaps in P and in R. D886–TF900 minimum gap: 0.0873 / 0.871 / 4.32 mm at 0.1° / 1° / 5°; 10.0 mm over 12.5–77.5°; 0.096 mm at 89.9° [V] |
| BOM / index / gap consistency | `r21_bom_audit.py` | 0 rows with need ≠ issued + unissued; 0 over-issue; 0 duplicate PN; 94 station-only pieces excluded from product need [V] |
| Fastener designation map | `r21_fastener_map.py` | 1,141 of 1,301 pieces map to a standard; 160 pieces in 9 rows need a decision [V] |
| Film end backing, keeper fit, screw clearance and protrusion | `r21_film_*.py` | §3 RT2-06 [V] |
| Feedback-root contact graph | `r21_root_contacts.py` | §3 RT2-07 [V] |
| Drive-line order along the axis | `r21_yorder.py` | §3 RT2-04 [V] |
| Stop and gear budget from the package's own R18/R14 screens | `r21_stop_gear_budget.py` | §3 RT2-04 [V on the stated inputs] |

Static overlaps by pair type are the same in P and R apart from multiplicity. All of them are external threads represented at major diameter inside tapped holes or nuts, or set screws:
- H14_M5X10/TF909
- D874 and D875 with HW_R13_M5X20 and HW_R13_M10X45
- BUY520 and BUY521 with H14_M6X20
- H14_M16X110 and H14_M16X90 with H14_N16
- H17_M10X45 with TF920P/R
- D870/D873 (M30×1.5 lock nut on spindle)
- D870/H14_M8X25 (axial screw)
- D873/HW_R13_M4TIP (set screw)
- D873/D892
- BUY530/H14_M4X12
- H14_M8X30/TF909
- HW_R13_M12X80 and H14_M12X110 with HW_R13_N12
- D889 and D890 with H14_M10X45
- D895/H14_M8X40
- H14_M4X12/H14_N4
- H17_M8X35/TF925

## 3. Answers to RT2-01 … RT2-10

### RT2-01: Manufacturing master (CONDITIONAL). Recommendation: approve scoped manufacture as issued.

**No double stock or specimen credit found [V].**
- Net need is 2,265 identities = 689 issued + 1,576 unissued. This holds on every one of the 220 BOM rows.
- 94 independent-station pieces (B01/SP04) are excluded from product need, not credited to it.
- No PN is allocated twice in the 172-entry index.

**All index↔BOM name differences are explained [V].**
- Eleven issued BOM PNs (J402, P105A/B, P106, P108, R105A, R106, R108, S302, S312, B200_R13) correspond to index supply PNs: the `*_FREE_R15/R18` free-state seals, and B201/B202_R18RAW for the rotor.
- The index-only PNs are station or tool items: B860–B862, TF881L/R, TF882–884, TF910L/R, TF912, TF930–932 and D542.

**What is missing, exactly** (the 1,576 unissued pieces = the 88 gap rows):

| Class | Rows | Pieces | PNs |
|---|---|---|---|
| Procurement contract | 67 | 1,498 | BUY*, H14_*, H17_*, HW_*, STD01B/C/P, STD02B, STD06B, STD07B, STD08B, STD14B |
| Product scope and capture | 12 | 60 | A703P, A703R, A704R8, A705, A706, A707, A710, B850–B853, HW_R11_GUIDE_M5 |
| Missing product interface | 6 | 6 | G840P1, G840P2, G843, P107, P107B, R107 |
| Known geometry/retention | 2 | 8 | P109, R109 |
| Custom fastener definition | 1 | 4 | STD01PC |

**Acceleration [R].**
1. Release the 1,141 standard-mappable fastener pieces as a single enquiry draft, using the designations in `results/results_r21_fastener_map.csv`. The rule L1 set still applies: confirm thread length b against the required engagement wherever the CAD shows "full thread".
2. Put these nine one-line decisions to L1. Each blocks only its own row:

| Row | Decision needed |
|---|---|
| HW_N10 ×2 rows (20 pcs) | M10, m 10, s 17 matches old DIN 980, not ISO 7042 (s 16). Choose ISO 7042-M10 and check the s 16 spanner, or name DIN 980V. |
| HW_N3 (57 pcs) | M3, m 4, s 5.5 matches a polyamide-insert nut (ISO 10511 / DIN 985), but the BOM says all-metal. Choose one and record its temperature limit. |
| STD08B (48 pcs) | Head 4.8 × 1.5 matches neither ISO 4762 M3 (5.5 × 3) nor ISO 7380-1 M3 (5.7 × 1.65). Treat it as a drawn special. See RT2-06 for the length change. |
| H14_PIN5 | Headed pin. Name the standard or issue a drawing. |
| HW_R13_M4TIP | Brass-tip set screw. Name the product. |
| HW_R8_HOOD_W5, HW_R9_HARD_W5, HW_W4_1_9 | Non-ISO 7089 washers (10/5.5 × 1, 9/4.5 × 1). These are intentional specials and need drawings. |

3. Add the `supply_PN` mapping (for example J402 ↔ J402_FREE_R15) as a column of the factory entry index. Receiving inspection then does not have to infer which free-state part is the installed one.

### RT2-02: Shells, rotors, WS17 (CONDITIONAL). Recommendation: proceed to coupons, with one rule restated and coupons grouped by joint family.

**Bevel-root rule [S + I].**
- The rule (`R19_L1_F06…json`, `bevel_root`) sets preparation 2.50 ± 0.05 and root 0.50 ± 0.05, and also requires preparation + root = measured t.
- The two tolerances only sum to 2.90–3.10 mm, so any plate outside that band is stopped by arithmetic, not by function.
- Inside the band the requirement is redundant: the factory cannot hold two independent ±0.05 features and also their sum.

The function of the joint is root fusion, which the root face and opening control, and retained wall ≥2.90 mm. [R] Restate the rule:
- measure t;
- control root face 0.50 ± 0.05 and opening 1.00 ± 0.05;
- record preparation = t − root as a result, not a target;
- a plate with t < 2.90 fails the existing `full3mm` rule anyway.

**Coupons by family, not by route [R].**
- WS17's 50 weld routes and the four shell welds fall into a few joint families with different acceptance. At least three:
  - the shell full-penetration 3 mm bevel butt, with full fusion and retained wall ≥2.90;
  - the WS17 sleeve-ring joint, with throat ≥1.30 after flush finishing and rail wall ≥2.80;
  - the WS17 structural fillets (a4 on TF926 sides, a5 leg-to-rail).
- One macro-sectioned coupon set per family, per process and position, cut from the actual issued heat or lot at its measured thickness, covers all routes of that family. Under ISO 15614-1 a 3 mm butt coupon qualifies 0.7t–1.3t (check against the edition L1 adopts).
- This replaces route-by-route trials with about three coupon programmes. The first-piece measurement plan stays as it is.

**Code-dependent point [I].**
- If EN 1993-1-8 is chosen, §4.5.1 requires a fillet length of at least max(30 mm, 6a) to count.
- The TF926 a4 × 20 mm side welds (6a = 24, so 30 mm governs) would therefore carry no design credit.
- Either lengthen them to ≥30 mm or do not rely on them. Under ISO 15614-1 alone this is a design question, not a coupon question.

### RT2-03: First rotor support and transfer (MUST-FIX). Counterexample, and a smallest change that removes the hand-off.

**Counterexample [V, S].** The three fixture rows (`R21_EXTERNAL_FIXTURE_PURCHASE_SPEC.csv`, ROT-P1/P2/R) place 10 mm Ø30 bands at world Y −813 and −35.
- On B200 (dry end at Y −851.5, local Z = −851.5 − Y) the dry band spans local Z 33.5–43.5.
- That overlaps the final grip zone Z 0–43 (30h7, Ra 0.8, the BK2 hub seat) over 9.5 mm. It conflicts with stage A1 ("no grip on blade, BK2, seal track") and with the B202 note "Protect polished journals from clamp teeth".
- The far band (local Z 811.5–821.5) lies on the A703/A704R8 clamp seat.
- J401_005 (local Z 85–125) and J401_006 (Z 762–802) sit between the bands. Each gland must therefore cross one band to reach its journal. Over 3 rotors that is 6 crossings, each requiring a qualified second capture under the current concept.

**Smallest change (preferred) [R].** Support the finished rotor between centres.
1. Re-cut a small DIN 332-1 centre in each finished end face. B202 currently removes the sacrificial centred pads, so the finished shaft has none.
   - Size: form A or R, about 2.5–3.15 mm, chosen by the stand vendor.
   - L1 must confirm that the far-end face carries no function that a centre would spoil.
2. Use a bench-centres stand with a locking tailstock. Two 60° centres give positive axial capture in both directions, which is not friction capture. Size each centre for ≥600 N transverse and ≥300 N axial, as the row requires.
3. Give each tailstock quill a Ø29.90 (−0.01) nose about 60 mm long, ending in the 60° point.
   - The quill is held rigidly by the stand, as a cantilever, not as a second pivot.
   - Thread the gland onto the nose before the quill is advanced into the shaft centre.
   - The gland then slides from the nose onto its journal while both centres stay engaged.
   - No support is opened, so the alternate-catch trial disappears.
   - Nose check under 600 N at 60 mm: δ ≈ 0.006 mm and bending stress ≈ 14 MPa [I].
   - The step from Ø29.90 to the 30h7 grip and the Ø6 cross-bore are the same lip-protection issue as today; use a thin assembly sleeve if J401 carries a lip.
4. The same stand serves as the runout-0.03-to-A inspection fixture B202 already requires. One purchase covers A1, A2 and inspection.

**Fallback if centres are refused.**
- Move the dry band to local Z ≈ 50–60 (world Y −801.5..−791.5). This is 30h8 exposed shaft, clear of the h7 grip and the Ø6 cross-pin bore at Z 79.
- Keep the current gland hand-off procedure.

**Acceptance.**
- Vendor drawing showing centre load ratings against the row's ≥600 N / ≥300 N.
- One dimensional-surrogate trial threading both glands with both centres engaged.
- Measured runout of the finished rotor on the stand.

### RT2-04: Minimum stop and support evidence before finite input (MUST-FIX)

**Torque path, from native R20 P [V] (`results_r21_driveline_order_P.txt`):** input D896 → D892 → BUY531 → BUY530 (torque transducer) → BUY531 → D530 → BUY521 (second limiter, 160 N·m) → BUY520 (primary limiter, 110 N·m) → D885 → P1 D870 → BUY504 mesh → P2 D870 → **D886 at Y −1147.5..−1098.5**. D886 is outboard of the P2 bearing at Y −1081.5..−1065.5 and reacts on TF900.

Consequences:
- The P2 leaf sees the stop through its BK2 coupling only.
- The P1 leaf also sees the gear mesh.
- The stop force loads the P2 spindle bearings as an overhung radial load, which tilts the gear axes.

**Numbers.** All are scaled linearly from the package's own R18 stop screen and R14 two-plane surrogate; no new spring is assumed. The stop normal is world X, which is the line of centres, so the stop force lies in the separating plane, as in case `P_stop90` [V, I].

| Case | P2 blade-edge error from stop, r = 80 / 65 / 50 mm | Additional P1 error from mesh shift, k soft / stiff | G1 peak line load ÷ catalogue-implied, k soft / stiff |
|---|---|---|---|
| 78 N·m normal closing | 0.072 / 0.109 / 0.184 mm | 0.108 / 0.046 mm | 0.87–1.00 / 0.61–0.63 |
| 120 N·m, BUY520 static release maximum | 0.111 / 0.168 / 0.283 mm | 0.166 / 0.071 mm | 1.08–1.24 / 0.76–0.78 |
| 150 N·m, BUY520 dynamic peak limit | 0.138 / 0.209 / 0.354 mm | 0.208 / 0.089 mm | 1.21–1.39 / 0.85–0.87 |
| 195 N·m, BUY521 dynamic peak (primary failed) | 0.180 / 0.272 / 0.460 mm | 0.270 / 0.116 mm | 1.38–1.58 / 0.97–0.99 |

How the table was built:
- k soft = bearing 25,000 / plate 20,000 N/mm; k stiff = 100,000 / 100,000 N/mm.
- The line-load range spans the two sign combinations of the plane-of-action misalignment (f_ma = 30 mm × (δ_dev·cos 20° ± δ_inc·sin 20°)).
- c_γ = 20 N/(mm·µm), face width 30 mm, r_p = 82.5 mm.
- The catalogue-implied line load is 423 N·m ÷ 82.5 mm ÷ 30 mm = 171 N/mm (BUY504 note; KHK's rating basis is unconfirmed).

Reading [I]:
- Torque into the stop is bounded by the limiters, so 200 N·m is a conservative screen. The relevant values are 120/150 N·m with the primary limiter working and 195 N·m without it.
- The closing error is not one number. It is:
  - for P2: stop deflection, which depends on the 50–80 mm contact radius (a factor of 2.6 across that band);
  - for P1: the above plus mesh shift;
  - and then the backlash phase.
- The F30B friction hubs allow P1/P2 phasing at assembly. Setting the phase with both leaves seated under a small closing torque takes backlash out of the closed position, so backlash must not be double-counted.
- The stop overhang is the dominant source of G1 face misalignment. It raises the plane-of-action misalignment 3.3–4.1× above the mesh-only value (R14 case `P_driven_jam`) at the soft bound, and about 20–35× at the stiff bound. Support stiffness then sets the magnitude. At the soft bound the catalogue margin is consumed at normal closing, which happens every cycle.

**Minimum combined evidence before planned torque [R].** Each item below is a measurement, not a spring assumption.
1. **Limiters.** Bidirectional static release of BUY520 within 100–120 N·m and of BUY521 within 152–168 N·m at 20 °C and 70 °C. Dynamic output peak ≤150 / ≤195 N·m at the actual speed and inertia. This is already the BUY520/521 contract; it must be done first because it bounds every number above.
2. **Support stiffness or loaded contact pattern for G1.**
   - Option (a): a static lateral load at D886 (no torque, no rotation), with dial indicators at both spindle ends, giving the in-situ bearing+plate stiffness.
   - Option (b): a marking-compound contact pattern at the 5/10/20 N·m increments of the R18 plan.
   - Acceptance: measured k ≥ 1 × 10⁵ N/mm, or the R14 surrogate re-run with the measured k giving peak line load ≤1.0× catalogue at 150 N·m.
3. **Closing error of each leaf**, measured at the blade edge (77 mm radius) as the R18 plan already proposes. Fit a line through the 5/10/20 N·m points. Accept when the error extrapolated to 150 N·m, plus U, is ≤ that leaf's measured seal compression reserve. P1 and P2 must be measured separately.

**Smallest design change [R].** Define the D886 contact radius by putting a crown (R ≈ 50 mm) on the D886 face so contact occurs at r ≈ 75 mm.
- D886 is "NEW PART ONLY" and unreleased, so this costs nothing in rework.
- Stop force and post deflection scale as 1/r and edge error as 1/r². At 78 N·m the band collapses from 0.072–0.184 mm to about 0.082 mm, and the radial load on the P2 bearings falls by 20% relative to r = 60.
- The Hertz line contact at 200 N·m on a 36 mm width is about 2,670 N, about 74 N/mm. That gives about 230 MPa against S355 (345 MPa yield) [I].
- L1 should check the TF900 head geometry and the open-end stop before adopting this.
- Fallback if the G1 measurement fails: a two-arm D886 reacting on two posts 180° apart. This turns the stop reaction into a pure couple and removes the overhung radial load, at the cost of a second post on TF900.

### RT2-05: Six wet stations, F07 (CONDITIONAL). Recommendation: approve machining and unloaded mating; keep preload, load and hot use separate.

**Arithmetic [V on the stated limits].**
- J404: total 3.98–4.02 minus pocket 1.48–1.52 leaves 2.46–2.54 against a minimum metal of 2.45.
- A709: 5.98–6.02 minus 1.48–1.52 leaves 4.46–4.54 against 4.45.
- The minimum-metal rule is implied by the other two only if both hold at every point. The margin is 0.01 mm.

**Measurements to name [R].**
- Per piece: total thickness and pocket depth at ≥3 points each (four corners plus centre where the geometry allows), recorded individually, never averaged. Remaining metal is derived at each point; flatness of both faces is recorded.
- Per station: the assembled free stack height and the fixed/float assignment by serial. These are the inputs to the later preload and thermal proof, which stays open.
- Nothing about the historical 1,000 N proxy reaching zero contact is closed by this approval.

### RT2-06: Film ends P109/R109 (MUST-FIX). One removable keeper, verified for fit and motion clearance, with one fastener change.

**What governs [V].**
- The brief's 224.79/435 mm² reconciles exactly: 224.791 mm² is the frame's own end-strip area (46.774 × 5 minus its Ø3.4 hole), and 435 mm² is 87 × 5, the full nominal film width.
- In that strip, however, the film material actually present is only 220.365 mm², because of the 39 mm corner relief. Of that, 214.235 mm² (97.2%) lies in the P110/R110 frame shadow and 6.13 mm² is unbacked.
- So backing is not the governing quantity.
- The defect is the Ø5 end hole at y = 2.5 being tangent to the film end: zero ligament. The film is retained only by clamp friction under one screw head.

**Smallest change [R]: keeper KP-1.**
- Material and size: 304 strip, 46.774 × 7 × 0.8 mm (full frame width × 7 mm), one per film end, so 16 in total.
- Clearance hole Ø3.4 at the existing end-screw position. It is clamped by the existing STD08B, so the metal interface is unchanged.
- The film's end-strip material is then captured between frame and keeper over 97% of its area (x 0–46.774 of about 0–48). Retention no longer depends on the ligament. The film contour can be released on the open-slot geometry once L1 accepts KP-1; the old tangent DXF stays void, and nothing is cut before that acceptance.

**Verification [V].**
- The keeper envelope intersects nothing in P or R except the eight end STD08B screws per configuration it is meant to sit under.
- Over 0–90° (5° steps) it clears every moving body by ≥12.58 mm (nearest: B200 at 25°).
- The films themselves touch the rotors (gap 0), which confirms the moving set is correct.
- With the screw heads raised by 0.8 mm, no moving body comes within 5 mm at any of 41 positions.

**The required companion change [V].**
- Current end-screw protrusion beyond HW_N3 is 1.75 mm (3.5 pitches). Under a 0.8 mm keeper it becomes 0.95 mm (1.9 pitches), which fails the F06 rule (≥2 full pitches).
- Lengthen the 16 end STD08B by 2 mm (M3 × 18 as a special) or 4 mm (× 20). Either gives protrusion of 2.95 or 4.95 mm.
- The added tip length clears every static and moving body; nearest is its own nut at 1.75 mm.

**Acceptance.**
- Fit-up of one end on a frame offcut.
- Film pull-out under hand load with the screw at its specified torque, compared against the clamp-only case.
- Thread protrusion of ≥2 pitches measured on every end screw.

### RT2-07: Feedback root, guards and access (MUST-FIX). Isolated issue: allocation and calculation, not geometry.

**Contact graph [V]** (`results_r21_root_contacts.json`), the same in P and R:
- A703 (fixed half-seat) and A704R8 (jaw) clamp B200. A704R8 bears on B850, and B852 links A703/A704R8/B850.
- B850 bridge sits on two B851 spherical seats, which sit on disc springs (BUY_R9_DS001500A) over HW_R11_GUIDE_M5 screws threaded into the A703 ears.
- The encoder platform (A705/A706/A707/A710) is a separate chain onto G841.
- Every overlap is a thread: GUIDE_M5 in A703, B853 on B852, HW_FLEX_M3 in A705/A706, HW_FB_FRONT/REAR in A710.
- Every link is a contact; designed clearances (B852 in B850 bore, springs on guides) are open.

The root is geometrically complete. What blocks powered motion is:
1. No product quantity is allocated. B01/E01 cover one Ø30 bench set only; the product needs A703P 2, A703R 1, A704R8 3, B850 3, B851 6, B852 3, B853 6, GUIDE_M5 6, A705/A706 3 each, A707/A710 12 each.
2. The A703 notes require an ear-bending check and a body-torsion check under the spring force (cold force 350–450 N, per the HW_R11_GUIDE_M5 note). Neither calculation is in the package. This is a desk calculation, not a test.
3. A704R8 fulcrum indentation and fatigue, and B850 crown/seat hysteresis, are listed as measured parameters. They are use-holds, not machining-holds.

**Guards and hand/tool [R].**
- The current tool pose excludes the hand and handle. Replace CAD hand models with the opening/reach tables of ISO 13857 for the G901/G902 shaft feedthroughs and the unused G904-covered ports.
- A Ø36 port around a Ø30 shaft leaves a ≤3 mm concentric gap, which falls in the smallest opening class.
- Keep fragment containment out of scope, as the drawings say.
- Do not recall the stable hood panels.

### RT2-08: SP04 four-head station (CONDITIONAL). Qualifiable. Arithmetic that makes M2–M4 concrete [I, R].

**Trip budget.** M2 requires F_trip,i ≤ 1,800 − U_i − O_i − M_i. The 1,500 N example therefore leaves U + O + M ≤ 300 N per head.
- A 0–2 kN class cell with ≤0.5% combined error and k = 2 gives U ≈ 20 N.
- Overshoot is dominated by latency: O ≈ (dF/dt)·t_lat, plus the actuator's stopping term. With t_lat = 50 ms (sample + processing + actuator), O stays ≤100 N only if dF/dt ≤ 2,000 N/s.
- So state a maximum loading rate per step. Prove it on the surrogate, as M3 already asks, rather than by calculation.

**Finite stroke.** Set the mechanical stroke limit so that k_head × remaining stroke + F_preload ≤ 1,800 N with the measured head stiffness. A failed channel then cannot exceed the limit even if the trip fails.

**Unloading.** Use synchronous steps of ≤10% of the current load, with an imbalance bound expressed in N per head. Never release one head while others are loaded; M4 already says this.

**Minimum surrogate.** A steel spring element of stiffness within ±30% of the expected head stiffness, loaded by the actual actuator through the actual chain at the planned rate. It must demonstrate the following on each channel separately:
- measured O_i;
- the trip;
- dropout behaviour, for example by unplugging one channel.

### RT2-09: Input withdrawal, rear plate, lock nuts (MUST-FIX). One hand-off sequence for future acceptance [R]

There is no rotor angular lock in the R20 parts list; I searched names and notes and found none. Today the only angular restraint is the drive line itself. Hence:

| Step | Before release, this support must be engaged | Then release |
|---|---|---|
| H0 | Isolation: actuator de-energised, both limiters in their recorded state, leaf at closed stop | — |
| H1 | **New: rotor angular lock** acting between B200 and the wet frame (for example, through the Ø6H6 datum-C cross-pin bore at local Z 79, if access is confirmed). Witness engagement by gauge or visually. | — |
| H2 | Dry-unit cradle on D878 under the D870 / D885 / BUY520–521 group | BK2 rotor-side hub clamp. The rotor stays carried by its J401 glands and the H1 lock. |
| H3 | Cradle carries the dry group | Bearing-housing bolts. Withdraw the dry group along −Y. The travel must exceed the 43 mm BK2 fit length plus clearance; check it against the 85 mm rear clearance. |
| H4 | Bench fixture holding the spindle on a non-functional diameter (soft jaws), with the dry group off the machine | D873 lock nuts (M4 brass-tip screws first). Never released in situ. |
| H5 | Reverse order to reinstall | Remove the H1 lock last, after BK2 re-clamp and limiter check. |

Rules for the sequence:
- J401, pins and studs are never removed; the sequence does not need them to be.
- Acceptance needs three things: the lock part, a cradle drawing with load rating, and a dimensional-surrogate trial of H2–H3.
- Until then, maintenance stays deferred, as L1 proposes.

### RT2-10: P2 optimisation (P2). Agree: keep everything off the current release gates.

Candidates that first-unit evidence could justify, each with the observation that would trigger it [R]:
- **Custom washers HW_R8_HOOD_W5, HW_R9_HARD_W5 and HW_W4_1_9 → ISO 7089.** Trigger: first-unit seating and bearing-area measurements show the special size buys nothing.
- **STD08B → a catalogue low-head M3.** Trigger: measured film clamp retention with the keeper (RT2-06) is adequate under a standard head.
- **D873 → a catalogue precision lock nut, M30 × 1.5 in the KM6 size class.** Trigger: D873 thread gauging or machining time is a problem on the first unit.
- **G843 stays deferred.**

No visual or cost change is supported yet, because no factory measurements have been returned.

## 4. Manufacturing acceleration, in order [R]

1. Now:
   - Release RT2-01 scope as issued.
   - Draft the standard-fastener enquiry (1,141 pieces) and put the 9 decision rows to L1.
   - Restate the bevel-root rule and start the coupon families (RT2-02).
   - Approve F07 machining with pointwise measurement (RT2-05).
2. In parallel, without waiting for tests:
   - Submit the KP-1 keeper and the STD08B length change (RT2-06) to L1. Once accepted, they unblock film cutting.
   - Add the D886 crown to the unreleased D886 (RT2-04).
   - Add centres to the B202 finish (RT2-03) and select one bench-centres stand.
   - Do the A703 ear and torsion calculations and the product allocation for the root (RT2-07).
3. Gated by L1 test permits (low energy, in this order): BUY520/521 calibration; then D886 lateral stiffness or G1 contact pattern; then 5/10/20 N·m blade-edge increments. In parallel, SP04 surrogate qualification (RT2-08).
4. Deferred: maintenance (RT2-09), until the H1 lock and cradle exist; P2 items (RT2-10).

## 5. Limits of this review

- **Wet/wet pairs not re-checked.** The R12–R12 pairs were inherited; the static check excludes them.
- **Discrete motion check.** Motion is checked at 41 discrete positions, not as a continuous sweep. The 0.1° and 89.9° end positions bound the end approach.
- **RT2-04 inherits the package's model and rating.** The numbers inherit the R14 linear surrogate (constant Ø30 shaft, no clearances) and the KHK catalogue rating, whose basis (life, application factors) is not confirmed. They are screens for choosing what to measure, not ratings.
- **Proposals only.** The keeper, centres, crown and hand-off sequence are proposals. They touch only parts not yet released: D886, B202 finishing, STD08B and the new keeper.
- **Film backing denominator.** The 435 mm² film statistic is reproduced (87 × 5 mm). My 97.2% figure uses the film material actually present in the strip as the denominator instead.

## 6. Reproduction

`tools/run_r21.sh <PART_1.zip> <PART_2.zip> [work] [results]` verifies the manifest and regenerates `results/`, taking about 20 minutes on one core. A full rerun from the zips reproduced every result file byte for byte, apart from the `seconds` timing field in `results_r21_check.json`. The tools read the package as data and never execute package scripts. They need Python 3.13 with the versions in `tools/requirements.txt`.
