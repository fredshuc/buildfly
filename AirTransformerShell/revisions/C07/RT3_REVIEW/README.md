# C07 RT3 independent red-team review

This review covers the AirTransformer two-bed C07 shell and ducts at frozen commit `2272676`. It checks C07 against the RT2 returns N1–N11, the RT1 cold-flow gates and the internal RT3 review, and gives separate verdicts for prototype detailing, bed-A cold flow, cutting, two-bed manufacture and live water.

- [C07_RT3_REVIEW.md](C07_RT3_REVIEW.md): verdicts, reproduction, N1–N11 dispositions, the service items requested, and the air-path and C1–C8 status.
- [C07_RT3_FINDINGS.csv](C07_RT3_FINDINGS.csv): one row per finding.
- [tools/](tools/): reproducible checks. Start with `run_all.sh`.
- [results/](results/): JSON outputs used in the review.

Status: review only. It changes no delivered file and is not a fabrication release.

**Superseded on 2026-11-06.** The owner reset the module topology, so the C07 detailing verdict is withdrawn. [TOPOLOGY_RESET/](TOPOLOGY_RESET/CUBE_TOPOLOGY_RESET.md) records what the reviews missed and gives the cube Z-flow concept: a vertical coil between two opposed sloped plenums, with a header-model distribution, an envelope check against the detailed C05 coils, path loss, open decisions and the carry-over list.
