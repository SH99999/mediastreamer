# ChatGPT-Codex Exchange Protocol v1

## Actors
- `chatgpt`
- `codex`

## Governed mode activation
- activation phrase: `governed mode on`
- after activation, persist relevant chat deltas to `exchange/chatgpt/sessions/<topic>__live_v1.md`
- max chat-only continuity window: 5 minutes

## Status model (canonical)
Allowed statuses:
- `live`
- `chatok`
- `ready-for-codex`
- `in-execution`
- `ready-for-chatgpt-review`
- `pre-ok`
- `ready-for-owner`
- `changes-requested`
- `closed`

## Required status marker
Each active exchange artifact must contain one status marker line:
- `status: <allowed-status>`

## Handshake order
`chat -> governed mode on -> live session artifact on git -> ship to codex -> (internal chatok) -> demand intake -> ready-for-codex -> in-execution -> ready-for-chatgpt-review -> (pre-ok OR owner-override) -> ready-for-owner -> closed`

Detailed behavior:
1. ChatGPT activates the thread using `governed mode on`.
2. ChatGPT captures relevant outcome in a live session file (`status: live`).
3. Owner requests `ship to codex`.
4. Codex internalizes `chatok` and promotes to demand intake with `status: ready-for-codex`.
5. Codex executes from demand + repo artifacts and marks `status: in-execution`.
6. Codex marks `status: ready-for-chatgpt-review` as the single review-ready handoff marker after documented output + PR are prepared.
   - required demand fields at this point:
     - `source_pr_url`
     - `source_branch`
     - `review_target_artifacts`
7. ChatGPT reviews against demand + repo truth; set `status: pre-ok` or `status: changes-requested`.
8. Codex prepares owner packet and sets `status: ready-for-owner` when either:
   - `chatgpt_review_result: pre-ok`
   - explicit owner override is recorded (`chatgpt_review_result: owner-override` and `owner_review_override: yes`)
9. After owner decision/merge and governance closeout completion, demand status is auto-moved to `closed`.

Override constraints:
- override is explicit and auditable
- override must not be represented as `pre-ok`

## Continuity rule
No relevant chat information may remain chat-only for more than 5 minutes.
Minimum persistence layer before full durable truth updates:
- `exchange/chatgpt/sessions/<topic>__live_v1.md`

## Execution gate rule
Relevant demand/idea items must carry:
- `execution_gate: now|quick_win|backlog`
- `execution_gate_label: gate:now|gate:quick-win|gate:backlog`
- `why_now`
- `why_not_now`
- `promotion_trigger`
- `safe_to_attach_to_current_package`
- `related_files_outputs`

Routing:
- `now` -> active demand execution
- `quick_win` -> Codex may attach if safe and coherent
- `backlog` -> preserved/visible; not silently executed

Index-vs-truth:
- labels are index/routing/query
- repo artifacts are canonical detailed truth

## Promotion rule (`chatok`)
- promotion source: `exchange/chatgpt/sessions/<topic>__live_v1.md`
- promotion target: `exchange/chatgpt/demands/<topic>__intake_v1.md`
- promotion status result: `ready-for-codex`
- live session remains the continuity artifact
- owner-facing command remains `ship to codex`; `chatok` is an internal lifecycle step

## Owner review pickup command
- owner command: `review now`
- pickup rule: locate demand artifacts with `status: ready-for-chatgpt-review`, then review using `source_pr_url`, `source_branch`, and `review_target_artifacts`

## Channel separation (required)
- Internal ChatGPT↔Codex exchange artifacts may be compact or machine-oriented.
- Owner-facing packet must remain human-readable and decision-ready.
- Owner packet is the only mandatory readable handoff object for decisioning.

## Stream entry requirement
Every stream entry must include:
- actor (`chatgpt` or `codex`)
- source file
- resulting status
- branch/PR path when implementation is requested

## Idea channel (two-round alignment)
1. ChatGPT creates `exchange/chatgpt/ideas/<topic>__idea_seed_v1.md` and sets `status: ready-for-codex`.
2. Codex returns round-1 implementation/governance proposal.
3. ChatGPT returns round-2 alignment (`*__round2_alignment_v1.md`) with agreement score.
4. Codex emits owner decision packet and governed implementation plan.
