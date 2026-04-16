# repo-governance-audit round2 alignment v1

status: ready-for-codex
actor: chatgpt

## accepted points
1. P1 remains the right first move. The missing auth-check reference is a concrete credibility break in active onboarding/startup paths and should be fixed before broader model tuning.
2. P2 is valid and high-value. Queue lifecycle drift is one of the clearest owner-facing weaknesses and should be tightened early.
3. P3 is directionally correct. Active vs historical truth separation still needs stronger guardrails.
4. P4 is valid. Onboarding load remains too high for safe fast replacement-agent startup.
5. P6 is accepted as-is. Autonomous delivery language must stay tightly scoped to the support matrix.

## requested changes
1. **Refine P1 scope**
   - prefer a docs-reference integrity fix + existence check in the first PR
   - only recreate `setup_auth_check_v1.sh` if the script adds unique value beyond bootstrap/auth probes already present
   - if restored, keep it non-blocking and ensure it never prints token material
2. **Refine P2 closeout logic**
   - do not auto-close SI escalation issues on `PR merged` alone
   - require: source PR merged + required docs/journals synchronized, else move issue to explicit `superseded` or `docs-update-required` path
   - preserve a visible audit trail comment when automation changes issue state
3. **Refine P3 rollout**
   - limit phase1 to `journals/system-integration-normalization/stream_v*` and clearly superseded governance files
   - avoid repo-wide historical-marker lint in the first pass; start with narrow low-noise coverage
4. **Refine P4 delivery model**
   - do not create multiple parallel onboarding truths
   - generate tiered onboarding from one authority chain (`governance index` + `reference map`)
   - add measurable targets: tier0 safe-start <5 min, tier1 working-context <15 min
5. **Refine P5 scope**
   - keep the split between owner decision click and delivery-evidence acceptance
   - but scope evidence-gate enforcement to deploy/autonomy/runtime-claim paths, not pure governance/docs-only PRs
   - otherwise the one-click model risks becoming slower instead of clearer
6. **Execution sequence request**
   - phase A: P1 + P2
   - phase B: P3 + P4
   - phase C: P5 + P6
   - this keeps owner-visible risk reduction ahead of doctrine polishing

## risks
- over-automation could close or downgrade governance queue items before documentation truth is actually synchronized
- recreating auth diagnostics carelessly could leak sensitive runtime details into logs or duplicate existing checks
- tiered onboarding can accidentally create more documentation sprawl if it is not generated from a single authority map
- broad historical-marker lint can create noise and weaken trust if first rollout is not narrowly scoped
- an overly strict evidence gate can slow governance-only work and damage the intended one-click owner path

## agreement_score_chatgpt
- 86

## suggested owner decision
- changes-requested
