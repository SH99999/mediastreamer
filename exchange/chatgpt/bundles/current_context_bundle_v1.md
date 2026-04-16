# ChatGPT Context Bundle v1

_Generated: 2026-04-16T19:37:59.449690+00:00_

## Usage
- Upload this single file in ChatGPT GUI to avoid multi-file permission prompts.
- Keep branch policy from embedded start prompt.

---

## File: `docs/agents/chatgpt_start_prompt_git_exchange_v3.md`

```md
# CHATGPT START PROMPT — GIT EXCHANGE V3 (OWNER AUDIT START)

```text
Role:
You are ChatGPT in the SH99999/mediastreamer Git exchange loop with Codex.

Mission:
Turn audit findings into ranked implementation proposals that Codex can verify and convert into owner-ready decision packets.

Hard boundaries:
- Read-only on all branches except `si/chatgpt-git-exchange-v1`.
- Never request direct edits on `main`.
- Propose branch plans only; Codex executes repo mutations.

Audit-start workflow (strict):
1) Open and fill `exchange/chatgpt/audit_basis/current_audit_basis_v1.md` first.
2) Keep findings essential and ranked by impact.
3) Set `status: ready-for-codex` after audit basis is complete.
4) Continue via inbox/outbox request-response artifacts.
5) Internal ChatGPT↔Codex notes may be compact/machine-oriented.
6) Final owner handoff must be human-readable in:
   `exchange/chatgpt/outbox/<topic>__owner_decision_packet_v1.md`.

Required read set (before first response):
- exchange/chatgpt/PROTOCOL_v1.md
- exchange/chatgpt/audit_basis/current_audit_basis_v1.md
- exchange/chatgpt/inbox/TEMPLATE__request_v1.md
- exchange/chatgpt/outbox/TEMPLATE__response_v1.md
- exchange/chatgpt/outbox/TEMPLATE__owner_decision_packet_v1.md
- exchange/chatgpt/streams/stream_v1.md

Response contract (strict):
1) ask summary (max 5 bullets)
2) blockers / missing input
3) implementation proposals (ranked)
4) branch + execution path
5) risks (essential)
6) agreement_score_chatgpt (0..100)
7) owner decision suggestion (`accept | changes-requested | reject`)

Speed mode:
- no filler
- no repeated context
- short structured blocks only
- if a key input is missing: state one blocker and continue with best proposal set
```
```

---

## File: `exchange/chatgpt/PROTOCOL_v1.md`

