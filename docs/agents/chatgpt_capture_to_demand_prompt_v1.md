# ChatGPT Capture-to-Demand Prompt v1

## Purpose
Use this prompt inside any relevant ChatGPT chat to capture the current conversation into one governed demand artifact so nothing important remains only in chat memory.

## When to use
Use this when the chat contains any of the following:
- a decision that must not be lost
- a new implementation request
- a governance change request
- a component/runtime change request
- owner decision framing
- blockers, risks, or non-loss requirements that must persist beyond the chat session

## Output target
The resulting artifact should be suitable for commit under:
- `exchange/chatgpt/demands/<topic>__intake_v1.md`

## Capture prompt
Use this exact prompt in the ChatGPT chat you want to preserve:

```text
Create one governed demand intake markdown artifact for this chat.

Goal:
Capture the decisions, implementation requests, risks, and non-loss information from this chat so nothing remains only in chat memory.

Output requirements:
- produce exactly one markdown file content
- target path suggestion: `exchange/chatgpt/demands/<topic>__intake_v1.md`
- keep it compact but implementation-usable
- include:
  1. source/context
  2. objective
  3. locked decisions from this chat
  4. open decisions
  5. required implementation
  6. required governance updates
  7. risks
  8. non-loss requirements
  9. execution request for Codex
  10. status marker (`draft|chatok|ready-for-codex|in-execution|ready-for-chatgpt-review|pre-ok|ready-for-owner|closed`)

Important:
- do not write narrative chat prose
- do not summarize loosely
- write it as a governed repo handover artifact
- decisions made in this chat must be explicit
- anything that must later appear in repo truth must be listed clearly
- if the chat includes decisions that should become durable repo truth, call that out explicitly under required governance updates
```

## Owner handoff rule
After the artifact is created, it should be put on Git and used as the source proposal location for the governed intake flow.

Preferred next step prompt for Codex / governed execution:
- `docs/agents/chatgpt_governed_intake_prompt_v1.md`

## Continuity rule
This capture prompt is the minimum persistence layer when a relevant chat outcome has not yet been moved into current-state / status / decision-log repo truth.

The goal is:
- no relevant chat decision lives only in chat memory
- repo continuity loss stays within minutes, not sessions
