# HYD3 F02 "Water-Only Interfaces" (2026-10-17): RT-01 addendum

Input: `HYD3_F02_Water_Only_Interfaces_20261017.stp`, SHA-256 `f4888a59…7e83988`. It is an AP214 file (OCCT 7.8 writer) with one assembly of 48 named products.

Baseline: AT-HYD3-MFG-C05 R1 as reviewed in [`../c05-rt01/RT01_REVIEW.md`](../c05-rt01/RT01_REVIEW.md). The "original version" in the separate thread *L1-CAD red team audit* was not available to this review. If it differs from C05 R1, re-run `tools/run_f02.sh` against it.

Labels: **[V]** computed here, **[S]** read from the file, **[I]** inference, **[R]** recommendation.

## Verdict

**F02 advances the hydronic concept, not the manufacturing definition.**

**What it gets right:**
- It replaces the C05 routing with four straight full-width headers and short drops.
- Corners fall from 386 to 40 in total, and from 54–58 to about 18–20 per active path.
- 102 spools become 26 lines.
- The 2.0 m³/h duty becomes positive even with plain miters: [V] about +13 … +16 kPa, against −7.5 … −11.5 kPa for C05 at best estimate.
- This is the routing simplification RT-01 asked for.

**What is missing or regressed:**
- The model is centre-line wires plus placeholder blocks.
- Its geometry contradicts itself:
  - 18 pipe-through-equipment conflicts;
  - 10 pipe-to-pipe conflicts;
  - six of the 14 valves are not connected to any line;
  - the return headers have no route to the CR/HR boundary.
- Against the host it is not cleaner than C05: 211 pipe pairs bare and 515 insulated, against 194 / 414 for C05's main spools.
- It is not yet usable as a fabrication model.

**As an integrator-communication model it is the right kind of artifact:** interfaces plus space plus intent, with the detail left to the supplier. It needs the corrections in §3 and the companion tables in §4 before it goes out.

## 1. What the file contains [S/V]

| Content | F02 | C05 R1 |
|---|---|---|
| Pipe geometry | 26 centre-line wires, 21.86 m, sharp corners, no OD or wall | 102 hollow spools, 52.74 m |
| Headers | 4 straight lines, 1,580 mm, along Y: CS X1090/Z560, HR X1010/Z500, CR X1090/Z1390, HS X1010/Z1450 | 22 drilled custom headers |
| Corners | 40 (all 90°) | 386 single-cut miters |
| Equipment | 14 envelopes: P×2, 3-way V×4, FS×2, XV×4, Q×2 | 100 commodity proxies |
| Absent | MV×4, FM×2, EV×4, RV×14, AV/DV, PT/TT, BLD×4, unions, supports, insulation, CR/HR boundary lines | all present as proxies |
| HX interfaces | 8 stubs, OD33.7 × 30 mm at X770–800. Their full volume coincides with the frozen HX host object, so they duplicate it | adapters + Rp1 sockets |
| Exchange | AP214, names only, no port datums, no line data | AP242 + parameter tables |

## 2. Checks

**Hydraulics [V].** Path H1 cold, bed A: source → pump → header (1.0 m run) → V_A_L → HX_A_L → FS gap → Q_A → HX_A_U → V_A_U → CR header. The return leg to the boundary is not modelled, so I bound it at 0 or 1.2 m + 2 corners.

