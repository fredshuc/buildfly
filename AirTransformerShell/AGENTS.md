# AirTransformerShell scope

- Store L2-MI shell2 work in fredshuc/buildfly/AirTransformerShell/.
- This folder covers the atmospheric AirTransformer two-core shell. Do not merge shell1 FA01 vessel work into it.
- Preserve delivered revisions. Place new CAD revisions under revisions/<revision>/.
- Track editable sources, interfaces, review documents and verification evidence. Keep complete CAD/native/input files in a named package when not expanded.
- Preserve existing damper and hydronics work elsewhere in the repository.
- Read the current HX interface before changing shell ports. Do not treat C02's Z-stagger, B-core rotation or W1/W2 swap as the next interface baseline.
- Keep the four-three-way-valve architecture. Weight optimization is paused unless the owner reopens it.
- Exclude temporary transfer payloads, tool logs, runtime dependencies, credentials and unrelated local files.
- Preserve all unrelated remote commits. Use ordinary commits and guarded fast-forward updates; do not force-push.
- A design geometry commit is not a manufacturing release. State the actual validation scope in the revision notes.
