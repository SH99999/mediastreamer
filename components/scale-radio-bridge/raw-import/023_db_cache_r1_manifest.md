# Bridge raw import manifest — 0.2.3 DB Cache R1

## Source lineage
- input archive: `radioscale_overlay_bridge_0.2.3_db_cache_r1.zip`
- package version: `0.2.3-db-cache-r1`
- plugin id: `radioscale_overlay_bridge`
- plugin type: `user_interface`

## Extracted files observed
- `index.js`
- `db_cache.py`
- `config.json`
- `UIConfig.json`
- `package.json`
- `install.sh`
- `uninstall.sh`
- `requiredConf.json`
- `README.md`
- `public/index.html`
- `public/style.css`
- `public/app.js`
- `i18n/strings_en.json`

## Intake classification
- status: raw imported problem branch
- role: DB-cache candidate with persistent SQLite sidecar
- known discussion point: opening behavior is problematic in the newer build
- value-add direction: persistent cache and duplicate-prevention memory for Spotify and lyrics workflows
