# AT-HYD3-MFG-C05 R1: RT-01 independent red-team review (hydronics)

Package: `hydronics/RT01_review/AT_HYD3_RT01_ENGLISH_MANUAL_REVIEW_20261014.zip.001/.002`, joined to SHA-256 `0e931351…34647af` (matches `SHA256.json`). The edition's `MANIFEST.json` (3,326 payloads) verifies with 0 mismatches.

Scope: read-only computation on the delivered native design, world BReps, AP242 files, flow graph and tables. No supplier was contacted, nothing was bought and no package script was executed. L1 owns every acceptance. This review issues no PASS and does not issue C06.

Labels:
- **[V]** computed here and reproducible from `tools/`.
- **[S]** taken from the package as stated.
- **[I]** engineering inference.
- **[R]** recommendation.

## 0. Conclusion

**C05 should not be repaired item by item.** C05 lists six unmet objectives (`C05_FINAL_STATS.json`, `not_achieved`). They fall into three kinds:

- **Nominal 2.0 m³/h is mostly an artifact.** It comes from loss allocations and the choice of fitting. It passes with a smallest change that keeps every end point fixed.
- **"TR01/RV/internal cavities/thermal evidence" reduces to three closable items:**
  - an actuator stroke-time specification;
  - an RV liquid-capacity datum;
  - a corrected expansion-vessel screen, which C05 gets wrong in both directions.
  Valve-cavity relief remains a vendor item.
- **The other four are real and share one root cause:**
  - zero intersections;
  - qualified pressure interfaces;
  - support load paths;
  - maintenance clearance.
  The router used axis-aligned polylines with zero-radius single-cut miters and 35–45 mm stubs. It welded custom threaded adapters to both ends of 3D weldments. It reserved no space for pipe insulation, and it kept oversized vessels in fixed orientations.

1. **The 2.0 m³/h failure is a fitting-choice problem, not a pump or diameter problem [V].**
   - I reproduced all 16 C05 duty margins exactly (difference < 10⁻⁹ kPa).
   - At 2.0 m³/h, each active path has 54–58 single-cut 90° miters. These cost 32–35 kPa, about half of the total loss.
   - Best estimate with geometry-resolved losses (Darby 3-K; actual run/branch flow in the 9 headers; actual connector bore steps):
     - margin is −11.5 / −10.0 / −10.1 / −7.5 kPa;
     - range −21.6 … −0.4 kPa;
     - still a FAIL, but not the −35 … −31 kPa C05 reports.
   - **Smallest change:** 114 of the 128 DN25 miters can take standard butt-weld elbows inside the existing centrelines, with no end point moved: 93 long-radius (LR) 1.5D and 21 short-radius (SR) 1D. The other 14 stay as miters.
     - Margin becomes **+11.1 / +14.5 / +11.2 / +15.0 kPa**. The low bound is +8.6 kPa.
     - The natural flow with the C05 pump curve becomes 2.21–2.31 m³/h.
     - The result survives a +50 % HX-loss error (+3.9 kPa worst case).
     - 2.58 m³/h still fails (−14.6 … −22.3 kPa).
   - **I built this CAD:**
     - 30 revised spools as world BReps plus one AP242 STEP;
     - clash pairs 390 → 376 and overlap volume −9 %;
     - 3 new contacts of ≤ 10 mm³;
     - 4.2 kg less 316L.
2. **26 mitered pieces cannot be made as drawn, and 42 more are below practical weld spacing [V].**
   - The 26 pieces have less than 10 mm of tube between their two cut planes, including 1.3 mm on the pump-discharge spools E011 and E034. They sit in 25 spools.
   - The 42 further pieces have less than 25 mm.
3. **14 of the 28 rigid threaded joints cannot be made up under C05's own sequence (hot work first, commodities after) [V].**
   - They are:
     - all 8 HX Rp1/R1 joints;
     - one side of each XV (4);
     - one side of each FS (2).
   - Each requires a 3D weldment to be spun several turns inside the bay.
   - **Smallest change:** 14 flat-face unions. The UF_G1 family already exists in C05, and the hydraulic cost is < 1 kPa per path.
   - Separately, the 11 mm "nominal engagement" is below the standard make-up. For 1"-11.5 NPT, hand-tight L1 is 10.16 mm and wrench make-up L3 is 6.63 mm, so about 16.8 mm.
4. **Layout cannot converge by sampling translations [V/I].**
   - **About half of all overlap volume is the four 12 L expansion vessels:**
     - 202 of 1,541 pairs;
     - 5.49 of 10.89 L.
   - **The vessels are about 2.4× larger than the physics needs** (≈ 5 L minimum; RT01-08).
   - Placement objects (commodities and supports) carry 7.2 L of overlap. Routing objects carry 3.7 L.
   - **No C05 pipe has insulation, although 5 °C water runs below any normal bay dew point.**
     - A 13 mm insulation envelope on the 34 main spools raises host conflicts from 194 to 414 pairs.
     - It raises host overlap from 0.36 to 3.49 L.
   - L1 must decide insulation (or drip management plus stated heat loss) before any further layout iteration is meaningful.
