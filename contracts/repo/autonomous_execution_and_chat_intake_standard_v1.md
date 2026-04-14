# AUTONOMOUS EXECUTION AND CHAT INTAKE STANDARD V1

## Purpose
This document defines the repo-side operating model for autonomous intake, routing, execution, escalation, and closure.

## Goal state
The target operating loop is:
1. demand is discussed in chat
2. the demand becomes a repo object such as an issue or PR
3. labels and workflows route the work automatically
4. component-local work proceeds through the appropriate lane
5. cross-component or system-wide impact escalates automatically to system integration / governance
6. supported component delivery can deploy, test, and roll back through repo workflows
7. merged work closes the loop through governance closeout workflows
8. the owner is involved mainly for actual decisions

## Core rule
The system must minimize recurring owner administration.
The owner should not need to manually maintain routing, branch lists, label assignments, or repetitive project bookkeeping when the repo can determine those automatically.

## Intake forms the repo must be able to handle
The operating model must support input such as:
- feature requests
- defects
- governance updates
- open decisions
- UI/UX design standard definition
- asset placement or asset routing work
- integration risks
- release readiness work

## Intake routing rule
New work should become a repo object with:
- component classification where possible
- impact classification
- issue type classification
- agent routing label
- state label
- source label

## UI/UX and asset handling rule
UI/UX design standards and asset-placement work are valid first-class repo demands.
They should route through the same issue governance system as code or deployment work.

Recommended routing:
- design standard definition -> `agent:ux` plus governance-relevant type/state labels
- asset placement work -> component label plus `agent:ux` when the work is presentation- or design-driven
- if a design or asset decision affects multiple components or shared contracts -> escalate to `agent:system-integration`

## Execution rule
Autonomous execution must use existing repo workflows and repo-controlled deploy/rollback paths.
Do not create parallel deployment mechanisms outside the repo contract.

## Safety rule
Autonomous execution should be conservative.
If a component is not yet declared delivery-capable in repo truth, the system should escalate or no-op safely instead of attempting unsupported deployment.

## Escalation rule
When a demand or change is:
- `impact:cross-component`
- `impact:system-wide`
- or touches governance, workflows, shared deployment logic, rollback logic, or shared contracts

it must escalate automatically to system integration / governance.

## Closure rule
The autonomous system is not complete until merged PRs normalize issue state and governance issue closure.

## Repo truth rule
Autonomous workflows do not replace repo truth.
The source of truth remains:
- governance contracts
- current-state journals
- decision logs
- stream journals

The autonomous system operates from that truth and should reinforce it.
