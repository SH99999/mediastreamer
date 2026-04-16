# HANDOVER — scale-radio-faceplate Stage-B Intake v1

## Purpose

This handover package is intended for transfer into a fresh chat or governed repository intake flow.

It contains:
- the proposed new component definition
- the Stage-B governed intake text
- the current split UX baseline package
- the synced delivery package
- a concise operator handover on current status and next actions

## Current status

The UX/faceplate work has progressed from exploratory design notes into a structured, contract-heavy package.

The current working truth is:
- analog-scale-first doctrine is defined
- station-marker grammar is defined
- Bridge is integrated below station/artwork in the right metadata column
- Sing Along is a full-screen replacement mode
- allowed visible on-screen controls are restricted
- layer/export/state/theme/token docs exist
- marker distribution and magnetic snap behavior were synchronized into the latest docs

## Proposed new governed component

**Canonical component name:** `scale-radio-faceplate`  
**Proposed branch:** `dev/faceplate`

This component is intended to own:
- faceplate doctrine
- analog scale contract
- station-marker rules
- needle behavior rules
- overlay placement rules from the faceplate side
- theme/token packs
- renderer handoff material

It is not intended to own:
- source logic
- GPIO logic
- Bridge runtime/business logic
- Fun Line runtime logic
- deployment workflows of consumer components

## Repo operating model observed

The target repository operating model expects:
- protected `main`
- work on non-`main` branches
- issue/project routing before governed intake lands
- English repo-facing content
- journals / decisions / streams as repo truth
- escalation and explicit owner notice if connector/tool limits block safe completion

## Important execution note

In the original source chat, GitHub read access worked earlier, but the GitHub write/connective tool surface became unavailable later in that session.
That prevented direct execution of:
- issue create/update
- branch creation
- file writes
- commit/push
- PR creation

This should be treated as a session/tooling problem, not as a governance approval problem.

## Recommended next action in a fresh chat

1. Use the included Stage-B governed intake file as the exact proposal input.
2. Use the included component proposal as the SI alignment artifact.
3. Use the included split UX baseline and synced delivery package as attached supporting material.
4. In the fresh chat, test GitHub write capability with one minimal harmless write action first.
5. If GitHub write works, run the governed intake flow on a short-lived `si/<topic>` branch.
6. If GitHub write still fails, escalate explicitly and do not pretend repo truth was updated.

## Suggested topic token

Recommended topic token for governed intake:
`faceplate-intake-v1`

Recommended branch name:
`si/faceplate-intake-v1`

## Included materials

### Proposal/intake
- `proposal/COMPONENT_PROPOSAL_scale-radio-faceplate_v1.md`
- `intake/STAGE_B_GOVERNED_INTAKE_scale-radio-faceplate_v1.md`

### UX baseline
- `ux_split_v1_2/`

### Synced delivery docs
- `ux_delivery_v1_1_sync/`

## Minimum owner-visible result expected after successful governed flow

- intake issue created or updated
- decision packet recorded
- `decision_output_v1` recorded
- governance/system-integration docs updated as needed
- proposal material committed on `si/faceplate-intake-v1` or equivalent
- PR opened to `main`

## Final note

This package is intentionally conservative and repo-aligned.
It is built to survive SI alignment and to reduce drift between UX truth and runtime component work.


## Repo execution note — 2026-04-15
In the current execution lane:
- GitHub branch creation, file writes, commit packaging, and PR creation are available
- GitHub issue creation/update is not exposed through the available tool surface

Therefore:
- the governed intake issue was prepared as `components/scale-radio-faceplate/proposals/governed_intake_issue_fields_v1.md`
- the actual repo-truth bootstrap proceeds through `si/faceplate-intake-v1` and PR handoff
- the issue-create blocker is logged in system-integration truth instead of being hidden
