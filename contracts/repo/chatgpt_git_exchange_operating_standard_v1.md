# CHATGPT GIT EXCHANGE OPERATING STANDARD V1

## Purpose
Define a governed, low-friction Git-native exchange lane for ChatGPT <-> Codex collaboration so owner overhead stays minimal and relevant chat outcomes become durable repo truth quickly.

## Scope
This standard governs:
- audit-finding exchange
- demand intake exchange from external ChatGPT sessions
- structured proposal/response loops
- continuity guarantees between chat outcomes and Git artifacts

## Core model
1. Exchange happens via repository artifacts (markdown + optional JSON metadata), not chat memory.
2. One dedicated SI branch carries each packaged exchange cycle (`si/chatgpt-git-exchange-<topic>`).
3. Owner role remains decision/merge authority only.
4. Agent/Codex lanes prepare branch, artifacts, PR, and response bundle.
5. Relevant chat outcomes must be captured to Git within 5 minutes.

## Canonical branch and path model
- branch for this capability bootstrap: `si/chatgpt-git-exchange-v1`
- reusable future branch pattern: `si/chatgpt-git-exchange-<topic>`
- canonical exchange root: `exchange/chatgpt/`
  - `exchange/chatgpt/sessions/`
  - `exchange/chatgpt/audit_basis/`
  - `exchange/chatgpt/inbox/`
  - `exchange/chatgpt/outbox/`
  - `exchange/chatgpt/demands/`

## Governed chat mode activation (mandatory)
Activation phrase:
- `governed mode on`

After activation:
- relevant chat deltas must be persisted to Git through a live session artifact
- owner should not need repeated long prompts/process re-explanations
- codex execution handoff must route through governed demand artifacts

## End-to-end governed chain (mandatory)
`chat -> governed mode on -> live session artifact on git -> ship to codex -> (internal chatok promotion) -> ready-for-codex -> in-execution -> ready-for-chatgpt-review -> pre-ok -> ready-for-owner -> closed`

Rules:
- Codex executes from demand artifacts stored in Git.
- Codex must not reconstruct execution scope from chat memory alone.
- Chat outcomes that materially affect repo truth (status/decisions/current-state/streams) must be copied into canonical repo truth files within the implementation package.

## Continuity rule (max knowledge-loss delta)
Once governed mode is active, no relevant information may exist only in chat memory for more than 5 minutes.

Relevant information includes:
- decisions and locked constraints
- risks and blockers
- implementation requests
- owner decision framing
- explicit non-loss requirements

Minimum acceptable persistence if durable truth updates are not yet ready:
- create/update `exchange/chatgpt/sessions/<topic>__live_v1.md` with lifecycle status + `last_material_update_utc`
- then promote to demand intake when owner requests `ship to codex` (internalizing `chatok`)

## Required exchange artifacts
1. `sessions/<topic>__live_vN.md` (governed live session continuity artifact)
2. `audit_basis/current_audit_basis_v1.md` (active basis file)
3. `inbox/<topic>__request_vN.md` (ChatGPT-origin input package)
4. `outbox/<topic>__response_vN.md` (Codex response with implementation plan)
5. `demands/<topic>__intake_vN.md` (ChatGPT demand intake contract)
6. optional sidecar metadata: `<same_name>.json` with fields:
   - `topic`
   - `source_chat_uri` (if available)
   - `owner_decision_needed`
   - `next_owner_click`
   - `status`

## Live session artifact contract (mandatory fields)
Each live session file under `exchange/chatgpt/sessions/` must include:
- source/context
- current objective
- locked decisions so far
- open decisions
- active implementation asks
- active risks/blockers
- non-loss requirements
- current lifecycle status
- last material update timestamp

## Demand artifact contract (mandatory fields)
Each demand intake file under `exchange/chatgpt/demands/` must include:
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

## Demand lifecycle statuses (canonical)
Allowed statuses are:
- `live`
- `chatok`
- `ready-for-codex`
- `in-execution`
- `ready-for-chatgpt-review`
- `pre-ok`
- `ready-for-owner`
- `changes-requested`
- `closed`

