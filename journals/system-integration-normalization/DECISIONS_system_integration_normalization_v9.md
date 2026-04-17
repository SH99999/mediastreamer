# DECISION LOG — system_integration_normalization

Status note: this v9 file remains the current SI/N decision addendum and is updated here after tuner autonomy promotion.

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

### DEC-system_integration_normalization-23
- Status: locked
- Decision: an explicit truthful negative answer is always preferred over fabricated progress, implied completion, false confidence, or placeholder delivery.
- Date context: truthfulness alignment phase
- Why this was chosen: repo truth and acceptance quality collapse when agents hide blockers or pretend work completed.
- What it affects: all chats, Codex lanes, workflow reporting, repo-truth maintenance, and owner communication.
- What it explicitly does NOT affect: the requirement to keep working autonomously when safe execution is actually possible.
- Follow-up needed: keep this rule visible in governance and agent-facing operating docs.

### DEC-system_integration_normalization-24
- Status: locked
- Decision: Git tags are created only for accepted stable baselines and governed rollback anchors, using the format `<component-suffix>-vMAJOR.MINOR.PATCH`.
- Date context: release-tagging alignment phase
- Why this was chosen: meaningful tags improve recovery and review, while tagging every intermediate state creates noise and weakens trust in tags.
- What it affects: Git tagging practice, stable baseline marking, and rollback anchor discoverability.
- What it explicitly does NOT affect: payload pointer names such as `current_dev` and `current`, or the requirement to keep journals and release handoff fields up to date.
- Follow-up needed: add tags conservatively only when a baseline is actually accepted or locked as rollback truth.

### DEC-system_integration_normalization-25
- Status: locked
- Decision: the current GUI concept is sufficient until full integration is explicitly opened and approved through SI governance.
- Date context: UI/GUI governance stabilization phase
- Why this was chosen: dev can proceed without blocking on speculative UI redesign while still keeping UI work governed.
- What it affects: UI/GUI backlog prioritization, intake scope, and SI stream tracking.
- What it explicitly does NOT affect: the requirement that UI/GUI work follows the same branch/PR/journal governance model.
- Follow-up needed: reopen only when full integration is intentionally started.

### DEC-system_integration_normalization-26
- Status: locked
- Decision: source-project behavior remains out of deploy-lane scope for now because interaction is governed in hardware via encoder short/long press.
- Date context: tuner scope-clarification phase
- Why this was chosen: prevents false deploy-contract expectations for artifacts intentionally controlled outside the current software deploy lane.
- What it affects: tuner deploy acceptance scope, SI status wording, and next-step prioritization.
- What it explicitly does NOT affect: future inclusion of source artifacts once full integration scope is explicitly opened.
- Follow-up needed: reassess when full integration is opened.

### DEC-system_integration_normalization-27
- Status: locked
- Decision: SI/governance execution must run on a dedicated branch per package using the `si/<topic>` pattern, then push that branch and open/update PRs from that same branch to protected `main`.
- Date context: branch-governance hardening phase
- Why this was chosen: removes ambiguity from generic working branches and enforces one clear local->git branch->PR promotion path for governed SI truth changes.
- What it affects: SI branch naming, push behavior, PR routing, and onboarding expectations for replacement chats and Codex lanes.
- What it explicitly does NOT affect: component specialist branch doctrine (`dev/<component>`) or exception-only use of `integration/staging`.
- Follow-up needed: keep AGENTS, SI index, and SI onboarding aligned with this branch rule.

### DEC-system_integration_normalization-28
- Status: locked
- Decision: SI onboarding must include explicit branch `work` rejection and remote preflight requirements (`git` remote must target `https://github.com/SH99999/mediastreamer.git`) before SI push/PR handoff.
- Date context: SI onboarding clarity hardening phase
- Why this was chosen: replacement agents need deterministic branch and remote checks to avoid local-only completion or ambiguous push targets.
- What it affects: SI onboarding checklist, agent preflight behavior, and PR readiness validation.
- What it explicitly does NOT affect: component runtime deploy contracts or autonomous support-matrix gating.
- Follow-up needed: keep onboarding, AGENTS, and SI status wording synchronized when remote strategy changes.

