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
   - `exchange/chatgpt/sessions/<topic>__protocol_v1.md` (compact materialized event protocol)
3. Promote with `ship to codex` to demand intake:
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
- include execution gate fields: execution_gate (now|quick_win|backlog), why_now, why_not_now, promotion_trigger, safe_to_attach_to_current_package, related_files_outputs, impacted_portfolio_component

When execution-ready:
- run ship-to-codex promotion into exchange/chatgpt/demands/<topic>__intake_v1.md
- set demand status to ready-for-codex (internal `chatok` is handled by Codex)
- ensure promotion metadata contains `codex_trigger: ship-to-codex` and materialized protocol link

Then follow lifecycle:
in-execution -> ready-for-chatgpt-review -> pre-ok -> ready-for-owner -> closed

Owner command surface must stay minimal:
- governed mode on
- ship to codex
- merge after pre-ok
```

## Owner handoff rule
After promotion to demand intake, use governed execution flow prompt:
- `docs/agents/chatgpt_governed_intake_prompt_v1.md`
- Codex owns gate/routing/decomposition; owner does not classify components, branches, or documentation targets manually.

## Continuity rule
After governed mode activation, no relevant chat information may remain chat-only for more than 5 minutes.
