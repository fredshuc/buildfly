# Two-bed module topology reset: four-core outdoor topology, vertical coil, cube

This is a red-team concept input for shell2's next revision. It is not a shell revision or a fabrication release. Revision 3 (6 November 2026) rebases the damper layout on the archived four-core outdoor sheet metal, [`references/four-core-outdoor/V050_SM_M2_IN1_R1_OUTDOOR_SHEET_METAL_ONLY.stp`](../../../../references/four-core-outdoor/V050_SM_M2_IN1_R1_OUTDOOR_SHEET_METAL_ONLY.stp) (SHA-256 `d20fbdc7…6f6ae`, 521 occurrences).

Labels:
- **[V]** computed here and reproducible with `tools/`.
- **[S]** taken from a delivered source.
- **[E]** estimate.
- **[R]** recommendation.

![Four-core topology, vertical-coil mapping and header model](fig_cube.png)

## 1. What the reviews missed

C04–C07 brought the air in through selector boxes **below** the coil and made it climb about 1 m through 32 inclined channels. Every problem RT1–RT3 then reviewed comes from that choice:
- the 2.55–2.76 m height;
- the weak regeneration-port authority (A1);
- the plates, slots and keepers;
- the 219–315 Pa internal path loss.

The reviews audited each revision inside its architecture and never asked why the air enters from below. RT3's "accept for prototype detailing" is withdrawn.

## 2. The four-core reference, read from its STEP [V, `results/four_core.json`]

Bed A, one bed column (Y −815 to −46.5):

| Element | Geometry |
|---|---|
| Coils | Two horizontal stages (Z 620–798 and 955–1133), X −410 to 590. Air passes vertically. |
| Upper plenum | A wedge under a roof **sloped 12.3°** (normal 0.213, 0, 0.977), running from Z 1381 at the front to Z 1164 at the rear. Depth is 248 mm at the front and 31 mm at the rear. |
| Lower plenum | A wedge over a floor sloped 12.3°, running from Z 561 at the front to Z 345 at the rear. Depth is 59 mm at the front and 275 mm at the rear. |
| P in | A vertical damper on the upper plenum's **front end wall** (X −505, Z 1133–1368). It is fed through an inlet box from the front at the top level. |
| R out | A damper on the **roof slope** next to that corner (X −484 to −252). It opens into the top chamber (Z 1381–1527), which leads to the rooftop-fan interface ring (X ±310, Y ±230, Z 1531). |
| P out | A vertical damper on the lower plenum's **rear end wall** (X +505, Z 358–586). It feeds the rear-bottom outlet duct (X 751–1200, Z 335–602). |
| R in | A damper on the **floor slope** next to that corner (X 252–484). It is fed by the hopper chamber below the floor (a 32.7° plate, X 265–748, Z 68–386), which is open at the bottom rear. |
| Corner hardware | A hinge element at each corner (X ≈ −500, Z ≈ 1385 at the top; mirrored at the bottom), plus outboard brackets. This is the original single-actuator, two-plate diverter location. |
| Damper planes | P (end wall) against R (slope): **77.7°** = 90° − 12.3°. |
| Envelope | 1900 × 1706 × 1500 mm, including the rear outlet annex. |

The rule the reference follows:
- **P dampers sit on the plenum end wall at each wedge's wide end**, perpendicular to the coil face, so process air enters and leaves along the manifold axis.
- **R dampers sit on the slope beside that corner** and open into a chamber outside the slope: a top chamber leading to the rooftop fan, and a bottom hopper leading from the floor.
- The two layouts are point-symmetric.

## 3. Mapping to one vertical coil per bed

| | Front plenum (−X of the coil): wedge, wide at the top | Rear plenum (+X of the coil): wedge, wide at the bottom |
|---|---|---|
| P | **P in on the top end face** (horizontal, at the corner). Air comes from the roof intake, descends and converges, then crosses the coil in +X. | **P out on the bottom end face** (at the corner). Air leaves at the floor. |
| R | **R out on the front slope** beside the top corner, into an exhaust chamber (depth S, between the slope and the front skin) that is open to the **rooftop fan**. | **R in on the rear slope** beside the bottom corner, from an intake chamber (depth S) that is open to the **floor**. It ascends, converges, then crosses in −X. |
| Damper planes | 90° − atan(D/H) = **63.4°** at D/H = 0.5 (55° at 0.7). The steeper plenum gives a smaller angle than the four-core 77.7°. | Same angle. |

