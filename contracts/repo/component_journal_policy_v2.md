# COMPONENT JOURNAL POLICY V2

## Purpose
Component journals are the canonical handoff layer between development, integration, workflows, and operator testing.

## Required journal files per component
Each component should maintain at least:
- `journals/<component>/current_state_v1.md`
- `journals/<component>/stream_v1.md`

## Current-state journal
The current-state journal is a factual snapshot.
It should answer:
- what the component is
- where it lives in the repo
- what currently works
- what is broken
- what branch and payload are active
- what should happen next

Update triggers:
- accepted deploy result
- accepted rollback result
- status promotion or demotion
- branch/path move
- major decision that changes operational reality

## Stream journal
The stream journal is append-only and concise.
It records meaningful events such as:
- payload imported
- workflow tested
- deploy passed
- rollback passed
- runtime bug identified
- branch rebased to current `main`
- accepted payload changed

## Journal quality rules
- factual, not narrative
- English only
- no placeholders after first real work starts
- reflect tested reality, not intention
- each entry should be brief and dated by context if available

## Ownership
- specialist chats provide repo-ready status updates for their component
- integration normalizes status wording and resolves branch/process consistency
- operator runs workflows and verifies runtime results

## Minimum update discipline
Every meaningful deployment cycle should update at least:
- component current state
- component stream

## System integration journal
The integration/system-normalization lane must also maintain its own current-state and decision log because it governs:
- branch discipline
- workflow model
- deployment semantics
- rollback semantics
- repo operating doctrine
Component journals are the repo-side memory for current state and the ongoing change stream.

## Required journal files per component
Each component should maintain at least:
- `journals/<component>/current_state.md`
- `journals/<component>/stream.md`

## Current state file rule
`current_state.md` must contain only the latest factual view:
- what the component is
- branch/ref truth
- payload path truth
- functional status
- deployment status
- locked decisions
- open risks
- next steps

## Stream file rule
`stream.md` is append-only and compact. Each meaningful change should add:
- date/context
- change made
- why it was made
- branch/ref
- impact on deployment or runtime

## Update triggers
Update journals when any of these happens:
- payload imported
- deploy script changed
- workflow behavior changed
- branch placement decision changed
- functional test result changed
- rollback behavior changed

## Ownership rule
- specialist chats may propose journal updates
- integration/system-normalization is responsible for keeping repo journals coherent

## Minimum standard
A placeholder journal is not acceptable once a component has payloads in Git.