```md
# ChatGPT-Codex Exchange Protocol v1

## Actors
- `chatgpt`
- `codex`

## Required status markers
Each active file must contain one status marker line:
- `status: draft`
- `status: ready-for-codex`
- `status: in-review-by-codex`
- `status: ready-for-chatgpt`
- `status: ready-for-owner`
- `status: closed`

## Handshake order
1. ChatGPT starts with `exchange/chatgpt/audit_basis/current_audit_basis_v1.md`
2. ChatGPT sets `status: ready-for-codex`
3. Codex reviews/evaluates and writes next request/response artifact if needed
4. Codex updates stream with actor and status transition
5. for decision rounds, both sides provide agreement scores and Codex derives owner decision draft
6. Codex publishes one human-readable owner packet in `exchange/chatgpt/outbox/*__owner_decision_packet_v1.md`

## Channel separation (required)
- Internal ChatGPT↔Codex exchange artifacts may be compact or machine-oriented.
- Owner-facing packet must remain human-readable and decision-ready.
- Owner packet is the only mandatory readable handoff object for decisioning.

## Stream entry requirement
Every stream entry must include:
- actor (`chatgpt` or `codex`)
- source file
- resulting status


## Idea channel (two-round alignment)
1. ChatGPT creates `exchange/chatgpt/ideas/<topic>__idea_seed_v1.md` and sets `status: ready-for-codex`.
2. Codex returns round-1 implementation/governance proposal.
3. ChatGPT returns round-2 alignment (`*__round2_alignment_v1.md`) with agreement score.
4. Codex emits owner decision packet and governed implementation plan.
```

---

## File: `exchange/chatgpt/audit_basis/current_audit_basis_v1.md`

```md
# Audit Basis v1 (active)

status: ready-for-codex
actor: chatgpt

## Scope
- component/governance scope: governance consistency, exchange-lane onboarding, one-click semantics, delivery evidence gating
- objective: provide ranked implementation findings and branchable execution paths that Codex can execute through repo branches and PRs

## Findings (essential, ranked)
1. Governance model is viable; the first implementation priority is hard separation of active vs historical truth chains plus a CI anti-reference guard.
2. Onboarding should keep mode-B safe-start as default and add explicit escalation triggers into the full governance chain.
3. One-click semantics and delivery normalization should be tightened together: split owner-governance click vs component-delivery click and require evidence-linked journal/decision updates for delivery/support-matrix promotion.

## Proposed next step for Codex
- branch suggestion: keep exchange work on `si/chatgpt-git-exchange-v1`; propose implementation lanes as `si/active-historical-separation`, `si/onboarding-safe-start-escalation`, and `si/one-click-delivery-evidence-gate`
- expected output: repo-ready implementation findings, branch plan, risk list, and PR-ready execution sequence without direct edits to `main`

## Handover
- set `status: ready-for-codex` when this file is complete
```

---

## File: `exchange/chatgpt/streams/stream_v1.md`

```md
# ChatGPT Exchange Stream v1

## Entries

### 2026-04-16 / cycle reset-v1 / audit-basis-first
- actor: `codex`
- source file: `exchange/chatgpt/audit_basis/current_audit_basis_v1.md`
- action: cleared legacy round1 inbox/outbox artifacts and reset basis to ChatGPT-first workflow
- status: `waiting-for-chatgpt`

### 2026-04-16 / cycle 20260416-190510 / round2-implementation-review
- actor: `codex`
- request: `exchange/chatgpt/inbox/round2-implementation-review__request_v1.md`
- response: `exchange/chatgpt/outbox/round2-implementation-review__response_v1.md`
- branch plan: `si/chatgpt-git-exchange-v1`
- owner decision needed: `accept | changes-requested | reject`
- status: `waiting-for-chatgpt`
```

---

## File: `exchange/chatgpt/inbox/TEMPLATE__request_v1.md`

```md
# <topic> request v1

## context
- source chat/session:
- goal:

## findings / request
1.
2.
3.

## constraints
- governance:
- timeline:

## requested output
- ranked implementation proposal list
```

---

## File: `exchange/chatgpt/inbox/round2-implementation-review__request_v1.md`

```md
<!-- cycle_id: 20260416-190510 -->
# round2-implementation-review request v1

status: ready-for-chatgpt
actor: codex

## context
- source chat/session: owner request for one additional ChatGPT<->Codex review round before owner decision
- goal: challenge and refine Codex implementation proposals, then derive owner-ready decision

## findings / request
1. Proposal A (P1): hard-separate active vs historical governance chain and add CI guard against references to superseded onboarding/index generations.
2. Proposal B (P1): run per-component deploy-process gap checks and update support matrix only with evidence-linked journal/decision updates.
3. Proposal C (P2): formalize one-click split terms (`owner-governance` vs `component-delivery`) across docs and status views.
4. Proposal D (P2): keep mode-B onboarding as default and enforce escalation triggers for full-chain reads.

## constraints
- governance: keep `main` protected; execution remains on SI/dev branches; no direct `main` edits
- timeline: this round should produce consensus rating + owner decision suggestion

## requested output
- ranked proposal adjustments (accept/modify/reject each proposal)
- agreement rating with Codex proposals (0..100)
- top risks/unknowns
- owner decision suggestion (`accept | changes-requested | reject`)
```

---

## File: `exchange/chatgpt/outbox/TEMPLATE__response_v1.md`

```md
# <topic> response v1

## ask summary
-

## blockers / missing inputs
-

## implementation proposals (ranked)
1.
2.
3.

## branch + execution path
- si/<topic>
- optional dev/<component>

## owner decision needed
- accept | changes-requested | reject
```

---

## File: `exchange/chatgpt/outbox/round2-implementation-review__response_v1.md`

```md
<!-- cycle_id: 20260416-190510 -->
# round2-implementation-review response v1

status: draft
actor: chatgpt

## ask summary
-

## blockers / missing inputs
-

## implementation proposals (ranked)
1.
2.
3.

## agreement with codex proposals
- agreement_score_chatgpt:
- proposal_a: accept|modify|reject
- proposal_b: accept|modify|reject
- proposal_c: accept|modify|reject
- proposal_d: accept|modify|reject

## risks / unknowns
-

## branch + execution path
- si/round2-implementation-review
- optional dev/<component>

## owner decision needed
- accept | changes-requested | reject
```

---

## File: `exchange/chatgpt/outbox/TEMPLATE__consensus_owner_decision_v1.md`

```md
# <topic> consensus owner decision v1

status: draft
actor: codex

## inputs
- agreement_score_chatgpt:
- agreement_score_codex:
- major_disagreement_topics:

## consensus rating
- consensus_band: high | medium | low
- rationale (essential):

## owner-ready decision derivation
- recommended_owner_decision: accept | changes-requested | reject
- mandatory_follow_up:
- merge_authorization_hint: yes | no
```

---

## File: `exchange/chatgpt/outbox/TEMPLATE__owner_decision_packet_v1.md`

```md
# <topic> owner decision packet v1

status: ready-for-owner
actor: codex

## decision summary
- recommendation: accept | changes-requested | reject
- confidence_band: high | medium | low
- agreement_score_chatgpt: <0..100>
- agreement_score_codex: <0..100>
- agreement_gap: <absolute difference>

## implementation proposal (ranked)
1.
2.
3.

## risks (essential)
-

## execution path
- branch: si/<topic>
- follow-up branches (optional): dev/<component>

## rollback
- strategy:
- command:

## owner next click
- accept | changes-requested | reject
```

---

## File: `docs/agents/chatgpt_start_prompt_idea_channel_v1.md`

```md
# CHATGPT START PROMPT — IDEA CHANNEL V1

```text
Role:
You are ChatGPT collaborating with Codex in the SH99999/mediastreamer idea channel.

Goal:
Convert new ideas (design to full Volumio GUI implementation) into governed implementation proposals with two alignment rounds.

Branch policy:
- read-only on all branches except `si/chatgpt-git-exchange-v1`
- never request direct edits on `main`
- propose branch/deploy plans only; Codex executes

Required sequence:
1) Start from `exchange/chatgpt/ideas/<topic>__idea_seed_v1.md`
2) Set `status: ready-for-codex`
3) Wait for Codex round-1 proposal
4) Return round-2 alignment in `*__round2_alignment_v1.md`
5) Keep internal exchange compact; owner output must be human-readable

Owner output target:
- `exchange/chatgpt/outbox/<topic>__owner_decision_packet_v1.md`
- include recommendation, risk, rollback, next owner click

Response contract:
1) ask summary (max 5 bullets)
2) proposal feedback
3) ranked implementation path
4) governance + component impact
5) agreement_score_chatgpt (0..100)
6) owner decision suggestion (accept|changes-requested|reject)
```
```

---

## File: `exchange/chatgpt/ideas/TEMPLATE__idea_seed_v1.md`

```md
# <topic> idea seed v1

status: draft
actor: chatgpt

## idea summary
-

## target scope
- component(s):
- expected user impact:

## constraints
- architecture:
- timeline:
- rollback expectations:

## requested codex output
- governance fit check
- implementation options (ranked)
- branch/deploy path

## handover
- set `status: ready-for-codex` when complete
```

---

## File: `exchange/chatgpt/ideas/TEMPLATE__round2_alignment_v1.md`

```md
# <topic> round2 alignment v1

status: draft
actor: chatgpt

## codex proposal feedback
- accepted points:
- change requests:
- risk concerns:

## agreement
- agreement_score_chatgpt: <0..100>
- suggested owner decision: accept | changes-requested | reject

## handover
- set `status: ready-for-codex` when complete
```
