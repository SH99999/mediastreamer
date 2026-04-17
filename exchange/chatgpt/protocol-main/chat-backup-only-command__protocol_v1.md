# chat-backup-only-command protocol v1

status: ready-for-owner
topic: chat-backup-only-command
last_updated_utc: 2026-04-17T21:15:00Z

## event history

### event-001
- timestamp_utc: 2026-04-17T10:35:00Z
- event_type: ship-to-codex-promotion
- summary: chat topic promoted as governed demand for implementing a persistence-only `backup chat only` command behavior.
- links:
  - demand_intake: exchange/chatgpt/demands/chat-backup-only-command__intake_v1.md
  - live_session: exchange/chatgpt/sessions/chat-backup-only-command__live_v1.md

### event-002
- timestamp_utc: 2026-04-17T21:15:00Z
- event_type: codex-implementation-ready
- summary: owner/protocol/governance docs updated so `backup chat only` persists continuity only and does not trigger Codex execution.
- links:
  - source_branch: si/chat-backup-only-command-v1
  - review_targets:
    - docs/agents/chatgpt_owner_quickstart_v1.md
    - docs/agents/owner_operational_reference_v1.md
    - docs/agents/chatgpt_capture_to_demand_prompt_v1.md
    - exchange/chatgpt/PROTOCOL_v1.md
    - contracts/repo/chatgpt_git_exchange_operating_standard_v1.md
