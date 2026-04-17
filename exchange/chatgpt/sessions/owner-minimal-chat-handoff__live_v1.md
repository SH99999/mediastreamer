# owner-minimal-chat-handoff live v1

status: live
actor: chatgpt

## source/context
- source chat/session: current governed ChatGPT session with owner
- source timestamp (UTC): 2026-04-17T00:00:00Z
- participants: owner, chatgpt

## current objective
- reduce owner interaction to `governed mode on` -> discussion -> `ship to codex` -> ChatGPT review/pre-ok visibility -> owner merge to `main`
- keep relevant chat decisions out of chat-only memory and on Git with minimal continuity loss
- avoid owner-side manual component routing, branch decomposition, demand close, and repetitive governance prompting

## locked decisions so far
1. owner should not need `chatok` as a manual operating command
2. owner should not need `close demand` as a manual operating command
3. Codex should own routing/decomposition across streams/components/branches/docs when work is shipped
4. ChatGPT should review Codex output and emit pre-ok before owner merge
5. repo truth must remain the durable memory surface so chats can recover with minimal delta

## open decisions
1. where `pre-ok` and `ready-for-owner` should be surfaced most clearly in existing owner-facing views
2. whether automatic live-session shipping can be fully automated inside the current chat product constraints or must remain activation-driven + state-driven

## active implementation asks
1. standardize owner-minimal governed chat handoff in repo truth
2. internalize `chatok` behind `ship to codex`
3. automate demand close after merge + review + closeout
4. surface `pre-ok` and `ready-for-owner` in existing owner-facing repo views without new dashboard sprawl

## active risks/blockers
1. current protocol still exposes `chatok` and `close demand` as visible lifecycle commands
2. true background live shipping from a private chat is limited by product/tooling constraints unless the chat itself writes the repo artifact
3. owner friction remains too high if routing/decomposition is not fully absorbed by Codex

## non-loss requirements
1. relevant decisions and process rules from this chat must not remain only in chat memory
2. owner should not have to restate process logic repeatedly across chats
3. repo truth should be recoverable by any fresh chat with minimal lag

## current lifecycle status
- live

## last material update timestamp
- 2026-04-17T00:00:00Z
