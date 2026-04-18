# chatgpt-preok-optional-owner-repo-truth live v1

status: closed
actor: chatgpt
last_material_update_utc: 2026-04-17T00:00:00Z

## source/context
- source chat/session: current governed ChatGPT session with owner
- source timestamp (UTC): 2026-04-17T00:00:00Z
- participants: owner, chatgpt

## current objective
- make ChatGPT `pre-ok` optional advisory instead of required merge gate
- keep owner merge decision repo-truth first while preserving auditability
- align canonical owner/exchange docs and demand lifecycle wording

## locked decisions so far
1. owner merge decision should not depend on ChatGPT pre-authorization
2. ChatGPT review remains optional advisory input
3. project custom fields remain optional convenience and must not become critical-path

## open decisions
1. none

## active implementation asks
1. update canonical governance/exchange docs to reflect optional advisory pre-ok
2. publish canonical main inbox snapshot and linked demand/protocol artifacts for pickup

## active risks/blockers
1. wording drift across owner/exchange docs if lifecycle language is not synchronized

## non-loss requirements
1. preserve continuity from this chat in repo artifacts
2. keep explicit auditability when override markers are used

## promotion note
- promoted to demand intake on `ship to codex`

## close metadata
- close_reason: merged-on-main
- closed_by_pr: #147
- governance_closeout_status: done
- next_owner_click: none
