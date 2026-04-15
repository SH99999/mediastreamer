# STREAM — system_integration_normalization

Status note: this v6 file supersedes `stream_v5.md` as the current SI/N stream because tuner now has a real repo-driven manual deploy/rollback lane after Bridge proved the lock-aware runtime path on the Pi.

## Entries
### 2026-04-12 / main / PR #26 merged
- governance v2 docs landed on `main`
- the first repo-native SI/N status and decision files were added
- purpose: move SI/N truth out of placeholder docs and into repo form

### 2026-04-13 to 2026-04-14 / main / merged governance sequence
- branch doctrine, artifact model, naming/release numbering, SI recovery onboarding, issue governance, weekly governance reports, autonomy layer, escalation workflows, and repo sanity controls were added across the governance build-out sequence
- purpose: convert the repository into an issue-driven, workflow-backed control plane

### 2026-04-14 / main / PR #62 merged
- protected-main truth maintenance operating model was added
- SI status v6, decisions v6, and stream v2 were added
- purpose: align SI truth to the locked public + protected-main operating model

### 2026-04-15 / main / follow-up SI truth alignment
- truthful execution and negative-answer rule was added to governed repo doctrine
- Git release tagging standard was added
- governance index and recovery onboarding were refreshed to the active SI truth chain
- purpose: keep repo truth trustworthy and keep replacement SI chats on the active document chain

### 2026-04-15 / main / Bridge validation follow-up
- bridge deploy pointer resolution and lock-aware rollback recovery fixes landed through PR #67
- bridge deploy and rollback were then validated on the target Pi
- purpose: prove the lock-aware deploy/test slot model with one real reference component

### 2026-04-15 / main / Tuner deploy-lane build-out
- verified that the imported tuner payload already exists in repo at `components/scale-radio-tuner/payload/current/`
- replaced the old placeholder tuner deploy hooks with real deploy candidate scripts under `components/scale-radio-tuner/deploy_candidates/`
- added `tools/deploy/sr-deploy-wrapper-v3.sh` so bridge and tuner can both use the generic wrapper family
- added `component-test-deploy-v10.yml` and `component-test-rollback-v10.yml` for manual tuner validation on the target Pi
- updated tuner current-state and stream truth to reflect the new deploy lane and the still-open `radio_scale_source` gap
- updated SI status to reflect that bridge is validated and tuner became a real manual deploy candidate
- purpose: move the next active component from legacy placeholder deploy doctrine into an actually executable repo-driven lane without pretending Pi validation already happened

### 2026-04-15 / main / Tuner validation follow-up
- added non-interactive privileged execution support for tuner through `PI_SUDO_PASSWORD`
- tuner deploy and tuner rollback both completed successfully on the target Pi
- purpose: establish tuner as the second validated manual deploy/rollback lane while keeping autonomous promotion as a separate explicit decision

### 2026-04-15 / work / System Integration Codex intake
- opened the System Integration Codex task lane in the current workspace branch
- re-read active governance and SI onboarding contracts before any repo mutation
- purpose: preserve SI execution traceability for this Codex-run integration pass


### 2026-04-15 / work / SI role-readiness and status reconciliation
- reviewed the current SI governance chain (`system_integration_governance_index_v7`, onboarding v7, status v8, decisions v9, stream v6)
- updated onboarding v7 to match current deploy truth that tuner manual deploy and rollback are already validated on the target Pi
- documented SI stream control-plane functions explicitly so replacement Codex lanes can verify role scope before mutating repo truth
- purpose: ensure replacement SI/Codex execution starts from accurate status and explicit control-plane responsibilities

### 2026-04-15 / work / Governance unification packaging for SI + UI + deploy model
- added a split delivery plan for governance normalization bundles covering deploy process, naming/release/path, UI/GUI governance inclusion, and status/journal schema consolidation
- added a dedicated deploy process standard defining manual-to-autonomous promotion gates and matrix synchronization expectations
- added a dedicated UI/GUI governance standard so UI artifacts follow the same branch/PR/release/journal/rollback doctrine
- aligned AGENTS, SI governance index, onboarding v7, and canonical governance sources with non-main branch execution and PR-only promotion to protected main after owner coordination
- purpose: package the requested governance-model repairs as explicit repo truth instead of chat-only direction

