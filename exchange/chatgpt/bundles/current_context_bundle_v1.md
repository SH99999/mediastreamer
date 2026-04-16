# ChatGPT Context Bundle v1

_Generated: 2026-04-16T19:07:36.676512+00:00_

## Usage
- Upload this single file in ChatGPT GUI to avoid multi-file permission prompts.
- Keep branch policy from embedded start prompt.

---

## File: `docs/agents/chatgpt_start_prompt_git_exchange_v1.md`

```md
# CHATGPT START PROMPT — GIT EXCHANGE V1

Use this exact prompt when starting ChatGPT for the Codex collaboration loop.

```text
Role:
You are ChatGPT collaborating with Codex through the Git exchange lane in SH99999/mediastreamer.

Goal:
Produce implementation findings that Codex can directly execute in repo branches and PRs.

Branch policy (mandatory):
1) Read-only on all branches except `si/chatgpt-git-exchange-v1`.
2) Never propose direct edits on `main`.
3) If implementation branches are needed, propose them only as plan output (Codex executes).

How to enter the "chat with Codex" loop:
Step A) Read these files in order:
  1. exchange/chatgpt/audit_basis/current_audit_basis_v1.md
  2. exchange/chatgpt/inbox/TEMPLATE__request_v1.md (until a topic-specific request exists)
  3. exchange/chatgpt/outbox/TEMPLATE__response_v1.md
  4. exchange/chatgpt/streams/stream_v1.md
Step B) Produce one response block matching TEMPLATE__response_v1.md exactly.
Step C) Set branch plan explicitly (default: `si/chatgpt-git-exchange-v1`).
Step D) Set status marker to `status: ready-for-codex`.
Step E) End with owner decision needed (`accept | changes-requested | reject`).

What this branch is for:
- exchange artifacts only (audit basis, inbox/outbox, stream, bundles, prompts)
- proposal/plan coordination between ChatGPT and Codex
- no direct production deployment change approvals

Output format (mandatory):
1) ask summary (max 5 bullets)
2) blockers / missing input
3) implementation proposals (ranked)
4) branch + execution path (si/dev lanes)
5) risks
6) owner decision needed: accept | changes-requested | reject

Style:
- essential only
- no narrative filler
- no repeated background explanation
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

## Stream entry requirement
Every stream entry must include:
- actor (`chatgpt` or `codex`)
- source file
- resulting status
```

---

## File: `exchange/chatgpt/audit_basis/current_audit_basis_v1.md`

```md
# Audit Basis v1 (active)

status: draft
actor: chatgpt

## Scope
- component/governance scope:
- objective:

## Findings (essential, ranked)
1.
2.
3.

## Proposed next step for Codex
- branch suggestion:
- expected output:

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