### DEC-system_integration_normalization-29
- Status: locked
- Decision: stage-B UI/UX autonomy uses proposal-reference intake (`proposal URI/path + revision`), owner decision packet output (`decision_output_v1`), and project-view blueprint truth in-repo.
- Date context: stage-B autonomy expansion phase
- Why this was chosen: multiple UI/UX proposal iterations require deterministic, low-click owner decisions and auditable routing without chat-memory dependency.
- What it affects: issue templates, SI onboarding, UI/UX governance intake, and owner decision preparation.
- What it explicitly does NOT affect: protected-`main` owner approval gate or support-matrix delivery gating for runtime deploy.
- Follow-up needed: apply project views to `https://github.com/users/SH99999/projects/1` with owner credentials if API access is unavailable in the current execution lane.

### DEC-system_integration_normalization-30
- Status: locked
- Decision: tuner is promoted into the autonomous delivery support matrix with governed defaults `git_ref=dev/tuner`, `payload=current`, `deploy_workflow=component-test-deploy-v10.yml`, and `rollback_workflow=component-test-rollback-v10.yml`.
- Date context: tuner autonomy promotion phase
- Why this was chosen: tuner deploy and rollback are now validated on the target Pi, and `dev/tuner` is aligned with `main`, so the support matrix can safely dispatch the same governed lane autonomously.
- What it affects: autonomous delivery dispatch, issue/PR-driven tuner auto-deploy routing, and SI support-matrix truth.
- What it explicitly does NOT affect: the still-open need to normalize the separate `radio_scale_source` artifact as part of the governed tuner component contract.
- Follow-up needed: normalize the remaining source-artifact gap without disabling the validated overlay/runtime/service lane.

### DEC-system_integration_normalization-32
- Status: locked
- Decision: prompt-ready status reporting is generated from repo truth into clickable markdown pages (`reports/status/*.md`) with concise summaries and Mermaid visuals for tuner, governance, UI, bridge, decisions, and blockers.
- Date context: status-report automation phase
- Why this was chosen: owner and chats need one-prompt status outputs without manual reconstruction from multiple files.
- What it affects: status communication format, report generation tooling, and owner click-path speed.
- What it explicitly does NOT affect: protected-main approval authority or runtime deployment contracts.
- Follow-up needed: keep report generator aligned with journal/status schemas and run report generation after material status changes.
## Superseded Decisions
- The earlier v8 truthfulness addendum remains historical; this v9 file is the current release-tagging addendum plus tuner autonomy promotion update.

### DEC-system_integration_normalization-31
- Status: locked
- Decision: owner decision handling uses a click-first structured model with project custom fields and a governed fallback structured PR comment (`<!-- owner-decision-v1 -->`) synchronized by workflow.
- Date context: owner decision friction reduction phase
- Why this was chosen: repeated free-text PR comments increase owner overhead and reduce deterministic automation.
- What it affects: owner PR decision flow, state-label synchronization, governance closeout readiness, and review click-path.
- What it explicitly does NOT affect: protected-`main` merge approval authority or the requirement for docs/journal truth updates.
- Follow-up needed: keep rollback switch and robustness checks active; disable automation quickly through `OWNER_DECISION_AUTOMATION_ENABLED=false` if behavior degrades.

### DEC-system_integration_normalization-33
- Status: locked
- Decision: governance-closeout automation must require evidence-gated transitions (`source PR merged` + `governance/journal/docs truth updated`) before assigning `state:done`; otherwise it must keep issues open with `state:docs-update-required` and write an explicit audit-trail comment.
- Date context: SI TOM stabilization and queue-closeout hardening phase
- Why this was chosen: merged PR state alone can over-close queue items and produce false owner pressure when governance truth is not actually aligned.
- What it affects: governance issue lifecycle reliability, owner queue trust, and closeout workflow behavior after merged PRs.
- What it explicitly does NOT affect: explicit PR-body close keywords after all closeout conditions are satisfied.
- Follow-up needed: periodically audit legacy open SI escalation items and close stale merged-source items with documented reasons.

### DEC-system_integration_normalization-34
- Status: locked
- Decision: SI startup must use one tiered onboarding model derived from a single active authority path (AGENTS -> SI governance index -> SI TOM -> current SI status/decisions/stream); historical SI streams and superseded docs are Tier-2 deep history only.
- Date context: authority-compression onboarding hardening phase
- Why this was chosen: replacing parallel startup chains with one active path reduces misreads, lowers onboarding burden, and prevents historical docs from competing with current truth.
- What it affects: SI role prompts, bootstrap reference mapping, onboarding guidance, and historical-stream labeling discipline.
- What it explicitly does NOT affect: preservation of historical materials for forensic/audit use.
- Follow-up needed: keep active startup references pointed at current truth and enforce deep-history boundaries when new stream generations are added.

