# COMPONENT STATUS — system_integration_normalization

Status note: this v6 file supersedes the earlier v5 autonomy-layer snapshot as the current SI/N status addendum.

## 1. Scope
- component name: system_integration_normalization
- legacy names / aliases: SI/N, integration chat, normalization lane
- responsibility boundaries: branch doctrine, workflow model, deploy semantics, rollback semantics, repo governance, release-path normalization, issue routing, escalation discipline, autonomous execution guardrails, cross-component normalization, protected-main truth maintenance operating model
- non-goals: specialist feature implementation inside component payloads, UI/UX design ownership, hardware implementation, unsupported component delivery automation

## 2. Current Functional Status
- what currently works:
  - governance, issue-routing, and reporting workflows exist on `main`
  - one-click branch rebase exists for all current and future `dev/*` and `integration/*` branches
  - weekly governance report issues are generated from repo truth
  - open decisions, branch drift, and journal freshness can become governance-routed issues automatically
  - PR governance review and governance closeout workflows are active
  - new governed components can be bootstrapped via workflow
  - release-readiness audit exists as a manual gate
  - an autonomous execution doctrine and SI escalation contract exist in repo form
  - a protected-main truth maintenance operating model now exists for safe handling of connector mutation limits
- what partially works:
  - autonomous delivery is still support-matrix limited and not yet broad across all active components
  - top-level truth-file mutation through the current connector surface remains limited, so replacement artifacts such as `ag_new.txt` may still be required
  - AGENTS pointer-chain alignment still requires owner application on `main`
- what is broken:
  - unsupported components cannot yet use autonomous delivery and must still escalate or no-op safely
- what was tested:
  - governance reporting and routing layers were merged and are available on `main`
  - project auto-add and project views were confirmed to work with the governance label model
  - branch creation and new-file repo-truth updates through the connector are working
- what is untested:
  - broader autonomous delivery beyond the current support matrix
  - a future connector path for safe in-place mutation of all protected truth files

## 3. Repository Mapping
- correct component path in repo: `journals/system-integration-normalization/`
- correct truth contracts: `contracts/repo/`
- correct support data path: `tools/governance/`
- correct branch model: `main` for truth; short-lived repo-control-plane branches for SI changes; `integration/staging` as an exception-only branch

## 4. Locked Decisions
### DEC-SIN-12
- decision: issue routing is label-based and one central GitHub Project is used instead of one project per component.
- rationale: low owner overhead and scalable routing.
- impact: governance issues route by label, not by assignee.

### DEC-SIN-13
- decision: autonomous execution must minimize recurring owner administration and use governed repo workflows and repo truth.
- rationale: the repo is becoming the operating system for the project.
- impact: workflows and docs must favor auto-routing, auto-reporting, and safe escalation.

### DEC-SIN-14
- decision: cross-component and system-wide impact must escalate automatically to system integration / governance.
- rationale: chat memory is not a safe integration bus.
- impact: escalation workflows and labels are required.

### DEC-SIN-15
- decision: autonomous delivery must be support-matrix based and conservative.
- rationale: not all components have normalized deploy/rollback contracts yet.
- impact: unsupported components must escalate or no-op safely instead of pretending delivery support exists.

### DEC-SIN-16
- decision: the repository remains public until further notice while `main` stays protected as the truth branch.
- rationale: low-cost operation is currently preferred over private-repo administration while protected `main` still preserves truth discipline.
- impact: work happens in public branches and PRs; accepted truth still gates on protected `main`.

### DEC-SIN-17
- decision: system integration uses short-lived repo-control-plane branches to `main` by default; `integration/staging` is exception-only.
- rationale: this minimizes branch clutter, truth ambiguity, and owner click overhead.
- impact: SI changes should normally ship as packaged PRs from temporary branches.

### DEC-SIN-18
- decision: when tooling, connector, access, or execution problems block safe completion, agents must escalate and inform instead of improvising, faking completion, or silently creating partial truth.
- rationale: false completion is more dangerous than an explicit blocker in a governed repo.
- impact: blocking technical issues become visible repo/integration risks instead of hidden drift.

### DEC-SIN-19
- decision: if the connector cannot safely mutate an existing protected truth file, the controlled replacement-file operating model is the standard exception path.
- rationale: protected truth must remain accurate even when the mutation surface is limited.
- impact: replacement artifacts such as `ag_new.txt` are allowed as an exception path when clearly documented.

## 5. Open Decisions
- when additional components become delivery-capable in the autonomous support matrix
- whether the repository should later move to private visibility if the cost/risk tradeoff changes
- whether low-risk PR classes should later auto-merge once the current packaged-review model has matured further

## 6. Runtime / Deployment Notes
- current autonomous delivery-capable component: Bridge
- delivery support matrix path: `tools/governance/autonomous_delivery_matrix_v1.json`
- unsupported components must not auto-deliver until their contracts are normalized
- owner remains the final onsite acceptance gate before stable truth is merged to `main`

## 7. Next Recommended Steps
1. align `AGENTS.md` on `main` using the `ag_new.txt` replacement artifact
2. review and merge this SI alignment package
3. keep incoming component PRs aligned to the locked public/protected-main operating model
4. continue component deploy/rollback normalization beyond Bridge
