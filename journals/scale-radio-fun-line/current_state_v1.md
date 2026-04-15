# CURRENT STATE — scale-radio-fun-line

## Component
- normalized component name: `scale-radio-fun-line`
- governed role: overlay / experience-layer component
- governed artifact pattern: runtime overlay plus source/open-entry pattern, with future visual packs possible
- active work lane: `dev/fun-line`

## Repo truth
- dedicated branch `dev/fun-line` exists
- repo payload pointer now exists at `components/scale-radio-fun-line/payload/current/` for governed deploy testing
- repo deploy candidate scripts now exist for apply/healthcheck/remove under `components/scale-radio-fun-line/deploy_candidates/`
- component remains in manual validation stage until target-Pi deploy and rollback evidence is recorded

## Lifecycle status
- `payload_complete`
- `deployment_candidate_started`
- `deploy_ready`
- `functional_acceptance_open`

## Accepted baseline
- authoritative runtime baseline: `0.4.2`
- Dog Line is the first production actor to carry forward

## Current known working behavior
- browser tile open works on the validated baseline
- GPIO / encoder open-close path works on the validated baseline
- radio playback remains stable while Fun Linea opens on the validated baseline
- overlay coordination with Radio Scale was validated enough to escape the earlier audio slowdown/conflict state
- open/close public hooks are part of the locked integration contract

## Current gaps
- later 0.5.0 and 0.6.0 lines are not authoritative runtime baselines
- config pages repeatedly failed and remain non-authoritative
- importer/catalog workflow must be treated as unvalidated/non-working
- payload path is normalized for deploy testing, but target-Pi validation evidence is still pending
- component must remain carefully coordinated with tuner so two heavy active renderers are never running simultaneously

## Repo-normalized next action
1. run target-Pi manual deploy test via `component-test-deploy-v10.yml` for `fun-line/current`
2. run target-Pi manual rollback test via `component-test-rollback-v10.yml` for `fun-line/current`
3. record deploy/rollback evidence in stream and SI status before autonomous promotion is treated as fully validated
4. preserve existing encoder/GPIO open-close hooks unchanged and keep Dog Line as first production actor
