# DEPLOYMENT TEST STRATEGY STANDARD V1

## Purpose
This standard defines a measurable, repeatable deployment-test strategy for all components on the target Pi.

## Outcome
After each Pi test run, the repository should have enough structured evidence to:
- evaluate deploy and rollback quality objectively
- compare run quality over time
- generate automated summaries and charts from run outputs

## Test layers
Every test run should execute and report these layers:
1. **L0 - pipeline/branch metadata**
2. **L1 - standard deploy contract checks**
3. **L2 - component-specific verification checks**
4. **L3 - rollback verification checks** (when rollback is part of the run)

## Required run metadata
Each run should record:
- component
- branch/ref
- payload
- workflow name/run id
- target host and slot/lock context
- start/end timestamps (UTC)
- final status (`pass`|`fail`)

## Measurable success metrics
At minimum, evaluate these metrics per run:
- deploy execution duration (seconds)
- healthcheck duration (seconds)
- rollback duration (seconds, if executed)
- required-check pass ratio (`passed_checks/total_checks`)
- critical-check failures (`0` required for pass)
- service/process stability checks (all required checks pass)

## Required evidence bundle (per run)
Store a run bundle under:
`artifacts/pi-test-results/<component>/<run-id>/`

Required files:
- `summary.json` (top-level result and timing)
- `checks.jsonl` (one JSON object per check)
- `environment.txt` (branch/ref/payload/workflow/target)
- `service_status.txt` (`systemctl` snapshots for relevant services)
- `process_snapshot.txt` (`ps`/`pgrep` summary for required processes)
- `notes.md` (short context for anomalies)

## Standard + component-specific script model
For each component, use:
- standard deploy/health/rollback scripts (existing contract)
- optional component-specific verification script:
  - `deploy_candidates/verify_pi_postdeploy_v1.sh`

Execution order for deploy runs:
1. `apply_payload_v1.sh`
2. `healthcheck_runtime_v1.sh`
3. `verify_pi_postdeploy_v1.sh` (if present)

Execution order for rollback runs:
1. `remove_active_v1.sh`
2. `verify_pi_postdeploy_v1.sh --post-rollback` (if present)

## Check result contract
Each line in `checks.jsonl` should include:
- `check_id`
- `layer` (`L1`/`L2`/`L3`)
- `severity` (`critical`|`major`|`minor`)
- `status` (`pass`|`fail`)
- `value` (numeric/string measurement)
- `threshold` (if measurable)
- `message`

## Pass/fail rule
A run is `pass` only if:
- all critical checks pass
- required-check pass ratio is at least `1.0`
- deploy and healthcheck completed without script error
- rollback completed without script error when rollback is requested

## Reporting and chart generation
The run bundles are machine-readable by design.
A report generator may produce:
- markdown summary tables
- trend charts (for example Mermaid charts)
- per-component pass-rate and duration trend views

## Governance update rule
If this strategy changes a component acceptance decision:
- update component current-state + stream
- update SI status/stream where the strategy materially changes operating truth
- keep matrix and workflow references aligned in the same change set when possible
