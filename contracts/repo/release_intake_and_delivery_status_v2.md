# RELEASE INTAKE AND DELIVERY STATUS V2

## Purpose
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
