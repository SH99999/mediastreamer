# CHATGPT GITHUB CONNECTION MODEL V1

## Purpose
This file records the practical GitHub access model used by this chat for repository work on `SH99999/mediastreamer`.

## Current connection path
This chat reaches the repository through the ChatGPT GitHub connector.

The connection has been used successfully for repository tasks such as:
- reading repository files
- reading recent pull requests
- checking active branches
- creating a dedicated working branch
- creating new files on that branch

## Practical operating model
The practical working pattern is:
1. inspect current repo truth from GitHub
2. prepare changes in a dedicated branch
3. write repo-native files or updates
4. open a pull request to `main`
5. let the repository owner review and merge

## Limits that matter operationally
This is not a local shell-based `git` workflow.

The chat should not assume:
- local `git` CLI usage
- SSH-based push from the chat
- direct Pi-side file editing through GitHub access alone
- direct runtime testing just because repo write access exists

## What this means for repository governance
- important operational knowledge must be written into the repo
- governance and journal files are required for continuity
- working rules should not remain only in chat history
- reviewable PR-based changes are the preferred way to mutate repo truth

## Recovery rule
If another chat takes over, it should verify the connector still works for the repository, then continue from the repo-native governance and journal documents rather than from memory.
