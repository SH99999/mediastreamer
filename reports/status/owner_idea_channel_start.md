# Owner Report — Idea Channel Start

## Purpose
Single owner entrypoint for new idea intake (design -> implementation), with two ChatGPT/Codex rounds and governed execution.

## Start prompt
- `docs/agents/chatgpt_start_prompt_idea_channel_v1.md`

## Required flow
1. ChatGPT creates idea seed in `exchange/chatgpt/ideas/`.
2. ChatGPT sets `status: ready-for-codex`.
3. Codex performs round-1 proposal + governance fit.
4. ChatGPT performs round-2 alignment.
5. Codex creates owner decision packet + implementation branch plan.
6. Owner approves (`accept|changes-requested|reject`).
7. Codex executes governed implementation and one-click delivery path.

## Expected owner packet
- recommendation
- risk rating
- rollback command
- next owner click
- auto-create/auto-deploy path (if eligible)
