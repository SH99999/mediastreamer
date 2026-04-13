# Scale Radio Bridge

## Purpose
Scale Radio Bridge is the provider-layer bridge for metadata enrichment, lyrics lookup, Spotify track matching, playlist add, and persistent cache behavior.

## Current role
- governed component: `scale-radio-bridge`
- current work lane: `dev/bridge`
- plugin/runtime identity: `radioscale_overlay_bridge`
- rollback anchor: `rsob_022sf22l.zip`
- conservative current dev branch baseline: `radioscale_overlay_bridge_0.2.3_db_cache_r1.zip`

## Boundaries
This component is a provider/bridge layer.
It does not own renderer layout, global controller logic, or overall overlay ownership.

## Current focus
- preserve the accepted rollback anchor
- validate the SQLite sidecar/cache branch on target Pi
- keep Spotify behavior conservative and preserve the hard backoff logic
- improve lyrics-sync quality without broad architectural drift

## See also
- `journals/scale-radio-bridge/current_state_v1.md`
- `journals/scale-radio-bridge/stream_v1.md`
- `contracts/repo/overlay_component_contract_v1.md`
