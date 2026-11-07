# Superseded development evidence

These files explain earlier findings and design iterations. They are not acceptance evidence for the delivered C11 assembly. The current assembly SHA256 and current source hashes in the parent evidence directory control review.

- `raw_pre_fix`: raw pre-normalization assembly and earlier Shell checks.
- `early_500kg_frame`: obsolete coarse frame model using the earlier 500 kg host assumption. Current calculations use the documented 1,000 kg host cap and meshes 24 / 48.
- `superseded_reference_checks/shell_external_design_check.json`: an earlier C10-based external check, superseded by the complete C11 cross-group checks.
- `superseded_reference_checks/invalid_solid_diagnostic.json`: investigation of original OEM valve STEP solids before dimension/volume-preserving export normalization.
- `superseded_reference_checks/mass_cap_audit.json`: preliminary owner-input mass bound, superseded by the final installed mass audit.
- `superseded_reference_checks/development_service_subset.json`: mixed-source development check. Only the final `evidence/service_subset.json` with the delivered S1 SHA applies to this version.
- `pre_fishmouth_fix`: failed equal-radius drain-branch cut, diagnosis and corrected-cut prototypes. Current exported-joint evidence is required.
- `pre_clamp_motion_fix`: rejected upper-frame ties that collided during continuous damper motion despite clear static endpoints.
- `pre_jaw_edge_clearance_fix`: the 40 mm jaw edge touched a condensate rail without positive overlap volume. The final 39 mm jaw trims 1 mm from that edge; the final distance check must confirm the gap.
- `rebuild_source_snapshots`: source and index snapshots from superseded task-owned temporary rebuilds, preserved before duplicate CAD/input copies were removed to reclaim local disk space.

Unresolved findings remain unresolved unless the final evidence explicitly demonstrates closure. Preserving an earlier failed or passed check does not transfer its result to a changed assembly.
