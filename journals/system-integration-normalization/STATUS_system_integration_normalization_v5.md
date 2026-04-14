# COMPONENT STATUS — system_integration_normalization

Status note: this v5 file supersedes the earlier v4 intake-specific snapshot as the current autonomous-governance SI/N status addendum.

## 1. Scope
- component name: system_integration_normalization
- legacy names / aliases: SI/N, integration chat, normalization lane
- responsibility boundaries: branch doctrine, workflow model, deploy semantics, rollback semantics, repo governance, release-path normalization, cross-component integration policy, issue routing, escalation discipline, autonomous execution guardrails
- non-goals: specialist feature implementation inside component payloads, UI/UX design ownership, hardware implementation, unsupported component delivery automation

## 2. Current Functional Status
- what currently works:
  - governance, issue-routing, and reporting workflows now exist on `main`
  - one-click branch rebase exists for all current and future `dev/*` and `integration/*` branches
  - weekly governance report issues are generated from repo truth
  - open decisions, branch drift, and journal freshness can become governance-routed issues automatically
  - PR governance review and governance closeout workflows are active
  - new governed components can be bootstrapped via workflow
  - release-readiness audit exists as a manual gate
  - an autonomous execution doctrine and SI escalation contract now exist in repo form
  - autonomous delivery support matrix now exists and declares Bridge as the current supported component for autonomous delivery
- what partially works:
  - autonomous delivery is currently support-matrix limited and not yet broad across all active components
  - AGENTS.md still points to older but compatible governance entrypoints rather than this v4/v5 layer
  - project auto-add works, but project field automation is not yet repo-managed
- what is broken:
  - unsupported components cannot yet use autonomous delivery and must still escalate or no-op safely
- what was tested:
  - governance reporting and routing layers were merged and are available on `main`
  - project auto-add and project views were confirmed to work with the governance label model
- what is untested:
  - first-run behavior of the new autonomy workflows after merge
  - autonomous delivery orchestration beyond the current support matrix

## 3. Repository Mapping
- correct component path in repo: `journals/system-integration-normalization/`
- correct truth contracts: `contracts/repo/`
- correct support data path: `tools/governance/`
- correct branch: `main` for truth; dedicated temporary working branches for repo-control-plane changes

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

## 5. Open Decisions
- how far project field automation should go beyond current label-based routing
- when each non-bridge component becomes delivery-capable in the support matrix
- how chat-to-repo intake should be automated beyond the current governance issue model

## 6. Runtime / Deployment Notes
- current autonomous delivery-capable component: Bridge
- delivery support matrix path: `tools/governance/autonomous_delivery_matrix_v1.json`
- unsupported components must not auto-deliver until their contracts are normalized

## 7. Next Recommended Steps
1. merge the autonomy-layer PR
2. run the label sync workflow once after merge
3. verify first runs of the new routing/escalation workflows
4. align active dev branches to current `main`
5. begin development against the governed repo control plane
