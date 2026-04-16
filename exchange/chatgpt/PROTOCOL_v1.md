# ChatGPT-Codex Exchange Protocol v1

## Actors
- `chatgpt`
- `codex`

## Required status markers
Each active file must contain one status marker line:
- `status: draft`
- `status: ready-for-codex`
- `status: in-review-by-codex`
- `status: ready-for-chatgpt`
- `status: ready-for-owner`
- `status: closed`

## Handshake order
1. ChatGPT starts with `exchange/chatgpt/audit_basis/current_audit_basis_v1.md`
2. ChatGPT sets `status: ready-for-codex`
3. Codex reviews/evaluates and writes next request/response artifact if needed
4. Codex updates stream with actor and status transition
5. for decision rounds, both sides provide agreement scores and Codex derives owner decision draft

## Stream entry requirement
Every stream entry must include:
- actor (`chatgpt` or `codex`)
- source file
- resulting status
