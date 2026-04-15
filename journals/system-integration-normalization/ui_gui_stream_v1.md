# STREAM — ui_gui_governance (system-integration)

Status note: this v1 file is the dedicated SI stream for cross-component UI/GUI governance work and dependencies.

## Scope boundary
This stream tracks only governance/control-plane reality for UI/GUI work:
- standards
- dependencies
- issue-routing rules
- deployment/rollback governance implications

It does not replace component-local runtime journals.

## Dependency anchors
- `contracts/repo/ui_gui_governance_standard_v1.md`
- `contracts/repo/deploy_process_standard_v1.md`
- `contracts/repo/component_artifact_model_v1.md`
- `contracts/repo/issue_governance_routing_standard_v1.md`
- `contracts/repo/system_integration_governance_index_v7.md`

## Entries
- 2026-04-15: Stream bootstrapped as the dedicated SI truth lane for UI/GUI governance and dependency tracking.
- 2026-04-15: Initial dependency anchors linked so UI/GUI decisions can be traced to deploy, artifact-role, and issue-routing doctrine.
- 2026-04-15: Rule recorded that UI/GUI governance entries here must be mirrored by component journals when runtime/deploy behavior changes in a component.
- 2026-04-15: Transitional decision recorded that the current GUI concept is sufficient until full integration is explicitly opened under SI governance.
- 2026-04-15: Stage-B autonomy contract added for UI/UX proposal-reference intake and owner `decision_output_v1` packet output.
- 2026-04-15: Project-view blueprint path added (`tools/governance/scale_radio_governance_delivery_views_v1.md`) for owner decision readiness in `Scale Radio Governance & Delivery`.
- 2026-04-15: Table and kanban markdown renderings added for project-view blueprint to improve owner-facing review in Git (`..._views_table_v1.md`, `..._views_kanban_v1.md`).
- 2026-04-15: Project-view triage definition was generalized to component-wide intake routing; UI/GUI remains in-scope via `agent:ux` and no longer assumes UI-only queue boundaries.
