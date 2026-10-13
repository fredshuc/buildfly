# C02 R21: RT-2 independent review

- `RT2_REVIEW.md` is the review. It opens with the conclusion, then:
  - what was verified, and the L1 corrections carried forward from RT-1;
  - answers to RT2-01 … RT2-10, each with exact PN/instance, source, counterexample, smallest change, acceptance and class;
  - an ordered manufacturing-acceleration plan, and the limits of the review.
- `RT2_FINDINGS.csv` has one row per finding. The Tag column marks each row as V (computed here), I (inference) or R (recommendation).
- `tools/` holds the scripts. To rerun: `tools/run_r21.sh <AT_DMP_R21_RT2_COMPLETE_PART_1_OF_2.zip> <..._PART_2_OF_2.zip> [workdir] [resultsdir]`, using the environment in `tools/requirements.txt`.
  - The script verifies the 815-entry manifest and regenerates `results/`. A full rerun reproduced every file byte for byte, apart from the `seconds` timing field in `results_r21_check.json`.
  - It reads the package as data and executes no project script.
  - It takes about 20 minutes on one core.
- `results/` contains:
  - the interference and motion check;
  - the BOM audit and fastener designation map;
  - the film keeper, clearance and protrusion studies;
  - the feedback-root contact graph;
  - the drive-line order along the shaft axis;
  - the stop and gear budget.

The input zips are in [`../c02-r21/`](../c02-r21/). Their SHA-256 values are `a1a2008459f7cf0b0ac587a507f20b2f2d7c7305618f7614345cca0e2c7b213d` (part 1) and `a3381aff73156dcdc48975d7b018279b2f099ad5fabec36ae259d5d456cb5b36` (part 2).
