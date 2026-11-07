# AirTransformerShell scope

- Store L2-MI shell2 work in fredshuc/buildfly/AirTransformerShell/.
- This folder covers the atmospheric AirTransformer drying-module assembly. The accepted C10 basis is two beds with two horizontal H01 cores per bed (four cores total). Do not merge shell1 FA01 vessel work into it.
- Preserve delivered revisions. Place new CAD revisions under revisions/<revision>/.
- Track editable sources, interfaces, review documents and verification evidence. Keep complete CAD/native/input files in a named package when not expanded.
- Preserve existing damper and hydronics work elsewhere in the repository.
- Read the current HX interface before changing shell ports. For the C11 task scope use HX/M101_C08_HORIZONTAL_H01 and the C10 installed assembly. Do not treat C02's Z-stagger, B-core rotation or W1/W2 swap as the next interface baseline.
- Keep the HYD-S2 series circuit with eight two-way selector valves, one FS/Q pair per bed and two common-return TA-Smart valves. Cold flow enters lower W1; hot flow enters upper W2. This supersedes the historical four-three-way-valve note. Weight optimization is paused unless the owner reopens it.
- Exclude temporary transfer payloads, tool logs, runtime dependencies, credentials and unrelated local files.
- Preserve all unrelated remote commits. Use ordinary commits and guarded fast-forward updates; do not force-push.
- C11 planning and L2 tasks are under revisions/C11/L1_TASKS/. C11 CAD is not issued by the task-document commit; preserve C10 and RT5 evidence.
- A design geometry commit is not a manufacturing release. State the actual validation scope in the revision notes.

