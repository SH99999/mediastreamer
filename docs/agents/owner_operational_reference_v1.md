# Owner Operational Reference v1

## Purpose
This is the single owner-facing page for decisions, onboarding links, governance operations, and review workflow.

## Owner role boundary (non-negotiable)
- Owner is expected to decide, not to execute PR mechanics.
- Agents/chats/Codex lanes must create/update branches and PRs and deliver decision-ready packets.
- Owner action is limited to decision (`accept | changes-requested | reject`) and optional merge authorization.
- If PR creation/update is blocked by connector/auth issues, the agent must report it explicitly and provide one fallback action request.
- Protected truth rule: only owner merges to `main`; agents prepare everything up to merge-ready state.

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


## Click-based owner decision (project/custom-field compatible)
Preferred: set decision via project custom fields.
Fallback: post this structured PR comment block:

```text
<!-- owner-decision-v1 -->
decision: accept
merge_authorization: yes
docs_journals_complete: yes
```

Automation syncs labels/state from this block through `owner-decision-click-sync.yml`.
Rollback switch: set repository variable `OWNER_DECISION_AUTOMATION_ENABLED=false` to disable automation and return to manual labeling/comments.

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
3. Open top item and use the prepared **SI Merge Request executive summary** packet (direct MR link + files-changed link + executive summary + risk + rollback).
4. If accepted, approve/merge PR to `main` (PR prepared and maintained by the agent lane).
5. Confirm post-merge automation:
   - rebase workflow (`si/*`, `dev/*`, `integration/*`)
   - governance closeout / decision verification comments
6. If an agent resumes after `main` changed, require bootstrap refresh (`agent_git_bootstrap_v1.sh`) so branch base is current before new edits.
7. Require merged short-lived `si/*` branch cleanup (local + remote), unless an explicit retention exception is documented.

Packet contract:
- [SI merge request executive summary v1](./si_merge_request_executive_summary_v1.md)

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
- [Status prompt/report automation guide](./status_prompt_reports_v1.md)

### Intake and governance automation
- [Governed demand intake template](../../.github/ISSUE_TEMPLATE/governed-demand-intake.yml)
- [UI/UX governance intake template](../../.github/ISSUE_TEMPLATE/ui-ux-and-asset-governance.yml)
- [Issue intake normalizer v2 workflow](../../.github/workflows/issue-intake-normalizer-v2.yml)
- [System integration escalation workflow](../../.github/workflows/system-integration-escalation.yml)
- [Open decision issues workflow](../../.github/workflows/open-decision-issues.yml)
- [Governance closeout workflow](../../.github/workflows/governance-closeout.yml)
- [owner-decision-click-sync workflow](../../.github/workflows/owner-decision-click-sync.yml)
- [governance-model-robustness-check-v1 workflow](../../.github/workflows/governance-model-robustness-check-v1.yml)

### Governance panel/view references
- [Project views blueprint](../../tools/governance/scale_radio_governance_delivery_views_v1.md)
- [Project views table rendering](../../tools/governance/scale_radio_governance_delivery_views_table_v1.md)
- [Project views kanban rendering](../../tools/governance/scale_radio_governance_delivery_views_kanban_v1.md)

## Prompt-ready status pages
Use these prompt aliases in ChatGPT/Codex:
- `status tuner`
- `status governance`
- `status ui`
- `status bridge`
- `status decisions`
- `status blocker`

Generated pages:
- [Status index](../../reports/status/index.md)
- [Status tuner](../../reports/status/tuner.md)
- [Status governance](../../reports/status/governance.md)
- [Status ui](../../reports/status/ui.md)
- [Status bridge](../../reports/status/bridge.md)
- [Status decisions](../../reports/status/decisions.md)
- [Status blocker](../../reports/status/blocker.md)
## Current recurring setup topics to monitor
- runtime token injection drift (`GH_TOKEN` / `GITHUB_TOKEN` not visible in active runtime session)
- branch discipline drift (agent starts on `work` instead of `dev/*` or `si/*`)
- connector-lane mismatch (issue create available but PR create blocked, or inverse)
