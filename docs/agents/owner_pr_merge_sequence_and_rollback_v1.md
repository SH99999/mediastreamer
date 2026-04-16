# OWNER PR MERGE SEQUENCE AND ROLLBACK PLAYBOOK V1

## Purpose
Provide a low-click, governance-safe merge sequence to `main`, including explicit rollback paths for wrong decisions.

## Quick links
- [Current open PRs (repo)](https://github.com/SH99999/mediastreamer/pulls)
- [Create PR for missing SI follow-up branch](https://github.com/SH99999/mediastreamer/compare/main...si/fun-line-followups-v1?expand=1)
- [Component deploy workflow v10](../../.github/workflows/component-test-deploy-v10.yml)
- [Component rollback workflow v10](../../.github/workflows/component-test-rollback-v10.yml)
- [Deploy process standard](../../contracts/repo/deploy_process_standard_v1.md)
- [Protected-main maintenance model](../../contracts/repo/protected_main_truth_maintenance_operating_model_v1.md)
- [SI governance index](../../contracts/repo/system_integration_governance_index_v7.md)

## Topic index
- [1) Mandatory guardrails](#1-mandatory-guardrails)
- [2) PRs to open if missing](#2-prs-to-open-if-missing)
- [3) Safe merge order into main](#3-safe-merge-order-into-main)
- [4) Rollback plan if owner decision is wrong](#4-rollback-plan-if-owner-decision-is-wrong)
- [5) Owner click-path checklist](#5-owner-click-path-checklist)

## 1) Mandatory guardrails
1. Never merge from `work`.
2. SI/governance changes must come from dedicated `si/<topic>` branches.
3. Merge only through reviewed PRs to protected `main`.
4. Keep rollback possible before and after merge.

## 2) PRs to open if missing
Open a PR if this branch has no PR yet:
- `si/fun-line-followups-v1` -> `main`
- suggested title: `Stabilize status report generator outputs and merge sequence guidance`
- suggested labels: `governance`, `agent:system-integration`, `component:system-integration`, `impact:system-wide`

## 3) Safe merge order into main
Use this order to avoid governance drift and preserve rollback clarity:
1. **PR-A (first):** `si/fun-line-followups-v1` -> `main` (this branch; includes follow-up fixes and owner playbook)
2. **PR-B:** `#92` measurable deploy test strategy (if still open and green)
3. **PR-C:** `#93` tuner journal normalization (if still open and green)
4. **PR-D:** `#94` owner decision click automation (merge last because it changes control-plane decision flow)
5. **PR-E:** `#85` faceplate intake only after confirming no conflicts with newer governance docs

If any PR conflicts with already merged truth, rebase that PR branch to `main`, re-run checks, and re-review before merge.

## 4) Rollback plan if owner decision is wrong
### Runtime rollback (Pi/plugin state)
Run workflow `component-test-rollback-v10` with:
- `git_ref=main`
- `component=fun-line` (or `tuner`)
- `payload=current`
- `target=primary` (or intended slot)

### Repo-truth rollback (governance/docs/workflow state)
1. Create `si/revert-<topic>` from `main`.
2. `git revert <merge_commit_sha>` (or a bounded range if needed).
3. Open PR `si/revert-<topic>` -> `main` with clear revert rationale.
4. Merge after owner review.

### Mandatory rollback note
Do not force-push to `main`; rollback must be explicit, reviewable, and journal-traceable.

## 5) Owner click-path checklist
1. Open PR list and confirm branch/source/target are correct.
2. Merge PR-A first (`si/fun-line-followups-v1`).
3. Validate rollback workflow visibility and input defaults.
4. Merge PR-B, PR-C, PR-D, PR-E one-by-one (no batch merges).
5. After each merge, verify no open blocker in SI status and that next PR rebases cleanly.
