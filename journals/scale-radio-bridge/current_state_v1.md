# CURRENT STATE — scale-radio-bridge

## Component
- normalized component name: `scale-radio-bridge`
- primary payload/plugin identity: `radioscale_overlay_bridge`
- governed artifact role: provider-layer overlay component with bridge/runtime behavior
- current work lane: `dev/bridge`

## Repo truth
- component root exists at `components/scale-radio-bridge/`
- dedicated branch `dev/bridge` exists and is the active component work lane
- this component already has the most mature repo-driven deploy/rollback lane in the repository

## Lifecycle status
- `payload_complete`
- `deployment_candidate_started`
- `deploy_ready`
- `tested_on_pi`
- `functional_acceptance_open`

## Accepted baselines
- rollback anchor: `rsob_022sf22l.zip`
- conservative current dev continuation: `radioscale_overlay_bridge_0.2.3_db_cache_r1.zip`
- authoritative provider posture: LRCLIB lyrics provider, conservative Spotify behavior, additive SQLite sidecar only

## Current known working behavior
- installable Volumio plugin artifact exists and runs as `radioscale_overlay_bridge`
- Spotify PKCE callback flow exists
- Spotify hard backoff is part of the accepted behavior and must be preserved
- fixed 4-playlist model remains the active architecture
- repo-driven deploy and rollback lane has already been validated through the generic workflow family on the Pi

## Current gaps
- lyrics sync quality is still the main unresolved functional weakness
- long-run validation of `bridge_cache.sqlite` and cache reuse is still pending
- broader Spotify redesign remains intentionally frozen pending credential/API-key clarification
- current branch remains a dev lane and is not yet promoted as the accepted `main` artifact truth

## Repo-normalized next action
1. keep `rsob_022sf22l.zip` documented as rollback anchor
2. validate `bridge_cache.sqlite` creation and reuse on target Pi
3. decide whether `0.2.3_db_cache_r1` becomes the next locked stable baseline
4. keep provider-layer scope intact and avoid renderer/controller drift
