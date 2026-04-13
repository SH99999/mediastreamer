# CURRENT STATE — scale-radio-starter

## Component
- normalized component name: `scale-radio-starter`
- governed role: startup/runtime glue and boot-handover component
- active baseline class: accepted stable starter line plus archived experiment lines
- repo work lane: `dev/starter` exists; accepted baseline is conceptually main-truth-ready but repo mapping still needs stricter normalization

## Repo truth
- dedicated branch `dev/starter` exists
- starter legacy handover confirms a stable accepted baseline, but repository path/payload mapping is still not cleanly grounded from the surviving chat context
- this component currently needs journal truth more than new architecture work

## Lifecycle status
- `payload_partial`
- `functional_acceptance_open`

## Accepted baseline
- `mediastreamer_bootdelay_fix_v0.1.0`
- `mediastreamer_hybrid_startup_standby_v0.2.2_stable`
- stable target preference:
  - `http://127.0.0.1:4004/` first
  - `http://127.0.0.1:3000/` fallback

## Current known working behavior
- `bootdelay=0` on the accepted line
- hybrid runtime starts through a `volumio-kiosk` drop-in and hybrid wrapper
- `mediastreamer-shellctl standby`, `wake`, and `status` are the authoritative runtime controls
- stable line is functionally accepted even if startup visuals are not yet appliance-grade

## Current gaps
- exact repo component-path and payload normalization still need confirmation against Git truth
- exact stable asset inventory for `v0.2.2 stable` remains uncertain in the surviving context
- later appliance/direct-now-playing lines are explicitly nonleading and should remain archived/experimental only
- deep idle, FPS cap, and render-throttling must remain unresolved here unless grounded by another specialist lane

## Repo-normalized next action
1. re-ground the actual starter payload/source tree in the repository
2. preserve `v0.1.0 + v0.2.2 stable` as the only active baseline
3. keep later startup variants archived as nonleading
4. avoid claiming performance/runtime truths from this lane that were not actually validated here
