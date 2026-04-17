# SI CODEX HANDOVER — Target Operating Model v2
_Date: 2026-04-17_

## 1. Purpose
This v2 model prepares a **cleaned operating baseline** for faster delivery without losing critical governance integrity.

This is not a reset/rewrite. It is a selective retention model:
- keep only operationally necessary knowledge
- preserve auditable repo truth
- reduce historical/control-plane noise in active startup and execution

---

## 2. What must be preserved (non-negotiable)
Only these knowledge classes are required in active operation:

1. **Component execution truth**
   - current component status
   - current deploy/rollback constraints
   - current supported delivery matrix posture

2. **Repo truth / process truth**
   - protected `main` and branch doctrine
   - active canonical contracts/standards
   - current SI status/decisions/active stream

3. **Governance runtime model**
   - agent roles and availability
   - owner decision contract (`one-click` decision marker)
   - SI orchestration/dependency ownership

4. **Execution continuity truth**
   - governed demand/protocol/session artifacts for active work
   - explicit backlog capture for non-immediate ideas/demands

Anything outside these classes is deep-history or derived surface by default.

---

## 3. Cleanout doctrine (what to remove from active path)
The active path must exclude:
- superseded/redundant narrative restatements
- parallel summary layers that do not add enforcement value
- historical stream generations from startup requirements
- inactive/duplicate prompt surfaces not needed for current execution

Rule:
- history is retained for audit, but moved out of active startup dependency.
- active startup must point to one canonical chain only.

---

## 4. Active startup model (fast specialist startup)
### Tier A: Safe-start (`< 5 min`)
Required:
1. branch/remote/bootstrap preflight
2. active authority chain
3. current package objective + first safe action

### Tier B: Specialist context (`< 15 min`)
Required:
1. component current-state + active stream tail
2. relevant deploy/autonomy constraints
3. open risks/blockers for that component

### Tier C: Forensics only
Historical streams, superseded docs, prior package generations.
Not required for normal startup.

---

## 5. Ownership model (streamlined)
### Owner
- decides `accept | changes-requested | reject`
- merge authorization on protected `main`
- large strategic decisions only

### SI Codex
- owns orchestration, dependency identification, cross-lane routing, and truth maintenance
- identifies system-wide impacts and propagates them across affected lanes
- enforces branch/process/governance contracts
- prepares PR-ready, rollback-ready owner packets

### Specialist/Fachchat lanes
- start quickly with Tier B component context
- execute scoped work on `dev/<component>` or dedicated `si/<topic>` package branch
- do not own cross-system governance truth

---

## 6. Backlog + demand handling model
- demand/idea not executed now must be preserved as backlog truth
- no idea/demand loss due to batching or scope deferral
- each deferred item keeps:
  - summary
  - scope/component
  - why_not_now
  - promotion trigger
  - related files/outputs

Execution gate remains explicit:
- `now`
- `quick_win`
- `backlog`

---

## 7. One-click + autonomous delivery boundaries
### Keep
- one-click owner decision path
- owner should not perform branch splitting, manifest authoring, or routing mechanics

### Do not overstate
- autonomous delivery only where support matrix + evidence permit
- governance/docs acceptance is not equivalent to runtime/deploy validation

---

## 8. ZIP intake and Codex manifest model (delivery simplification)
- one raw ZIP handoff may be used as concrete artifact input
- ChatGPT may provide hints, but not canonical branch/path manifest truth
- Codex must generate canonical manifest from ZIP + demand + protocol + repo truth
- distribution across target lanes is sequential, deterministic, and reported in one result report

---

## 9. Implementation rules for TOM v2 preparation
1. do not mutate `main` directly
2. package changes on dedicated branch and PR to `main`
3. no new dashboard/board/html surfaces
4. no second governance system
5. no parallel truth chains

---

## 10. Acceptance for TOM v2 adoption package
- active startup chain shortened and explicit
- historical noise removed from startup dependency
- component/specialist startup is faster and scoped
- SI orchestration/dependency role is explicit
- owner one-click model preserved
- backlog preservation enforced
- governance integrity preserved while delivery speed improves
