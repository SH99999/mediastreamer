# integration-chatgpt-habit live v1

status: live
actor: chatgpt

## source/context
- source chat/session: current governed ChatGPT session with owner
- source timestamp (UTC): 2026-04-17T11:20:00Z
- participants: owner, chatgpt

## current objective
- use `integration/chatgpt` as the standard ChatGPT write/push branch for governed chat artifacts until the main-inbox trigger path is operationally frictionless
- preserve current chat decisions, process clarifications, and codex handoff expectations in repo truth without losing information

## locked decisions so far
1. `integration/chatgpt` should be treated as the habitual ChatGPT working branch for repo-backed chat artifacts
2. owner wants minimal interaction and no repeated governance explanations
3. owner wants a deterministic codex trigger path plus materialized protocol and continuity backup
4. owner wants explicit agent registry / availability / startup / delegation truth in repo

## open decisions
1. whether ChatGPT should continue writing first to `integration/chatgpt` and rely on Codex to publish canonical `main` inbox snapshots until direct main publication is operationally solved

## active implementation asks
1. formalize use of `integration/chatgpt` in rules and startup/onboarding where appropriate
2. keep chat continuity and codex handoff artifacts preserved on this branch when direct main publication is not available to ChatGPT

## active risks/blockers
1. direct writes to protected `main` are blocked for ChatGPT in the current tool path
2. codex automatic pickup from `main` still requires SI Codex to be alive and using the watcher correctly

## non-loss requirements
1. this branch-use decision and the current chat rationale must not remain only in chat memory
2. current chat state must remain recoverable for a fresh chat or Codex lane

## current lifecycle status
- live

## last material update timestamp
- 2026-04-17T11:20:00Z
