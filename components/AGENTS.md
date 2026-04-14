# AGENTS.md

## Scope
This file applies to everything under `components/`.

## Component development rules
- treat each `components/scale-radio-<component>/` directory as one governed component
- a component may contain multiple artifacts/plugins with different roles
- default artifact roles include `runtime`, `launcher`, `service`, `renderer`, `source_tile`, `bridge`, `ui_entry`, `helper`
- keep artifact role language explicit in docs, deploy candidates, and journals
- `bootstrap new components using contracts/repo/new_component_intake_standard_v2.md before adding payload structure`

## Volumio 4 plugin expectations
- align with Volumio 4 / Bookworm realities
- keep plugin category and runtime role explicit
- document whether an artifact is a Volumio plugin, service, helper script set, renderer, or overlay entry artifact
- when rollback applies to a plugin, document whether Volumio unregistration is required

## Overlay-specific rule
Components that participate in overlay ownership must document:
- what opens the overlay
- what renders the overlay
- whether hidden mode exists
- whether overlay arbitration/ownership files are used
- rollback behavior

## Packaging and releases
- use component-level release numbering by default
- if multiple artifacts move together, they share the component release number
- do not create separate version lines for launcher/runtime pairs unless governance explicitly records that split

## Path discipline
- put payloads under `payload/`
- put deploy scripts under `deploy_candidates/`
- do not scatter active release logic across unrelated directories
