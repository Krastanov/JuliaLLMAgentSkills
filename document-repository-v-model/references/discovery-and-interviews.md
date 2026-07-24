# Discovery and Interviews

Use this reference to establish intended behavior for a new project or recover it from
an existing repository. Keep interviews short and evidence-led.

## Contents

- [New projects](#new-projects)
- [Existing projects](#existing-projects)
- [Confidence and baseline rules](#confidence-and-baseline-rules)

## New projects

Interview and draft in rounds. After each round, summarize the proposed records,
uncertainties, and exclusions for developer confirmation.

### Round 1: repository and intent

Ask only enough to establish:

- Repository and independently released product boundaries.
- Stakeholders, actors, and who accepts the result.
- Operational scenarios and intended environments.
- Outcomes and measurable success.
- Explicit non-goals and prohibited behavior.
- Consequence of failure, risk, and required reviewer independence.
- Legal, platform, compatibility, resource, or delivery constraints.

Draft `STK` outcomes without implementation terminology. Obtain explicit confirmation
before treating them as the baseline.

### Round 2: observable system behavior

Ask about capabilities, inputs and outputs, external interfaces, quality attributes,
error behavior, compatibility ranges, performance budgets, and recovery behavior. Draft
`SYS` records and `SYSV` intent together. Resolve vague adjectives with examples or
thresholds.

### Round 3: logical contracts

Derive `SUB` responsibilities and boundary semantics, then only the non-obvious `CMP`
contracts needed for correct implementation and evidence. Ask the developer when a
choice changes observable behavior or represents a genuine tradeoff. Do not ask them to
invent details that repository conventions can settle safely.

### Round 4: implementation context and evidence

Separate normative specification and router-local rules before capturing architecture,
packages, tools, workflows, and rationale in `.agents/context/`. Assign each retained
context leaf exactly one dominant need: `Guided learning`, `Task playbook`, `Reference`,
or `Explanation`. Create only leaves that answer an evidenced agent retrieval need.
Map all right-side actions, unresolved issues, environments, and durable evidence
locations. Add source routers only after actual code roots or meaningful boundaries
exist.

Finish by showing the intended specification, unresolved decisions, and planned evidence
to the developer for approval.

## Existing projects

Start with read-only discovery. Parallelize only when applicable instructions permit it.
Use distinct lanes so conclusions can be reconciled:

1. Public docs, examples, manifests, release metadata, and declared compatibility.
2. Source entry points, architecture, state and error boundaries, and external APIs.
3. Tests, fixtures, CI, supported environments, runtime checks, and observed behavior.
4. Existing `AGENTS.md`, `.agents/`, design documents, issue references, and relevant
   history.

Do not change source code during a documentation-only discovery or forward test.
Do not execute a credentialed, destructive, externally mutating, costly, or
production-facing test merely to establish documentation evidence. Unless the developer
has explicitly authorized a suitably isolated and reversible run, record the action as
planned and specify the fixture, safeguards, and acceptance environment it needs.

### Maintain an evidence ledger

For each candidate claim, record:

| Field | Meaning |
| --- | --- |
| Candidate claim | The smallest behavior, intent, decision, or conflict being assessed |
| Evidence | Exact file, symbol, test, commit, release, or developer statement |
| Evidence kind | Documentation, code, test, runtime, history, or interview |
| Confidence | High, medium, or low, with a short reason |
| Conflict | Contrary evidence or missing perspective |
| Proposed class | Intended specification, accepted decision, defect/spec gap, obsolete behavior, or unresolved |

Code and tests are evidence of current behavior. They are not automatic proof that the
behavior is desired. Public documentation may describe intent but still be stale. A
developer statement can establish intent, but compare it with shipped compatibility and
stakeholder commitments before removing behavior.
Do not equate an export list with a stable public contract: reconcile exports, explicit
stability/private markers, release notes, supported examples, and actual downstream use.

For CI evidence, trace each matrix value, environment variable, feature flag, tag, and
filter through the test entry point to the selected cases. Similar job and selector
names are not evidence that the intended shard actually runs.

Before turning a candidate into a normative statement, try to falsify it. Probe empty,
malformed, boundary, fallback, negative, and repeated-call cases in proportion to risk.
Exercise each public entry point, default, override, and diagnostic path that can reach
the behavior.
Treat words such as “all,” “every,” “any,” “deterministic,” and “supported” as prompts
for counterexamples. If known behavior contradicts a proposed universal claim, keep the
conflict unresolved or narrow the record; draft status does not make an internally
inconsistent statement acceptable.

For filesystem deletion or other destructive state changes, also probe canonicalized
and traversal paths, symlinks or aliases, pre-existing and stale success markers,
partial prior runs, zero/negative/nonnumeric/overflow limits, and repeated invocations.
State containment relative to resolved targets, not merely a configured path string.
Treat “fail open,” “continue,” and “recover” as caller-control-flow claims unless
evidence separately establishes remote atomicity, rollback, idempotent retry, and the
resulting partial state.

### Interview only the gaps

After discovery, ask compact questions about matters inspection cannot establish:

- Which users and scenarios are authoritative?
- Is a surprising behavior intentional, tolerated debt, or a defect?
- Which compatibility promises and exclusions must remain?
- Which conflicts should be resolved now and which remain explicit?
- What failure consequences or acceptance thresholds drive assurance?

Show the exact competing evidence with each question. Avoid asking for facts already
available in the repository.

### Classify before moving prose

Assign each observed claim to one class:

- **Intended specification:** confirmed normative behavior; move or write it in the
  V-model with objective evidence.
- **Accepted implementation decision:** current “how” and rationale; keep it in a context
  topic linked to the fulfilled specification.
- **Defect or specification gap:** code and intended behavior differ; keep the mismatch
  explicit and do not rewrite either side to hide it.
- **Obsolete behavior:** no longer intended; remove current-state guidance and retain a
  short retirement note only when compatibility requires one.
- **Unresolved:** evidence conflicts or intent is unavailable; record the question,
  evidence, owner, and review trigger.

Preserve useful existing open/avoid criteria, source anchors, test anchors, commands, and
local rules. Replace duplicated normative prose with canonical V-model links. After
separating specification and router-local material, classify each retained context leaf
as `Guided learning`, `Task playbook`, `Reference`, or `Explanation`; do not create
empty category scaffolding.

## Confidence and baseline rules

- Baseline only developer-confirmed or otherwise authoritative intended behavior.
- Leave inferred records in `draft` status and identify their evidence.
- Do not turn “the test currently passes” into a stakeholder outcome.
- Do not infer that a cited test covers clauses or edge cases it never exercises.
- Do not turn one example into a general compatibility guarantee.
- Do not silently choose between documentation and code when they conflict.
- Record what was not inspected and why.
