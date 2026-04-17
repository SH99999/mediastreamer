# chat-backup-only-command intake v1

status: ready-for-owner
actor: chatgpt

## source/context
- source chat/session: current governed ChatGPT session with owner
- source timestamp (UTC): 2026-04-17T10:35:00Z
- participants: owner, chatgpt

## objective
- implement a pure `backup chat only` command so owner can preserve relevant chat context to Git without triggering Codex execution
- keep the distinction explicit between backup-only persistence and `ship to codex` execution handoff
- preserve important decisions, risks, requests, and references with minimal owner effort

## locked decisions
1. `backup chat only` should update continuity artifacts only and must not create a Codex execution trigger
2. `ship to codex` remains the command that creates executable demand + pickup trigger
3. materialized chat protocol should preserve important rationale, decisions, open questions, risks, and Git references without full raw transcript storage
4. owner should have a minimal distinction between backup-only and execution handoff

## open decisions
1. whether `backup chat only` should remain an explicit owner-facing command or later fold into a smaller command surface

## required implementation
1. define a canonical `backup chat only` command and lifecycle behavior
2. ensure backup-only updates live session and materialized protocol without creating demand or pickup trigger
3. keep owner command surface minimal and unambiguous
4. update owner/chat-facing docs only as needed so the distinction is explicit

## required governance updates
1. keep the solution inside the existing exchange / demand / protocol model
2. avoid creating a second backup system or new dashboard/html surface
3. preserve the owner-minimal command surface and make the distinction auditable in repo truth

## risks
1. without a backup-only command, owner may use `ship to codex` when only persistence is desired
2. mixing backup-only and execution-trigger behavior would create process ambiguity

## non-loss requirements
1. the distinction between backup-only persistence and Codex execution trigger must not remain only in chat memory
2. owner should be able to preserve current chat state without accidentally starting execution work

## execution request for Codex
- execution branch: si/chat-backup-only-command-v1
- required output: PR to `main` + decision-ready packet + rollback command + next owner click

## execution gate
- execution_gate: now
- execution_gate_label: gate:now
- why_now: current owner command set lacks an explicit backup-only command and risks accidental execution handoff
- why_not_now: delaying leaves ambiguity in the governed chat flow
- promotion_trigger: owner requested a pure chat-backup capability and then explicitly used `ship to codex`
- safe_to_attach_to_current_package: yes
- related_files_outputs: docs/agents/chatgpt_owner_quickstart_v1.md; docs/agents/chatgpt_capture_to_demand_prompt_v1.md; exchange/chatgpt/PROTOCOL_v1.md
- impacted_portfolio_component: system-integration

## label index (query/routing)
- expected_labels:
  - gate:now
  - state:ready-for-agent
  - component:system-integration
  - agent:system-integration
- label_truth_rule: labels route/query only; repo sections in this file remain canonical detailed truth

## lifecycle tracking
- codex_trigger: ship-to-codex
- materialized_protocol: exchange/chatgpt/protocol-main/chat-backup-only-command__protocol_v1.md
- main_inbox_snapshot: exchange/chatgpt/inbox-main/20260417T202000Z__chat-backup-only-command__intake_snapshot_v1.md
- source_pr_url: https://github.com/SH99999/mediastreamer/pull/167
- source_branch: si/chat-backup-only-command-v1
- review_target_artifacts: docs/agents/chatgpt_owner_quickstart_v1.md; docs/agents/owner_operational_reference_v1.md; docs/agents/chatgpt_capture_to_demand_prompt_v1.md; exchange/chatgpt/PROTOCOL_v1.md; contracts/repo/chatgpt_git_exchange_operating_standard_v1.md
- chatgpt_review_result: optional-not-run
- owner_review_override: no
- owner_override_note:
- governance_closeout_status: in-pr
- next_owner_click: review PR #167 and decide `accept | changes-requested | reject`
