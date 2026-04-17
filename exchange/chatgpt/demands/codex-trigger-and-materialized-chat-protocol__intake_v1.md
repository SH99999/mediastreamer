# codex-trigger-and-materialized-chat-protocol intake v1

status: ready-for-codex
actor: chatgpt

## source/context
- source chat/session: current governed ChatGPT session with owner
- source timestamp (UTC): 2026-04-17T00:00:00Z
- participants: owner, chatgpt

## objective
- make `ship to codex` repo-effective so Codex can deterministically know there is work to do from repo truth
- add a canonical materialized chat protocol artifact so important conversation history survives beyond the live chat and can be used by Codex or a fresh chat
- keep owner effort minimal and preserve the existing owner-minimal command surface

## locked decisions
1. a Git artifact on a side branch alone is not sufficient unless Codex has a clear repo-visible trigger path
2. `ship to codex` should become the canonical trigger that both writes repo truth and gives Codex a deterministic pickup path
3. a materialized chat protocol should be event-based and compact, not a raw full transcript
4. the protocol must preserve decisions, open questions, risks, execution requests, and links to related Git objects
5. the new mechanism must not add dashboard or governance sprawl

## open decisions
1. whether Codex pickup should be implemented via branch/path watcher only or via a stricter demand-handshake contract plus branch/path watcher
2. whether materialized protocol should live only under `exchange/chatgpt/sessions/` or additionally be promoted/linked from demand artifacts automatically

## required implementation
1. standardize the repo-visible Codex trigger path for `ship to codex`
2. ensure Codex can detect work from repo truth without owner re-explaining the task
3. add a canonical materialized chat protocol template and lifecycle rule
4. ensure protocol + demand + live session work together without parallel truth drift
5. update owner/SI-facing docs only as needed so the behavior is explicit and deterministic

## required governance updates
1. keep the solution inside the existing `exchange/chatgpt/` model; do not create a second exchange system
2. update canonical protocol/standard/playbook docs if required so trigger behavior and protocol artifact are part of repo truth
3. keep owner-minimal flow intact: owner should not need extra commands beyond the existing minimal surface

## risks
1. current demand/live artifacts may still depend too much on explicit Codex chat prompting if trigger semantics remain weak
2. without a materialized protocol, new chats/agents still lose some conversation rationale between live session and durable truth
3. overbuilding this area could create governance/meta sprawl instead of appliance-supporting continuity

## non-loss requirements
1. the rationale behind repo-visible Codex triggering must not remain only in chat memory
2. the need for an event-based materialized protocol must be preserved as a formal requirement
3. owner should not need to restate prior chat history to a new agent/chat

## execution request for Codex
- execution branch: si/codex-trigger-and-materialized-chat-protocol-v1
- required output: PR to `main` + decision-ready packet + rollback command + next owner click

## execution gate
- execution_gate: now
- execution_gate_label: gate:now
- why_now: current owner-minimal flow still depends too much on direct Codex prompting and lacks a canonical materialized protocol artifact
- why_not_now: delaying leaves a continuity and pickup ambiguity in the governed chat flow
- promotion_trigger: owner explicitly requested implementation now
- safe_to_attach_to_current_package: yes
- related_files_outputs: exchange/chatgpt/PROTOCOL_v1.md; contracts/repo/chatgpt_git_exchange_operating_standard_v1.md; docs/agents/chatgpt_capture_to_demand_prompt_v1.md; exchange/chatgpt/protocol-main/TEMPLATE__protocol_snapshot_v1.md; exchange/chatgpt/inbox-main/TEMPLATE__intake_snapshot_v1.md
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
- materialized_protocol: exchange/chatgpt/protocol-main/codex-trigger-and-materialized-chat-protocol__protocol_v1.md
- main_inbox_snapshot:
- source_pr_url: https://github.com/SH99999/mediastreamer/pull/142
- source_branch: si/codex-trigger-and-materialized-chat-protocol-v1
- review_target_artifacts: exchange/chatgpt/PROTOCOL_v1.md; contracts/repo/chatgpt_git_exchange_operating_standard_v1.md; docs/agents/chatgpt_git_exchange_playbook_v1.md; docs/agents/chatgpt_capture_to_demand_prompt_v1.md; exchange/chatgpt/protocol-main/TEMPLATE__protocol_snapshot_v1.md; exchange/chatgpt/inbox-main/TEMPLATE__intake_snapshot_v1.md; tools/governance/chatgpt_materialize_protocol_v1.py; tools/governance/chatgpt_publish_main_snapshot_v1.py
- chatgpt_review_result: pending
- owner_review_override: no
- owner_override_note:
- governance_closeout_status: pending
- next_owner_click: review now
