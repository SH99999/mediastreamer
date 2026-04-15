# FALLBACK MANUAL — CONNECTOR BLOCKED (GitHub write unavailable) V1

## Purpose
Define the exact fallback path when a chat/agent cannot create/update GitHub issues, push branches, or open PRs due connector/auth limitations.

## Trigger conditions
Use this manual when any of the following occurs:
- issue create/update API is unavailable in the current connector lane
- `git push` fails due missing auth/connector write access
- PR creation endpoint is unavailable

## Non-negotiable behavior
- never claim delivery success if push/PR/issue mutation did not happen
- return `Delivered to Git: NO` with one concrete blocker and one owner action
- keep partial artifacts in deterministic repo paths when possible

## Fallback sequence (must be in order)
1. **Stop claiming completion**
   - return NO block immediately using `docs/agents/chat_to_git_delivery_process_v1.md` contract
2. **Package missing mutation payload in repo**
   - create deterministic artifact file(s), e.g.:
     - `components/<component>/proposals/governed_intake_issue_fields_v1.md`
     - `docs/agents/fallback_payloads/<topic>_owner_action_v1.md`
3. **Record exact owner action**
   - one action only, e.g.:
     - "create issue using packaged fields file"
     - "push branch `<branch>` with commit `<sha>`"
     - "open PR `<branch> -> main`"
4. **Continue local truth only if safe**
   - journals/docs can be updated locally and committed
   - do not state GitHub-side objects exist unless verified
5. **Handoff**
   - provide artifact path + branch + commit in final NO block

## Owner fast-path decisions
When blocker is connector-only and technical truth is complete:
- owner may merge PR if review is satisfactory
- owner may execute missing external step manually (issue/PR creation) from packaged artifact
- owner may request secondary agent with working connector to perform only missing GitHub mutation

## Example NO block
```text
Delivered to Git: NO
Branch: dev/tuner
Blocker: GitHub issue create/update unavailable in this connector lane.
What was completed locally: Updated tuner stream and committed as <sha>; packaged issue fields at components/scale-radio-tuner/proposals/governed_intake_issue_fields_v1.md.
Owner action: Create the issue from that file and continue with PR review.
```

## Verification checklist after fallback
- artifact path exists in repo
- branch + commit are provided
- exactly one owner action is stated
- no false claim about created issue/PR/push
