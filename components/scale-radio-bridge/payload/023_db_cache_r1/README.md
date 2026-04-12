# RadioScale Overlay Bridge 0.2.3 DB Cache R1

Baseline-safe build based on the approved reference package `rsob_022sf22l.zip`.

## Scope of this release

This release adds a persistent SQLite sidecar cache without changing the core Spotify lookup strategy or the approved baseline UI logic.

Added:
- persistent SQLite sidecar cache
- persistent lyrics cache
- persistent Spotify match cache
- persistent negative cache
- persistent playlist dedupe cache
- artwork metadata / URL references stored together with Spotify matches
- plugin settings and clear-cache action for the DB layer

Not changed on purpose:
- baseline Spotify backoff strategy
- baseline Spotify query timing / matching flow
- baseline overlay layout and UI behavior
- baseline LRCLIB provider choice for lyrics

## Restore point

If this branch must be abandoned, roll back to the approved baseline by reinstalling:
- `rsob_022sf22l.zip`

Optional cleanup after rollback:
- delete `/data/configuration/user_interface/radioscale_overlay_bridge/bridge_cache.sqlite`

## Persistent DB location

`/data/configuration/user_interface/radioscale_overlay_bridge/bridge_cache.sqlite`

## Safety model

The bridge now checks the SQLite cache before a normal online lookup and stores results after a normal online lookup. If the DB layer is unavailable, the bridge continues with the existing in-memory cache and online path.
