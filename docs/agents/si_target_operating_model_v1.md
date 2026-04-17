# SI CODEX HANDOVER — Target Operating Model v1
_Date: 2026-04-16_

## 1. Purpose
This handover is for a replacement **System Integration Codex** lane.

It is **not** a greenfield redesign.
It must **build on the current repository state** and stop the current pattern of meta-layer sprawl, drift, and owner-friction.

Primary goal:
- stabilize the SI operating model
- reduce onboarding/read burden
- preserve what already works
- close the most damaging gaps first
- avoid another rebuild cycle

---

## 2. Re-evaluation of the latest changes

## 2.1 What is already good and should be kept
Keep these as part of the baseline operating model:

1. **Protected `main` as repo truth**
   - `main` remains the protected truth branch.
   - SI/governance work happens on dedicated `si/<topic>` branches.
   - This is already aligned in current governance and should not be reopened.

2. **Conservative autonomous delivery**
   - support matrix remains the right gate
   - currently supported subset is narrow and that is good
   - do not broaden autonomy by policy language alone

3. **Status packet + one-click direction**
   - machine-readable status packets plus markdown adapters are the right direction
   - `next_owner_click`, scoring, rollback fields, and report generation should be kept

4. **Branch-scope guard + source-registry lint**
   - these are real anti-drift controls
   - keep them active and refine only if they create proven noise

5. **Mode-B / role bootstrap direction**
   - role-aware bootstrap and deferred reference mapping are the right response to long read chains
   - this should be simplified and made more authoritative, not discarded

6. **ChatGPT↔Codex Git exchange lane**
   - keep the governed exchange concept
   - but do not let it multiply prompts/dashboards/templates without restraint

---

## 2.2 What is currently wrong or unstable
These are the key problems the new SI Codex must treat as real defects, not cosmetic issues.

### A. Documentation / executable contract drift
Startup/onboarding docs and executable helper presence must stay aligned. `tools/governance/setup_auth_check_v1.sh` is now present and should be treated as part of startup truth verification.

Implication:
- if any startup-referenced helper is missing in repo state, treat as a `repo-truth defect`
- repair the contradiction in the same package instead of carrying narrative-only claims

### B. Queue lifecycle is not self-closing
There are open SI escalation issues whose source PRs are already merged.
That means the queue can overstate current owner action and create fake operational pressure.

Implication:
- owner boards/issue views are not fully trustworthy
- closeout automation is incomplete
- this is a P1/P2 operational gap

### C. Too much meta-layer growth in one day
Recent changes added many prompts, templates, bundles, dashboards, rendered views, owner boards, exchange helpers, and round-based artifacts.
Some are useful, but together they create a second-order maintenance problem.

Implication:
- the repo is at risk of optimizing the control plane faster than the actual integration flow
- onboarding and interpretation cost rise again
- the new SI Codex must **freeze meta-layer expansion**

### D. Onboarding is still too heavy
The onboarding/journal audit already proves the read chain is still large.
Mode-B helps, but the system still has too many documents in the active path.

Implication:
- replacement Codex lanes can still skip or misread critical truth
- efficiency goal is not achieved yet

### E. Historical-vs-active truth is still not hard enough
Journal versioning improved, but the repo still carries too much readable historical material close to active truth.
The boundary is better than before, not yet strong enough.

Implication:
- replacement lanes can still drift into old sources
- history preservation is fine, authority clarity is still too soft

---

## 2.3 What must be frozen immediately
The new SI Codex must **not** spend time creating more of the following until stabilization work is done:

- new owner dashboards
- new HTML summary pages
- new prompt generations / prompt versions unless replacing an existing canonical prompt
- new exchange sub-channels unless replacing a canonical one
- new duplicate summary docs that restate current truth without adding enforcement value
- broad new governance standards when the problem can be solved by tightening an existing canonical file

Rule:
**No new meta artifacts unless they replace or delete older ones in the same PR.**

---

## 3. Target Operating Model v1

## 3.1 Core operating principle
The SI lane is a **repo control plane**, not a writing lane.

Its job is to:
- keep truth authoritative
- keep execution paths deterministic
- minimize owner clicks
- minimize replacement-agent read burden
- preserve rollback and evidence discipline

