# Live Sessions

Governed-mode live continuity artifacts:
- `<topic>__live_v1.md`

## Activation and minimal command surface
- `governed mode on`
- `ship to codex`

## Required live-session fields
- source/context
- current objective
- locked decisions so far
- open decisions
- active implementation asks
- active risks/blockers
- non-loss requirements
- current lifecycle status
- last material update timestamp (UTC)

## Continuity SLA
After governed mode is active, no relevant chat delta may remain chat-only for more than 5 minutes.

## Materialized protocol rule
- keep the protocol artifact compact and event-based (no raw full transcript)
- protocol events must preserve: decisions, open questions, risks/blockers, execution asks, and links to related Git objects
- whenever `ship to codex` promotion happens, append a protocol event linking:
  - live session artifact
  - demand intake artifact
  - execution branch hint
- canonical protocol artifact path is `exchange/chatgpt/protocol-main/<topic>__protocol_v1.md`
