# Failed equal-radius fishmouth iteration

This assembly had valid-looking branch shapes but the equal-radius Boolean fishmouth cut removed no material. The exported lower joints exposed approximately 97 mm3 of unintended overlap each. The design-space Boolean had missed it; that apparent pass was insufficient.

The final source uses a radius 9.15 mm fishmouth, an explicit 0.15 mm weld root gap and a D16.2 opening. It asserts actual fishmouth material removal. `evidence/trap_joint_export_check.json` verifies all four final joints before and after STEP export. Welding, bore finish and leakage remain qualification requirements.

These files preserve the failed iteration and diagnosis. Only unchanged non-Shell group checks may be reused, with exact source STEP SHA256 comparison and fresh assembly readback recorded in the final reports. Shell checks from this folder are superseded and cannot establish final acceptance.
