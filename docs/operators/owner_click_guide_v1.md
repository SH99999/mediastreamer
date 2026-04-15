# OWNER CLICK GUIDE V1

## Purpose
This file explains what the repository already automates, what the owner should click or decide, and how to interpret governance issues and workflows.

## Your role
Your role is mainly:
- approve or reject real decisions
- merge reviewed PRs into protected `main`
- run a few key manual workflows when needed
- use the issue queue as a management dashboard, not as a second source of truth

You should not need to do repetitive routing, label maintenance, branch-list maintenance, or repetitive cleanup if the repo can do it automatically.

## Core rule for issues
Issues are the **operating queue** built from repo truth.
Contracts and journals remain the actual truth source.

## What to do with created issues
### Informational only
Usually informational / monitoring issues:
- weekly governance report issues
- branch drift issues where you only need visibility before choosing to rebase
- journal freshness issues if the responsible lane can handle them without your decision

### Act / decide
You should act when an issue has labels or meaning such as:
- `state:needs-decision`
- `state:awaiting-owner`
- `impact:system-wide`
- `impact:cross-component`
- `type:decision`
- or the issue clearly asks for approval of one path over another

### After decision
Your decision should normally result in:
1. a PR updating docs/journals/workflows if needed
2. merge to `main`
3. governance closeout workflow handling the issue state automatically

## Most important workflows for you
### 1. `rebase-dev-and-integration-branches-on-main`
Use when:
- active branches have drifted behind `main`
- before starting a new dev block
What it does:
- rebases all `dev/*` and `integration/*` branches, or one selected branch, onto `main`
- pushes rebased branches back automatically
Your click pattern:
- Actions -> `rebase-dev-and-integration-branches-on-main` -> Run workflow
- choose `all` or `single`

### 2. `component-test-deploy-v6`
Use when:
- you want to test deploy a component payload to the Pi
What it does:
- checks out `main` control-plane state
- checks out the selected `git_ref` into a target dir
- deploys via repo wrapper against the selected payload
Your click pattern:
- Actions -> `component-test-deploy-v6` -> Run workflow
- choose `git_ref`, `component`, `payload`

### 3. `component-test-rollback-v6`
Use when:
- you want to remove/rollback a deployed test payload from the Pi
What it does:
- checks out `main` control-plane state
- checks out the selected `git_ref`
- runs repo rollback via wrapper

### 4. `release-readiness-audit`
Use when:
- you want a compressed readiness view before broader development or release decisions
What it does:
- checks README/current_state/stream presence
- checks branch drift
- checks open decisions
- writes a summary table

### 5. `weekly-governance-report-issue`
Use when:
- you want a current weekly management summary immediately rather than waiting for schedule
What it does:
- creates or updates one weekly governance report issue from repo truth

### 6. `issue-intake-normalizer-v2`
Use when:
- a new governed issue was created but labels/routing look wrong
- an intake issue needs manual normalization
What it does:
- reads the issue body and applies the managed labels correctly

### 7. `bootstrap-new-component`
Use when:
- a truly new governed component must be created under the repo model
What it does:
- creates the governed bootstrap structure for the new component

## Important background automation you usually do not need to run manually
- `ensure-governance-labels`
- `open-decision-issues`
- `branch-drift-issues`
- `journal-freshness-issues`
- `pr-governance-review`
- `governance-closeout`
- `issue-context-enrichment`
- `system-integration-escalation`
- `decision-verification-on-merge`
- `repo-control-plane-sanity-check`
- `autonomous-delivery-orchestrator`

These mostly keep the queue, routing, escalation, and closure loops alive in the background.

## Communication model
### Best way to communicate work
- discuss demand in chat
- create or update a governed issue if the work needs repo visibility/routing
- let labels/workflows route it
- ask the relevant specialist lane or SI lane to prepare the PR
- merge when ready

### When to escalate in chat immediately
Bring work to system integration first when it affects:
- multiple components
- workflows
- rollback/deploy rules
- governance docs
- naming/branch doctrine
- shared UX standards or shared asset rules

## Practical owner loop
1. review the issue queue and weekly report
2. decide only the items that truly need owner choice
3. let chats/agents prepare PRs
4. review/merge PRs to `main`
5. run deploy/rebase/audit workflows when needed

## What you usually do NOT need to do
- manually classify issues one by one if the intake model worked
- manually maintain label taxonomy
- manually keep a spreadsheet or parallel project memory
- manually rebase branches from your PC unless the workflow path is broken

## Current caution
The system is now strong enough to operate, but repo-truth cleanup is still important for:
- starter
- fun-line
- hardware

Those areas may still need more direct SI attention than the more automated/governed parts of the system.
