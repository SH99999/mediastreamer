# Idea Channel (ChatGPT ↔ Codex)

Purpose: collect new ideas (design through full GUI implementation), run two alignment rounds, then hand over a governance-ready implementation packet.

Flow:
1. ChatGPT writes `*__idea_seed_v1.md`.
2. Codex writes round-1 response and request.
3. ChatGPT returns round-2 alignment response.
4. Codex emits owner-ready implementation packet.

Execution gate rule:
- every idea seed must include `execution_gate: now|quick_win|backlog` and companion rationale fields
- quick wins may be attached by Codex only when safe/coherent
- backlog ideas must preserve summary, impacted portfolio/component, related outputs, why_not_now, and promotion_trigger

Execution-gate label mapping:
- `execution_gate: now` -> `gate:now`
- `execution_gate: quick_win` -> `gate:quick-win`
- `execution_gate: backlog` -> `gate:backlog`

Owner-query indexing:
- labels are the index for routing/query
- idea artifact fields remain canonical detailed truth
