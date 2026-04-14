# SYSTEM INTEGRATION ESCALATION CONTRACT V1

## Purpose
This document defines when work must escalate automatically to the system integration / governance lane.

## Escalation triggers
Automatic escalation is required when an issue or PR:
- carries `impact:cross-component`
- carries `impact:system-wide`
- touches governance contracts
- touches workflow files
- touches shared deploy tooling
- touches shared rollback behavior
- changes branch/process doctrine
- affects multiple governed components

## Escalation output
An escalation should create or update a governance-routed system integration issue with:
- source link to the triggering issue or PR
- summary of why escalation happened
- affected components where known
- pointers to the repo truth that should be reviewed

## Routing labels
System integration escalation issues should carry at least:
- `governance`
- `component:system-integration`
- `agent:system-integration`
- `type:integration-risk` or `type:governance-update` depending on the trigger
- `impact:cross-component` or `impact:system-wide`
- an appropriate state label

## Owner involvement rule
Escalation should reduce owner review load by surfacing only the real decision or integration risk.
It should not require the owner to manually discover affected docs or component relationships.

## Documentation rule
If escalation results in a decision or doctrine change, the relevant governance docs and journals must be updated in the resulting PR.
