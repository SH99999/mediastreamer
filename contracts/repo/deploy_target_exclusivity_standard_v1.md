# DEPLOY TARGET EXCLUSIVITY STANDARD V1

## Purpose
This document defines the mandatory exclusivity rules for deploying, testing, accepting, and rolling back component candidates on a target Pi.

## Leading rule
One target Pi may have only one active deploy/test slot at a time.

No other branch, workflow, chat, or agent may deploy to the same target while that slot is occupied.

## Why this exists
Without exclusivity:
- one candidate can overwrite another during a test window
- test observations become invalid
- rollback anchors become ambiguous
- owner review load increases because runtime truth becomes unclear

## Target status model
Each governed target Pi uses one of these statuses:
- `free`
- `deploying`
- `test_open`
- `rollback_running`
- `blocked`

## Status meaning
### `free`
The target is available for a new deploy/test run.

### `deploying`
A workflow has acquired the target and is actively deploying.
No other deploy or rollback may begin.

### `test_open`
A deploy finished and the target is reserved for validation of that candidate.
No other deploy may begin until the slot is released, rolled back, or times out.

### `rollback_running`
A rollback is actively in progress.
No other deploy or rollback may begin.

### `blocked`
The target is in a manual-attention state because deploy, rollback, or lock handling did not complete cleanly.
No other deploy may begin until the block is explicitly resolved.

## Lock ownership rule
A deploy/test slot records at least:
- target identifier
- component
- git ref
- payload
- state
- workflow/run owner marker
- acquired timestamp
- lease expiry when applicable

## Timeout rule
`deploying` and `test_open` may carry a lease timeout.
If the timeout expires, a later workflow may reclaim the slot.

Timeout is a recovery aid, not the preferred normal path.
Normal completion should release the slot explicitly.

## Allowed transitions
- `free` -> `deploying`
- `deploying` -> `test_open`
- `deploying` -> `blocked`
- `test_open` -> `rollback_running`
- `test_open` -> `free`
- `rollback_running` -> `free`
- `rollback_running` -> `blocked`
- `blocked` -> `rollback_running`
- `blocked` -> `free` only through explicit governed release or recovery

## Required workflow behavior
### Deploy workflow
A deploy workflow must:
1. acquire the target slot before touching runtime state
2. fail fast if the target is not `free` or safely reclaimable by timeout
3. set the target to `deploying`
4. set the target to `test_open` on successful deploy
5. release or block the slot explicitly on failure

### Rollback workflow
A rollback workflow must:
1. acquire the slot only from a compatible occupied state such as `test_open` or `blocked`
2. set the target to `rollback_running`
3. release the slot to `free` on successful rollback
4. set the target to `blocked` on rollback failure

### Test completion / acceptance release
A governed release step must exist so the active test slot can be returned to `free` after:
- acceptance of the tested candidate
- explicit abandon of the test window
- a governed manual release after inspection

## Safety rule
If the workflow cannot safely determine or mutate the target slot state:
- do not deploy anyway
- do not silently overwrite another active test window
- escalate and inform

## Starter exception
Starter remains a separate normalization case.
This contract governs target exclusivity and test integrity; it does not by itself make Starter deploy-ready.

## Relation to stable/rollback baselines
For non-Starter components:
- repo truth is the leading truth before first real target deployment
- a new stable/rollback anchor is declared only after branch deploy, target validation, and owner acceptance

## What not to do
- do not run parallel deploys on the same target
- do not overwrite an occupied test window silently
- do not treat a technically dispatchable workflow as permission to deploy when the target is reserved
