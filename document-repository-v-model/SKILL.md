---
name: document-repository-v-model
description: Build, migrate, audit, review, update, and compact agent-facing repository documentation with nested AGENTS.md routers, selectively loaded Diátaxis-style .agents context, structured V-model specifications, and bidirectional verification traceability. Use when creating documentation for a new or existing repository, migrating a monolithic AGENTS.md, defining or auditing V-model traceability, interviewing developers to recover intended behavior, adding nested AGENTS.md files, organizing agent context, reviewing .agents consistency, or compacting stale and duplicated repository context.
---

# Document Repository V-Model

Create a small, navigable documentation system that separates normative product
specification from implementation decisions. Treat the V-model as a general repository
profile, not as a claim of NASA, FDA, ECSS, or V-Modell XT compliance.

## Start

1. Read every applicable repository instruction before inspecting or changing files.
2. Determine the repository boundary, worktree rules, code roots, existing documentation,
   and whether the request is creation, migration, review, or update.
3. Preserve useful material and user changes. Do not infer intended behavior from code or
   tests alone.
4. Keep normative behavior under `.agents/v-model/`; keep implementation-facing
   learning, task, reference, and explanation material in `.agents/context/`.
5. Load only the references needed for the selected workflow. Never recursively load the
   entire `.agents/` tree.

## Select a Workflow

- For a new repository, read [discovery and interviews](references/discovery-and-interviews.md),
  interview in short rounds, confirm stakeholder outcomes before deriving requirements,
  then add context and routers only as real boundaries emerge.
- For an existing repository or monolithic guide, read
  [discovery and interviews](references/discovery-and-interviews.md) and
  [repository layout](references/repository-layout.md). Discover evidence read-only,
  classify observed behavior, and baseline only confirmed intent.
- For a consistency review or compaction, read
  [review and compaction](references/review-and-compaction.md). Update canonical content
  before shortening routers, then recheck links, traceability, and meaning.
- For a feature or release update, run a mini-V: revise affected outcomes and requirements,
  update contracts and verification actions, record implementation decisions separately,
  and assess regression impact.

Read [V-model and traceability](references/v-model-and-traceability.md) whenever creating,
changing, or auditing specification records. Read
[agent context documentation](references/agent-context-documentation.md) only when
creating, migrating, splitting, reviewing, or compacting `.agents/context/`; skip it for
router-only or V-model-only work. Read
[subagent playbooks](references/subagent-playbooks.md) only when delegation is permitted
and risk, scale, or requested independence justifies separate investigators or reviewers.

## Build the Documentation

Use [repository layout](references/repository-layout.md) as the topology contract. Start
from the files under `assets/templates/` selectively; do not copy a template for a
boundary or record that does not exist. Replace every template token and adapt commands
to repository evidence.

Keep each `AGENTS.md` to inherited-scope deltas, local commands and rules, and links that
say when deeper context should be opened. Put detailed implementation-facing material in
selectively routed context files. Use stable specification and verification IDs exactly
as defined by the V-model reference, with objective pass criteria and many-to-many
reverse links.

When intent is uncertain, preserve the uncertainty explicitly and ask the developer only
about intent or genuine tradeoffs. Do not silently choose code, tests, or old prose as
the authority. Do not write an unconditional normative claim when repository evidence
already contains a counterexample.

## Validate

Run the dependency-free, read-only linter from this skill directory:

```text
python3 scripts/lint_repository_docs.py REPOSITORY \
  [--source-root PATH ...] [--json] [--fail-on-warn]
```

Use repeated `--source-root` options for nonstandard or polyglot layouts. Without an
option, the linter uses `src` only when it exists. Resolve every integrity error. Treat
warnings proportionally, but remove avoidable router-size and duplication warnings.

Then review semantics the linter cannot prove:

1. Confirm each normative statement represents intended behavior.
2. Confirm specifications remain understandable without decision documents.
3. Try to falsify universal claims with boundary, malformed, and fallback cases.
4. Confirm every clause in an action’s pass criterion is supported by the cited evidence
   and that its status is no stronger than that evidence.
5. Confirm evidence references are durable and statuses are current.
6. Confirm each context leaf has one dominant need and routers load only relevant detail.
7. Confirm no source files changed when the task was documentation-only.

## Report

Report the selected profile, code roots, files created, moved, or retired, unresolved
intent or traceability gaps, linter result, semantic review result, developer
confirmations still needed, and any checks not run.