### 2026-04-15 / work / Tuner autonomy gate activation follow-up
- enabled tuner in `tools/governance/autonomous_delivery_matrix_v3.json` with `dev/tuner` and payload `current` plus v10 deploy/rollback workflow bindings
- extended `tools/deploy/sr-deploy-wrapper-v2.sh` so tuner is no longer an unsupported component in the shared wrapper path
- tightened deploy-process governance by adding explicit autonomy-enable checks for lock-aware slot success, journal synchronization, and runtime-risk assessment
- updated tuner and SI journals to reflect that tuner autonomy is enabled for the normalized overlay/runtime/service lane while `radio_scale_source` remains an explicit gap
- purpose: move tuner into the same autonomy loop class as bridge without hiding the remaining multi-artifact normalization debt

### 2026-04-15 / work / UI governance stream activation
- created `journals/system-integration-normalization/ui_gui_stream_v1.md` as the dedicated SI stream for UI/GUI governance standards and dependency tracking
- updated UI/GUI governance standard to include explicit scope boundaries and mandatory SI stream logging for cross-component UI governance decisions
- aligned SI governance index, onboarding read order, and SI status mapping to include the new UI/GUI governance stream path
- purpose: ensure UI/GUI governance truth is explicitly journaled and dependency-traceable instead of implicit in generic SI notes

### 2026-04-15 / work / UI scope and source-scope clarification follow-up
- recorded that the current GUI concept is sufficient until full integration is explicitly opened
- aligned SI status/onboarding and tuner journals so source-project behavior is explicitly out of deploy-lane scope and hardware-governed (encoder short/long press) for now
- purpose: remove ambiguity in open decisions and keep dev-start scope aligned with owner instructions

### 2026-04-15 / work / Fun Line deploy-lane activation
- added Fun Line deploy candidate scripts and a governed `payload/current` pointer so lock-aware deploy/rollback tests can run through the repo wrapper lane
- extended wrapper support (`sr-deploy-wrapper-v2.sh` and `sr-deploy-wrapper-v3.sh`) so `fun-line` can execute deploy and rollback like bridge/tuner
- updated autonomous delivery matrix v3 and v10 workflow defaults so Fun Line can be selected directly for manual target-Pi deploy and rollback tests
- purpose: make Fun Line the next runnable deploy/test/rollback lane in the autonomous governance path

### 2026-04-15 / si/governance-branch-model / SI branch-governance hardening
- locked the SI rule that governance/control-plane changes must run on dedicated `si/<topic>` branches, then push and open/update PRs from that same SI branch to protected `main`
- aligned AGENTS, branch strategy, SI governance index, and SI onboarding with the same local -> branch -> PR operating path
- updated SI decision and status truth to include the explicit SI branch naming requirement as a governed operating constraint
- purpose: enforce a single, auditable branch path for autonomous SI/governance execution

### 2026-04-15 / si/governance-branch-model / SI onboarding branch+remote preflight clarification
- added explicit onboarding and AGENTS rules that branch name `work` is invalid for SI-governance truth mutations and must be replaced by `si/<topic>` before continuing
- added mandatory remote preflight check requiring remote `git` to point to `https://github.com/SH99999/mediastreamer.git` before push/PR handoff
- updated SI decision/status truth with the new onboarding clarity constraint for replacement agent lanes
- purpose: close the remaining onboarding ambiguity about branch naming and push target remote for SI agents

### 2026-04-15 / si/governance-branch-model / Stage-B UI/UX autonomy expansion
- added `contracts/repo/ui_ux_stage_b_autonomous_loop_standard_v1.md` to define proposal-reference intake, owner decision packet contract, and deterministic routing outputs
- extended governed intake templates with proposal URI/revision and explicit decision options for low-click owner approval preparation
- added canonical project-view blueprint `tools/governance/scale_radio_governance_delivery_views_v1.md` for project `Scale Radio Governance & Delivery`
- updated SI governance index, onboarding, and SI decision/status truth to include stage-B autonomy operating rules and project-view setup boundary
- purpose: prepare repeatable UI/UX iteration handling without relying on chat memory or manual copy/paste loops

### 2026-04-15 / si/project-views-rendering / Project view renderings added to repo truth
- added table-rendered and kanban-rendered companions for the project-view blueprint so owner can review view definitions directly in Git without jumping into project UI first
- linked canonical blueprint to companion renderings for deterministic cross-reference
- purpose: make project-view setup auditable and quickly reviewable in markdown render form

