# Discovery and Interviews

Use this reference to turn a rough new-project prompt into an implementation-ready
design or to compare an existing codebase with developer-confirmed goals. Keep interviews
short, concrete, and iterative.

## New projects

Interview before writing code. After each round, summarize proposed requirements,
uncertainties, and exclusions for confirmation.

### Round 1: purpose and boundary

Establish:

- Products, repositories, users, stakeholders, and acceptance authority.
- Operational scenarios, intended environments, and measurable success.
- Explicit non-goals and prohibited behavior.
- Failure consequences, risk, and required reviewer independence.
- Legal, platform, compatibility, resource, and delivery constraints.

Draft `STK` outcomes without implementation terminology. Do not treat them as confirmed
until the developer approves them.

### Round 2: observable behavior

Ask about capabilities, inputs, outputs, external interfaces, quality attributes, error
behavior, compatibility, performance budgets, and recovery. Draft `SYS` requirements
and `SYSV` actions together. Replace vague adjectives with examples or thresholds.

### Round 3: independent implementation boundaries

Derive `SUB` responsibilities and interface semantics, then the non-obvious `CMP`
contracts needed for implementation and verification. Make ownership, inputs, outputs,
state transitions, errors, dependencies, and integration order explicit enough that
several agents can work on nonoverlapping parts without guessing shared contracts.

Ask the developer when a choice changes observable behavior or represents a genuine
tradeoff. Let repository conventions settle low-impact implementation details.

### Round 4: working context and evidence

Capture architecture choices, packages, tools, commands, workflows, and rationale in
`.agents/context/`. Assign each context leaf one dominant need: `Guided learning`,
`Task playbook`, `Reference`, or `Explanation`. Create source routers only after code
roots or meaningful boundaries exist.

Map verification actions, integration checkpoints, unresolved issues, environments, and
durable evidence locations. Show the complete temporary design and planned work split to
the developer before implementation begins.

During implementation, use the V-model to coordinate agents and update durable docs as
the repository takes shape. At completion, reconcile behavior and evidence, transfer
brief unresolved gaps to persistent context or issues, and delete the V-model.

## Existing codebases

Create a temporary V-model only for a holistic goal-versus-implementation review. For
routine documentation maintenance, inspect the repository directly and keep the V-model
absent.

Begin a holistic review with read-only discovery. Use distinct lanes when delegation is
permitted:

1. Public docs, examples, manifests, release metadata, and compatibility promises.
2. Source entry points, architecture, state and error boundaries, and external APIs.
3. Tests, fixtures, CI, supported environments, runtime checks, and observed behavior.
4. Existing `AGENTS.md`, `.agents/context/`, design documents, issue references, and
   relevant history.

Do not change source code during discovery. Do not run credentialed, destructive,
externally mutating, costly, or production-facing tests without explicit authorization
and suitable isolation. Record unsafe actions as planned evidence with their fixtures,
safeguards, and environment.

### Maintain an evidence ledger

For each candidate claim, record:

| Field | Meaning |
| --- | --- |
| Candidate claim | Smallest behavior, goal, decision, or conflict being assessed |
| Evidence | Exact file, symbol, test, commit, release, or developer statement |
| Evidence kind | Documentation, code, test, runtime, history, or interview |
| Confidence | High, medium, or low, with a short reason |
| Conflict | Contrary evidence or missing perspective |
| Proposed class | Intended goal, accepted decision, design defect, missing implementation, obsolete behavior, or unresolved |

Code and tests show current behavior; they do not establish that it is desired. Public
documentation can describe intent but may be stale. Compare developer statements with
shipped compatibility and stakeholder commitments.

Trace CI matrix values, flags, tags, and filters through the actual test entry point.
Before accepting a universal claim, probe empty, malformed, boundary, fallback,
negative, and repeated-call cases in proportion to risk. For destructive behavior, also
check canonical paths, traversal, aliases, stale success markers, partial prior runs,
invalid limits, and retries.

### Interview only the gaps

Ask the developer what inspection cannot establish:

- Which users, scenarios, outcomes, and exclusions are authoritative?
- Is surprising behavior intentional, tolerated debt, a design defect, or missing work?
- Which compatibility promises must remain?
- Which conflicts should be resolved now?
- What failure consequences and acceptance thresholds drive assurance?

Show the competing evidence with each question. Convert confirmed goals into the
temporary V-model, then compare them systematically with implementation and evidence.

### Classify review findings

- **Matched:** implementation and evidence satisfy confirmed intent.
- **Design defect:** architecture or boundary choices obstruct a confirmed goal.
- **Missing implementation:** confirmed behavior is absent or incomplete.
- **Unintended behavior:** implemented behavior conflicts with a confirmed goal.
- **Verification gap:** a claim lacks objective or durable evidence.
- **Accepted decision:** current implementation choice and rationale belong in context.
- **Unresolved:** record the question, evidence, owner, and review trigger.

Complete the agreed review output or corrections, update durable docs, reduce unfinished
items to concise current gaps, then delete the V-model and run the linter in `absent`
mode.

## Confidence rules

- Treat only developer-confirmed or otherwise authoritative goals as normative.
- Do not turn a passing test into a stakeholder outcome.
- Do not claim that evidence covers clauses or edge cases it never exercises.
- Do not generalize one example into a compatibility guarantee.
- Keep conflicts visible and record what was not inspected.
