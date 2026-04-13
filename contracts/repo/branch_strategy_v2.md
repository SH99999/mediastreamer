# BRANCH STRATEGY V2

Status: canonical branch doctrine for repository operation.

## Leading rule
The branch follows the **component lifecycle**, not the individual plugin count.

A component may contain multiple deployable artifacts or plugins.
That does **not** automatically justify separate branches.

## Canonical branch doctrine
- `main` = truth for workflows, governance, accepted stable artifacts, and operator-visible execution paths.
- `dev/<component>` = active component work lane.
- `integration/staging` = optional integration-owned temporary branch kept aligned to `main` when actively used.

`integration/staging` is **not** a second truth branch.

## Persistent branches
- `main`
- `integration/staging`
- `dev/tuner`
- `dev/bridge`
- `dev/autoswitch`
- `dev/fun-line`
- `dev/starter`
- `dev/hardware`

## Branch ownership
### main
- protected truth branch
- workflows live here
- governance lives here
- accepted stable artifacts live here
- no uncontrolled direct development

### integration/staging
- owned by system integration / normalization
- used for temporary integration packaging, repo-control-plane work, contract alignment, and staging-only integration blocks
- should be reset or realigned to current `main` when reused

### dev/<component>
- owned by the relevant specialist lane for that component
- contains evolving payloads, deploy candidates, docs, and journals for that component
- should stay at `0 behind main` whenever practical

## One component, multiple artifacts
A component may ship multiple deployable artifacts with different roles, for example:
- `runtime`
- `launcher`
- `service`
- `renderer`
- `source_tile`
- `bridge`
- `ui_entry`

These artifacts normally stay on the **same component branch**.

## When to split into separate branches
Split only when the artifacts have materially different:
- owners
- rollout cadence
- rollback semantics
- acceptance path
- deployment contract

If those conditions are not true, keep one branch and document multiple artifact roles inside the component.

## Bridge-specific note
Bridge is an overlay component.
Its governance must explicitly describe:
- overlay ownership / arbitration behavior
- interaction with other overlays
- launcher/open-entry artifact if present
- runtime overlay artifact if present
- rollback and Volumio unregistration behavior where applicable

## Promotion rule
Promotion to `main` happens by component block, not by arbitrary single plugin fragment, unless governance explicitly documents an exception.
