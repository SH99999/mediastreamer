# CHATGPT GIT EXCHANGE OPERATING STANDARD V1

## Purpose
Define a governed, low-friction Git-native exchange lane for ChatGPT <-> Codex collaboration so owner overhead stays minimal.

## Scope
This standard governs:
- audit-finding exchange
- demand intake exchange from external ChatGPT sessions
- structured proposal/response loops

## Core model
1. Exchange happens via repository artifacts (markdown + optional JSON metadata), not chat memory.
2. One dedicated SI branch carries each packaged exchange cycle (`si/chatgpt-git-exchange-<topic>`).
3. Owner role remains decision/merge authority only.
4. Agent/Codex lanes prepare branch, artifacts, PR, and response bundle.

## Canonical branch and path model
- branch for this capability bootstrap: `si/chatgpt-git-exchange-v1`
- reusable future branch pattern: `si/chatgpt-git-exchange-<topic>`
- canonical exchange root: `exchange/chatgpt/`
  - `exchange/chatgpt/audit_basis/`
  - `exchange/chatgpt/inbox/`
  - `exchange/chatgpt/outbox/`
  - `exchange/chatgpt/demands/`

## Required exchange artifacts
1. `audit_basis/current_audit_basis_v1.md` (active basis file)
2. `inbox/<topic>__request_vN.md` (ChatGPT-origin input package)
3. `outbox/<topic>__response_vN.md` (Codex response with implementation plan)
4. optional sidecar metadata: `<same_name>.json` with fields:
   - `topic`
   - `source_chat_uri` (if available)
   - `owner_decision_needed`
   - `next_owner_click`
   - `status`

## Standard exchange loop (minimal owner path)
1. ChatGPT-side findings/proposals are placed in `exchange/chatgpt/inbox/`.
2. Codex lane converts to governed response in `exchange/chatgpt/outbox/` with concrete implementation list.
3. If repo mutation is required, Codex executes on dedicated SI/dev branches and opens/updates PR(s).
4. Owner receives one decision-ready summary and approves/rejects.

## Living exchange stream (mandatory)
- active stream file: `exchange/chatgpt/streams/stream_v1.md`
- every new exchange cycle must append one entry with:
  - actor (`chatgpt|codex`)
  - cycle id
  - source request file
  - response file
  - proposed implementation branch(es)
  - owner decision needed

## Autonomous cycle bootstrap
- script: `tools/governance/chatgpt_exchange_cycle_v1.py`
- intent:
  1. generate new inbox/outbox files from templates
  2. append cycle entry to `exchange/chatgpt/streams/stream_v1.md`
  3. keep repeatable no-memory exchange flow

## Review/evaluation trigger detection
- watcher script: `tools/governance/chatgpt_exchange_watch_v1.py`
- rule: Codex evaluates when status marker `ready-for-codex` is present in basis/request artifacts

## ChatGPT start prompt artifact
- canonical prompt file: `docs/agents/chatgpt_start_prompt_git_exchange_v1.md`
- branch rule inside prompt:
  - read-only on all branches except the supervised exchange branch

## GUI/no-shell compatibility artifact
- bundle generator: `tools/governance/chatgpt_no_shell_bundle_v1.py`
- output: `exchange/chatgpt/bundles/current_context_bundle_v1.md`
- intent: one-file upload path for ChatGPT GUI sessions with restrictive file-access prompts

## Demand intake extension
Demands produced in ChatGPT should be captured under:
- `exchange/chatgpt/demands/<demand-id>__intake_v1.md`
and then routed into governed issue/branch flows.

## Safety rules
- do not treat inbox/outbox files as deployment approval by themselves
- all protected truth still merges via PR to `main`
- if connector/auth is blocked, produce explicit blocker + one owner action

## Success condition
- ChatGPT exchange is reproducible from Git history alone
- owner can follow and decide with minimal additional steps
- implementation suggestions are explicit, ranked, and branchable
- exchange cycles can be initialized automatically through the cycle bootstrap script
