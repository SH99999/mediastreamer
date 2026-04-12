# RELEASE INTAKE AND DELIVERY STATUS V2

## Purpose
This document defines the repository-wide status language for release intake, normalization, deployment readiness, testing, rollback, and promotion to `main`.

## Canonical branch doctrine
- `main` = truth for governance, workflows, accepted stable artifacts, and operator-visible execution paths.
- `dev/<component>` = component work lane and payload preparation lane.
- `integration/staging` = integration-owned branch kept aligned to `main` when in active use.
- Active `dev/*` branches should stay at `0 behind main` whenever possible.

## Status vocabulary
Use only these primary status values in component current-state journals and release notes.

### `raw_intake_started`
Release material entered the repository and the target branch/path is known.

### `payload_partial`
Payload tree exists but completeness or correctness is not yet trusted.

### `payload_complete`
Expected payload structure is present and core runtime files are in place.

### `deployment_candidate_started`
Deploy, healthcheck, and rollback scripts exist or are actively being prepared.

### `deploy_ready`
The repository-driven workflow can install and remove the payload using clean-replace semantics.

### `tested_on_pi`
Deploy and/or rollback ran on a real Pi through the active workflow lane.

### `functional_acceptance_open`
Deployment path works, but component-level feature acceptance is still open.

### `accepted_for_main`
The payload is stable enough to be treated as current truth on `main`.

### `rolled_back`
The active deployment was removed, unregistered when applicable, and Volumio recovery was verified.

## Required fields in every component current-state journal
- component name
- repo path
- active branch
- accepted payload name, if any
- current lifecycle status values
- last deploy workflow used
- last rollback workflow used
- last known runtime result
- next recommended action

## Promotion rule
A component may be promoted to `main` only when:
1. payload is complete
2. repo-driven deploy works
3. repo-driven rollback works
4. current-state journal is updated
5. intended stability level is explicit

## Current rollout order
1. bridge
2. tuner
3. starter
4. autoswitch
5. fun-line
6. hardware

Bridge and tuner are the current highest-priority production-facing lanes.
This contract defines how a component release moves from raw intake to deployable and eventually to stable truth.

## Status levels
- `placeholder`: reserved path only, no usable release content
- `raw_intake_started`: extracted or imported files are being brought into Git
- `payload_present`: payload tree exists in the correct component path
- `deploy_candidate_started`: deploy candidate scripts exist
- `deploy_ready`: deploy and rollback workflows are usable against the component
- `functional_acceptance_pending`: deploy lane works but functional validation is incomplete
- `accepted_for_main`: release is accepted as current truth on `main`
- `superseded`: older release retained for history only

## Required release contents
A release is not considered real unless it contains:
- extracted payload tree under `components/<component>/payload/<release_name>/`
- install path logic
- rollback logic
- healthcheck logic
- current branch/ref placement decision

## Placement rule
- stable/current truth may live on `main`
- evolving or not-yet-accepted work lives on `dev/<component>`

## Current rollout order
1. bridge and tuner first
2. autoswitch, starter, fun-line, hardware staged behind them

## Current known accepted truths
- workflows and governance/control-plane live on `main`
- Bridge deploy lane is repo-driven and selectable by `git_ref` and `payload`
- tuner is treated as main-truth payload

## Required release handoff fields
Every release handoff should state:
- component
- branch/ref
- payload path
- current status level
- what was tested
- what remains open
- rollback expectations
