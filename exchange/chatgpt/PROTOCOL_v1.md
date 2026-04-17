# ChatGPT-Codex Exchange Protocol v1

## Actors
- `chatgpt`
- `codex`

## Status model (canonical)
Allowed statuses:
- `draft`
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
`chat -> demand -> chatok -> ready-for-codex -> in-execution -> ready-for-chatgpt-review -> pre-ok -> ready-for-owner -> closed`

Detailed behavior:
1. ChatGPT captures relevant outcome in a demand intake file.
2. ChatGPT sets `status: chatok` once demand content is accurate.
3. ChatGPT/Codex sets `status: ready-for-codex` when execution can start.
4. Codex executes from repo artifacts and marks `status: in-execution`.
5. Codex marks `status: ready-for-chatgpt-review` after documented output + PR are prepared.
6. ChatGPT reviews against demand + repo truth; set `status: pre-ok` or `status: changes-requested`.
7. Codex prepares owner packet and sets `status: ready-for-owner` only after pre-ok path is satisfied.
8. After owner decision/merge, mark `status: closed`.

## Continuity rule
No relevant chat information may remain chat-only for more than 5 minutes.
Minimum persistence layer before full durable truth updates:
- `exchange/chatgpt/demands/<topic>__intake_v1.md`

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
