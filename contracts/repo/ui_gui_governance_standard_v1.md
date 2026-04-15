# UI GUI GOVERNANCE STANDARD V1

## Purpose
This standard ensures UI/GUI work is governed under the same repository model as runtime and deploy work.

## Leading rule
UI/GUI is not an exception lane.
UI/GUI changes must follow the same branch, PR, release, journal, rollback, and governance routing rules as all other component artifacts.

## Boundaries and non-goals
### In scope
- governance rules for UI/GUI artifacts and overlays
- release/deploy/rollback governance implications for UI/GUI artifacts
- issue-routing and escalation behavior for UI/GUI work

### Out of scope
- component-specific implementation details that belong in component payload docs
- replacing component runtime journals with SI-level UI notes

## Scope
Applies to:
- overlays
- renderer artifacts
- `ui_entry` artifacts
- source tiles and visual navigation entries
- UI assets tied to deployable component payloads

## Transitional integration rule
- the current GUI concept is sufficient until full integration is explicitly started and approved through SI/governance.
- until that point, UI/GUI work is treated as stabilization and governance consistency work, not as a redesign program.

## Governance requirements
- UI/GUI changes must happen on non-`main` branches
- UI/GUI changes promote through PR into protected `main` after owner coordination
- UI/GUI changes must update component journals when operational reality changes
- UI/GUI issue intake and escalation must use the same governed issue-routing model
- cross-component UI/GUI governance decisions must be logged in `journals/system-integration-normalization/ui_gui_stream_v1.md`

## Artifact-role expectations
When relevant, docs and manifests should explicitly mark role names such as:
- `<component>:ui_entry`
- `<component>:renderer`
- `<component>:source_tile`
- `<component>:bridge`

## Deploy and rollback expectations
If UI/GUI artifacts are deployed with runtime artifacts:
- rollout and rollback behavior must be explicit in component current-state
- overlay ownership/hidden-mode behavior must be documented where applicable
- unregistration behavior must be documented when applicable to Volumio plugins

## Release and path consistency
- UI/GUI artifacts must follow the same naming and release numbering standards
- payload paths remain under the governed component payload tree
- UI-only work must not bypass component-level release governance