### 2026-04-15 / si/project-views-multicomponent / Project views generalized beyond UI-only routing
- updated project-view blueprint and companion renderings so intake triage covers UI/UX and component/runtime lanes using existing `agent:*` labels
- added a dedicated `Component Delivery Readiness` view definition keyed by component + release-readiness/defect/integration-risk labels
- aligned Stage-B autonomy standard and SI onboarding checklist wording so proposal intake and owner decision packets are explicitly multi-component, not UI-only
- purpose: keep one project as the control-plane for all governed components instead of a UI-only queue subset

### 2026-04-15 / si/agent-bootstrap-git / Agent git bootstrap and first-reply contract
- added `tools/governance/agent_git_bootstrap_v1.sh` to standardize canonical remote setup and quick push-auth probing at session start
- added `docs/agents/agent_git_bootstrap_v1.md` with mandatory first reply format (`ready now` + exact `owner action needed`)
- aligned AGENTS, SI governance index, and onboarding read chain so every replacement agent runs bootstrap and immediately reports blockers instead of delaying with implicit assumptions
- purpose: ensure all development/governance lanes can self-prepare branch+remote flow and ask for exactly the missing owner action when runtime auth is absent

### 2026-04-15 / si/pr83-followup / PR83 review-comment fixes
- updated `agent_git_bootstrap_v1.sh` so canonical SSH and HTTPS remote forms are treated as equivalent and existing working SSH remotes are not forcibly rewritten
- purpose: avoid breaking already-working SSH-auth environments when mandatory bootstrap is executed

### 2026-04-15 / si/agent-bootstrap-git / zero-click rebase automation follow-up
- updated `rebase-dev-and-integration-branches-on-main.yml` so branch rebasing auto-triggers on every push to `main` (while preserving manual dispatch)
- updated `agent_git_bootstrap_v1.sh` to auto-fetch and rebase `si/*`, `dev/*`, and `integration/*` branches onto latest `git/main` at session start when the working tree is clean
- updated bootstrap/onboarding docs to require reporting `base sync` status in the first owner-facing reply
- purpose: minimize owner clicks after merge by keeping repo branches and agent local bases current by default

### 2026-04-15 / main / Tuner autonomy promotion
- tuner was promoted into the autonomous delivery support matrix
- matrix defaults were fixed to `dev/tuner` plus payload `current`
- bridge matrix defaults were refreshed to the currently validated v9 workflow pair
- purpose: keep execution moving forward without a manual-only holding pattern once the validated runtime lane already exists

### 2026-04-15 / si/chatgpt-intake-prompt / URI-based owner prompt for governed intake
- added `docs/agents/chatgpt_governed_intake_prompt_v1.md` with minimal and strict templates so owner can provide one structured input and avoid repeated copy/paste from external chats
- updated Stage-B autonomy standard to require URI-based intake fields and explicit agent execution expectations through PR-ready handoff
- updated SI onboarding read order/checklist to include the new prompt contract for external ChatGPT proposal ingestion
- purpose: make proposal handoff deterministic so agents can take over Git/governance lifting and leave owner with approval-only action

### 2026-04-15 / si/chat-delivery-instructions / explicit delivered-to-git status contract
- added `docs/agents/chat_to_git_delivery_process_v1.md` with exact ordered execution steps (bootstrap, branching, mutation, validation, push, PR) and mandatory final status blocks
- updated `docs/agents/chatgpt_governed_intake_prompt_v1.md` to require explicit `Delivered to Git: YES/NO` reporting with branch/commit/PR or blocker+owner-action
- updated SI governance index and SI onboarding read chains to include the new chat-to-git process document
- purpose: remove ambiguity for external chats and force one clear owner-facing statement about whether delivery reached Git or is blocked

### 2026-04-15 / si/container-startup-setup-v1 / container startup setup normalization
- added `tools/governance/container_startup_setup_v1.sh` to provide deterministic runtime initialization for cloud agents
- script now aligns both remotes (`git` canonical + `origin` compatibility), runs bounded npm dependency installs only on payload paths with `package.json`, and executes bootstrap/auth diagnostics
- added `docs/agents/container_startup_setup_v1.md` with one-command usage and environment variable contract
- updated SI onboarding and SI governance index read chains to include the new container startup setup document
- purpose: avoid startup stalls in generic setup phases and reduce repeated owner troubleshooting for runtime auth/remote drift

