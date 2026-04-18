# codex-trigger-and-materialized-chat-protocol intake snapshot v1

status: closed
pickup_rule: main-inbox-v1
snapshot_immutable: true
snapshot_id: 20260417T100459Z
created_at_utc: 2026-04-17T10:04:59Z
trigger_command: ship to codex
close_reason: merged-on-main; demand closed

## codex pickup contract
- execution_branch: si/main-inbox-codex-trigger-and-protocol-snapshots-v1
- pickup_ready_marker: status: pickup-ready
- pickup_source: exchange/chatgpt/inbox-main/

## source artifacts
- demand_intake: exchange/chatgpt/demands/codex-trigger-and-materialized-chat-protocol__intake_v1.md
- materialized_protocol: exchange/chatgpt/protocol-main/codex-trigger-and-materialized-chat-protocol__protocol_v1.md

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


## risks
1. current demand/live artifacts may still depend too much on explicit Codex chat prompting if trigger semantics remain weak
2. without a materialized protocol, new chats/agents still lose some conversation rationale between live session and durable truth
3. overbuilding this area could create governance/meta sprawl instead of appliance-supporting continuity


## execution requests
1. standardize the repo-visible Codex trigger path for `ship to codex`
2. ensure Codex can detect work from repo truth without owner re-explaining the task
3. add a canonical materialized chat protocol template and lifecycle rule
4. ensure protocol + demand + live session work together without parallel truth drift
5. update owner/SI-facing docs only as needed so the behavior is explicit and deterministic


## related git objects
- demand_path: exchange/chatgpt/demands/codex-trigger-and-materialized-chat-protocol__intake_v1.md
- protocol_path: exchange/chatgpt/protocol-main/codex-trigger-and-materialized-chat-protocol__protocol_v1.md
- snapshot_path: exchange/chatgpt/inbox-main/20260417T100459Z__codex-trigger-and-materialized-chat-protocol__intake_snapshot_v1.md
