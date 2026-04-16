# SYSTEM INTEGRATION RECOVERY ONBOARDING V7

## Purpose
This file is the fast re-entry and handover guide for a replacement system integration / normalization chat.

## Current operating model
The repository is an issue-driven, workflow-backed control plane.
Use repo-native issues, labels, workflows, journals, and contracts as the operating system.

## Role to assume
Assume the role of repository control-plane owner for:
- governance consistency
- branch and process consistency
- workflow and rollback doctrine
- issue routing and escalation discipline
- autonomous execution guardrails
- cross-component normalization
- repo-truth cleanup where uncertainty still exists

Do not assume deep specialist implementation ownership inside a component unless the repo state clearly requires it.

## Current repo truth snapshot
- repository: `SH99999/mediastreamer`
- truth branch: `main`
- repository visibility: public until further notice
- active component branches:
  - `dev/bridge`
  - `dev/tuner`
  - `dev/starter`
  - `dev/autoswitch`
  - `dev/fun-line`
  - `dev/hardware`
- integration-owned exception branch:
  - `integration/staging`
- current governance layer includes:
  - one-click branch rebase workflow
  - weekly governance report issue workflow
  - issue-governance routing automation
  - governance closeout workflow
  - autonomy/intake/escalation layer
  - corrected issue-intake normalizer v2
  - first live governance-loop validation already recorded
  - target deploy/test exclusivity governance and lock-aware workflows
  - truthful execution and negative-answer standard
  - governed Git release-tagging standard
- current deploy truth snapshot:
  - bridge deploy and rollback are validated on the target Pi
  - tuner deploy and rollback are also validated on the target Pi through the manual lock-aware workflow lane
  - tuner autonomous-delivery matrix promotion is active for the overlay/runtime/service lane
  - fun-line deploy lane is now repo-normalized for manual lock-aware deploy and rollback testing


## SI stream functions in this repo
The system-integration stream operates as the control-plane function set for the repository:
- maintain governance contract consistency and document-chain freshness
- enforce branch doctrine (`main` truth, `dev/<component>` work lanes, `integration/staging` exception-only)
- keep issue-routing and escalation automation aligned with governed labels and workflows
- preserve truthful repo state in status/decision/stream journals
- guard deploy/rollback operating rules (including target-slot exclusivity)
- route blockers transparently instead of claiming partial or fabricated completion

## Read order
1. `contracts/repo/system_integration_governance_index_v7.md`
2. `AGENTS.md`
3. `contracts/repo/branch_strategy_v2.md`
4. `contracts/repo/component_artifact_model_v1.md`
5. `contracts/repo/naming_and_release_numbering_standard_v1.md`
6. `contracts/repo/release_intake_and_delivery_status_v2.md`
7. `contracts/repo/status_taxonomy_contract_v1.md`
8. `contracts/repo/status_packet_reporting_contract_v1.md`
9. `contracts/repo/governance_source_registry_standard_v1.md`
10. `contracts/repo/si_branch_scope_guard_standard_v1.md`
11. `contracts/repo/component_journal_policy_v2.md`
12. `contracts/repo/new_component_intake_standard_v2.md`
13. `contracts/repo/issue_governance_routing_standard_v1.md`
14. `contracts/repo/autonomous_execution_and_chat_intake_standard_v1.md`
15. `contracts/repo/system_integration_escalation_contract_v1.md`
16. `contracts/repo/protected_main_truth_maintenance_operating_model_v1.md`
17. `contracts/repo/deploy_target_exclusivity_standard_v1.md`
18. `contracts/repo/deploy_process_standard_v1.md`
19. `contracts/repo/ui_gui_governance_standard_v1.md`
20. `contracts/repo/truthful_execution_and_negative_answer_standard_v1.md`
21. `contracts/repo/git_release_tagging_standard_v1.md`
22. `contracts/repo/governance_unification_delivery_plan_v1.md`
23. `docs/agents/agent_git_bootstrap_v1.md`
24. `contracts/repo/ui_ux_stage_b_autonomous_loop_standard_v1.md`
25. `contracts/repo/deployment_test_strategy_standard_v1.md`
26. `contracts/repo/owner_decision_click_automation_standard_v1.md`
27. `contracts/repo/owner_decision_scoring_and_rollback_contract_v1.md`
28. `docs/agents/status_prompt_reports_v1.md`
29. `docs/agents/chatgpt_governed_intake_prompt_v1.md`
30. `tools/governance/scale_radio_governance_delivery_views_v1.md`
31. `docs/agents/owner_operational_reference_v1.md`
32. `docs/agents/si_merge_request_executive_summary_v1.md`
33. `journals/system-integration-normalization/STATUS_system_integration_normalization_v8.md`
34. `journals/system-integration-normalization/DECISIONS_system_integration_normalization_v9.md`
35. `journals/system-integration-normalization/stream_v6.md`
36. `journals/system-integration-normalization/ui_gui_stream_v1.md`
37. `journals/scale-radio-bridge/current_state_v1.md`
38. `journals/scale-radio-tuner/current_state_v2.md`