### DEC-system_integration_normalization-35
- Status: locked
- Decision: one-click owner/status packet outputs must split claims into `governance/docs accepted`, `runtime validated`, and `autonomy eligible`, and only runtime/deploy/rollback/autonomy classes are evidence-gated.
- Date context: evidence-gated one-click hardening phase
- Why this was chosen: previous one-click packets could be misread as broader runtime/autonomy validation, especially on governance/docs-only packages.
- What it affects: status packet schema, report generators, enforcement checks, and owner packet wording.
- What it explicitly does NOT affect: lightweight handling for governance/docs-only/control-plane packages that do not claim runtime/deploy/autonomy impact.
- Follow-up needed: keep packet/report contract and enforcement checks aligned when claim fields evolve.

### DEC-system_integration_normalization-36
- Status: locked
- Decision: component truth uses an explicit evidence-led claim ledger (`repo_ready_payload_present`, `deploy_ready`, `tested_on_target`, `rollback_verified`, `runtime_validated`, `autonomy_eligible`, `tested_scope`, `evidence_path`, `rollback_path`, `source_ref`) and status packets must align to that ledger.
- Date context: component evidence-ledger and claim-normalization phase
- Why this was chosen: component current-state, SI status, matrix posture, and owner/status packet wording were drifting and could overstate validation/autonomy.
- What it affects: component current-state files, autonomous support matrix wording, status packet schema/report generation, and claim consistency checks.
- What it explicitly does NOT affect: creation of new dashboards/boards/report surfaces.
- Follow-up needed: keep component claim ledgers updated whenever deploy/rollback/runtime/autonomy truth changes materially.

### DEC-system_integration_normalization-37
- Status: locked
- Decision: SI startup/onboarding uses one compressed active path with tiered scope (`Tier 0`, `Tier 1`, `Tier 2`) and active docs must not require historical/superseded material outside explicit Tier-2 deep-history use.
- Date context: authority-compression onboarding hardening completion phase
- Why this was chosen: long startup read chains and mixed active/historical references increased misread risk and onboarding burden.
- What it affects: SI governance index, onboarding v7, role bootstrap references/profiles, and startup prompt wording.
- What it explicitly does NOT affect: preservation of historical stream generations and superseded docs for forensic review.
- Follow-up needed: keep active startup references anchored to the authority chain and treat any missing startup-referenced file as a repo-truth defect.


### DEC-system_integration_normalization-38
- Status: locked
- Decision: the governed ChatGPT->Codex lifecycle is `chat -> demand -> chatok -> ready-for-codex -> in-execution -> ready-for-chatgpt-review -> pre-ok -> ready-for-owner -> closed`, with a maximum 5-minute chat-only continuity window for relevant outcomes.
- Date context: chat-to-demand autoroute and repo-continuity hardening phase
- Why this was chosen: execution drift and knowledge loss increase when decisions remain in chat memory instead of durable repo artifacts.
- What it affects: exchange demand artifacts, watcher automation, playbook/start prompts, and owner handoff sequencing.
- What it explicitly does NOT affect: creation of new dashboards/boards/html surfaces or parallel exchange systems outside `exchange/chatgpt/`.
- Follow-up needed: keep demand artifact contract, status lifecycle, and watch automation aligned as exchange tooling evolves.


### DEC-system_integration_normalization-39
- Status: locked
- Decision: governed chat mode is activated by `governed mode on`; after activation, relevant chat deltas must be persisted to `exchange/chatgpt/sessions/<topic>__live_v1.md` within 5 minutes and promoted at `chatok` to `exchange/chatgpt/demands/<topic>__intake_v1.md` with `ready-for-codex`.
- Date context: chat governed-mode and repo continuity hardening phase
- Why this was chosen: owner repetition and chat-memory-only drift remain high without a one-time activation model and live continuity artifact.
- What it affects: exchange lifecycle semantics, watcher routing, live-to-demand promotion, and owner command surface.
- What it explicitly does NOT affect: addition of dashboards/boards/html surfaces or creation of a second exchange system.
- Follow-up needed: keep session template, promotion helper, and protocol statuses aligned as exchange tooling evolves.
