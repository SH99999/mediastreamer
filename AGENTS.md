# AGENTS.md

## Purpose
This file provides repository-wide operating instructions for coding agents working in this repo.

## Read first
Before touching files, read these governance documents on `main`:
- `contracts/repo/branch_strategy_v2.md`
- `contracts/repo/component_artifact_model_v1.md`
- `contracts/repo/naming_and_release_numbering_standard_v1.md`
- `contracts/repo/release_intake_and_delivery_status_v2.md`
- `contracts/repo/component_journal_policy_v2.md`
- `contracts/repo/repository_language_standard_v2.md`
- `contracts/repo/system_integration_governance_index_v5.md`
- `contracts/repo/new_component_intake_standard_v2.md`
- `contracts/repo/protected_main_truth_maintenance_operating_model_v1.md`
- `docs/agents/system_integration_recovery_onboarding_v5.md`

## Core doctrine
- `main` is the canonical protected truth branch for workflows, governance, accepted stable artifacts, and operator-visible execution paths.
- the repository remains public until further notice.
- `dev/<component>` is the active component work lane.
- `integration/staging` is an exception-only temporary integration-owned branch and not a second truth branch.
- one component may contain multiple deployable artifacts/plugins.
- do not split branches only because a component has multiple plugins.
- Bridge is an overlay component and must be treated as such in docs, journals, deploy logic, and rollback logic.

## Release and naming rules
- follow `contracts/repo/naming_and_release_numbering_standard_v1.md`
- mutable payload names are reserved: `current_dev`, `current`
- new normalized immutable releases should use `vMAJOR.MINOR.PATCH`
- do not invent new naming patterns without updating governance first

## Documentation and journals
- repository-facing content is English
- journals, decisions, and streams are mandatory repo truth
- update journals when deployment reality or component state changes materially
- prefer factual current-state updates over narrative prose

## Workflow doctrine
- active deploy workflows live on `main`
- current supported deploy lane is the v6 generic component workflow family unless newer governance supersedes it
- do not reintroduce obsolete workflow generations
- system integration should use short-lived repo-control-plane branches to `main` by default

## CI doctrine
- keep the repository free of Python cache artifacts
- do not commit placeholder governance documents for active standards
- shell scripts should remain syntax-clean under `bash -n`

## Required behavior for agents
- make repository changes in a dedicated non-`main` branch
- keep changes scoped and governance-consistent
- prefer component-level changes over ad-hoc plugin-fragment changes
- if a new operational rule is introduced, put it into governance docs instead of relying on chat memory
- bootstrap new components using `contracts/repo/new_component_intake_standard_v2.md`
- if tooling, connector, access, or execution problems block safe completion, escalate and inform instead of improvising, faking completion, or silently creating partial truth
- if a protected truth file cannot be safely mutated through the available connector surface, use the controlled replacement-file operating model instead of pretending the direct mutation succeeded

## Skills and reference docs
Agents should consult:
- `docs/agents/skill_volumio4_plugin_development_v1.md`
- `docs/agents/skill_overlay_component_governance_v1.md`
- `docs/agents/reference_repositories_and_docs_v1.md`
- `docs/agents/system_integration_recovery_onboarding_v5.md`