This matches the stated requirements:
- P comes from the top and leaves at the floor.
- R comes from the bottom and leaves through the top, ready for a rooftop extraction fan.
- The two independent dampers keep the four-core positions. Both openings share the corner edge, so a sealing two-plate diverter could return without changing the shell.
- Regeneration is counter-current, P +X and R −X, as D01 assumes [S].

Revision 2 of this note put P on the slope and R on the roof at the top corner. That was the wrong way round, and it is corrected here.

## 4. Concept checks [V, `results/cube_concept.json`, `results/skeleton_selfcheck.json`]

Baseline: D = 500 mm, bed pitch 800 mm, R chamber depth S = 300 mm, coil active face Z 300–1300.

**Envelope.** The shell is **1824 (X) × 1620 (Y) × 1520 (Z) mm**, and all damper bodies are inside it. Actuators are not included. For comparison, C07 is 1750 × 2156 × 2762 mm.

**Fit.** The two detailed 549-solid C05 coils have **zero intersections**:
- The slopes meet the coil frame lands at the apex lines; that is the seal line.
- The P dampers clear the coil by 79 mm and the R dampers by 386 mm.
- The water bay sits in the upper rear dead space, 370 mm from the coil.

**Skeleton self-check.** 32 solids, with no intersections other than the four intended R-damper openings in the slopes.

**Velocities.**
- Mouth: P at 4870 m³/h runs at 4.42 m/s (q 11.5 Pa); R at 2435 m³/h at 2.21 m/s.
- R chamber at the corner: 0.184 m², giving 3.7 m/s.
- The R damper bodies are 141 mm from the skins.

**Face distribution** [V, `results/zflow.json`]. The 1-D Z-manifold header model uses k_d 0.6–1.0, k_c 1.8–2.2, wall friction, and a coil of 60 Pa at 2.21 m/s.

| D = 0.5 m | Process: min–max of mean, CV | Regeneration |
|---|---|---|
| Wedge closing **on the coil land** | 0.958–1.126, 1.1–1.9% | 0.978–1.089, 0.8–1.3% |
| Wedge 10 mm short of the land | 0.788–1.179, 5.2–6.8% | CV 3.4–4.5% |
| Constant-depth plenum | 0.820–1.246, 9.5–12.5% | — |

At D = 0.6–0.7 m the wedge-to-land case improves to a CV of 0.4–1.3%. The four-core wedges had apex gaps of 31 mm (upper) and 59 mm (lower) [V]. The model says those gaps cost several percent of CV, so **closing the wedge onto the coil land is a hard detail requirement**.

**Inlet jets.**
- **P** enters through the top end face, along the plenum axis, so its jet is benign.
- **R** enters through the rear slope, with its jet aimed at the coil and downward at about 6 m/s through the 630 × 180 opening. This is the one sensitive inlet, and the header model does not resolve it (of order 5–15% at the bottom bands [E]).
- The collector outlets (R through the front slope, P through the floor) are insensitive.

**G0′** is therefore one test: the R slope inlet discharging into a full-width wedge. If needed, a turning-vane cassette fits in the R damper's inner flange.

**Path loss** [E, `results/cube_screens.json`]. The process path is **102–166 Pa** including both dampers, against 233–315 Pa for the selector-box path on the same basis. That saves 67–212 Pa, or about **0.15–0.5 kW of fan shaft power** per running fan.

**Size trade.**

| Option | Shell X | Distribution | Dihedral |
|---|---|---|---|
| D = 500, S = 300 (baseline) | 1.82 m | Header-model CV ≈ 2% | 63° |
| D = 600, S = 300 | 2.02 m | Better | 59° |
| D = 500, S = 300, with a slim (≤ 60 mm) R damper like the four-core blades | 1.72 m (S ≈ 200 mm) | Same as baseline | 63° |

