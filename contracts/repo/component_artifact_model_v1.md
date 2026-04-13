# COMPONENT ARTIFACT MODEL V1

## Purpose
This contract defines how one repository component may contain multiple deployable artifacts, plugins, or helper units without fragmenting governance or branch doctrine.

## Leading rule
A **component** is the functional delivery unit.
An **artifact** is one deployable or runtime piece inside that component.

Governance, branch ownership, rollout state, and journals default to the **component** level.

## Artifact roles
A component may contain one or more artifacts with explicit roles, for example:
- `runtime`
- `launcher`
- `service`
- `renderer`
- `source_tile`
- `bridge`
- `ui_entry`
- `helper`

## Required artifact fields
Each component should eventually document, for every artifact:
- artifact name
- artifact role
- implementation type
- whether it is a Volumio plugin, service, script set, or helper asset
- whether it is user-visible
- whether it is required for deployment success
- whether rollback must unregister it from Volumio

## Default rule for two-plugin patterns
If a component contains:
- one plugin/artifact with the effective runtime logic, and
- one plugin/artifact that exposes the icon, button, source tile, or overlay entry,
then both artifacts still belong to the **same component** unless explicitly split by governance.

## Branch rule
One component normally uses one branch:
- `dev/<component>` for evolving work
- `main` for accepted truth

Do not create separate branches only because the component has multiple plugins.

## Release rule
Multiple artifacts that belong to one component should normally move together under one component release number.
Only split release numbers when governance explicitly records that the artifacts are independently versioned.

## Bridge overlay rule
Bridge must be treated as a multi-artifact overlay component when applicable.
Typical Bridge artifacts may include:
- runtime overlay artifact
- launcher or open-entry artifact
- optional helper/runtime coordination files

Bridge component docs and journals should record:
- overlay ownership semantics
- interaction with other overlay screens
- what opens the overlay
- what actually renders or maintains the overlay
- rollback and unregistration requirements

## Documentation rule
Component journals remain at the component level, but they should mention artifact roles whenever those roles matter for deployment, rollback, acceptance, or user-visible behavior.
