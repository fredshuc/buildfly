# AT-HYD3-MFG-C05 R1: RT-01 independent red-team review (hydronics)

- `RT01_REVIEW.md` is the review. It opens with the conclusion, then covers:
  - what was checked;
  - findings RT01-01 … RT01-14, each with object, source, counterexample, smallest change, closure evidence and class;
  - the package worksheet R01–R24;
  - root causes and the minimum next engineering outcome;
  - limits.
- `RT01_FINDINGS.csv` has one row per finding. The Tag column is V (computed here), S (package-stated), I (inference) or R (recommendation).
- `RT01_REVIEW_WORKSHEET.csv` and `RT01_REVIEW_RECEIPT.json` are the package's own worksheet and receipt templates, filled in.
- `results/cad/` holds the CAD improvement: the 30 OD33.7 spools with standard butt-weld elbows replacing 114 of 128 miters. End points are unchanged. The folder has one world BRep per spool and `RT01_REVISED_DN25_SPOOLS_AP242.step` (30 named products).
- `tools/` holds the scripts. To rerun: `tools/run_rt01.sh ../RT01_review [workdir]`, using the environment in `tools/requirements.txt` (Python 3.13, cadquery-ocp 8.0.1, CoolProp).
  - The script joins and hash-checks the split ZIP, verifies the manifest and regenerates `results/`.
  - It reads the package as data and executes no package script.
  - The Boolean-heavy steps take about 50 minutes on one core.

Input: [`../RT01_review/`](../RT01_review/). The joined ZIP SHA-256 is `0e931351b87aeabf54ee12f92433c28dfd499534a339a304bea17c69134647af`.
