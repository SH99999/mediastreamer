# COMPONENT STATUS — system_integration_normalization

Status note: this v8 file remains the current SI/N status addendum and is updated here after successful tuner target-Pi validation.

## 1. Scope
- component name: system_integration_normalization
- legacy names / aliases: SI/N, integration chat, normalization lane
- responsibility boundaries: branch doctrine, workflow model, deploy semantics, rollback semantics, repo governance, release-path normalization, issue routing, escalation discipline, autonomous execution guardrails, cross-component normalization, protected-main truth maintenance operating model, target deploy/test exclusivity rules
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
  - a protected-main truth maintenance operating model exists for safe handling of connector mutation limits
  - a target deploy/test exclusivity contract and lock-aware workflow family exist on `main`
  - bridge deploy and rollback are validated on the target Pi
  - tuner deploy and rollback are now also validated on the target Pi through the manual lock-aware workflow lane
- what partially works:
  - autonomous delivery is still support-matrix limited and not yet broad across all active components
  - top-level truth-file mutation through the current connector surface remains limited, so replacement artifacts may still be required in some cases
  - tuner deploy normalization currently covers the overlay/runtime/service lane only; the separate `radio_scale_source` artifact is still not normalized as a deployable repo payload
- what is broken:
  - unsupported components still cannot use autonomous delivery and must still escalate or no-op safely
- what was tested:
  - governance reporting and routing layers were merged and are available on `main`
  - project auto-add and project views were confirmed to work with the governance label model
  - branch creation and new-file repo-truth updates through the connector are working
  - bridge lock-aware deploy and rollback path are validated on the real Pi
  - tuner lock-aware deploy and rollback path are validated on the real Pi
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

### DEC-SIN-20
- decision: one target Pi may have only one active deploy/test slot at a time; no other deploy may run while that slot is occupied.
- rationale: parallel deploys destroy test validity and make rollback anchors ambiguous.
- impact: deploy/test/rollback workflows must respect target-slot state such as `free`, `deploying`, `test_open`, `rollback_running`, and `blocked`.

## 5. Open Decisions
- when tuner should enter the autonomous delivery support matrix after its now-successful manual Pi validation
- when additional components beyond bridge and tuner become delivery-capable in the autonomous support matrix
- whether the repository should later move to private visibility if the cost/risk tradeoff changes
- whether low-risk PR classes should later auto-merge once the current packaged-review model has matured further

## 6. Runtime / Deployment Notes
- current validated deploy/rollback reference components:
  - Bridge
  - Tuner overlay/runtime/service lane
- delivery support matrix on `main` remains conservative until tuner is explicitly promoted by decision
- owner remains the final onsite acceptance gate before stable truth is merged to `main`
- tuner still has one explicit contract gap: the separate `radio_scale_source` artifact is not yet normalized inside the new deploy lane

## 7. Next Recommended Steps
1. decide whether tuner should now enter the autonomous delivery matrix
2. normalize the separate `radio_scale_source` artifact if tuner must again ship both overlay and source as one governed lane
3. normalize the next component wrapper contract after bridge and tuner
