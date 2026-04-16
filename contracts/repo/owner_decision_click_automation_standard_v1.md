# OWNER DECISION CLICK AUTOMATION STANDARD V1

## Purpose
This standard reduces owner comment overhead by introducing a structured click/selection decision path for PR governance outcomes.

## Core model
Owner decisions should be captured through structured fields (Project custom fields or fallback structured comment) and synchronized into governed PR labels.
PR creation and PR updates are execution responsibilities of agents/chats/Codex lanes, not the owner.

## One-click ownership operating contract (mandatory)
- `main` is protected truth and merge authority remains owner-only.
- delivery path is deterministic: `local branch -> github.com branch -> PR to main`.
- branch push and PR lifecycle actions (create/update/rebase/respond) are automated responsibilities of agents/chats/Codex lanes.
- owner should receive one decision-ready packet and choose `accept | changes-requested | reject` without performing PR mechanics.
- owner merge click happens only after governance validation checks are green and requested evidence is present.

## Role split (mandatory)
- **Owner:** decision authority only (`accept | changes-requested | reject`) and merge authorization (`yes | no`).
- **Agent/Chat/Codex lane:** create/update branch, push branch, create/update PR, apply requested changes, and keep docs/journals in sync.
- **Never require owner PR authoring** as a normal operating path.
- **Exception only:** if connector/auth is blocked, agent must provide one explicit fallback handoff and mark delivered status truthfully.

## Decision fields
Minimum required fields:
- `decision`: `accept | changes-requested | reject`
- `merge_authorization`: `yes | no`
- `docs_journals_complete`: `yes | no`

Optional fields:
- `scope`
- `followup_note`

## Click-path precedence
1. Project custom fields on the owner queue item (preferred click-path).
2. Structured PR comment block with marker `<!-- owner-decision-v1 -->` (fallback when project-field API bridge is unavailable).

## SI merge-request packet requirement
For SI/governance changes, agents/chats/Codex must provide a prepared **SI Merge Request executive summary** packet with:
- direct PR link
- files-changed/compare link
- concise executive summary
- explicit risk level (`low|medium|high`)
- rollback command
- explicit `owner decision needed`
- explicit `next_owner_click`
- SI comment-ready block the owner can use without extra navigation

Contract source:
- `docs/agents/si_merge_request_executive_summary_v1.md`


## Post-merge temporary branch cleanup
After owner merge to `main`, agents/chats/Codex should delete merged short-lived topic branches (`si/<topic>` and temporary hotfix branches) locally and on `github.com` unless an explicit hold is documented.

Rollback safety note:
- branch deletion does not remove rollback capability because rollback is performed from `main` history (revert commit path)
- if a branch must be retained for legal/audit reasons, record the exception in SI stream with retention owner

## Label synchronization contract
Owner decision synchronization should maintain exactly one active state label:
- `accept + merge_authorization=yes + docs_journals_complete=yes` -> `state:awaiting-owner`
- `accept + merge_authorization=yes + docs_journals_complete=no` -> `state:docs-update-required`
- `changes-requested` -> `state:ready-for-agent`
- `reject` -> `state:done`

## Rollback model (mandatory)
Automation must be reversible without history loss:
- feature-flag gate: `OWNER_DECISION_AUTOMATION_ENABLED`
- rollback action: disable flag and revert to manual owner comments/labels
- no destructive mutation of journals or decision logs during rollback
- synchronization comments remain as evidence trail

## Satellite processes that must stay aligned
- owner operational reference
- project view blueprint and field definitions
- PR governance review workflow
- governance closeout workflow
- SI status/decision/stream logs
- branch auto-rebase workflow for `si/*`, `dev/*`, and `integration/*`
- bootstrap/reporting prompts that instruct agents/chats to refresh/rebase after `main` changes

## Robustness double-check
Before enabling on `main`, run governance-model robustness checks to verify:
- required docs/workflows/scripts exist
- owner decision field contract is present
- rollback flag path is documented
- structured fallback marker path is available

## Safety rule
If parsing fails or fields are incomplete:
- do not apply destructive label changes
- emit explicit blocker comment with required owner action
- prefer truthful negative status over assumed decision
