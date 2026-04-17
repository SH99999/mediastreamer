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

## Evidence-led claim ledger
- claim.repo_ready_payload_present: `true`
- claim.deploy_ready: `true`
- claim.tested_on_target: `true`
- claim.rollback_verified: `true`
- claim.runtime_validated: `true`
- claim.autonomy_eligible: `true`
- claim.tested_scope: `bridge provider-layer deploy/rollback lane on target Pi`
- claim.evidence_path: `journals/scale-radio-bridge/current_state_v1.md; journals/scale-radio-bridge/stream_v1.md; tools/governance/autonomous_delivery_matrix_v3.json`
- claim.rollback_path: `.github/workflows/component-test-rollback-v9.yml (component=bridge, payload=current_dev)`
- claim.source_ref: `reports/status/packets/bridge.json`

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
