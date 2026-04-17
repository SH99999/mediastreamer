# chat-backup-only-command live v1

status: live
actor: chatgpt

## source/context
- source chat/session: current governed ChatGPT session with owner
- source timestamp (UTC): 2026-04-17T10:35:00Z
- participants: owner, chatgpt

## current objective
- define and implement a pure `backup chat only` command so owner can preserve relevant chat context to Git without triggering Codex execution
- keep the distinction explicit between backup-only persistence and `ship to codex` execution handoff
- preserve important decisions, risks, requests, and references with minimal owner effort

## locked decisions so far
1. `backup chat only` should update continuity artifacts only and must not create a Codex execution trigger
2. `ship to codex` remains the command that creates executable demand + pickup trigger
3. materialized chat protocol should preserve important rationale, decisions, open questions, risks, and Git references without full raw transcript storage
4. owner should have a minimal distinction between backup-only and execution handoff

## open decisions
1. whether `backup chat only` should remain an explicit owner-facing command or later fold into a smaller command surface

## active implementation asks
1. define a canonical backup-only command and lifecycle behavior
2. ensure backup-only updates live session and materialized protocol without creating demand/inbox pickup
3. keep owner command surface minimal and unambiguous

## active risks/blockers
1. without a backup-only command, owner may use `ship to codex` when only persistence is desired
2. mixing backup-only and execution-trigger behavior would create process ambiguity

## non-loss requirements
1. the distinction between backup-only persistence and Codex execution trigger must not remain only in chat memory
2. owner should be able to preserve current chat state without accidentally starting execution work

## current lifecycle status
- live

## last material update timestamp
- 2026-04-17T10:35:00Z