## Standard exchange loop (minimal owner path)
1. ChatGPT activates governed mode with `governed mode on`.
2. ChatGPT writes/updates live session artifact in `exchange/chatgpt/sessions/` (`status: live`).
3. Owner requests `ship to codex`; Codex internalizes `chatok` and promotes live context into `exchange/chatgpt/demands/<topic>__intake_v1.md`.
4. Demand is moved to `status: ready-for-codex`.
5. Codex marks `status: in-execution` while implementing governed repo changes.
6. Codex marks `status: ready-for-chatgpt-review` after implementation artifacts + PR are prepared.
7. ChatGPT reviews against demand + repo truth and sets `status: pre-ok` or `status: changes-requested`.
8. Codex updates owner packet and sets `status: ready-for-owner` when pre-ok is satisfied.
9. Owner decides/merges; demand closes automatically after merge + governance closeout completion.

## Living exchange stream (mandatory)
- active stream file: `exchange/chatgpt/streams/stream_v1.md`
- every new exchange cycle must append one entry with:
  - actor (`chatgpt|codex`)
  - cycle id
  - source request file
  - response file
  - demand file (when applicable)
  - proposed implementation branch(es)
  - owner decision needed
  - status transition

## Autonomous cycle bootstrap
- script: `tools/governance/chatgpt_exchange_cycle_v1.py`
- intent:
  1. generate new inbox/outbox files from templates
  2. optionally generate demand intake file from template
  3. append cycle entry to `exchange/chatgpt/streams/stream_v1.md`
  4. keep repeatable no-memory exchange flow

## Review/evaluation trigger detection
- watcher script: `tools/governance/chatgpt_exchange_watch_v1.py`
- rule: Codex evaluates when status marker `ready-for-codex` is present in watched demand/request/basis artifacts
- the watcher must report live session `chatok` artifacts as promotion-required and report `ready-for-codex` artifacts as codex-actionable

## Promotion rule: internal `chatok` live session -> demand intake
- promotion source: `exchange/chatgpt/sessions/<topic>__live_v1.md` with `status: live|chatok`
- promotion target: `exchange/chatgpt/demands/<topic>__intake_v1.md`
- demand status after promotion: `ready-for-codex`
- live artifact remains continuity memory and must continue tracking material updates
- promotion helper: `tools/governance/chatgpt_promote_live_to_demand_v1.py --topic <topic> --ship-to-codex`

## ChatGPT review/pre-ok gate
- Codex implementation output must include documented branch/PR/rollback path.
- ChatGPT review compares implementation output against demand + repo truth.
- Demand lifecycle must not advance to `ready-for-owner` without `pre-ok` or explicit `changes-requested` handling.
- Existing owner-facing surfaces (owner action board / owner decision board / status index / owner dashboard) must expose `pre-ok`, `ready-for-owner`, PR link, and next owner click without requiring owner lifecycle reconstruction.

## Codex-owned routing and decomposition
- owner does not classify components/streams/docs manually
- Codex performs routing, branch creation, decomposition into streams/components, required governance/status/decision updates, and PR preparation
- routing/decomposition logic must remain repo-driven and auditable

## Durable truth update obligation
Execution packages must update durable repo truth when impacted:
- decisions
- status/current-state
- streams
- onboarding links / active-path references
- governance issue closeout transitions

## ChatGPT start prompt artifact
- canonical prompt file: `docs/agents/chatgpt_start_prompt_git_exchange_v1.md`
- branch rule inside prompt:
  - read-only on all branches except the supervised exchange branch

## GUI/no-shell compatibility artifact
- bundle generator: `tools/governance/chatgpt_no_shell_bundle_v1.py`
- output: `exchange/chatgpt/bundles/current_context_bundle_v1.md`
- intent: one-file upload path for ChatGPT GUI sessions with restrictive file-access prompts

## Safety rules
- do not treat inbox/outbox/demand files as deployment approval by themselves
- all protected truth still merges via PR to `main`
- if connector/auth is blocked, produce explicit blocker + one owner action
- no new dashboards/boards/html surfaces are required by this standard
- owner command surface should remain minimal: `governed mode on`, `ship to codex`, `merge after pre-ok`

## Success condition
- ChatGPT exchange is reproducible from Git history alone
- relevant chat outcomes are captured to repo artifacts within 5 minutes
- owner can follow and decide with minimal additional steps
- implementation suggestions are explicit, ranked, and branchable
- exchange cycles can be initialized and watched automatically through existing exchange scripts
