# ChatGPT Materialized Protocol (main)

Canonical compact protocol artifacts for durable conversation context.

## Purpose
- event-based, compact, link-rich protocol history
- preserve decisions, open questions, risks, execution requests, related Git objects
- readable by a fresh chat/agent without raw full transcript dumps

## Canonical artifact
- `exchange/chatgpt/protocol-main/<topic>__protocol_v1.md`

## Rules
- append events; do not rewrite prior event meaning
- keep compact and decision-/risk-/request-oriented
- do not store full raw chat transcript by default
