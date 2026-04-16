# repo-governance-audit response v1

status: ready-for-codex
actor: chatgpt

## ask summary
- audit governance consistency against current repo truth
- validate agent onboarding, roles, and rules of engagement
- evaluate one-click ownership concept, status/reporting, and queue behavior
- review autonomous deploy/test/rollback doctrine, data/version handling, and security-visible concerns
- return ranked issues plus branchable mitigation path for Codex and owner decisioning

## blockers / missing inputs
- this pass validates repository truth, workflows, reports, and issue state through the GitHub connector; it is not a shell-level or runner-host penetration test
- target-Pi workflow job logs were not exhaustively sampled in this pass, so runtime assurance is based on contracts, reports, matrix state, and documented workflow logic
- connector evidence shows queue-state shortcomings, but GitHub Project custom-field state was not directly inspected here

## implementation proposals (ranked)
1. **P1 — fix onboarding/auth contract breakage first**
   - create or remove the missing `tools/governance/setup_auth_check_v1.sh` reference path
   - add a CI/docs-reference existence check so onboarding docs cannot point to missing executable assets again
   - update `container_startup_setup_v1.md`, owner/agent setup references, and any startup prompts in one change set
2. **P2 — close the governance queue lifecycle gap**
   - add deterministic closeout/retire logic for SI escalation issues once the source PR is merged or explicitly superseded
   - add a stale-governance sweeper that re-labels or closes queue items whose source PR is already merged and whose required docs are complete
   - ensure queue state cannot silently drift away from PR state
3. **P3 — hard-separate active vs historical truth chains**
   - normalize older SI stream generations with explicit `historical` / `read-only` markers
   - extend the superseded-document index so version sprawl stays searchable but non-authoritative
   - add a low-noise lint to detect writable historical docs or active docs missing current-authority markers
4. **P4 — reduce onboarding load with a tiered execution profile**
   - keep mode-B startup as default safe-start
   - define `tier0 / tier1 / tier2` onboarding bundles so replacement agents can reach safe action sooner without losing the full reference chain
   - keep one pointer map authoritative and measure target read-time reduction against the current audit baseline
5. **P5 — tighten one-click from decisioning to evidence-backed closeout**
   - split owner-governance click (`accept | changes-requested | reject`) from delivery-support promotion and runtime acceptance
   - require explicit evidence bundle linkage before `auto_delivery_supported`, `accepted_for_main`, or queue closeout can move forward
   - propagate the same contract into status packets, owner decision packets, and governance closeout workflows
6. **P6 — keep autonomous delivery conservative and measurable**
   - maintain the support-matrix gate for unsupported components
   - only widen autonomous scope after measurable Pi test evidence is stored and linked from journals/status packets
   - add one explicit statement in owner-facing reports clarifying that autonomy applies only to the support-matrix subset, not the whole repo

## branch + execution path
- primary exchange lane: `si/chatgpt-git-exchange-v1`
- proposed SI execution branches:
  - `si/auth-diagnostics-contract-fix`
  - `si/governance-queue-closeout-automation`
  - `si/history-marker-and-superseded-cleanup`
  - `si/onboarding-tiered-execution-profile`
  - `si/one-click-delivery-evidence-gate`
- optional component follow-up lanes only when a finding requires component-local journal/current-state correction:
  - `dev/bridge`
  - `dev/tuner`
  - `dev/fun-line`

## risks (essential)
- stale escalation/queue items can give the owner a false picture of what still needs action
- missing executable assets behind onboarding docs reduce trust in the onboarding contract and increase replacement-agent friction
- long read chains increase the chance of partial reading, outdated assumptions, and unsafe shortcut behavior
- historical doc/version sprawl can reintroduce parallel truth if authority marking is not tightened
- autonomous-delivery language can be over-read unless support-matrix boundaries remain explicit in all owner-facing outputs
- public-repo operation plus self-hosted-runner doctrine is workable, but it keeps operational surface area visible and requires continued secret/runner hygiene

## agreement_score_chatgpt
- 89

## owner decision suggestion
- changes-requested

## detailed finding notes
### F1 — governance model viability: **strong, but not yet self-closing**
The repo now has a real control-plane model: protected `main`, dedicated `si/*` governance branches, label-based routing, status packets, and CI-backed guardrails. The doctrine is coherent enough to continue scaling, but it still depends on cleanup/closure automation that has not fully caught up with the written model.

### F2 — onboarding: **safe, but still too expensive**
Mode-B startup and the reference map materially improve re-entry, but the total read surface is still too large for fast replacement-agent activation. The current model is safe-start capable, not yet low-friction.

### F3 — one-click concept: **validated for packets, partial for lifecycle**
Decision packet fields, rollback scoring, `next_owner_click`, and integration checks are in place. The remaining weakness is not packet generation itself, but the coupling from owner packet -> PR state -> issue queue closeout -> post-merge hygiene.

### F4 — data/versioning: **history preserved, authority still noisy**
Versioned status/decision/stream files protect history and rollback reasoning, but they also grow the interpretation surface. Older files need stronger historical marking so authority stays obvious under speed pressure.

### F5 — deploy/test/rollback: **robust doctrine, limited supported scope**
The workflow model is lock-aware, branch-ref based, and failure-aware. The audit concern is not lack of design, but potential overstatement: only the support-matrix subset should be treated as autonomous, and acceptance still needs explicit evidence discipline.
