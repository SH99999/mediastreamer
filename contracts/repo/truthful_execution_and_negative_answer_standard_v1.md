# TRUTHFUL EXECUTION AND NEGATIVE ANSWER STANDARD V1

## Purpose
This document defines the mandatory truthfulness rule for governed repo work by chats, agents, and automation.

## Leading rule
An explicit truthful negative answer is always preferred over fabricated progress, implied completion, false confidence, or placeholder delivery.

## Why this exists
False completion is more dangerous than an explicit blocker because it:
- corrupts repo truth
- wastes owner review time
- hides real technical limitations
- creates invalid assumptions for later agents and workflows
- makes test evidence and acceptance unreliable

## Mandatory behavior
When a chat, agent, or workflow cannot safely complete a requested action, it must:
1. say that the action did not complete
2. state the real blocker or limitation
3. distinguish facts from assumptions
4. avoid claiming repository or runtime changes that did not actually happen
5. escalate and inform when the blocker affects repo truth, cross-component work, deploy/test integrity, or protected-main maintenance

## Negative-answer rule
A negative answer is the correct answer when:
- the connector cannot safely mutate the target file
- access is missing
- the tool surface cannot perform the requested action
- runtime validation did not happen
- deploy or rollback could not be verified
- a contract is not yet fulfilled
- the result would otherwise be a placeholder or pretend-delivery

## What not to do
- do not say or imply that a file was updated when only a draft or replacement artifact exists
- do not say or imply that deploy succeeded when only workflow dispatch was attempted
- do not say or imply that runtime behavior is validated when no real target-Pi validation happened
- do not hide uncertainty behind vague wording
- do not substitute wishful thinking for repo truth

## Relation to existing rules
This standard complements:
- protected-main truth maintenance
- escalation on technical blockers
- deploy target exclusivity
- journal and decision freshness

It does not weaken speed or autonomy.
It defines the honesty boundary that keeps autonomous operation trustworthy.
