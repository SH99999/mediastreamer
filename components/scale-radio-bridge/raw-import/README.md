# Bridge raw import

This directory tracks the first raw intake of the existing Bridge software into the repository.

## Imported source candidates

### Stable reference
- package lineage: `rsob_022c2_stabil.zip`
- version string in package: `0.2.2-c2`
- role in current project: best-known more stable bridge baseline

### Problematic newer candidate
- package lineage: `radioscale_overlay_bridge_0.2.3_db_cache_r1.zip`
- version string in package: `0.2.3-db-cache-r1`
- role in current project: newer DB-cache branch with opening issues

## Intake rule

These files are imported first as raw payload reference material.
They are not yet treated as normalized deploy-ready Bridge runtime.

## Why both versions are kept

The stable version is needed as a baseline for behavior comparison.
The newer version is needed because it adds the persistent DB/cache layer that addresses Spotify API pressure and repeated lookup cost.
