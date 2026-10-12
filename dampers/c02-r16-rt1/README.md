# C02 R16: RT-1 independent review

- `RT1_REVIEW.md` is the review. It opens with the conclusion, then gives answers to the eight RT-1 questions (exact PN/instance, source, counterexample, smallest change, acceptance), proposed release waves and confidence.
- `RT1_FINDINGS.csv` has one row per finding, in the RT-1 return format.
- `tools/` holds the scripts. To rerun: `tools/run_r16.sh <AT_DMP02_C02_R16_FULL_INTEGRATION_RT1_20261012.zip> [workdir]`, with the Python environment from `tools/requirements.txt`. The script verifies the 209-entry manifest and regenerates `results/` byte for byte. The package is read as data; no project script is executed.
- `results/` contains the ECO Boolean studies, masses/CG and the proposed release waves.

The input package is not stored here. Its SHA-256 is `cbfe74c5b1b18c1617e2fe116691417c75029354d77d5ecaa82c368060086c8a` (26,361,962 bytes).
