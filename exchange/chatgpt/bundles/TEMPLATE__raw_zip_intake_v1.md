# <topic> raw ZIP intake v1

status: ready-for-codex
actor: chatgpt

## bundle identity
- bundle_id: <bundle-id>
- topic: <topic>
- created_at_utc: <YYYY-MM-DDTHH:MM:SSZ>
- zip_artifact_path: exchange/chatgpt/bundles/<bundle-file>.zip

## governed source references
- source_demand_path: exchange/chatgpt/demands/<topic>__intake_v1.md
- source_protocol_path: exchange/chatgpt/protocol-main/<topic>__protocol_v1.md

## optional mapping hints (non-canonical)
- hint_notes:
  1. 
- hint_targets:
  1. target_branch_hint:
     target_path_hint:

## non-loss notes
1. ZIP + hints are input only and must not be treated as canonical branch/path manifest.
2. Codex must generate canonical distribution manifest from repo truth before execution.
