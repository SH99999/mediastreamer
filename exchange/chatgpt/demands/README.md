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
- execution gate fields (`execution_gate`, `why_now`, `why_not_now`, `promotion_trigger`, `safe_to_attach_to_current_package`, `related_files_outputs`, `impacted_portfolio_component`)
- label index block (`expected_labels`, `label_truth_rule`)

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

## Execution gate routing
- `execution_gate: now` -> active execution package
- `execution_gate: quick_win` -> may be attached by Codex only when safe/coherent
- `execution_gate: backlog` -> preserved and visible; not silently executed

## Execution-gate label mapping
- `execution_gate: now` -> `gate:now`
- `execution_gate: quick_win` -> `gate:quick-win`
- `execution_gate: backlog` -> `gate:backlog`

Labels are indexing/routing helpers only.
Detailed truth remains in demand artifact sections.
