# HYD3 F02 water-only interfaces: RT-01 addendum

- `F02_REVIEW.md` checks the 2026-10-17 F02 STEP against C05 R1. It gives:
  - the verdict;
  - the contents;
  - hydraulic, fabricability, connectivity, internal and host checks;
  - the corrections needed before the file goes to a supplier;
  - the recommended integrator package.
- `tools/run_f02.sh <F02.stp> <extracted C05 RT01 package>` reproduces `results/`. It reuses `../c05-rt01/tools`.
- `TREND_v0498B_C05_F02.md` compares v0498B (C4, 2026-09-02) → C05 R1 → F02 on the same DFM measures. It also documents the HX port relocation that explains C05's complexity. Pass the v0498B STEP as the 4th argument of `run_f02.sh` to reproduce it.
