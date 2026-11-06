# C09 four-core AirTransformer integration

On GitHub, extract C09_CAD_REVIEW.zip at repository root to obtain the expanded files. For the full water reference, also extract C09_HYDRONICS.zip from hydronics/four-core-series.

Start with `cad/C09_INSTALLED_S1.step` for bed A in process and bed B in regeneration. Open `cad/C09_INSTALLED_S2.step` independently for the opposite states. Each exchange contains one shell, four complete unhanded heat exchangers and the four installed D03 selectors. Use `cad/C09_SHELL.step` for coordination without dampers or coils. The physical valve island, connection spools and actuator bodies on the water circuit are pending. See the mode-specific connection register in `hydronics/four-core-series/`.

## Rebuild from a checkout

Use Python 3.12, CadQuery 2.8, OCP 7.9 and NumPy. Set `CADQUERY_LIBDIRS` to an existing compatible installation if necessary. From the repository root, run the following commands. All paths and coordinates refer to the four-core global millimetre frame.

```sh
python AirTransformerShell/revisions/C09/build_c09.py
python AirTransformerShell/revisions/C09/verify_c09.py
python AirTransformerShell/revisions/C09/verify_sections.py
python AirTransformerShell/revisions/C09/plot_section.py
```

The builder pins the historical outdoor-sheet and D03 file checksums, takes actual D03 product leaves from each delivered state, and suppresses D03's copy of the reference host. The four-core HX input retains its shared product definition, including 549 occurrences at each of four placements. When comparing a rebuilt STEP, use occurrence identity, geometry, source hashes and the fit tests. STEP headers may carry different dates.

Read `RED_TEAM_HANDOFF_EN.md` and the two independent reviews for dispositions. `development_pass1/` retains the first export's evidence. Use `evidence/` for the delivered geometry.
