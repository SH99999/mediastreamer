# Demands

Demand intake files extracted from ChatGPT sessions live here:
- `<topic>__intake_v1.md`

## Required structure
Use `TEMPLATE__intake_v1.md` and keep all required sections:
- source/context
- objective
- locked decisions
- open decisions
- required implementation
- required governance updates
- risks
- non-loss requirements
- execution request for Codex
- status marker

## Lifecycle statuses
Use only canonical statuses:
- `live` (session stage; demand file starts after promotion)
- `ready-for-codex`
- `in-execution`
- `ready-for-chatgpt-review`
- `pre-ok`
- `ready-for-owner`
- `changes-requested`
- `closed`

## Continuity rule
Relevant chat outcomes must be captured to this folder within 5 minutes if durable truth updates are not yet applied.
Before demand exists, continuity must be captured in `exchange/chatgpt/sessions/<topic>__live_v1.md`.