It is **not** the SI lane’s job to keep generating more narrative surfaces.

---

## 3.2 Canonical authority chain
The new SI Codex must operate with this order of authority:

1. `AGENTS.md`
2. `contracts/repo/system_integration_governance_index_v7.md`
3. canonical repo contracts in `contracts/repo/`
4. current SI status + decisions + active stream
5. generated reports
6. issue queue / owner boards / dashboards
7. chat memory

Interpretation rule:
- generated reports are derived surfaces
- issues are an operating queue
- dashboards are convenience surfaces
- only contracts + current-state/decisions are authoritative

---

## 3.3 Canonical artifact model for SI
The SI lane should converge on these artifact classes only:

### A. Authoritative state
- one current SI status file
- one current SI decision log
- one active SI stream

### B. Structured event / evidence
- status packets
- evidence bundles
- workflow outputs
- generated audits / proof reports

### C. Owner decision surfaces
- one owner packet per decision package
- owner board(s) only if generated from authoritative data

### D. Exchange surfaces
- one canonical ChatGPT↔Codex exchange root
- request/response/owner packet only
- no uncontrolled parallel prompt trees

Rule:
If a new file does not fit one of these classes, it should probably not be added.

---

## 3.4 Branch model
Keep and enforce:

- `main` = protected truth
- `si/<topic>` = system integration / governance package branch
- `dev/<component>` = component specialist lane
- `integration/staging` = rare exception only

Additional rule for replacement SI Codex:
- every SI package branch must have one narrow purpose
- do not bundle stabilization, dashboards, prompts, and unrelated policy changes together

---

## 3.5 Owner interaction model
Owner should receive only:
- prepared PR / merge-request packet
- risk
- rollback command
- next owner click
- explicit blocker if action is needed

Owner should **not** be required to:
- reconstruct repo state
- navigate multiple dashboards to find truth
- infer whether queue items are stale
- author PR mechanics

---

## 3.6 Onboarding model
The new SI Codex should implement a **three-tier read model** derived from one authority chain:

### Tier 0 — safe-start
Goal: start safely within minutes.
Contains only:
- current branch rule
- current remote rule
- current authority chain
- current blocker rule
- current delivery contract
- exact first actions

### Tier 1 — working context
Goal: enough context to execute a governed SI package.
Contains:
- active status
- active decisions
- active stream recent tail
- current open risks
- current package backlog

### Tier 2 — deep history
Goal: historical analysis only.
Contains:
- older journals
- superseded docs
- historical stream generations
- prior optimization packages

Rule:
Tier 0 and Tier 1 must be generated from current authority, not hand-maintained as separate parallel truth.

---

## 3.7 Evidence and one-click model
Keep one-click, but tighten its boundary.

### One-click applies to:
- owner decisioning
- owner merge authorization
- rollback-ready review packets
- generated status views

### One-click does not automatically imply:
- deploy support
- runtime acceptance
- autonomous widening
- queue closeout without conditions

For any deploy/autonomy claim, require:
- evidence link
- tested scope
- rollback path
- source commit / packet path

---

## 3.8 Historical material handling
Historical files are allowed, but must be clearly subordinate.

Rules:
- old stream generations = explicit `historical` / `read-only`
- superseded contracts = indexed and clearly lower-precedence
- no new entries into non-current stream generations
- no owner-facing links should prefer historical docs over current docs

---

## 4. Immediate implementation plan for the new SI Codex

## Phase 0 — Stabilize before adding anything
Branch:
- `si/si-tom-stabilization-v1`

Deliverables:
1. add this operating model into repo as one canonical SI TOM doc
2. update SI governance index / onboarding / AGENTS references only as needed
3. add a freeze rule for meta-artifact growth
4. create a compact "do not add" list for SI Codex

Acceptance:
- no new dashboards/prompts/views introduced in this package
- branch is narrow and explanatory
- owner packet clearly says this is a stabilization package

---

## Phase 1 — Fix broken truth and queue trust
Branch suggestions:
- `si/auth-contract-repair-v1`
- `si/queue-closeout-hardening-v1`

### Package 1A — auth contract repair
Actions:
- keep startup helper references aligned with actual repo file presence (no narrative-only startup claims)
- either:
  - restore it safely, or
  - remove all references and replace with the actual supported auth-check path