### 2026-04-15 / si/container-startup-fix / cloud startup non-blocking and auth probe hardening
- updated `tools/governance/container_startup_setup_v1.sh` to default `RUN_NPM_INSTALL=false` so startup does not hang on dependency installation; bounded npm install remains opt-in via env flag
- added `tools/governance/setup_auth_check_v1.sh` and integrated token-aware dry-run probing so runtime can verify whether env token auth is actually usable for push
- updated bootstrap logic to retry push auth probe with authenticated HTTPS URL when `GH_TOKEN`/`GITHUB_TOKEN` exists but credential helpers are unavailable
- updated container startup documentation with explicit Codex cloud behavior notes (setup-only token visibility vs runtime availability) and startup recommendations
- purpose: make cloud runtime startup deterministic and prevent repeated false-negative "push auth blocked" loops caused by setup/runtime auth mismatch

### 2026-04-15 / si/container-startup-fix / codex-cloud environment setup clarification
- updated startup script to skip clone unless `ALLOW_CLONE_IF_MISSING=true`, reducing risk of blocking startup when repo is not yet mounted
- published explicit owner-facing Codex cloud setup checklist in `docs/agents/codex_cloud_environment_setup_v1.md` with exact env vars and minimal custom startup wrapper
- updated container startup documentation and onboarding/index read chains to point to the new cloud setup checklist
- purpose: provide one clear configuration path (auto setup preferred, minimal custom wrapper optional) so agents start reliably without environment-level trial and error

### 2026-04-15 / si/onboarding-prompts-all-streams / unified stream onboarding prompts
- added `docs/agents/onboarding_prompts_all_streams_v1.md` with exact copy/paste onboarding prompts for all active stream lanes (SI, GUI/UI, bridge, tuner, fun-line, starter, autoswitch, hardware)
- included a dedicated GUI/UI onboarding prompt and shared Delivered-to-Git completion contract for deterministic owner-facing status
- updated SI governance index and SI onboarding read order to include the new all-stream prompt catalog
- purpose: provide one canonical prompt source so owner can spin up any stream agent without retyping lane-specific governance constraints

### 2026-04-15 / si/onboarding-prompts-all-streams / connector-blocked fallback manual
- added `docs/agents/fallback_connector_blocked_manual_v1.md` with exact fallback sequence for connector/write failures (issue create blocked, push blocked, PR create blocked)
- codified deterministic packaging of missing GitHub mutations into repo artifacts plus one-action owner handoff in `Delivered to Git: NO` format
- updated SI governance index and onboarding read order to include the fallback manual in canonical agent startup docs
- purpose: keep delivery truthful and operational when ChatGPT/Codex lanes cannot mutate GitHub directly due connector limitations

### 2026-04-15 / si/cloud-startup-quickfix / startup diagnostics decoupled from container boot
- updated `tools/governance/container_startup_setup_v1.sh` to skip governance diagnostics by default (`RUN_GOVERNANCE_DIAGNOSTICS=false`) so container startup cannot stall on bootstrap/auth checks
- updated cloud setup docs to include the new env flag and explicit post-start verification flow (`agent_git_bootstrap_v1.sh` + `setup_auth_check_v1.sh`)
- documented why branch-only docs can show GitHub 404 when opened via `main` URLs before merge, with guidance to use PR branch/files-changed view
- purpose: keep Codex cloud startup deterministic while preserving governance diagnostics as explicit, operator-triggered checks after boot

### 2026-04-15 / si/bootstrap-branch-prep / prevent refspec-missing startup failures
- updated `tools/governance/agent_git_bootstrap_v1.sh` to accept an optional requested branch argument (`si/*`, `dev/*`, `integration/*`) and automatically prepare that branch before push steps
- branch prep behavior now checks out remote branch when available, otherwise creates requested branch from `git/main`
- updated `docs/agents/agent_git_bootstrap_v1.md` to document branch-target mode and the new `branch prep` status line in required first reply format
- purpose: avoid repeated `src refspec ... does not match any` failures when agents start on non-target branches like `work`

### 2026-04-15 / si/bootstrap-push-auth-fallback / token-backed git push probing
- updated `tools/governance/agent_git_bootstrap_v1.sh` so when `GH_TOKEN`/`GITHUB_TOKEN` exists but plain HTTPS push auth fails, bootstrap configures a local repo credential helper and retries push probing
- fallback now also tests tokenized HTTPS URL probe and reports explicit detail (`configured credential helper...` vs `token present but push dry-run failed`)
- updated agent/cloud setup docs to reflect this behavior and reduce false `push auth: blocked` statuses in Codex cloud sessions
- purpose: let agent lanes with valid env tokens push with standard `git push -u git <branch>` instead of failing on username prompt
