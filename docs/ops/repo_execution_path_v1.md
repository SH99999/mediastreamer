# REPO EXECUTION PATH V1

## Purpose
This document is the short operating path for any specialist chat that needs to continue development from the repository.

## Read order
1. `contracts/repo/branch_strategy_v1.md`
2. `contracts/volumio4/volumio4_plugin_config_contract_v1.md`
3. `contracts/hardware/hardware_config_contract_v2.md`
4. `contracts/coding/coding_standard_v1.md`
5. `contracts/gui/gui_foundation_v1.md`
6. `contracts/observability/performance_status_matrix_v1.md`
7. `contracts/deployment/deployment_decisions_v1.md`
8. `docs/ops/release_creation_path_v1.md`

## Branch rules
- `main` = stable, manually runnable workflows live here
- `integration/staging` = integration-owned control-plane work
- `dev/<component>` = component development and payload work

## Required workflow model
- workflows live on `main`
- workflows accept a branch/ref input
- operator runs workflows manually from the Actions UI
- workflow checks out the selected branch/ref and executes the selected payload/scripts from there

## Release path
1. work on `dev/<component>`
2. add exact extracted payload files under `components/<component>/payload/<release_name>/`
3. make deploy candidate scripts work from that payload
4. run deploy workflow from `main` against `dev/<component>`
5. test on Pi
6. if not acceptable, run rollback workflow
7. only then open a focused PR to `main`

## Access expectation for specialist chats
A specialist chat must be able to:
- read the repository contracts and current payloads
- commit to its `dev/<component>` branch
- open a PR when the release is stable enough

The operator must be able to:
- run the workflows from `main`
- inspect results
- trigger rollback

## Important limit
Repository documentation can standardize the process, but it does not grant GitHub tool access by itself. If a specialist chat cannot write to Git directly, it must still produce repo-ready output and hand it to the integration chat or the operator for commit.
