# SKILL — AUTONOMOUS REPO OPERATIONS V1

## Purpose
This skill defines how an agent should work inside the governed autonomous repo model.

## Core operating pattern
1. turn the user's demand into the correct repo object
2. rely on repo labels and workflows for routing where possible
3. escalate to system integration when work is cross-component or system-wide
4. use governed workflows for deployment and rollback
5. leave a repo-native trail in contracts or journals when operational truth changes

## Intake guidance
Use repo issues for:
- decisions
- governance updates
- integration risks
- branch drift follow-up
- journal gaps
- UI/UX standard work
- asset placement work

Use the label-based routing model instead of inventing ad-hoc issue wording.

## Execution guidance
If delivery automation is needed, consult:
- `tools/governance/autonomous_delivery_matrix_v1.json`

Only components marked delivery-capable should be auto-delivered.
Unsupported components should escalate instead.

## Escalation guidance
Escalate automatically when work:
- affects multiple components
- touches workflows or deploy tooling
- changes governance contracts
- affects rollback behavior
- has system-wide impact

## Documentation guidance
When repo truth changes materially, update:
- the relevant governance contracts
- the relevant current-state journals
- the relevant decision logs when a decision changed
- the relevant stream journals when meaningful state changed
