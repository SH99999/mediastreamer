# codex-trigger-and-materialized-chat-protocol live v1

status: chatok
actor: chatgpt

## source/context
- source chat/session: current governed ChatGPT session with owner
- source timestamp (UTC): 2026-04-17T00:00:00Z
- participants: owner, chatgpt

## current objective
- make `ship to codex` repo-effective so Codex knows what to do without relying only on direct chat prompting
- add a materialized chat protocol artifact so important discussion history survives beyond the live chat and can be used by Codex or a fresh chat
- keep owner effort minimal and preserve the existing owner-minimal command surface

## locked decisions so far
1. a Git artifact on a side branch alone is not enough unless Codex has a clear repo-visible trigger path
2. `ship to codex` should become the canonical trigger that both writes repo truth and gives Codex a deterministic pickup path
3. a materialized chat protocol should be event-based and compact, not a raw full transcript
4. the protocol must preserve decisions, open questions, risks, execution requests, and links to related git objects
5. the new mechanism must not add dashboard or governance sprawl

## open decisions
1. whether Codex pickup should be implemented via branch/path watcher only or via a stricter demand-handshake contract plus branch/path watcher
2. whether materialized protocol should live only under `exchange/chatgpt/sessions/` or additionally be promoted/linked from demand artifacts automatically

## active implementation asks
1. standardize the repo-visible Codex trigger path for `ship to codex`
2. ensure Codex can detect work from repo truth without owner re-explaining the task
3. add a canonical materialized chat protocol template and lifecycle rule
4. ensure protocol + demand + live session work together without parallel truth drift

## active risks/blockers
1. current repo truth documents demand/live artifacts, but Codex trigger semantics are still not strong enough to assume zero-touch pickup from side-branch artifacts alone
2. without a materialized protocol, new chats/agents still lose some conversation rationale between live session and durable truth
3. overbuilding this area could create governance/meta sprawl instead of appliance-supporting continuity

## non-loss requirements
1. the rationale behind repo-visible Codex triggering must not remain only in chat memory
2. the need for an event-based materialized protocol must be preserved as a formal requirement
3. owner should not need to restate prior chat history to a new agent/chat

## current lifecycle status
- chatok

## last material update timestamp
- 2026-04-17T09:55:26Z
