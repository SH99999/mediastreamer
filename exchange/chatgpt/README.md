# ChatGPT Exchange Root

## Purpose
Git-native exchange area for ChatGPT <-> Codex collaboration artifacts.

Protocol:
- `exchange/chatgpt/PROTOCOL_v1.md`

## Subdirectories
- `audit_basis/` active audit baseline documents
- `inbox/` ChatGPT-origin requests/findings
- `outbox/` Codex responses + implementation proposals
- `demands/` demand intakes extracted from ChatGPT sessions
- `streams/` living exchange stream entries
- `bundles/` single-file context bundles for GUI/no-shell ChatGPT sessions

## Naming convention
- requests: `<topic>__request_vN.md`
- responses: `<topic>__response_vN.md`
- demand intake: `<demand-id>__intake_vN.md`