- add a docs-reference existence check for executable paths

Acceptance:
- no active doc points to a missing executable file
- no auth helper prints sensitive material
- startup path is internally consistent again

### Package 1B — queue closeout hardening
Actions:
- closeout must not trigger on PR merged alone
- require:
  - source PR merged
  - required docs/journals aligned
  - explicit state transition path (`done`, `superseded`, or `docs-update-required`)
- write one audit-trail comment on automated state changes
- clean obviously stale existing SI escalation issues

Acceptance:
- open SI escalation issues match real pending work
- no merged-source issue remains open without an explicit reason

---

## Phase 2 — Reduce read burden and truth ambiguity
Branch suggestions:
- `si/historical-boundary-hardening-v1`
- `si/tiered-onboarding-v1`
- `si/authority-compression-onboarding-hardening-v1` (combined package when both scope slices ship together)

### Package 2A — historical boundary hardening
Actions:
- start with SI stream generations and clearly superseded governance docs only
- mark older SI stream generations clearly historical/read-only
- tighten superseded index
- avoid repo-wide lint blast in first pass

Acceptance:
- active SI truth path is obvious
- historical docs remain readable but non-competitive

### Package 2B — tiered onboarding
Actions:
- generate Tier 0 / Tier 1 from current authority chain
- keep one reference map authoritative
- reduce active default read path drastically

Target:
- Tier 0 safe-start under 5 minutes
- Tier 1 working-context under 15 minutes

Acceptance:
- replacement SI Codex can start from one compact path
- no duplicate manual truth trees are introduced

---

## Phase 3 — Tighten one-click without slowing governance
Branch suggestion:
- `si/evidence-gated-one-click-v1`

Actions:
- keep owner packet / next_owner_click / scoring / rollback fields
- scope stricter evidence-gate only to:
  - deploy claims
  - autonomy claims
  - runtime acceptance claims
- do not force heavy evidence process on governance/docs-only packages

Acceptance:
- owner flow remains fast
- deploy/autonomy claims become harder to overstate
- governance-only PRs remain lightweight

---

## 5. Hard rules for the new SI Codex

1. **Do not restart architecture work.**
   Build on the existing governance stack.

2. **Do not expand the meta layer first.**
   Stabilize truth, onboarding, and queue trust first.

3. **Do not write broad narrative documents when a contract or generator update is enough.**

4. **Do not add new owner-facing surfaces unless they replace old ones.**

5. **Do not bundle unrelated SI topics into one PR.**

6. **Do not describe autonomy more broadly than the current support matrix proves.**

7. **Do not trust stream text over file existence.**
   If stream says a file was added but the file is absent, treat that as a repo-truth defect.

8. **Do not use dashboards as truth.**
   Dashboards are derived convenience only.

9. **Do not create new parallel onboarding chains.**
   Tiered onboarding must be generated from one authority chain.

10. **Do not keep stale queue items open just because automation has not caught up.**

---

## 6. First reply contract for the replacement SI Codex
The new SI Codex first response should contain only:

### A. What it is adopting as baseline
- current `main`
- current SI governance stack
- this TOM
- current support-matrix and branch model

### B. What it will not do
- no rebuild from scratch
- no new dashboard/prompt growth before stabilization
- no direct edits to `main`

### C. First three package branches
- branch 1: SI TOM stabilization
- branch 2: auth contract repair
- branch 3: queue closeout hardening

### D. Exact owner action needed
- ideally: none before first stabilization PR is prepared

---

## 7. Recommended repo file to add
Suggested canonical path:
- `docs/agents/si_target_operating_model_v1.md`

If Codex wants a governance contract path instead:
- `contracts/repo/system_integration_target_operating_model_v1.md`

Preferred recommendation:
- put the full TOM in `docs/agents/`
- add a short reference line in SI governance index + onboarding
- do not create both full versions

---

## 8. Bottom line
The repository does **not** need another reinvention cycle.

It needs a replacement SI Codex that:
- accepts the current governance baseline
- freezes meta sprawl
- repairs broken repo truth
- closes queue drift
- compresses onboarding
- tightens active-vs-historical authority
- keeps one-click fast but evidence-bound where runtime claims are involved

That is the shortest path to a stable SI control plane without losing the investment already made.