5. **The expansion-vessel (EV) screen is wrong in both directions [V].**
   - **Expansion:** C05 requires 1.71 L per domain. The physical duty is 0.59 L (16.6 L domain, 10 → 90 °C).
     - C05 counts each vessel's own 12 L as expanding water and adds a ×1.5 factor on 4 %.
     - The "factory 2.5 barg precharge" therefore fails for the wrong reason: expansion passes even then (2.68 barg final).
   - **Contraction, the case that actually fails, is not screened.**
     - Every trip of a hot bed isolates 16.6 L at about 82 °C. Cooling to 10 °C needs 0.48 L back from the vessel.
     - With precharge ≥ pressure at the vessel, the vessel holds 0 L. That applies to 1.0 barg at the D07 minimum source pressure of 1.0 barg, and to any 2.5 barg case. The bed then goes sub-atmospheric.
   - **Smallest change:** precharge 0.7 barg (or p_min at the EV minus 0.3 bar). Both directions then pass over 1.0–2.0 barg. This is a commissioning setting and a label, not hardware.
6. **TR01 reduces to a stroke-time requirement [V/S].**
   - Valworx states that the DPS positioner drives closed on loss of 4–20 mA at motor speed. A last-link break is therefore an ordinary powered close.
   - With the specified 9 s stroke at 2.0 m³/h:
     - |dv/dt| is 0.38–0.46 m/s² (limit 0.5; marginal at the −10 % stroke tolerance);
     - internal surge is about 5–6 kPa.
   - At the 3.5 m³/h source cap, |dv/dt| reaches 0.67–0.83 m/s².
   - Strokes of **≥ 15 s (3.5 m³/h)**, ≥ 21 s (7 m³/h emergency) or ≥ 32 s (C05's "≥ 8 s effective closure") meet the limits with no LOGO/AM2AQ/UPS ramp layer.
7. **Holds that can be closed by calculation now [V]:**
   - **RQ01 (RV liquid capacity).** Blocked-in residual heat (200 kJ/60 s into 16.6 L) needs 1.9 L/h of relief flow.
   - **Header and branch pressure design.** At ≤ 0.6 MPa the required wall is < 0.1 mm against 3.2 mm. The real header issue is weld access: 18.15 mm stubs at a 35 mm pitch with 13.7 mm between adjacent branch pipes.
   - **Thermal cycling of the stainless lines.** A both-ends-fixed screen gives ≤ 0.70 of the B31.3-type allowable at 5 × 10⁵ cycles. The open item is the HX-port reaction, up to 235 N and 38 N·m per cycle, against unknown brazed-port allowables.

**Confidence:**
- High: reproduction of C05 numbers; piece fabricability; make-up logic; workload; EV arithmetic.
- Medium: best-estimate loss coefficients. Darby 3-K is used outside its validation for close-coupled miters, so I carry ±25 %.
- Medium: EV conclusions. They use the C05 domain volumes and an isothermal gas.
- Low to medium: flexibility. It is a screen with no support model and no known cycle count.

**Evidence that would change these conclusions:**
- a vendor ΔP curve for the HX cores (C05 allocates 14 kPa);
- a measured pump curve;
- EV elevation relative to z0 and the actual source pressures at the EVs;
- adsorption cycle time (number of thermal cycles);
- HX-port load allowables;
- measured actuator stroke on signal loss;
- L1's insulation decision.

## 1. What was checked, and how

| Check | Tool | Result |
|---|---|---|
| ZIP + manifest | `rt01_manifest.py`, `run_rt01.sh` | Joined ZIP SHA-256 matches; 3,326 payloads, 0 mismatches [V] |
| AP242 read-back, S1 and S2 | `rt01_step_readback.py` | 362 solids each = 356 occurrences + 4 state indicators (336 mm³), with FM_CS and FM_HS stored as 2 solids each. Physical volume 120,095,227 mm³ equals native exactly; S1 ≡ S2 [V] |
| Workload / BOM claims | `rt01_workload.py` | 21.2858 + 31.4586 = 52.7444 m; 386 corners, all 90°, all zero radius; 616 = 386 + 136 + 76 + 14 + 4; 68 undefined ends; 18.864 L water; 90.6 kg 316L tube [V] |
| R02 old-WATER exclusion | `rt01_clash_census.py` | 78 WATER occurrences, 0 retained; 0 of 784 C04 host pairs involve WATER. C05 claim reproduced [V] |
| R03 clash method | `rt01_cad_elbows.py` | Delivered E004/E011 reproduce C05 pair volumes to 0.1 mm³. Two host contacts on E011 are missing from the C05 list: R7_A/B_REAR_X_GO, 2.6 and 52.6 mm³ [V] |
| Hydraulic reproduction | `rt01_hydraulics.py` | 16/16 margins reproduced; each state has a unique simple supply→return path [V] |
| Best-estimate hydraulics, elbow fit, operating flow | `rt01_hydraulics.py`, `rt01_elbow_fit.py` | §2 RT01-01/02 [V] |
| Revised CAD (30 DN25 spools) + clash re-check | `rt01_cad_elbows.py`, `rt01_export_step.py` | Monte-Carlo self-check of the all-miter rebuild vs delivered solid: symmetric difference 0 on all 30. Revised clash table in results [V] |
| Miter piece fabricability | `rt01_miter_pieces.py` | §2 RT01-03 [V] |
| Threaded make-up feasibility | `rt01_threaded_makeup.py` | §2 RT01-04 [V] |
| Insulation space claim | `rt01_insulation_envelope.py` | §2 RT01-06 [V] |
| EV two-direction duty, size, shuttle | `rt01_ev.py`, `rt01_ev_shuttle.py` | §2 RT01-08 [V] |
| TR01 closure transient | `rt01_tr01.py` | §2 RT01-10 [V on stated assumptions] |
| Thermal-cycling flexibility | `rt01_flex.py` | §2 RT01-11 [V screen] |
| Vent/drain pockets | `rt01_pockets.py` | §2 RT01-12 [V] |

Correction to my own work, recorded for audit: the first flexibility run ended each chain at the header weld face instead of the HX equipment face. That left 39–294 mm of header and connector out of the model. It produced two false "fails" (ratios 1.33 and 1.05). The corrected chains include the header run and the connector, and every chain passes. Only corrected results are in `results/`.

## 2. Findings

Each finding gives object and state, source, counterexample, smallest change, closure evidence and class. `RT01_FINDINGS.csv` carries the same rows.

### RT01-01: Nominal 2.0 m³/h. MUST-FIX, smallest change available

**Objects.** The active paths, with flow states H1/H2 per C05 `calculate.py`:
- H1 cold: CS→MV_CS→XV_CS→P_CS→FM_CS→H_CS→V_A_L(A→AB)→HX_A_L→FS_A→Q_A→HX_A_U→V_A_U(AB→A)→H_CR→XV_CR→MV_CR→CR.
- The other three paths are analogous.
- Each has 35 edges, 15 spools, 9 headers and 24 connectors. The path is unique in every state [V].

**C05 loss composition at H1, 5 °C, 2.0 m³/h (kPa) [V]:**

| Term | C05 | Best estimate (BE) | BE + elbows |
|---|---|---|---|
| Pipe friction (11.2 m, f = 0.028) | 5.2 | 5.1 | 5.1 |
| Corners: 56 single-cut 90° miters | 37.8 (K 84) | 34.9 (K 77.6) | 12.3 (K 27.3) |
| 9 headers | 8.1 (K 18) | 2.4 (K 5.2) | 2.4 |
| 24 connectors | 16.2 (K 36) | 1.3 (K 3.0) | 1.3 |
| 2 HX (tubes 6.3 + port necks 8.0) [S] | 14.3 | 14.3 | 14.3 |
| Valves: 2 three-way (Kv 10) + 5 (Kv 47.9) [S] | 8.9 | 8.9 | 8.9 |
| Meters [S] | 3.6 | 3.6 | 3.6 |
| **Total** | **94.2** | **70.6** | **48.0** |
| Available (curve − 0.3 m) − 10 kPa source − 5 kPa reserve [S] | 59.0 | 59.0 | 59.0 |
| **Margin** | **−35.1** | **−11.5** | **+11.1** |

**What is wrong in the C05 allocation.**
- **Headers [V].** K = 2 is applied to every header. Seven of the nine headers on each path are traversed straight through: MV:2, P:1, HX P1/P7 headers and FS:1/2. For those, a welded-tee run has K ≈ 0.25. Only H_CS/H_HS and H_CR/H_HR turn the flow into a branch (stub-in tee branch, K ≈ 1.73).
- **Connectors [V].** K = 1.5 is applied to each connector. The modelled bore steps are 27.3 → 24 (NPT), 25 (R1/Rp1), 23.5 (G1 seat) and 30 (G1.5). Sudden contraction and expansion give K 0.06–0.20 referred to pipe velocity.
- **Miters [V].** The miter value is about right. K = 1.5 against Darby's 1.39 (cold) and 1.34 (hot). The miters are what really costs the margin.

**Results at 2.0 m³/h [V]:**

| State | C05 | BE (range) | Elbow-fitted (low) | Q at zero margin: C05 / BE / fitted (m³/h) |
|---|---|---|---|---|
| H1 cold (bed A) | −35.15 | −11.5 (−21.6 … −3.9) | +11.1 (+8.7) | 1.60 / 1.84 / 2.21 |
| H1 hot (bed B) | −34.21 | −10.0 (−19.8 … −2.5) | +14.5 (+12.6) | 1.59 / 1.85 / 2.30 |
| H2 cold (bed B) | −33.64 | −10.1 (−19.9 … −2.7) | +11.2 (+8.6) | 1.62 / 1.85 / 2.21 |
| H2 hot (bed A) | −31.47 | −7.5 (−16.8 … −0.4) | +15.0 (+13.0) | 1.62 / 1.89 / 2.31 |

Notes on the ranges:
- BE range: connector K ×0.5…×2 and miter K ×0.8…×1.25 (coupling of close miters).
- Fitted low: connector ×2 and remaining miters ×1.25.
- At 1.72 m³/h, BE already passes (+8.2 … +10.1 kPa). At 2.58 m³/h every option fails.

**Smallest change [R].** Without moving any end point:
- For each OD33.7 corner, choose the largest butt-weld elbow that fits the two adjacent straight pieces. LR 1.5D needs 38.1 mm centre-to-end; SR 1D needs 25.4 mm. Elbow-to-elbow and elbow-to-connector-face welds are allowed.
- Across the 30 spools with corners: 93 LR, 21 SR, 14 miters kept.
- The kept miters are E004, E018, E021, E052, E055, E067, E075, E087, E105 and E110 (1 each), and E011 and E034 (2 each).
- The supplier must confirm the elbow dimensions (ASME B16.9 NPS1 LR = 38.1 mm; EN 10253-type equivalent for OD33.7).

**Trade-off [I].**
- Each elbow adds one butt weld, because a miter is one joint and an elbow is two. The DN25 joint count rises by 114.
- In exchange:
  - every one of these joints is a square-cut, orbital-weldable joint on a catalogue fitting instead of a hand-fitted 45° miter;
  - the stress-intensification factor (SIF) at each corner falls from 2.55 to 1.38;
  - 26 non-fabricable pieces become moot where an elbow replaces them (RT01-03).
- CNC bending (CLR 2D–3D) has zero joints at the corner. It fits only where the straights are long enough (≥ 2R + clamp length). Use it opportunistically.

**CAD delivered [V].**
- `results/cad/RT01_SP_E***_ELBOWS.brep` (30 files) and `RT01_REVISED_DN25_SPOOLS_AP242.step`: 30 named products, 272 solids. The read-back volume equals the build to 0.3 mm³.
- Clash re-check against all 2,810 retained host BReps and all other C05 occurrences:
  - 390 → 376 pairs and 1,612.6 → 1,462.3 cm³;
  - 17 pairs removed;
  - 3 new contacts: E010/C05_CS01_H04 9.9 mm³ and E027 against MI8 seal-requirement objects 5960/5961, 1.1 mm³ each.
- Steel volume falls from 6,506 to 5,976 cm³ (−4.2 kg).

**Closure evidence.**
- The supplier elbow catalogue confirms centre-to-end.
- The revised spools are re-checked in the full stage model.
- A commissioning ΔP measurement of each path at 0.5/1.0/2.0 m³/h fits K_total within ±25 % of the BE.

### RT01-02: Hydraulic method corrections. Correction to C05 analysis

- **[S/V]** The duty route was found by BFS over the graph with every XV/FS/MV open. In H1/H2 it gives the correct unique path, so this is not an error here. In a mixed (M) state it would not be unique, so a future screen should assert path uniqueness.
- **[V]** C05 adds full header lengths (290 mm) to friction. The actual flow length is 80–255 mm. The effect is negligible at 0.1 kPa.
- **[S]** The HX term contains 8.0 kPa of "port neck" allocation: 4 × (K 3 + 1.02 m of 28 mm bore). That is 56 % of the HX term and it has no vendor basis. It is the next largest unvalidated item after the connectors. Replace it with a vendor ΔP curve.
- **[S]** At 5 °C, tube Re = 2,023 (laminar). C05 forces f ≥ 0.05 in the 1,800–4,000 band. That is conservative and I keep it.

### RT01-03: 26 mitered pieces cannot be made. MUST-FIX

**[V] Geometry.** A single-cut 90° miter plane at a corner (incoming a, outgoing u) has normal (a+u)/|a+u|. The shortest generator of a straight piece with centreline L between two miters is:

g_min = L − r·|b − a|

where a and b are the directions of the neighbouring pieces. The term |b − a| is 0 for a Z-jog, √2 for an out-of-plane turn and 2 for a U-turn. At a square-cut terminal end the term is r.

| Class | DN25 | DN15 | Total |
|---|---|---|---|
| g_min < 10 mm (no practical fit-up, purge or torch access) | 5 | 21 | 26 |
| 10 ≤ g_min < 25 mm (manual TIG only, no orbital head) | 14 | 28 | 42 |
| ≥ 25 mm | 143 | 277 | 420 |

Worst cases:
- E011 and E034 piece 5: a 35 mm U-turn piece on OD33.7, g_min = 1.3 mm. These are the FM → H_CS/H_HS discharge spools.
- E120: a 2.5 mm Z-jog.
- E144 and E152: 13 mm terminal pieces on DN15.
- In total, 25 spools contain at least one piece < 10 mm (`results/rt01_miter_pieces.csv`).

E011 also loops 315 mm away and back to enter H_CS at its far end, although FM_CS:2 sits 60 mm directly below the header. That one loop is the result of fixing the header main face at y = −10.

**Smallest change [R].**
- On DN25, RT01-01 removes the problem wherever an elbow replaces the miter.
- On DN15 service and instrument lines (no flow), adopt a rule: g_min ≥ 25 mm, otherwise re-route or use a bent tube (CLR 1.5–2D on 21.3 × 2.6).
- For H_CS/H_HS, move the FM connection to a branch next to the FM outlet, or make the main face the y = −300 end. This deletes the E011/E034 loop.

**Closure evidence.** The piece table is regenerated with zero entries below 25 mm. A WPS coupon is made on the shortest remaining miter piece.

### RT01-04: 14 threaded joints cannot be made up. MUST-FIX

**[V]** Weldments were grouped by matching faces (spools + headers + welded connectors), giving 26 weldments. A threaded joint can be made up only by turning one of:
- a loose union tail (ZR R1 tails);
- a 2-port body whose other port is still free (MV, XV, FS);
- a straight single-spool weldment.

Under C05's stated order (hot work on spools and headers before valves and instruments, see `C05_ASSEMBLY_SERVICE_AND_SUPPORT_EN.txt`), these cannot be made:
- **8 HX joints.** The Rp1 female socket must be screwed onto the frozen HX R1 male by turning a 3D weldment of up to 10 members (e.g., E058 + HX_A_L:P1 header + 6 service branches + EV inlet).
- **XV_CS/CR/HS/HR :2 (4).** The body turn is used up on :1, and the other side is a 3D weldment.
- **FS_A:2 and FS_B:2 (2).** Same reason.

The MV bodies are makeable because E003/E017/E026/E040 are straight 17 mm spools.

**Smallest change [R].**
- Put a flat-face union (the existing UF_G1 family) at each HX port.
- Put a UF_G1 union at one port of each XV and FS.
- Hydraulic cost is about K 0.3 each, under 1 kPa per path.
- The better option at the HX ports is RT01-11: a short braided 316L hose with a swivel union.
- Alternative for XV/FS: 3-piece full-bore ball valves with butt-weld ends. The swing-out centre removes 12 NPT joints and their leak paths. This needs an actuator and positioner change, which is L1's call.

**Closure evidence.** A written make-up sequence where every threaded joint names its turning member. A dry-fit of one bed module.

### RT01-05: Thread engagement basis. SHOULD-FIX

- **[S]** C05 places every adapter at 11 mm "nominal engagement" and states that this is not a cut basis.
- **[S/V]** ASME B1.20.1 for 1"-11.5 NPT: L1 (hand-tight) = 10.16 mm and L3 (wrench make-up) = 6.63 mm. A made-up joint is therefore ≈ 16.8 mm, a systematic +5.8 mm per NPT end. ISO 7-1 R1 is similar: gauge length 10.4 mm ± 1 turn (2.3 mm) plus 1.5–3 turns of make-up.
- **[R]**
  - Use L1 + L3 (NPT) and gauge length + 2 turns (ISO 7) as the nominal.
  - Provide one adjustable joint (a union) per rigid chain to absorb ±1 turn.
  - NPT and BSP coexist (20 NPT, 12 R1, 8 Rp1). Kit and mark them separately: 1" NPT (11.5 TPI) and R1 (11 TPI) start by hand and then leak.

### RT01-06: No insulation space claim. DECISION (L1)

**[V]** None of the 102 spools carries insulation geometry. The 5 °C cold lines and the reversing bed lines run below any normal bay dew point; the host register (G12) already lists vapour barrier and drip management as open.

With a 13 mm envelope (OD 59.7 mm) on the 34 main spools, exact miters, and other main spools also insulated:

| | Bare | Insulated |
|---|---|---|
| Host pairs | 194 | 414 |
| Host overlap volume | 0.36 L | 3.49 L |
| Water-object overlaps (directed) | 198 | 306 |

Only 4 of the 34 main spools stay host-clear when insulated. On the 35 mm header pitch, the envelopes of the 21.3 mm branches (47.3 mm OD) overlap by construction.

**[R]** Before any C06-type layout work, L1 must choose one of:
- **(a)** Insulate all cold and reversing lines. This needs a host space allocation (IF05_01) and a header pitch of ≥ 50 mm.
- **(b)** Bare lines in a drained wet bay. This needs a stated condensate load and stated parasitic heat: about 55–60 W/m of bare DN25 at 82 °C in a 30 °C bay is [I] ≈ 0.7 kW on the 11–13 m hot path.

**Closure evidence.** The decision is recorded in the source register and reflected in the CAD envelope.

### RT01-07: Clash root cause. Re-plan, do not resample

- **[V]** Of the 1,541 C05 pairs:
  - 1,008 involve a routing object (pipe, connector, header, adapter or seal), 3.68 L in total;
  - 533 are commodity or support placement against the host or each other, 7.22 L.
  - Only 160 pairs are under 10 mm³.
  - The 4 EVs alone account for 202 pairs and 5.49 L.
- **[S]** Translation sampling (≤ 125 per device, bbox-ranked, first 8 Boolean-checked) cannot prove infeasibility. It also never addressed device size or orientation.
- **[R] Order of work:**
  1. Resize the EVs (RT01-08) and re-place them.
  2. Re-place the pumps, meters and valve stations with explicit rotation freedom and an insulation envelope.
  3. Re-route with the rule set below. The router should optimise for fewest corners and use catalogue fittings.

**Proposed routing rules [R]:**
- bend radius ≥ 1D, using catalogue elbows;
- g_min ≥ 25 mm;
- ≤ 4 corners per spool unless justified;
- every threaded port has a union or a turnable member;
- header pitch ≥ 50 mm;
- vent at every local high point and drain at every local low point.

**Closure evidence.** Zero material intersections in the full stage set, with insulation envelopes.

### RT01-08: Expansion vessels. MUST-FIX (setting) + size option

**[V]** Basis:
- isothermal gas;
- IAPWS-95 densities (CoolProp);
- largest H1/H2 domain = C05 known water 15.56 L + 1 L allowance = 16.56 L;
- RV-limited final 2.8 barg [S].

| Precharge | p at EV | Water in EV | Expansion 10 → 90 °C (+0.590 L): final | Contraction 82 → 10 °C (−0.483 L): final |
|---|---|---|---|---|
| 1.0 barg (C05) | 1.0 barg | 0.00 L | 1.10 barg ✓ | **vacuum ✗** |
| 1.0 barg | 1.5 | 2.39 L | 1.66 ✓ | 1.38 ✓ |
| 2.5 barg (factory) | 1.0–2.0 | 0.00 L | 2.68 ✓ | **vacuum ✗** |
| **0.7 barg** | 1.0 | 1.79 L | 1.12 ✓ | 0.91 ✓ |
| **0.7 barg** | 2.0 | 5.18 L | 2.29 ✓ | 1.80 ✓ |

- C05 requires 1.71 L. That is max(27, V + 13) × 0.04 × 1.5, which counts each vessel's own 12 L as system water. The physical duty is 0.59 L.
- **[V]** The minimum vessel at 0.7 barg over 1.0–2.0 barg (0.2 L water seal) is **5.0 L**. The 12 L vessel is 2.4× that.
- **[V/I] Shuttle.** On each reversal a bed changes source. The pressure at its direct EV therefore changes by the hot/cold static difference plus the flow-induced change (inlet ↔ outlet). A 12 L vessel at 1.0 barg precharge moves 1.1 / 2.4 / 4.0 L for a 0.2 / 0.5 / 1.0 bar change, and that water ends up in the other source.
  - D07 allows each source anywhere in 0.10–0.20 MPa(g).
  - With 0.5 bar between sources and 2 EVs per bed, about 4.8 L of hot water is pushed into the cold circuit on each reversal. That is [I] ≈ 1.5 MJ, about 20 % of the bed water's sensible switching load.

**[R]**
- Set precharge on site to (minimum pressure at the EV elevation − 0.3 bar), nominally 0.7 barg. Tag each vessel and record the value.
- Add to D07: "hot and cold static pressure at z0 equal within ±0.1 bar".
- Consider 8 L vessels, which give margin at about 2/3 of the shuttle volume and less space claim. Confirm the vendor size.

**Closure evidence.**
- EV elevations versus z0.
- A two-direction table with measured source pressures.
- At commissioning, a pressure-hold test over a hot-trip cool-down.

### RT01-09: RQ01 relief liquid capacity. CLOSE BY CALCULATION

- **[V]** β(80 °C) = 6.41 × 10⁻⁴ K⁻¹. 200 kJ/60 s into 16.56 L gives 0.049 K/s (+3.0 K in 60 s). The relief duty is **1.9 L/h**.
- **[R]** Close RQ01 when the vendor confirms the RV's liquid capacity at set + 10 % ≥ 0.01 m³/h. Any ½" thermal relief valve has orders of magnitude margin.
- **[V]** Related: the MV–XV interspaces (Z_INTERSPACE_*) have no RV. Water trapped there at 5 °C and warmed to 30 °C would reach ≈ 8 MPa if fully rigid. They are protected only procedurally ("lock bleed open").
- **[R]** Fit a ½" thermal relief, or a key interlock (MV cannot be closed unless BLD is open).
- **[R] VQ01, sealed ball cavities.** Specify cavity-relieved (upstream-vented) balls for the MV/XV/FS and the 3-way selectors, or obtain each vendor's cavity-relief statement. This is a purchase-specification item, not a layout one.

### RT01-10: TR01. Turn the open item into an actuator specification

- **[S]** Valworx DPS behaviour:
  - fails closed on loss of control signal, at motor speed;
  - holds position on loss of power unless BSR is fitted;
  - published 0–90° cycle time is 58 s for the 5616 series.
  - These facts come from search-result extracts of Valworx product pages (e.g. the 5616 DPS kit page). Neither the manufacturer PDF referenced by C05 nor the vendor site resolved from this environment. Confirm with the vendor before specifying.
- **[V] Model.** Quasi-steady closure of a Kv 47.9 ball valve with an x³ characteristic (x² and x⁴ as sensitivity) in series with the rest of the loop, rigid column.

| Case | Kv_sys | 9 s stroke: t_eff 90→10 % / max dv/dt | Stroke for dv/dt ≤ 0.5 m/s² | Stroke for t_eff ≥ 8 s |
|---|---|---|---|---|
| 2.0 m³/h, pump | 2.6 | 2.3–2.8 s / 0.38–0.46 m/s² | 6.8–8.3 s | 26–31 s |
| 3.5 m³/h, source cap | 2.5 | 2.3–2.7 s / 0.67–0.83 | 12–15 s | 26–32 s |
| 7.0 m³/h, emergency | 5.0 | 3.2–3.4 s / 1.07–1.17 | 19–21 s | 21–23 s |

- At 9 s, the surge is 5–15 kPa internal (13 m), plus 38–117 kPa per 100 m of external source pipe. The Joukowsky bound of 1.3–4.7 MPa applies only to closure faster than 2L/a, which is about 20 ms here.
- **[R]** Specify an XV/FS powered stroke of ≥ 30 s/90°, with the same speed on signal loss and on BSR, confirmed by bench test. This meets every TR01 limit by itself and removes:
  - the LOGO/AM2AQ ramp layer;
  - its uncovered controller and output faults;
  - the UPS sizing question.
- **Cost [I].** About 1 min of extra switching dead time per reversal. Normal changeover is already ramped to 0.5 m³/h and is unaffected. L1 must weigh this against the adsorption cycle time.
- **Closure evidence.** Bench test: cut the 4–20 mA loop at 2.0 and 3.5 m³/h and log Q(t) and p(t).

### RT01-11: Thermal cycling and HX-port loads. CONDITIONAL

- **[V] Screen.** 3D linear frame, both anchors fixed, no supports, rigid corners, ΔT = 77 K, α = 16.4 × 10⁻⁶ K⁻¹, E = 195 GPa.
  - SIFs: miter 2.55, LR elbow 1.38, threaded end 2.3.
  - Allowable: S_A = f(1.25 Sc + 0.25 Sh) with Sc = Sh = 115 MPa.

| Chain | Corners | S_E miter / elbow (MPa) | Ratio at N = 5 × 10⁵ (S_A 75 MPa) | HX-port reaction |
|---|---|---|---|---|
| V_A_L:AB → HX_A_L:P1 | 9 | 18.4 / 14.0 | 0.25 / 0.19 | 73 N, 10.6 N·m |
| V_A_U:AB → HX_A_U:P7 | 8 | 46.4 / 36.1 | 0.62 / 0.48 | 194 N, 33.0 N·m |
| HX_A_L:P7 → HX_A_U:P1 (via FS, Q) | 21 | 31.8 / 31.8 | 0.42 | 176 N, 22–30 N·m |
| V_B_L:AB → HX_B_L:P1 | 9 | 28.0 / 24.9 | 0.37 / 0.33 | 120 N, 23.5 N·m |
| V_B_U:AB → HX_B_U:P7 | 9 | 52.3 / 41.2 | 0.70 / 0.55 | 235 N, 38.3 N·m |
| HX_B_L:P7 → HX_B_U:P1 | 21 | 27.6 / 27.6 | 0.37 | 145 N, 23–26 N·m |

- The stainless lines pass the screen. The open item is 23–38 N·m per cycle on CW602N adapters brazed to copper HX headers, with no stated allowable.
- **[R]** Use a 300–500 mm braided 316L hose with a swivel union at each of the 8 HX ports. It addresses four things at once:
  - the HX-port loads;
  - the HX make-up (RT01-04);
  - tolerance to the frozen X800 ports;
  - HX removal for service.
  - Hydraulic cost is K ≈ 1 per hose, about 1.8 kPa per path. The elbow-fitted margin covers it.
- **Closure evidence.**
  - HX vendor nozzle-load allowables.
  - A flexibility run with the real supports and the hoses.
  - The cycle count, from cycle time × design life.

### RT01-12: Vent and drain pockets. SHOULD-FIX

- **[V]** 64 spools contain internal local high or low points (≥ 1 OD) with no vent or drain. Vents and drains exist only on headers.
  - DN25: 10 high and 9 low points.
  - DN15: 18 high and 45 low points.
- They cause air binding at fill and leave water that cannot drain after factory hydrotest. Shipping below 0 °C would then risk freeze rupture.
- **[R]** Add a routing rule (RT01-07). Write a post-hydrotest blow-down procedure with dry-air verification.

### RT01-13: Headers. CONDITIONAL

- **[V]** All 76 branch stubs project 18.15 mm from the header OD, at a uniform 35 mm pitch, rotated in 90° steps. That leaves 13.7 mm between adjacent DN15 branch pipes. The spool butt weld sits about 14 mm from the saddle-weld toe.
- **[V]** Pressure design is not a real hold. At ≤ 0.6 MPa (the HX rating), the required wall is 0.088 mm against 3.2 mm, and opening reinforcement is satisfied by excess wall.
- **[R]**
  - Close the pressure hold by calculation.
  - Make a weld-access mock-up of one 7-branch header (H_CS) before any further header design.
  - Consider standard reducing tees or a machined block for the 4 source headers.

### RT01-14: Package-level observations

- **[V]** The clash list omits two small host contacts found here (E011 against R7_*_REAR_X_GO). The C05 host comparator set is therefore narrower than the 2,810 retained BReps. State its filter.
- **[S]** Drawing set: F01/F02 give the 8 Rp1 HX sockets a plain OD46 with no wrench flats, while the NPT and R1 adapters have AF41. A socket that must be torqued onto a brass HX adapter needs flats, and the HX adapter needs a back-up hold. The 102 spools are defined only by the centre-line coordinate CSV, with no isometrics or cut-piece drawings. RT01-03 shows why per-piece drawings are needed.
- **[S]** The CS02 standalone support is not installed, and the 48 inherited support failures remain. The vessel, pump and valve-station load paths, and an 18 kg full EV on DN15 lines, need their own brackets. They are not reviewed here beyond this note.

## 3. Review worksheet R01–R24

`RT01_REVIEW_WORKSHEET.csv` gives the status, observation, quantity and closure for each check. Summary:
- **REPRODUCED:** R01, R02, R07, R08 (end matching), R11, R18, R19 (pipe water, tube mass).
- **NOT_REPRODUCED (C05 result is wrong or overstated):**
  - R12: allocations;
  - R13: the EV requirement is overstated and contraction is missing;
  - R14: the factory precharge fails by contraction, not expansion.
- **CONDITIONAL:** R03 (method reproduced; two omissions), R09, R10, R15, R16, R17, R20, R21, R23.
- **INSUFFICIENT_EVIDENCE:** R04, R05, R06 (sampling design; I did not re-run poses).
- **R22/R24:** holds re-sorted in §4.

## 4. Root-cause groups and the minimum complete next outcome

**Root causes [I]:**
1. **Routing primitive.** Zero-radius single-cut miters on axis-aligned polylines with short stubs. This drives RT01-01, 03, 11 and 12, and part of 07.
2. **Joint concept.** Custom threaded adapters welded to both ends of 3D weldments, with hot work done first. This drives RT01-04 and 05.
3. **Space claim.** Oversized EVs, no insulation envelope, fixed device orientation. This drives RT01-06 and 07.
4. **Analysis allocations.** Header/connector K, EV water budget, factory precharge, TR01 framed as a controls problem. This drives RT01-02, 08, 09 and 10.

**Retain:**
- the logical intent (156/162 graph, protection taps);
- the pump selection;
- the HX X800 ports;
- the D07 contract (adding the ±0.1 bar static-pressure equality);
- 26 of 30 DN25 route corridors, with elbows;
- the C05 clash, read-back and workload infrastructure, which reproduces.

**Rework:**
- DN15 service routing under the g_min rule;
- the H_CS/H_HS main-face orientation;
- the union and hose set (14 + 8);
- EV size and precharge;
- XV/FS actuator stroke.

**Interface decisions for L1:**
- insulation (a or b);
- EV size;
- XV/FS stroke versus switching dead time;
- whether 3-piece weld-end valves are acceptable.

**Minimum complete next engineering outcome [R], ordered:**
1. L1 records decisions on insulation, EV size and stroke.
2. Device re-placement with rotation freedom, sized to the decided envelopes.
3. Re-route with the RT01-07 rule set (catalogue elbows, g_min ≥ 25 mm, unions, vents and drains, insulation envelope).
4. Re-run the same three checks (zero intersections, hydraulic duties using the BE method with a vendor HX curve, EV two-direction table).
5. One bed module dry-fit, with the make-up sequence demonstrated.

## 5. Limits

- C01–C04 originals and the full parent assembly are not in the package. Conclusions on stage sequences, service tools (AF46, EV withdrawal) and supports are limited to what C05 contains.
- I did not re-run the 125-point layout sampling, the AF46 poses or the 33/84 graph cases.
- Loss coefficients are correlations, not tests. The HX, valve and meter terms are C05's.
- The flexibility check is a screen without supports. The EV check uses C05 domain volumes and isothermal gas.
- The revised spools change corners only. Their remaining clashes are the layout's (RT01-07).
- Several external facts were not opened at source. Valworx DPS behaviour and cycle time come from search-result extracts. ASME B1.20.1 / ISO 7-1 dimensions, Darby 3-K constants and the B31.3 SIF/allowable forms are from the reviewer's knowledge. Confirm all of them against current documents before purchase or design release.
