# Review and Compaction

Use this reference for a holistic goal-versus-code review or for reducing persistent
agent context without weakening current guidance.

## Choose the review scope

- **Holistic review:** Interview the developer, create a temporary V-model, compare the
  whole codebase with confirmed goals, update durable docs, and delete the V-model at
  completion.
- **Documentation review:** Check routers, context, commands, links, duplication, and
  drift with the V-model absent. Do not reconstruct one.

Review persistent docs after changes to architecture, code roots, ownership boundaries,
supported environments, commands, or test strategy. Run the linter first, but do not
treat a clean result as semantic approval.

## Independent review streams

When scale and permissions allow, separate these passes:

1. **Router and link integrity:** scopes, code roots, inheritance deltas, open conditions,
   local links, and meaningful boundaries.
2. **Code/test versus context:** implementation, tests, CI, commands, anchors,
   compatibility, rationale, and context-need fit.
3. **Duplication and context cost:** repeated prose, oversized routers, mixed-purpose
   topics, stale logs, unnecessary hops, and default-loaded detail.
4. **Intent and coverage:** only for a holistic review; compare temporary V-model records
   with source and evidence, including counterexamples and nonconformance.

Use an independent reviewer for high-risk conclusions. Reconcile findings centrally;
reviewers return evidence and impact rather than competing rewrites.

## Reconciliation order

1. Resolve or explicitly record conflicts about intent.
2. Update durable context and commands.
3. Repair links and indexes.
4. Shorten root and nested routers last.
5. Re-run mechanical and semantic review after moves or deletions.
6. For a holistic review, transfer unresolved work to concise current gaps, remove
   V-model links, delete the V-model, and lint with `--v-model absent`.

## Compaction rules

- Replace duplicated prose with one canonical statement and contextual links.
- Keep a rule in the closest router where it applies; remove inherited restatements.
- Give every context leaf one dominant need: `Guided learning`, `Task playbook`,
  `Reference`, or `Explanation`.
- Split a mixed-purpose document only when substantial sections have distinct open
  conditions and are independently useful.
- Merge small topics only when agents always need them together.
- Remove obsolete current-state material and rely on Git history.
- Retain a brief retirement note only when compatibility or migration work needs it.
- Keep generated reports and bulky artifacts outside `.agents/`.
- Do not copy a temporary V-model into context. Preserve only useful current knowledge
  and brief actionable gaps.

Before deleting or moving a document, find inbound links and repair them in the same
change.

## Warning budgets

The linter warns at these defaults:

| Document | Lines | Words | Records |
| --- | ---: | ---: | ---: |
| Root `AGENTS.md` | 100 | 700 | — |
| Nested `AGENTS.md` | 40 | 250 | — |
| Any `.agents/**/index.md` | 100 | 600 | — |
| Context detail or active V-model shard | 200 | 1,200 | 40 |

Treat a warning as a retrieval-cost signal. A justified large context leaf may remain,
but an oversized router is usually the wrong place for detail. Use `--fail-on-warn` for
a strict gate after proportional exceptions have been resolved.

The linter also checks context metadata, reachability, routing depth, duplicate prose,
bulky artifacts, likely source boundaries without routers, and placeholders in active
baselined profiles.

## Semantic checklist

- Does each `AGENTS.md` say what to open and when?
- Can an agent reach the relevant context without loading unrelated material?
- Does each context leaf serve its declared need and remain useful without a V-model?
- Do documented commands work from their stated scope?
- Do prose claims about source paths, workflows, and child routers match the repository?
- Are current architecture decisions and rationale kept in context rather than routers?
- Are unresolved implementation gaps brief, actionable, and current?
- For a holistic review, does each normative statement reflect confirmed intent rather
  than observed behavior?
- Have universal claims survived boundary and counterexample checks?
- Does cited evidence exercise every clause, direction, entry point, and edge case it
  claims?
- Do CI values, tags, flags, and filters select the cited tests end to end?
- Are design defects, missing behavior, unintended behavior, and verification gaps
  visible rather than normalized away?
- At final handoff, is `.agents/v-model/` absent with no stale links or IDs?

## Idempotence check

After a broad documentation update, run a second pass from the resulting repository
state. It should make no unnecessary edits. A nonempty second diff indicates unstable
ordering, duplicated authority, unresolved template tokens, or unclear routing.
