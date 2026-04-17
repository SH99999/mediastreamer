# ChatGPT Owner Quickstart v1

## Purpose
Provide the minimum owner command path for governed ChatGPT↔Codex operation.

## Canonical owner command sequence
1. `governed mode on`
2. discussion
3. `ship to codex`
4. `review now`
5. merge to `main` after ChatGPT `pre-ok`

## Review pickup marker (single source)
Use demand artifacts under `exchange/chatgpt/demands/` and locate:
- `status: ready-for-chatgpt-review`

Required references in the same demand:
- `source_pr_url`
- `source_branch`
- `review_target_artifacts`

## Owner action intent
- `review now` means ChatGPT should pick up demands marked `ready-for-chatgpt-review` and review against listed source refs.
- `chatok` and demand closeout remain internal automation/lifecycle mechanics.

## Guardrails
- no new dashboard/board/html surfaces are required for this flow
- labels are index only; repo artifacts remain canonical truth
