# ChatGPT Context Bundle v1

_Generated: 2026-04-16T18:47:42.387143+00:00_

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
  2. exchange/chatgpt/inbox/audit-findings-round1__request_v1.md
  3. exchange/chatgpt/outbox/TEMPLATE__response_v1.md
  4. exchange/chatgpt/streams/stream_v1.md
Step B) Produce one response block matching TEMPLATE__response_v1.md exactly.
Step C) Set branch plan explicitly (default: `si/chatgpt-git-exchange-v1`).
Step D) End with owner decision needed (`accept | changes-requested | reject`).

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

## File: `exchange/chatgpt/audit_basis/current_audit_basis_v1.md`

```md
# Audit Basis v1 (active)

## Source
Owner-provided governance audit (2026-04-16) is treated as current baseline for exchange cycles.

## Core findings (essential)
1. Governance model is viable; consolidation is the primary gap.
2. Onboarding is consistent but too heavy.
3. One-click is strong for owner governance, partial for repo-wide delivery.
4. Active vs historical truth-chain separation needs hardening.
5. Delivery normalization is not complete across all components.

## Expected response format
Codex outbox responses must provide:
- ranked implementation list
- branchable execution path
- explicit owner decision needed
```

---

## File: `exchange/chatgpt/streams/stream_v1.md`

```md
# ChatGPT Exchange Stream v1

## Entries

### 2026-04-16 / cycle 20260416-182645 / audit-findings-round1
- request: `exchange/chatgpt/inbox/audit-findings-round1__request_v1.md`
- response: `exchange/chatgpt/outbox/audit-findings-round1__response_v1.md`
- branch plan: `si/chatgpt-git-exchange-v1`
- owner decision needed: `accept | changes-requested | reject`
- status: `response-written-awaiting-owner-decision`
```

---

## File: `exchange/chatgpt/inbox/audit-findings-round1__request_v1.md`

```md
<!-- cycle_id: 20260416-182645 -->
# audit-findings-round1 request v1

## context
- source chat/session: governance audit acceptance + owner decision capture on 2026-04-16
- goal: convert accepted audit direction into ranked implementation findings for Codex execution planning

## findings / request
1. Governance model is accepted as viable; the primary gap is consolidation rather than base model redesign.
2. Immediate priority is hard separation of active vs historical truth chains plus a CI anti-reference guard.
3. Onboarding should keep mode-B safe-start as default and add explicit escalation triggers into the full governance chain.
4. One-click terminology must be split everywhere into owner-governance click vs component-delivery click.
5. Delivery/support-matrix updates must only move when evidence-linked journal and decision updates exist.

## constraints
- governance: use repo-truth only; no direct edits to main; exchange work stays on `si/chatgpt-git-exchange-v1`
- timeline: round1 should produce ranked implementation direction and branchable execution plan only

## requested output
- ranked implementation proposal list
- explicit branch plan
- risks
- owner decision needed
```

---

## File: `exchange/chatgpt/outbox/audit-findings-round1__response_v1.md`

```md
<!-- cycle_id: 20260416-182645 -->
# audit-findings-round1 response v1

## ask summary
- Audit basis says governance is viable; consolidation is the primary gap.
- Hardening active-vs-historical truth separation is the highest-value first implementation target.
- Onboarding should keep safe-start behavior but reduce weight through explicit escalation triggers.
- One-click must be split into owner-governance click vs component-delivery click.
- Delivery normalization and support-matrix changes should be evidence-linked only.

## blockers / missing inputs
- Inbox request is still mostly placeholder and does not yet contain cycle-specific findings, concrete scope, or constraints.
- No evidence bundle is linked from the inbox request for this cycle.
- No specific component is named yet, so opening a dev lane now would be premature.

## implementation proposals (ranked)
1. Harden active-vs-historical chain separation with CI anti-reference guard.
   - scope: define active chain markers, archive boundaries, and fail CI when active docs reference historical artifacts.
   - rank rationale: directly addresses the highest-risk governance inconsistency.
   - risks: false positives during migration; older docs may still contain implicit legacy references.
2. Consolidate onboarding around mode-B safe-start plus explicit escalation triggers.
   - scope: keep low-risk default onboarding and define exact triggers for escalation into the full governance chain.
   - rank rationale: reduces onboarding friction without dropping governance safety.
   - risks: under-specified triggers could allow incomplete governance handling.
3. Split one-click terminology and enforcement across repo-truth docs.
   - scope: replace ambiguous one-click wording with owner-governance click and component-delivery click.
   - rank rationale: prevents process and expectation drift.
   - risks: documentation could diverge from actual workflows if not updated together.
4. Gate delivery/support-matrix promotion through evidence-linked journal and decision updates.
   - scope: require deploy/test/rollback evidence before support-matrix state changes.
   - rank rationale: closes the current normalization gap across components.
   - risks: slower status promotion until evidence discipline is normalized.

## branch + execution path
- current exchange lane: `si/chatgpt-git-exchange-v1`
- recommended implementation lane 1: `si/active-historical-separation`
- recommended implementation lane 2: `si/onboarding-safe-start-escalation`
- recommended implementation lane 3: `si/one-click-terminology-split`
- optional dev lane: open only after a component-specific delivery gap is named and evidence-backed.

## owner decision needed
- accept | changes-requested | reject
- recommended now: accept ranked direction and request a non-placeholder inbox update for the next cycle.
```
