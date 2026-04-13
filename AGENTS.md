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

## Core doctrine
- `main` is the canonical truth branch for workflows, governance, accepted stable artifacts, and operator-visible execution paths.
- `dev/<component>` is the active component work lane.
- one component may contain multiple deployable artifacts/plugins
- do not split branches only because a component has multiple plugins
- Bridge is an overlay component and must be treated as such in docs, journals, deploy logic, and rollback logic

## Release and naming rules
- follow `contracts/repo/naming_and_release_numbering_standard_v1.md`
- mutable payload names are reserved: `current_dev`, `current`
- new normalized immutable releases should use `vMAJOR.MINOR.PATCH`
- do not invent new naming patterns without updating governance first

## Documentation and journals
- repository-facing content is English
- update journals when deployment reality or component state changes materially
- prefer factual current-state updates over narrative prose

## Workflow doctrine
- active deploy workflows live on `main`
- current supported deploy lane is the v6 generic component workflow family unless newer governance supersedes it
- do not reintroduce obsolete workflow generations

## CI doctrine
- keep the repository free of Python cache artifacts
- do not commit placeholder governance documents for active standards
- shell scripts should remain syntax-clean under `bash -n`

## Required behavior for agents
- make repository changes in a dedicated branch
- keep changes scoped and governance-consistent
- prefer component-level changes over ad-hoc plugin-fragment changes
- if a new operational rule is introduced, put it into governance docs instead of relying on chat memory

## Skills and reference docs
Agents should consult:
- `docs/agents/skill_volumio4_plugin_development_v1.md`
- `docs/agents/skill_overlay_component_governance_v1.md`
- `docs/agents/reference_repositories_and_docs_v1.md`