## 5. Owner decisions still open

1. **Damper end housings (topology-independent).** Each damper's shaft runs along Y. Bed A's and bed B's dampers sit at identical positions, so side-by-side 706 mm dampers leave 94 mm between beds at an 800 mm pitch, while two inboard R21/D01 feedback ends need 434 mm [V, RT1 D1]. The four-core reference solves this with shared corner hardware between the beds (Y −33 to +18). Options:
   - **(a) recommended:** a single-ended damper, with drive and feedback at the outboard end;
   - (b) rotate bed B by 180°, which conflicts with same-orientation water;
   - (c) a pitch of ≥ 1140 mm, which ends the cube.
2. **Damper orientation.** The P dampers lie flat with vertical flow. The R dampers are inclined 63° from horizontal. All shafts stay horizontal. The R21 P cold test already used vertical P flow (O1′) [S], but D01 is qualified for horizontal flow. Confirm the wet bay, film retention and drainage for each position.
3. **Weather and water.**
   - The roof P intake needs a hood and mist eliminator.
   - The floor R intake and the floor P outlet need under-unit clearance or a plinth with separated openings.
   - Drain the front plenum's apex trough at the coil bottom land, and the floor ahead of the P-out damper.
   - The C05 tray stays.
4. **Fans.** A rooftop R exhaust fan (draw-through) and a P fan blowing through at the roof intake give the pressure hierarchy P > ambient > R. Tracer-test the cross-leak through the closed damper at each corner.
5. **Coil service.** Lateral ±Y withdrawal, as in C07. Neither the R chambers nor the dead spaces are in the coil's path, but the cube has not been swept.

## 6. Carry-over

| Keep | Drop |
|---|---|
| M101 C05 coil, tray, vents and the signed W1→W2 function table | Selector boxes, 8-channel guide stacks, 32 plates, slots and keepers |
| The seal approach: stiff carrier, gasket on the 20 mm lands, closed force loop, plus RT3 D1–D3 | The plinth and the 2.76 m height; stacked P/R ports on one box face |
| HYD-R2 eight-valve bay in the upper rear dead space (shorter spools) | C06/C07 discharge sleeves and the inner rear damper bay |
| D01 dampers at the four-core corner positions (subject to §5.1–5.2), with point bearings re-laid for flat (P) and 63° slope (R) mounting | Plate-jet face probes; the C07 R-vane bosses (replaced by an optional vane cassette on the R slope inlet) |
| The C1–C8 test logic, bed A first, regeneration first | RT1's G0 (replaced by G0′ on the R slope inlet) |

## 7. Next steps

1. **Shell2.** Issue C08 on this topology, with D, S, the pitch, the apex detail, the chamber partitions and the dead-space allocation.
2. **Damper owner.** Decide §5.1 and §5.2.
3. **G0′.** Mock-up or CFD of the R slope inlet into a full-width wedge, with the C05 coil as a porous zone. Accept on the C3 gate.
4. **Hydronics and HX.** Re-route the four spools in the rear dead space, and check the vent high points.

## 8. Reproduction (CadQuery 2.8)

```sh
python tools/read_4core.py ../../../../references/four-core-outdoor/V050_SM_M2_IN1_R1_OUTDOOR_SHEET_METAL_ONLY.stp results/four_core.json
python tools/zflow_manifold.py results/zflow.json
python tools/cube_concept.py <M101_D952_P254_220_39x6_C05.step> results 500 800 300
python tools/skeleton_selfcheck.py results/CUBE_CONCEPT_SKELETON.step results/skeleton_selfcheck.json
python tools/cube_screens.py results/cube_concept.json results/cube_screens.json
python tools/figure_cube.py results/cube_concept.json results/zflow.json results/four_core.json fig_cube.png
```

The C05 STEP is the gzip member of `HX/M101_D952_P254_220_39x6_C05/M101_C05_RT2_CAD.zip`. Adding `--step` to `cube_concept.py` writes the 860 MB version that includes both coils; it is not committed.