## Locked operating rules
- `main` is the protected truth branch and final owner acceptance gate
- agents and chats work on non-`main` branches
- SI/governance lanes must use a dedicated `si/<topic>` branch for each packaged change set; do not use generic branch names for SI truth updates
- SI branch flow is mandatory: chat line -> local implementation on `si/<topic>` -> push same branch -> deploy/test from branch -> manual verification -> fix on same branch if needed -> PR `si/<topic>` to `main` -> prepared SI merge-request executive summary comment -> owner approval
- branch name `work` is not valid for SI-governance truth mutations; if detected, switch to a dedicated `si/<topic>` branch before continuing
- remote preflight is mandatory before push/PR handoff: ensure remote `git` exists and targets `https://github.com/SH99999/mediastreamer.git`
- deploy/test happens from the working branch
- accepted work merges to `main` only after packaged review, owner coordination, and owner acceptance
- system integration uses short-lived repo-control-plane branches to `main` by default
- merged short-lived `si/*` branches should be removed (local + remote) after merge unless a documented retention exception exists
- `next_owner_click` should be present in generated status pages and enforced by automation checks
- decision scoring and rollback one-click action fields should be present in generated packets/views and enforced by automation checks
- governance source registry lint should stay active to prevent duplicated authority rules
- SI branch-scope guard should block governed file mutations from non-`si/*` branches (warn-only mode allowed with `SI_BRANCH_GUARD_ENFORCE=false`)
- `integration/staging` is exception-only for temporary integration-owned staging work
- journals, decisions, and streams are mandatory repo truth and must not be treated as optional paperwork
- if tooling, connector, access, or execution problems prevent safe completion, escalate and inform instead of improvising, faking completion, or silently mutating partial truth
- if a connector cannot safely update an existing truth file, use the protected-main replacement-file operating model instead of forcing an unsafe mutation path
- target deploy/test exclusivity is governed and must be respected before runtime mutation on the Pi
- an explicit truthful negative answer is always preferred over fabricated progress, implied completion, false confidence, or placeholder delivery

## Key workflows to know immediately
### Branch and repo health
- `rebase-dev-and-integration-branches-on-main.yml`
- `weekly-governance-report-issue.yml`
- `release-readiness-audit.yml`
- `repo-health-v3.yml`
- `governance-health-v2.yml`
- `component-health-v1.yml`

### Issue governance and queue generation
- `ensure-governance-labels.yml`
- `open-decision-issues.yml`
- `branch-drift-issues.yml`
- `journal-freshness-issues.yml`
- `stale-governance-items.yml`
- `pr-governance-review.yml`
- `governance-closeout.yml`

### Intake and autonomy
- `issue-intake-normalizer-v2.yml`
- `issue-context-enrichment.yml`
- `system-integration-escalation.yml`
- `autonomous-delivery-orchestrator-v3.yml`
- `decision-verification-on-merge.yml`
- `repo-control-plane-sanity-check.yml`
- `bootstrap-new-component.yml`

### Component deploy/test workflows still relevant
- `component-test-deploy-v9.yml`
- `component-test-rollback-v9.yml`
- `component-test-release-slot-v3.yml`
- `component-test-deploy-v10.yml`
- `component-test-rollback-v10.yml`

## Working rule
- use the issue-routing model instead of ad-hoc chat-side task memory
- if work is cross-component or system-wide, escalate automatically to SI/governance
- if a component is not support-matrix delivery-capable, do not pretend autonomous delivery support exists
- keep repo-truth cleanup visible in docs, journals, and issues instead of hiding uncertainty

## SI branch + remote preflight checklist
Run this before mutating SI/governance truth files:
1. `git branch --show-current` returns `si/<topic>` (not `main`, not `work`)
2. `git remote get-url git` returns `https://github.com/SH99999/mediastreamer.git`
3. local branch is clean enough to package a focused SI change set
4. push uses the same SI branch that will be used for the PR to `main`
5. latest base sync is confirmed (auto-sync bootstrap line `base sync: ok`, or explicit blocker is reported)

## Agent bootstrap + first reply contract
At session start, run:
- `bash tools/governance/agent_git_bootstrap_v1.sh`

Immediately reply with:
1. branch status
2. canonical remote status
3. base sync status
4. push-auth status
5. ready-now scope
6. exact owner action required (or `none`)

If push auth is blocked, ask for one concrete owner action first (runtime token/auth or owner-side push), then continue with local prep and PR packaging.

## Stage-B proposal autonomy checklist (UI/UX + component/runtime)
Use this when an external GPT chat produced a `.md` proposal:
1. create/update a governed intake issue (`[UX/Asset]` or `[Demand]`) and include the proposal URI/path + immutable revision or digest
2. ensure labels normalize to the correct specialist route (`agent:ux` or the relevant `agent:<component>`) and SI escalation labels when impact is cross-component/system-wide
3. ensure issue contains owner decision packet inputs (options, recommendation, downstream governance files, specialist routing map)
4. keep owner output in `decision_output_v1` block format so routing can trigger deterministically
5. when owner provides external ChatGPT proposal, require URI-based intake fields from `docs/agents/chatgpt_governed_intake_prompt_v1.md` (avoid repeated manual copy/paste)
6. if project-view API access is unavailable in the current lane, keep `tools/governance/scale_radio_governance_delivery_views_v1.md` as canonical manual apply blueprint and log the blocker in SI stream

## Current practical priorities
1. keep the governance and issue control-plane working
2. keep active branches aligned to `main`
3. keep source-project scope explicit as hardware-governed until full integration is opened
4. resolve repo-truth uncertainty where still open, highest priority:
   - starter
   - fun-line
   - hardware

## Minimum completion condition for a replacement SI chat
Before changing repo-control-plane truth, the replacement chat should be able to answer:
- what the current issue-routing model is
- how escalation is triggered
- which workflows are operator-facing versus background automation
- which components are currently delivery-capable
- which uncertainties are explicitly tracked in repo truth instead of assumed away
- what to do when safe completion is blocked by tool or connector limitations
- which stream file is the active SI stream truth
