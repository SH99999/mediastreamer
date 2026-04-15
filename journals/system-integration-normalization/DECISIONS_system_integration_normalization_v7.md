# DECISION LOG — system_integration_normalization

Status note: this v7 file supersedes the earlier v6 SI alignment addendum as the current SI/N decision addendum.

## Decision Entries

### DEC-system_integration_normalization-13
- Status: locked
- Decision: issue routing uses one central project plus label-based routing instead of one project per component or assignee-based agent routing.
- Date context: governance routing phase
- Why this was chosen: reduces owner admin overhead while staying automatable.
- What it affects: issue routing, project usage, and agent-lane classification.
- What it explicitly does NOT affect: optional human assignees for human ownership.
- Follow-up needed: keep project views aligned with the label taxonomy.

### DEC-system_integration_normalization-14
- Status: locked
- Decision: autonomous execution must minimize recurring owner administration and operate from repo truth.
- Date context: autonomy layer definition phase
- Why this was chosen: the owner should mainly take decisions, not perform repetitive system administration.
- What it affects: workflow design, escalation behavior, and governance reporting.
- What it explicitly does NOT affect: the owner's approval role on protected-main merges.
- Follow-up needed: prefer automation over manual bookkeeping when safe.

### DEC-system_integration_normalization-15
- Status: locked
- Decision: cross-component and system-wide impact must escalate automatically to system integration and governance.
- Date context: autonomy layer definition phase
- Why this was chosen: decisions that affect multiple lanes must not remain trapped in one chat or one component lane.
- What it affects: issue routing, escalation workflows, and SI issue creation.
- What it explicitly does NOT affect: component-local work with no cross-component effect.
- Follow-up needed: keep escalation logic aligned with impact labels and governance docs.

### DEC-system_integration_normalization-16
- Status: locked
- Decision: autonomous delivery must be support-matrix based and conservative.
- Date context: autonomy layer definition phase
- Why this was chosen: only components with normalized deploy and rollback contracts should auto-deliver.
- What it affects: autonomous delivery behavior.
- What it explicitly does NOT affect: future expansion of delivery support to more components once normalized.
- Follow-up needed: update the delivery matrix when additional components become support-ready.

### DEC-system_integration_normalization-17
- Status: locked
- Decision: UI/UX design standard and asset-placement work are first-class repo demands and must route through the same governance issue model as code or deployment work.
- Date context: autonomy layer definition phase
- Why this was chosen: non-code product work still affects the appliance and must not bypass repo governance.
- What it affects: chat intake handling, issue routing, and UX-related escalation.
- What it explicitly does NOT affect: whether the work is implemented by a code lane or a UX lane.
- Follow-up needed: keep UX and asset work mapped into the issue-routing model.

### DEC-system_integration_normalization-18
- Status: locked
- Decision: the repository remains public until further notice while `main` stays protected as the truth branch.
- Date context: operating-model alignment phase
- Why this was chosen: protected `main` preserves truth discipline while avoiding additional paid/private-repo overhead right now.
- What it affects: repository visibility, review posture, and the public branch/PR operating model.
- What it explicitly does NOT affect: a future visibility change if the cost/risk tradeoff changes later.
- Follow-up needed: revisit only if the owner changes the visibility strategy.

### DEC-system_integration_normalization-19
- Status: locked
- Decision: system integration uses short-lived repo-control-plane branches to `main` by default; `integration/staging` is exception-only.
- Date context: operating-model alignment phase
- Why this was chosen: it minimizes branch clutter, truth ambiguity, and owner click overhead.
- What it affects: SI branch usage and packaged PR behavior.
- What it explicitly does NOT affect: specialist `dev/<component>` branches.
- Follow-up needed: use `integration/staging` only for explicit temporary staging cases.

### DEC-system_integration_normalization-20
- Status: locked
- Decision: when tooling, connector, access, or execution problems block safe completion, agents must escalate and inform instead of improvising, faking completion, or silently creating partial truth.
- Date context: operating-model alignment phase
- Why this was chosen: explicit blockers are safer than false completion in a governed repo.
- What it affects: all chat and Codex lanes, especially when technical execution is blocked.
- What it explicitly does NOT affect: normal safe branch-plus-PR execution when the tools work.
- Follow-up needed: route such blockers as integration-risk when they affect repo truth or cross-component work.

### DEC-system_integration_normalization-21
- Status: locked
- Decision: if a connector cannot safely mutate an existing protected truth file, the controlled replacement-file operating model is the standard exception path.
- Date context: operating-model alignment phase
- Why this was chosen: truth quality must survive tool limitations without pretending a direct mutation succeeded.
- What it affects: maintenance of protected truth files such as `AGENTS.md`.
- What it explicitly does NOT affect: the default expectation that truth changes should still use the normal branch-plus-PR path whenever possible.
- Follow-up needed: use clearly named replacement artifacts such as `ag_new.txt` and state the required owner action explicitly.

### DEC-system_integration_normalization-22
- Status: locked
- Decision: one target Pi may have only one active deploy/test slot at a time, and workflows must refuse deployment when the target is already in a governed occupied state.
- Date context: deploy-exclusivity alignment phase
- Why this was chosen: parallel deploys invalidate tests and destroy confidence in rollback anchors.
- What it affects: deploy, rollback, autonomous delivery dispatch, and all target-Pi validation behavior.
- What it explicitly does NOT affect: the separate question of whether a component's deploy/rollback contract is mature enough to use the slot.
- Follow-up needed: validate the new lock-aware workflow family with Bridge on the real Pi.

## Superseded Decisions
- The earlier v6 SI alignment addendum remains historical; this v7 file is the current deploy-exclusivity addendum.
