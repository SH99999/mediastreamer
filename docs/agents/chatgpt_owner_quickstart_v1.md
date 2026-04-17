# ChatGPT Owner Quickstart v1

## Purpose
Provide the minimum owner command path for governed ChatGPT↔Codex operation.

## Canonical owner command sequence
1. `governed mode on`
2. discussion
3. `backup chat only` (optional persistence-only checkpoint; no Codex execution trigger)
4. `ship to codex` (execution trigger)
5. `review now`
6. merge to `main` when PR is decision-ready on repo truth (`pre-ok` optional advisory)

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
- ChatGPT `pre-ok` remains optional advisory; owner can decide directly from repo-truth packet and PR evidence.
- owner does not need to tell Codex which side branch to inspect; `ship to codex` publishes canonical pickup snapshot under `exchange/chatgpt/inbox-main/` on `main`.
- `backup chat only` persists continuity artifacts only (live session/protocol update) and must not create demand `ready-for-codex` or inbox-main `pickup-ready` trigger artifacts.

## Guardrails
- no new dashboard/board/html surfaces are required for this flow
- labels are index only; repo artifacts remain canonical truth
