# RELEASE INTAKE AND DELIVERY STATUS V2

## Purpose
This document defines the repository-wide status language for release intake, normalization, deployment readiness, testing, rollback, and promotion to `main`.

## Canonical taxonomy source
Canonical lifecycle statuses are defined in:
- `contracts/repo/status_taxonomy_contract_v1.md`

This document must stay aligned to that source and must not introduce a second conflicting status list.

## Canonical branch doctrine
- `main` = truth for governance, workflows, accepted stable artifacts, and operator-visible execution paths.
- `dev/<component>` = component work lane and payload preparation lane.
- `integration/staging` = integration-owned branch kept aligned to `main` when in active use.
- Active `dev/*` branches should stay at `0 behind main` whenever possible.

## Status vocabulary
Use only canonical values from `status_taxonomy_contract_v1.md` in component current-state journals and release notes.
Legacy vocabulary must be normalized via the migration map from the canonical taxonomy contract.

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

## Historical note
Earlier generations used alternate terms such as `deploy_candidate_started` and `functional_acceptance_pending`.
Those terms are now treated as legacy aliases and must be normalized using the canonical migration map.

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

## Simplified release/rollback rule
Minimum operational model for this repository family:
- `main` is the single accepted software truth branch.
- rollback should use governed Git tags that point to accepted baselines.
- `dev/*` branches are for in-progress work only and should not be treated as a second truth line.

If a component no longer depends on payload-folder pointer switching, tag-based rollback is the preferred mechanism.

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