Method: same as RT01-01 (Darby 3-K; 3 tee turns; C05's HX, valve, meter and pump terms; 10 kPa source and 5 kPa reserve).

| | Path | Corners | Margin, miters | Margin, LR elbows |
|---|---|---|---|---|
| 5 °C | 7.2–8.4 m | 18–20 | +12.7 … +14.5 kPa | +22.4 … +23.2 kPa |
| 80 °C | 7.2–8.4 m | 18–20 | +14.5 … +16.1 kPa | +23.8 … +24.5 kPa |

**Piece fabricability [V].** Only 2 miter pieces have a minimum generator below 25 mm: CS_A and CR_A, a 26 mm terminal piece giving 9.1 mm. C05 had 68.

**Internal conflicts [V].** The check sweeps OD33.7 tubes along the lines with exact miters and tests them against the real equipment solids.

| Class | Pairs | Overlap | Examples |
|---|---|---|---|
| Header tees (expected) | 9 | 14 cm³ | header ↔ branch |
| Line terminating on its own equipment (acceptable) | 13 | — | AB lines at the valve faces, Q, pump ports |
| **Line through equipment** | **18** | ≈ 600 cm³ | HR_A and HS_A run 245 mm through the V_A_L / V_A_U bodies to reach port B. HX_A_L_CLOSE runs through FS_A and XV_HS. A_FS_TO_Q and A_Q_TO_UPPER run through the hot pump P_HS (169 / 170 mm). B side mirrors this through P_CS, FS_B, XV_CS. PUMP_TO_HEADER_CS runs 132 mm through XV_CS, across its flow axis |
| **Pipe through pipe** | **10** | 42 cm³ | HX_A_L_CLOSE ∥ A_FS_TO_Q at 18.9 mm centre spacing over 420 mm (13.0 cm³), B side 17.9 cm³. CS_B and the pump branch enter the CS header 8 mm apart. Several crossings |

**Connectivity [V].**
- FS_A, FS_B and the four XV have **no line attached**. They sit in a parking row (X801–1049, Z606–738 / 954–1086).
- The FS position on each bed is a 292 mm gap between free ends (X868.9–1161.1, Y∓280, Z672), but no FS is placed in it.
- CR and HR headers end free. No line leaves them for the boundary.
- Only CS and HS have boundary points, at (1180, ±450).

**Host [V].** Same 2,810 retained host BReps and Boolean method as RT-01.

| Objects | Pairs | Overlap |
|---|---|---|
| 26 lines, bare | 211 | 0.51 L |
| 26 lines, 13 mm insulation | 515 | 5.29 L |
| 14 equipment envelopes | 172 | 2.32 L |

For comparison, C05's 34 main spools gave 194 / 0.36 L bare and 414 / 3.49 L insulated. The worst equipment items are FS_A and FS_B in the parking row against insulation and wet-service objects (43 and 47 pairs, about 0.44 L each), followed by V_A_U and V_B_U.

The four straight headers are not free of the host either:
- HR and HS (X1010) pass through the centre frame post F_POST_1020_0 (1.8 cm³ each).
- Host pairs per header: CS 5, HR 9, CR 71 (insulation and module bodies), HS 18.
- A full-width header needs a corridor reserved in the host, and none exists today.

## 3. Corrections before the file goes to a supplier [R]

1. **Place the FS and XV on their lines with flow axes aligned.** FS goes in the 292 mm gaps. XV goes on the source lines (C05 P&ID: upstream of the pump) and on the return lines. Delete the parking row.
2. **Model the CR and HR return lines** to the boundary, with XV and MV, and define the four boundary ports (position, axis, connection standard).
3. **Reach each three-way valve port from outside its body.** Today the B and A port lines come up through the valve.
4. **Separate the parallel bed runs** (≥ OD + 2 × insulation + 20 mm, i.e. ≥ 80 mm centre-to-centre, against 18.9 mm now). Reroute A/B_FS_TO_Q and A/B_Q_TO_UPPER away from the pumps. Space the header branches ≥ 80 mm apart (the pump branch and CS_B are 8 mm apart today).
5. **Add the missing P&ID items as tagged envelopes,** even coarse ones: MV×4, FM×2, EV×4 (≈ 5–8 L, RT01-08), RV/AV/DV/PT/TT taps. An integrator quotes from the tag list.
6. **Replace the 8 HX stubs with interface datums:** point + axis + "R1 male CW602N, brazed, no hot work, back-up hold required". The stubs currently overlap the HX host object entirely.
7. **Re-export as AP242** with the tag names, and supply a line list as CSV or PDF beside it.

## 4. What accelerates the integrator most [R]

Send a short interface-control package rather than a finished pipe model, and let the integrator return the detailed design:
1. **P&ID and equipment list** (C05 graph, tags, fail positions).
2. **Interface control table:** 8 HX ports, 4 boundary ports, pump/valve power and I/O, mounting points.
3. **Space envelope:** allowed volume and a simplified host keep-out STEP, the 2,810 objects decimated to boxes.
4. **Duty and conditions:**
   - flow 0.5 / 2.0 m³/h;
   - water 5–82 °C, cycling;
   - source 0.10–0.20 MPa(g);
   - ΔP budget: ≈ 59 kPa available, of which HX + valves + meters take ≈ 27 kPa;
   - design pressure and RV set point.
5. **Design rules from RT-01:**
   - catalogue bends or elbows, no single-cut miters;
   - a union or swivel at every threaded port, and hoses at the HX ports;
   - vent and drain at local extremes;
   - the insulation decision;
   - EV size and 0.7 barg precharge;
   - XV/FS stroke ≥ 30 s.
6. **Deliverables expected back:**
   - AP242 with pipe solids;
   - isometrics and BOM;
   - hydraulic and flexibility calculations;
   - weld and test plan;
   - lead times.

F02 already supplies most of item 3's intent and the HX half of item 2. With §3 done it becomes the geometric attachment to this package.

## 5. Limits

- No pipe sizes are given in F02. OD33.7/ID27.3 is assumed for every line, including the headers.
- The return-leg hydraulics are bounded, not modelled.
- Equipment envelopes are taken as drawn.
- The "original" in the other thread was not compared.
