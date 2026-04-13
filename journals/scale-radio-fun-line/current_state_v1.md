# CURRENT STATE — scale-radio-fun-line

## Component
- normalized component name: `scale-radio-fun-line`
- governed role: overlay / experience-layer component
- governed artifact pattern: runtime overlay plus source/open-entry pattern, with future visual packs possible
- active work lane: `dev/fun-line`

## Repo truth
- dedicated branch `dev/fun-line` exists
- legacy handover confirms the runtime baseline and decision set strongly, but repo payload normalization remains incomplete and should be treated as an active normalization task
- this component should remain dev-only for now

## Lifecycle status
- `payload_partial`
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
- exact repo-normalized payload paths for overlay/source/packs remain unresolved
- component must remain carefully coordinated with tuner so two heavy active renderers are never running simultaneously

## Repo-normalized next action
1. normalize repo truth around `0.4.2` only
2. mark later 0.5.0 and 0.6.0 lines as nonleading/partial in repo docs
3. preserve existing encoder/GPIO open-close hooks unchanged
4. reintroduce only one production visual pass first: Dog Line
