# ChatGPT Main Inbox Snapshots

Canonical trigger-facing intake snapshots for Codex pickup from `main`.

## Purpose
- append-only, immutable intake snapshots
- owner/chat-facing `ship to codex` trigger output
- safe to read from protected `main`
- canonical Codex pickup source after promotion

## Canonical naming pattern
- `<YYYYMMDDTHHMMSSZ>__<topic>__intake_snapshot_v1.md`

## Rules
- append-only (never overwrite older snapshots)
- each snapshot is self-contained enough for Codex start
- labels remain routing index; snapshot content is detailed trigger truth
