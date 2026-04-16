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
