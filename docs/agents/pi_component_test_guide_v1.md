# PI COMPONENT TEST GUIDE V1

## Purpose
This guide translates the deployment test strategy into component-level execution checklists.

Primary standard:
- `contracts/repo/deployment_test_strategy_standard_v1.md`

## Common execution flow (all components)
1. Prepare branch/ref and payload.
2. Run deploy workflow/script lane.
3. Run standard healthcheck.
4. Run component-specific verification script (`verify_pi_postdeploy_v1.sh`) when present.
5. Run rollback workflow/script lane when part of the test cycle.
6. Collect evidence bundle under `artifacts/pi-test-results/<component>/<run-id>/`.
7. Generate summary report/charts.
8. Update journals with factual results.

## Component checklists

### bridge (`dev/bridge`)
Required extra checks:
- overlay opens from intended entry path
- expected bridge runtime state appears without ownership conflicts
- cache DB path exists/reuses as expected (`bridge_cache.sqlite` if in scope)

Recommended `verify_pi_postdeploy_v1.sh` checks:
- overlay-process check
- UI path response check
- bridge cache file check

### tuner (`dev/tuner`)
Required extra checks:
- runtime plugin and renderer-service are both healthy
- source-tile checks only if explicitly in active scope

Recommended `verify_pi_postdeploy_v1.sh` checks:
- renderer service active
- runtime files present
- expected tuner process/service coupling valid

### fun-line (`dev/fun-line`)
Required extra checks:
- plugin payload files present in live path
- kiosk/chromium/Xorg runtime remains healthy after deploy

Recommended `verify_pi_postdeploy_v1.sh` checks:
- UI route render check
- process stability check over short interval

### starter (`dev/starter`)
Required extra checks:
- deploy contract normalization checks
- runtime entry and rollback clean-up checks

### autoswitch (`dev/autoswitch`)
Required extra checks:
- switching triggers and runtime behavior checks
- rollback restores previous expected state

### hardware (`dev/hardware`)
Required extra checks:
- non-deploy hardware integration checks documented as observational metrics
- no false claim of deploy support if lane is non-deploy

## Evidence bundle minimum template
For each run include:
- `summary.json`
- `checks.jsonl`
- `environment.txt`
- `service_status.txt`
- `process_snapshot.txt`
- `notes.md`

## Report generation
Use the side tool:
- `python3 tools/governance/pi_test_results_report_v1.py --root artifacts/pi-test-results --out artifacts/pi-test-results/report.md`

The report includes:
- component pass/fail summary table
- duration averages
- Mermaid chart blocks for quick visual trend review in GitHub markdown
