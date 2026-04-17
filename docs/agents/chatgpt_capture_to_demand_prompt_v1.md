# ChatGPT Capture-to-Demand Prompt v1

## Purpose
Use this one-time activation prompt in any repo-relevant chat so material decisions are persisted to Git with governed continuity and can be routed into Codex execution.

## When to use
Use this when the chat contains any of the following:
- locked decisions that must not be lost
- implementation requests
- governance update requirements
- owner decision framing
- blockers, risks, or non-loss requirements

## Activation and output targets
1. Activate governed mode in chat: `governed mode on`.
2. Persist live continuity to:
   - `exchange/chatgpt/sessions/<topic>__live_v1.md`
3. Promote with `chatok` to demand intake:
   - `exchange/chatgpt/demands/<topic>__intake_v1.md`

## Capture prompt
Use this exact prompt in the ChatGPT chat you want to preserve:

```text
governed mode on
Topic: <topic>

Create or update one live continuity artifact for this chat at:
exchange/chatgpt/sessions/<topic>__live_v1.md

Requirements:
- persist all material deltas to Git within 5 minutes
- include source/context, current objective, locked decisions, open decisions, active implementation asks, active risks/blockers, non-loss requirements, lifecycle status, last_material_update_utc

When execution-ready:
- run chatok promotion into exchange/chatgpt/demands/<topic>__intake_v1.md
- set demand status to ready-for-codex (ship to codex)

Then follow lifecycle:
in-execution -> ready-for-chatgpt-review -> pre-ok -> ready-for-owner -> closed

Owner command surface must stay minimal:
- governed mode on
- chatok
- ship to codex
- close demand
```

## Owner handoff rule
After promotion to demand intake, use governed execution flow prompt:
- `docs/agents/chatgpt_governed_intake_prompt_v1.md`

## Continuity rule
After governed mode activation, no relevant chat information may remain chat-only for more than 5 minutes.
