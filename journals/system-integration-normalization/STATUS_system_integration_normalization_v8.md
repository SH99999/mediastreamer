# COMPONENT STATUS — system_integration_normalization

Status note: this v8 file remains the current SI/N status addendum and is updated here after successful tuner target-Pi validation and autonomy promotion.

## 1. Scope
- component name: system_integration_normalization
- legacy names / aliases: SI/N, integration chat, normalization lane
- responsibility boundaries: branch doctrine, workflow model, deploy semantics, rollback semantics, repo governance, release-path normalization, issue routing, escalation discipline, autonomous execution guardrails, cross-component normalization, protected-main truth maintenance operating model, target deploy/test exclusivity rules
- non-goals: specialist feature implementation inside component payloads, UI/UX design ownership, hardware implementation, unsupported component delivery automation

## 2. Current Functional Status
- what currently works:
  - governance, issue-routing, and reporting workflows exist on `main`
  - governance closeout now applies evidence-gated state transitions so referenced governance issues move to `state:done` only when a merged source PR exists and governance/journal/docs truth paths were updated in the merged PR
  - SI onboarding is now tiered (`Tier 0` safe-start, `Tier 1` working context, `Tier 2` deep history) and active startup truth is explicitly anchored to AGENTS + SI index + SI TOM + current SI status/decisions/stream
  - SI startup references are compressed to one canonical active path with explicit deep-history boundary and startup acceptance targets (`Tier 0 < 5m`, `Tier 1 < 15m`)
  - status/owner packet claim classes now separate `governance/docs accepted`, `runtime validated`, and `autonomy eligible`, with evidence-gated runtime/autonomy assertions and truthful degradation when evidence is missing
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
  - tuner deploy and rollback are validated on the target Pi through the manual lock-aware workflow lane
  - bridge and tuner are both enabled in the autonomous delivery support matrix
- what partially works:
  - governed chat mode can now persist live session continuity artifacts under `exchange/chatgpt/sessions/` and promote `chatok` sessions into `ready-for-codex` demand artifacts
  - chat-to-demand exchange lane remains active under `exchange/chatgpt/` with watcher support for `ready-for-codex` artifacts
  - autonomous delivery remains support-matrix gated, currently including Bridge and Tuner while Fun Line and other components remain unsupported until evidence-led claims are completed
  - top-level truth-file mutation through the current connector surface remains limited, so replacement artifacts may still be required in some cases
  - tuner deploy normalization is intentionally scoped to overlay/runtime/service while source-selection behavior remains hardware-governed (encoder short/long press) until full integration
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
- active SI UI/GUI governance stream path: `journals/system-integration-normalization/ui_gui_stream_v1.md`
- correct truth contracts: `contracts/repo/`
- correct support data path: `tools/governance/`
- correct branch model: `main` for truth; dedicated short-lived `si/<topic>` branches for SI/governance changes; `integration/staging` as an exception-only branch

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

### DEC-SIN-21
- decision: SI/governance work must follow a dedicated branch path `si/<topic>` from local implementation to pushed branch and PR to protected `main`.
- rationale: branch clarity is required for autonomous governance discipline and avoids drift from generic local branch names.
- impact: SI lane execution, onboarding, and PR preparation now require explicit SI branch naming and same-branch promotion to `main`.

### DEC-SIN-22
- decision: SI onboarding preflight must explicitly reject branch name `work` for SI truth changes and must verify remote `git` points to `https://github.com/SH99999/mediastreamer.git` before push/PR handoff.
- rationale: avoids ambiguous local execution and prevents pushes to the wrong remote.
- impact: replacement SI agents must run branch+remote preflight checks before packaging governed SI changes.

### DEC-SIN-23
- decision: stage-B UI/UX autonomy requires proposal-reference fields and decision options in intake issues, plus `decision_output_v1` as canonical owner decision output block.
- rationale: repeated UI/UX iterations need deterministic automation anchors and low-click owner decision handling.
- impact: issue templates and onboarding now require proposal URI/revision and decision options; project view setup follows the in-repo blueprint.

### DEC-SIN-25
- decision: status prompts are fulfilled via generated repo pages under `reports/status/` with clickable source links and compact visual summaries.
- rationale: reduces owner and agent overhead for recurring status requests and keeps outputs anchored to Git truth.
- impact: status handling for `status tuner|governance|ui|bridge|decisions|blocker` now maps to generated markdown artifacts.

### DEC-SIN-24
- decision: owner decision handling is click-first via project custom fields with structured PR-comment fallback (`<!-- owner-decision-v1 -->`) and label sync automation.
- rationale: reduces repetitive owner comment overhead while preserving auditable and deterministic state transitions.
- impact: PR decision flow, state-label synchronization, and owner approval queue handling.

## 5. Open Decisions
- when additional components beyond bridge, tuner, and fun-line become delivery-capable in the autonomous support matrix
- whether the repository should later move to private visibility if the cost/risk tradeoff changes
- whether low-risk PR classes should later auto-merge once the current packaged-review model has matured further
- whether project view creation for `Scale Radio Governance & Delivery` should be executed by API automation or owner one-time manual apply from the canonical blueprint
- whether PR #85 faceplate bootstrap is accepted as Phase A suggestion scope before any broader governance integration package

## 6. Runtime / Deployment Notes
- current validated deploy/rollback reference components:
  - Bridge
  - Tuner overlay/runtime/service lane
- next manual validation target with repo deploy lane ready:
  - Fun Line overlay lane (`current`)
- delivery support matrix on `main` now supports Bridge and Tuner for autonomous dispatch; Fun Line is explicitly held non-autonomous pending target-Pi deploy/rollback evidence
- autonomous deploy line remains partial at repository scope because other components are still unsupported
- owner remains the final onsite acceptance gate before stable truth is merged to `main`
- source-project artifacts remain temporarily out of deploy-lane scope and are controlled via hardware interaction rules (encoder short/long press) until full integration

## 7. Next Recommended Steps
1. normalize the separate `radio_scale_source` artifact if tuner must again ship both overlay and source as one governed lane
2. normalize the next component wrapper contract after bridge and tuner
3. keep source-project scope boundaries explicit (hardware-governed until full integration)
4. standardize immutable payload naming and governed pointer resolution across deployable components
5. enforce the 5-minute chat-to-demand continuity SLA for relevant chat outcomes and route all execution from demand artifacts
6. keep owner command surface constrained to `governed mode on | chatok | ship to codex | close demand` for governed chat lanes
