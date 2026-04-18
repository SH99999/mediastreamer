# chatgpt-preok-optional-owner-repo-truth protocol snapshot v1

status: closed
actor: chatgpt-codex
source_live_session: exchange/chatgpt/sessions/chatgpt-preok-optional-owner-repo-truth__live_v1.md
source_demand_intake: exchange/chatgpt/demands/chatgpt-preok-optional-owner-repo-truth__intake_v1.md
last_event_utc: 2026-04-17T11:40:47Z

## current objective
- make ChatGPT `pre-ok` optional advisory instead of required merge gate
- keep owner merge decision repo-truth first while preserving auditability
- align canonical owner/exchange docs and demand lifecycle wording

## material events
### event 001
- event_utc:
- event_type: governed-mode-activated | ship-to-codex-promotion | codex-execution-started | review-ready | pre-ok | changes-requested | owner-override | owner-ready | closed
- actor: chatgpt | codex | owner
- summary:
- locked_decisions:
  1.
- open_decisions:
  1.
- risks:
  1.
- execution_requests:
  1.
- related_git_objects:
  - live_session:
  - demand_intake:
  - main_inbox_snapshot:
  - source_branch:
  - source_pr_url:
  - review_target_artifacts:

### event 002
- event_utc: 2026-04-17T11:31:01.367343+00:00
- event_type: ship-to-codex-promotion
- actor: codex
- summary: promotion from live session to ready-for-codex demand intake completed
- decisions:
  1. owner-visible trigger remains `ship to codex`.
- open_questions:
  1. none recorded in this event.
- risks_blockers:
  1. none recorded in this event.
- execution_requests:
  1. execute demand on declared SI branch and prepare PR to main.
- related_git_objects:
  - live_session: exchange/chatgpt/sessions/chatgpt-preok-optional-owner-repo-truth__live_v1.md
  - demand_intake: exchange/chatgpt/demands/chatgpt-preok-optional-owner-repo-truth__intake_v1.md
  - source_branch:
  - source_pr_url:
  - review_target_artifacts:
### event 003
- event_utc: 2026-04-17T11:31:12.552251+00:00
- event_type: ship-to-codex-promotion
- actor: codex
- summary: promotion from live session to ready-for-codex demand intake completed
- decisions:
  1. owner-visible trigger remains `ship to codex`.
- open_questions:
  1. none recorded in this event.
- risks_blockers:
  1. none recorded in this event.
- execution_requests:
  1. execute demand on declared SI branch and prepare PR to main.
- related_git_objects:
  - live_session: exchange/chatgpt/sessions/chatgpt-preok-optional-owner-repo-truth__live_v1.md
  - demand_intake: exchange/chatgpt/demands/chatgpt-preok-optional-owner-repo-truth__intake_v1.md
  - source_branch:
  - source_pr_url:
  - review_target_artifacts:

### event 004
- event_utc: 2026-04-17T11:40:47Z
- event_type: closed
- actor: codex
- summary: merged-main delivery present; stale pickup artifacts closed after implementation landed via PR #147
- locked_decisions:
  1. owner merge decision is optional-advisory with respect to ChatGPT pre-ok.
- open_decisions:
  1. none.
- risks:
  1. none requiring further execution.
- execution_requests:
  1. none.
- related_git_objects:
  - live_session: exchange/chatgpt/sessions/chatgpt-preok-optional-owner-repo-truth__live_v1.md
  - demand_intake: exchange/chatgpt/demands/chatgpt-preok-optional-owner-repo-truth__intake_v1.md
  - main_inbox_snapshot: exchange/chatgpt/inbox-main/20260417T113113Z__chatgpt-preok-optional-owner-repo-truth__intake_snapshot_v1.md
  - source_branch: si/agent-registry-delegation-and-startup-v1
  - source_pr_url: https://github.com/SH99999/mediastreamer/pull/147
  - review_target_artifacts: docs/agents/owner_operational_reference_v1.md; docs/agents/chatgpt_owner_quickstart_v1.md; exchange/chatgpt/PROTOCOL_v1.md
