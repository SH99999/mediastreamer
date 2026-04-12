# COMPONENT JOURNAL POLICY V2

## Purpose
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
