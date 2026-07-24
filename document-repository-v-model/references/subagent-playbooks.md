# Subagent Playbooks

Use this reference only when the environment and applicable instructions permit
delegation. Scale independence and specialist effort to risk; keep one coordinator
responsible for intent, reconciliation, and final edits.

## Contents

- [Isolation rules](#isolation-rules)
- [Risk-scaled staffing](#risk-scaled-staffing)
- [Standard V-layer cohorts](#standard-v-layer-cohorts)
- [Existing-repository discovery](#existing-repository-discovery)
- [Consistency review](#consistency-review)
- [Clean-room forward testing](#clean-room-forward-testing)

## Isolation rules

- Give each operator a concrete, bounded, primarily read-only lane.
- Provide the skill path, repository path, exact pinned commit, and a normal user-style
  request. Do not reveal expected answers, suspected defects, or another reviewer’s
  conclusions.
- Use a separate disposable clone or worktree per writing agent. Never let agents edit
  the same worktree.
- For discovery and evaluation, prohibit source-code changes and pushes.
- Ask for evidence with exact file/symbol/test anchors, confidence, conflicts, and
  unresolved questions.
- Keep one slot for the coordinator when concurrency is limited.

If subagents are unavailable, perform the same lanes sequentially and use a fresh context
for the independent review when possible.

## Risk-scaled staffing

| Risk/scale | Suggested approach |
| --- | --- |
| Tiny, low-risk repository | One operator plus a short independent trace/size review |
| Ordinary repository | Coordinator plus documentation/source and test/trace operators |
| Large brownfield or polyglot repository | Coordinator plus code/spec archaeologist, verification mapper, and boundary/router reviewer |
| High assurance or destructive behavior | Add domain, security/safety, failure-injection, environment, and independent trace specialists as relevant |

Do not add specialists merely to fill slots. Add them when a distinct evidence domain or
independence requirement exists.

## Standard V-layer cohorts

| Layer | Cohort |
| --- | --- |
| `STK` / `ACC` | Domain or stakeholder proxy; acceptance-scenario designer; independent trace reviewer |
| `SYS` / `SYSV` | Requirements analyst; black-box verification designer/executor; relevant performance, security, or compatibility specialist; reviewer |
| `SUB` / `INTV` | One contract investigator per important boundary; dependency/environment or failure-injection specialist; architecture/trace integrator |
| `CMP` / `UNITV` | Component/unit-test investigator; static-analysis or code-inspection investigator; orphan/coverage reviewer |

A specialist may cover several roles in a small repository. Preserve independence for the
final trace review when failure impact warrants it.

## Existing-repository discovery

Give operators nonoverlapping questions:

- **Public contract operator:** Inspect public docs, examples, manifests, release metadata,
  and declared compatibility. Return candidate observable claims and contradictions.
- **Code archaeologist:** Inspect entry points, data/state/error boundaries, public APIs,
  and major subsystems. Return observed behavior and architecture decisions separately.
- **Verification mapper:** Inspect tests, CI, fixtures, supported environments, skips,
  expected failures, and evidence durability. Return coverage and orphan candidates.
- **Agent-context reviewer:** Inspect existing routers and context for scope, duplication,
  open/avoid criteria, anchors, staleness, and likely migration targets. Separate
  specification and router-local rules, then classify each retained leaf as
  `Guided learning`, `Task playbook`, `Reference`, or `Explanation`.

The coordinator merges evidence into one ledger, asks the developer only unresolved
intent questions, and classifies claims before anyone writes a baseline.

## Consistency review

Assign independent passes for router/link integrity, V-model/traceability, source/test
drift, and duplication/token cost. Require each finding to include:

1. Severity and affected IDs/files.
2. Exact evidence.
3. Why it is inconsistent or costly.
4. Smallest safe correction.
5. Whether developer intent is required.

For every `passing` action sampled, open the cited evidence and compare its exercised
cases with each phrase in the procedure and pass criterion. Sample universal normative
claims with at least one boundary or counterexample search. Mechanical reverse links are
not semantic coverage.

For the context-cost pass, start with representative repository tasks and follow only
the links an agent would be told to open. Report missing routes, unnecessary hops,
indexes presenting more than seven choices, unrelated documents loaded, and mixed or
incorrect context needs. Do not recursively preload `.agents/` to perform this review.

Have the coordinator deduplicate findings and apply changes in the reconciliation order
from `review-and-compaction.md`.

## Clean-room forward testing

Skill maintainers should forward-test with disposable clones pinned to exact commits.
Use three small operators concurrently with one coordinator; for a large case use an
operator, code/spec archaeologist, and verification mapper, then reuse them as independent
cross-reviewers.

Core release cases:

- `QuantumSavory.jl`: preserve selective router/context strengths while detecting drift
  and separating specification from decisions.
- `PBCCompiler.jl`: migrate a monolithic `AGENTS.md`.
- `TermInterface.jl`: verify proportional output for a tiny library.
- `QuantumClifford.jl`: exercise brownfield discovery and subsystem traceability.
- `WebQuantumSavory`: exercise polyglot roots and cross-stack contracts.

Rotate `QuantumInterface.jl` for externally consumed contracts,
`julia-buildkite-plugin` for no conventional `src/`, and `AnythingLLMDocs.jl` for
external-service and safety-aware acceptance planning. Never execute a live destructive
test merely to evaluate documentation generation.

Require:

- No hard linter errors or avoidable router warnings.
- Complete bidirectional traceability.
- No implementation decisions duplicated into specification.
- No observed behavior promoted to intent without evidence or confirmation.
- Selective context loading and no source-code changes.
- An empty unnecessary second-pass diff.
- Independent approval for correctness, proportionality, interview quality, and context
  efficiency.

Keep prompts, raw diffs, linter JSON, and scores outside the shipped skill. Retain them
only until findings are incorporated, then remove clones and temporary artifacts.
