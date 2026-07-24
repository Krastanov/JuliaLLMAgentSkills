# Review and Compaction

Use this reference for scheduled audits, release readiness, drift checks, and efforts to
reduce agent context cost without weakening meaning.

## Contents

- [Review triggers](#review-triggers)
- [Independent review streams](#independent-review-streams)
- [Reconciliation order](#reconciliation-order)
- [Compaction rules](#compaction-rules)
- [Warning budgets](#warning-budgets)
- [Semantic consistency checklist](#semantic-consistency-checklist)
- [Idempotence check](#idempotence-check)

## Review triggers

Review after changes to observable behavior, public interfaces, architecture, code roots,
ownership boundaries, supported environments, or test strategy. Also review before a
major release and at least quarterly for an actively maintained repository.

Run the linter first to expose mechanical failures, but do not treat a clean linter result
as semantic approval.

## Independent review streams

When scale and permissions allow, separate these passes:

1. **Router and link integrity:** scopes, code roots, inheritance deltas, open/avoid
   routing, local links, and meaningful boundaries.
2. **V-model and traceability:** record quality, parent layers, objective criteria,
   right-side coverage, methods, statuses, evidence, and nonconformance.
3. **Code/test versus context:** current implementation, tests, CI, commands, anchors,
   compatibility, decision-document drift, and context-need fit.
4. **Duplication and context cost:** repeated prose, oversized routers, overlapping
   or mixed-purpose topics, stale logs, unnecessary routing hops, and material that
   should not load by default.

Use an independent reviewer for high-risk conclusions. Reconcile findings centrally;
reviewers identify evidence and impact but do not each rewrite the canonical files.

## Reconciliation order

1. Resolve or explicitly record conflicts about intent.
2. Update canonical V-model or context content.
3. Repair traceability and durable evidence references.
4. Update indexes and detailed topic routing.
5. Shorten root and nested routers last.
6. Re-run mechanical and semantic review after every move or deletion.

This order prevents a concise router from pointing to stale or missing detail.

## Compaction rules

- Replace duplicated prose with one canonical statement and contextual links.
- Keep a rule in the closest router where it applies; remove inherited restatements.
- Separate normative specification and router-local rules before classifying context.
- Assign every context leaf exactly one dominant need: `Guided learning`,
  `Task playbook`, `Reference`, or `Explanation`.
- Split a mixed-purpose context document only when substantial sections serve distinct
  retrieval needs; otherwise keep its dominant need and link to supporting context.
- Do not add empty need categories, and do not move a leaf merely to fill a taxonomy.
- Merge small topics only when agents always need them together and they share a
  dominant need.
- Remove obsolete current-state material and rely on Git history.
- Retain a brief retirement/replacement record only when compatibility or migration
  work needs it.
- Never shorten a requirement by weakening actors, conditions, thresholds, exclusions,
  or pass/fail meaning.
- Prune historical run logs from verification records. Retain current status, durable
  evidence locations, and unresolved nonconformance.
- Keep generated reports and bulky artifacts outside `.agents/`.

Before deleting or moving a document, find all inbound links and specification IDs.
Repair those references in the same change. Verify that a proposed merge does not combine
normative specification with implementation rationale.

## Warning budgets

The linter warns, rather than fails, at these default budgets:

| Document | Lines | Words | Records |
| --- | ---: | ---: | ---: |
| Root `AGENTS.md` | 100 | 700 | — |
| Nested `AGENTS.md` | 40 | 250 | — |
| Any `.agents/**/index.md` | 100 | 600 | — |
| Context detail or V-model shard | 200 | 1,200 | 40 |

Treat a warning as a retrieval-cost signal. A justified large shard may remain, but an
oversized router is usually the wrong place for detail. Use `--fail-on-warn` for a strict
release gate after known proportional exceptions have been resolved.

The linter also warns about invalid context metadata, unreachable context leaves,
oversized or over-nested context routing, unjustified missing specification links,
duplicated prose, bulky artifacts, likely source boundaries without routers, and
placeholders in baselined profiles.

## Semantic consistency checklist

- Does each `AGENTS.md` say what to open and when, without preloading everything?
- Starting from a concrete task, can an agent reach the relevant context leaf without
  browsing or loading unrelated context?
- Does each context leaf consistently serve its declared dominant need:
  `Guided learning`, `Task playbook`, `Reference`, or `Explanation`?
- Do prose claims about child routers match routers that actually exist?
- Are commands executable from the scope where they are documented?
- Does each normative record express intended behavior rather than observed accidents?
- Has each universal or deterministic claim survived boundary and counterexample review?
- For destructive behavior, were path traversal, symlinks, stale state, partial prior
  runs, invalid limits, and repeated invocations checked?
- Do fail-open or recovery claims distinguish caller continuation from partial side
  effects, rollback, and retry behavior?
- Can the V-model be understood without decision documents?
- Do parent and verification links represent real semantic coverage?
- Does every claimed consumer of a shared schema or registry actually load or derive
  from it, rather than maintain an independent copy?
- Does each criterion permit an objective decision, and does cited evidence exercise
  every clause, direction, entry point, and edge case it claims?
- Are fixtures discriminating, or could a swapped field, direction, branch, or order
  produce the same expected result?
- Do CI matrix values, environment variables, tags, and filters actually select the
  cited tests end to end?
- Does each `passing` status still match durable evidence?
- Are current source paths, workflow names, and tool choices kept out of normative
  compatibility or interface outcomes?
- Are failure paths, external interfaces, performance, security, and compatibility
  covered in proportion to risk?
- Do context decisions still match source and test anchors?
- Are unresolved mismatches visible rather than normalized away?

## Idempotence check

After a migration or broad update, run a second documentation pass from the resulting
repository state. It should make no unnecessary edits. A nonempty second diff indicates
unstable ordering, duplicated authority, unresolved template tokens, or unclear routing.
Fix the cause instead of accepting churn.
