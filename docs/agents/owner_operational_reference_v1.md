# Owner Operational Reference v1

## Purpose
This is the single owner-facing page for decisions, onboarding links, governance operations, and review workflow.

## Decision and review workflow (defined)
### Where to give improvement feedback
- **Preferred:** directly on the PR as review comments (inline where possible).
- **Allowed:** in chat for quick triage or urgent steering.

### Should the PR be closed when improvements are needed?
- **No (default):** keep PR open, request changes, agent updates same branch/PR.
- **Yes (exception):** close only if scope is rejected or replaced by a new branch/topic.

### Owner merge decision contract
Use this short format in chat or PR comment:
- `decision: accept | changes-requested | reject`
- `scope: <component/governance topic>`
- `mandatory follow-up: <required change>`
- `merge authorization: yes | no`

## Are we ready to develop? (YES/NO gate)
Answer **YES** only if all are true:
1. `main` is protected and PR-gated.
2. Bootstrap reports:
   - branch = `dev/<component>` or `si/<topic>`
   - remote `git` = `https://github.com/SH99999/mediastreamer.git`
   - base sync = `ok`
   - push auth = `ok`
3. active issue/PR carries governance routing labels.
4. affected journals are updated (`current_state` + `stream`).
5. deploy/rollback evidence exists when runtime/deploy paths changed.

If one gate fails: not ready -> use blocker handling below.

## Blocker handling (Delivered-to-Git: NO)
Require exactly:
1. one blocker only
2. what is completed locally
3. one owner action only
4. no claim of pushed PR when not pushed

## Owner click-path (daily)
1. Open project board: [Scale Radio Governance & Delivery](https://github.com/users/SH99999/projects/1)
2. Review queue defined in: [Project view blueprint](../../tools/governance/scale_radio_governance_delivery_views_v1.md)
3. Open top item and verify decision packet + recommended option.
4. If accepted, approve/merge PR to `main`.
5. Confirm post-merge automation:
   - rebase workflow
   - governance closeout / decision verification comments

## Can ChatGPT issue creation be automated?
**Yes.** Intake creation/normalization/routing is workflow-backed.
- Use the governed issue templates.
- Workflows normalize labels and route/escalate automatically.
- If a connector lane cannot create issues, use fallback: package issue fields in PR + one owner action.

## Minimal owner checks (copy/paste)
```bash
bash tools/governance/agent_git_bootstrap_v1.sh
bash tools/governance/setup_auth_check_v1.sh
```
Interpretation:
- `push auth: ok` and `Auth check: result=ok` => agent can push and open PR.
- `blocked` => fix runtime auth injection or perform final push manually.

## Primary links (clickable)
### Governance core
- [AGENTS.md](../../AGENTS.md)
- [SI governance index v7](../../contracts/repo/system_integration_governance_index_v7.md)
- [Protected-main operating model](../../contracts/repo/protected_main_truth_maintenance_operating_model_v1.md)
- [Deploy process standard](../../contracts/repo/deploy_process_standard_v1.md)
- [UI/GUI governance standard](../../contracts/repo/ui_gui_governance_standard_v1.md)

### Onboarding and execution
- [SI recovery onboarding v7](./system_integration_recovery_onboarding_v7.md)
- [Agent git bootstrap guide](./agent_git_bootstrap_v1.md)
- [Codex cloud environment setup](./codex_cloud_environment_setup_v1.md)
- [Container startup setup](./container_startup_setup_v1.md)
- [Chat-to-Git delivery process](./chat_to_git_delivery_process_v1.md)
- [Connector-blocked fallback manual](./fallback_connector_blocked_manual_v1.md)

### Intake and governance automation
- [Governed demand intake template](../../.github/ISSUE_TEMPLATE/governed-demand-intake.yml)
- [UI/UX governance intake template](../../.github/ISSUE_TEMPLATE/ui-ux-and-asset-governance.yml)
- [Issue intake normalizer v2 workflow](../../.github/workflows/issue-intake-normalizer-v2.yml)
- [System integration escalation workflow](../../.github/workflows/system-integration-escalation.yml)
- [Open decision issues workflow](../../.github/workflows/open-decision-issues.yml)
- [Governance closeout workflow](../../.github/workflows/governance-closeout.yml)

### Governance panel/view references
- [Project views blueprint](../../tools/governance/scale_radio_governance_delivery_views_v1.md)
- [Project views table rendering](../../tools/governance/scale_radio_governance_delivery_views_table_v1.md)
- [Project views kanban rendering](../../tools/governance/scale_radio_governance_delivery_views_kanban_v1.md)

## Current recurring setup topics to monitor
- runtime token injection drift (`GH_TOKEN` / `GITHUB_TOKEN` not visible in active runtime session)
- branch discipline drift (agent starts on `work` instead of `dev/*` or `si/*`)
- connector-lane mismatch (issue create available but PR create blocked, or inverse)
