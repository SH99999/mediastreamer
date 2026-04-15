# SYSTEM INTEGRATION RECOVERY ONBOARDING V6

## Purpose
This file is the fast re-entry and handover guide for a replacement system integration / normalization chat.

## Current operating model
The repository is an issue-driven, workflow-backed control plane.
Use repo-native issues, labels, workflows, journals, and contracts as the operating system.

## Role to assume
Assume the role of repository control-plane owner for:
- governance consistency
- branch and process consistency
- workflow and rollback doctrine
- issue routing and escalation discipline
- autonomous execution guardrails
- cross-component normalization
- repo-truth cleanup where uncertainty still exists

Do not assume deep specialist implementation ownership inside a component unless the repo state clearly requires it.

## Current repo truth snapshot
- repository: `SH99999/mediastreamer`
- truth branch: `main`
- repository visibility: public until further notice
- active component branches:
  - `dev/bridge`
  - `dev/tuner`
  - `dev/starter`
  - `dev/autoswitch`
  - `dev/fun-line`
  - `dev/hardware`
- integration-owned exception branch:
  - `integration/staging`
- current governance layer includes:
  - one-click branch rebase workflow
  - weekly governance report issue workflow
  - issue-governance routing automation
  - governance closeout workflow
  - autonomy/intake/escalation layer
  - corrected issue-intake normalizer v2
  - first live governance-loop validation already recorded
  - target deploy/test exclusivity governance and lock-aware workflows
  - truthful execution and negative-answer standard
  - governed Git release-tagging standard

## Read order
1. `contracts/repo/system_integration_governance_index_v6.md`
2. `AGENTS.md`
3. `contracts/repo/branch_strategy_v2.md`
4. `contracts/repo/component_artifact_model_v1.md`
5. `contracts/repo/naming_and_release_numbering_standard_v1.md`
6. `contracts/repo/release_intake_and_delivery_status_v2.md`
7. `contracts/repo/component_journal_policy_v2.md`
8. `contracts/repo/new_component_intake_standard_v2.md`
9. `contracts/repo/issue_governance_routing_standard_v1.md`
10. `contracts/repo/autonomous_execution_and_chat_intake_standard_v1.md`
11. `contracts/repo/system_integration_escalation_contract_v1.md`
12. `contracts/repo/protected_main_truth_maintenance_operating_model_v1.md`
13. `contracts/repo/deploy_target_exclusivity_standard_v1.md`
14. `contracts/repo/truthful_execution_and_negative_answer_standard_v1.md`
15. `contracts/repo/git_release_tagging_standard_v1.md`
16. `journals/system-integration-normalization/STATUS_system_integration_normalization_v7.md`
17. `journals/system-integration-normalization/DECISIONS_system_integration_normalization_v9.md`
18. `journals/system-integration-normalization/stream_v5.md`
19. active component journals under `journals/<component>/`

## Locked operating rules
- `main` is the protected truth branch and final owner acceptance gate
- agents and chats work on non-`main` branches
- deploy/test happens from the working branch
- accepted work merges to `main` only after packaged review and owner acceptance
- system integration uses short-lived repo-control-plane branches to `main` by default
- `integration/staging` is exception-only for temporary integration-owned staging work
- journals, decisions, and streams are mandatory repo truth and must not be treated as optional paperwork
- if tooling, connector, access, or execution problems prevent safe completion, escalate and inform instead of improvising, faking completion, or silently mutating partial truth
- if a connector cannot safely update an existing truth file, use the protected-main replacement-file operating model instead of forcing an unsafe mutation path
- target deploy/test exclusivity is governed and must be respected before runtime mutation on the Pi
- an explicit truthful negative answer is always preferred over fabricated progress, implied completion, false confidence, or placeholder delivery

## Key workflows to know immediately
### Branch and repo health
- `rebase-dev-and-integration-branches-on-main.yml`
- `weekly-governance-report-issue.yml`
- `release-readiness-audit.yml`
- `repo-health-v3.yml`
- `governance-health-v2.yml`
- `component-health-v1.yml`

### Issue governance and queue generation
- `ensure-governance-labels.yml`
- `open-decision-issues.yml`
- `branch-drift-issues.yml`
- `journal-freshness-issues.yml`
- `stale-governance-items.yml`
- `pr-governance-review.yml`
- `governance-closeout.yml`

### Intake and autonomy
- `issue-intake-normalizer-v2.yml`
- `issue-context-enrichment.yml`
- `system-integration-escalation.yml`
- `autonomous-delivery-orchestrator-v2.yml`
- `decision-verification-on-merge.yml`
- `repo-control-plane-sanity-check.yml`
- `bootstrap-new-component.yml`

### Component deploy/test workflows still relevant
- `component-test-deploy-v7.yml`
- `component-test-rollback-v7.yml`
- `component-test-release-slot-v1.yml`

## Working rule
- use the issue-routing model instead of ad-hoc chat-side task memory
- if work is cross-component or system-wide, escalate automatically to SI/governance
- if a component is not support-matrix delivery-capable, do not pretend autonomous delivery support exists
- keep repo-truth cleanup visible in docs, journals, and issues instead of hiding uncertainty

## Current practical priorities
1. keep the governance and issue control-plane working
2. keep active branches aligned to `main`
3. resolve repo-truth uncertainty where still open, highest priority:
   - starter
   - fun-line
   - hardware
4. keep component journals and decisions updated as active repo truth
5. package repo-truth changes so owner review stays low-click
6. validate the new lock-aware Bridge reference path on the real Pi

## Minimum completion condition for a replacement SI chat
Before changing repo-control-plane truth, the replacement chat should be able to answer:
- what the current issue-routing model is
- how escalation is triggered
- which workflows are operator-facing versus background automation
- which components are currently delivery-capable
- which uncertainties are explicitly tracked in repo truth instead of assumed away
- what to do when safe completion is blocked by tool or connector limitations
- which stream file is the active SI stream truth
