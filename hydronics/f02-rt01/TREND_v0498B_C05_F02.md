# DFM trend: v0498B (C4, 2026-09-02) → C05 R1 (2026-10-13) → F02 (2026-10-17)

Inputs:
- `V0498B_VS2D_P0_X800_VS2D_P0_CANDIDATE_C4_ANALYSIS.step`: SHA-256 `f3d1b1ec…214a3b`. AP242, product "C4", 90 parts.
- C05 R1: the RT01 package.
- F02: `HYD3_F02_Water_Only_Interfaces_20261017.stp`.

Every check uses the same tools and the same 2,810-object C05 host. Labels: [V] computed, [I] inference.

## Verdict

**Per part modelled, the manufacturing definition got worse from v0498B to C05, and F02 has not yet recovered it.** The direction since C05 is right, though.

- **v0498B was already a fabricable vocabulary [V]:**
  - hollow 33.7 × 3.2 pipe solids;
  - 28 standard LR 1.5D elbows (R 38.1) and 4 tees, with no single-cut miters;
  - shortest straight between welds 49.8 mm;
  - vendor-detail R3025 valve bodies with ZR2325 unions on all 12 valve ports;
  - zero internal conflicts.
- **v0498B solved a smaller problem:**
  - bed side only: valves, headers and HX fit-ups;
  - no pumps, XV/MV, FS, Q, EV or protection;
  - drawn for an earlier HX port layout.
- **The HX port layout changed, which explains why C05 became complex [V].** v0498B links lower P7 to upper P1 at Y ±72.5 with a 0.31 m U-loop. The current frozen HX (R4_S02, in the C05 host) has those two ports at the far end, Y ±781/±791. The bed link therefore has to travel about 710 mm along the HX, and it now also carries FS and Q. v0498B's bed-link fit-ups land where the current HX has no port, and its upper AB fit-up is 10 mm off the current P7. It cannot be built on the current HX.
- **C05 met the larger scope with the wrong fabrication vocabulary:** 386 single-cut miters, 26 pieces under 10 mm, and 14 threaded joints that cannot be made up.
- **F02 restores the right topology for the full scope** (straight headers, few corners). It drops to centre-line wires, however, and has 28 internal conflicts.

**Right direction [I]:** F02's system topology and scope, built with v0498B's part vocabulary. That means solid pipes, LR elbows and tees, vendor valve bodies with unions at every port, and a zero-conflict check. Neither file does both today.

## Like-for-like comparison [V]

Bed side, H1 cold, bed A: header → valve → HX lower → bed link → HX upper → valve → header. Pressure drop at 2.0 m³/h, 5 °C, counts pipe and corner losses only. HX, valves, FS, Q and meters are excluded because v0498B has no FS or Q.

| Measure | v0498B | C05 R1 | F02 |
|---|---|---|---|
| Scope | bed side only | full system | full system, partial components |
| HX port layout | earlier (bed link at the same end) | current (far end) | current |
| Pipe definition | hollow solids, LR elbows, tees | hollow solids, single-cut miters | wires, sharp corners |
| Bed-side path length | 1.85 m | 5.10 m | 5.29 m (FS gap included) |
| Bed-side corners | 10 LR elbows | 29 miters | 16 undefined |
| Bed-side pipe + corner ΔP | 2.3 kPa | 20.5 kPa (6.5 with elbows) | 12.4 kPa as miters, 4.7 as LR elbows |
| Pieces < 10 mm between welds | 0 (shortest 49.8 mm) | 26 | 2 |
| Valve bodies | vendor detail, ZR unions on all ports | dimensioned surrogates, ZR unions | boxes, no ports |
| Internal conflicts | 0 | 579 pairs (whole system) | 28 (18 through equipment, 10 pipe–pipe) |
| Host pairs, pipes | 97 (0.50 L) for about 9.9 m | 194 (0.36 L) for the 21.3 m main spools | 211 (0.51 L) for 21.9 m |
| Host pairs, valves/actuators | 0 valve/union; 35 actuator envelope (0.03 L) | part of 533 placement pairs | 172 for all equipment (2.3 L) |
| HX joints | pipe ends butt at the X800 face; bed link rigid between two HX ports | Rp1 sockets; 8 cannot be made up | datums missing |
| Exchange | AP242, named parts | AP242 + tables | AP214, names only |

Host conflicts per metre of pipe are similar in all three (≈ 9–10 pairs/m). v0498B was drawn against an earlier host, so its 97 pairs are partly host changes since September, not design defects.

## Carry forward [I]

- **From v0498B:**
  - the part vocabulary (LR elbows, tees, set-on branches, vendor valve geometry, unions on every valve port);
  - its zero-conflict discipline;
  - its compact valve-to-header drops (1–4 elbows each).
- **From F02:** the four straight headers with short drops, and the full system scope.
- **New, because the HX changed:**
  - a bed link that runs about 710 mm along the HX and carries FS and Q;
  - a union, flexible hose or other non-rotating joint at every HX port. v0498B's rigid U-loop between two HX ports shares C05's make-up problem, and is worse because both ends are fixed.

## Limits

- No hydraulic comparison is made for the whole system. v0498B has no source side, pump, FS or Q.
- v0498B is compared against the current host and HX. Its conflicts against the host it was drawn for are not known.
- Belimo-style designations (R3025, ZR2325, LRQ24A) are taken from the part names as given.
