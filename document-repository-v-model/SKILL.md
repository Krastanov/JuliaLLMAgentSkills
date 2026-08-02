---
name: document-repository-v-model
description: "Create and audit durable agent-facing repository documentation. Use a temporary V-model only when interviewing a developer before code exists to turn a rough project prompt into a design independent agents can implement, or during a holistic codebase review to compare implementation with intended goals and expose design or implementation gaps. Also use when creating or migrating nested AGENTS.md routers and selectively loaded .agents context, or linting and compacting agent documentation."
---

# Document Repository V-Model

Build durable `AGENTS.md` routers and `.agents/context/` documentation. Create a V-model
only as a temporary coordination artifact for an initial design or a holistic review.

## Start

1. Read every applicable repository instruction before inspecting or changing files.
2. Establish the repository boundary, worktree rules, code roots, existing documentation,
   and developer authority.
3. Choose exactly one workflow:
   - **Initial design:** no implementation exists yet; turn a rough prompt into an
     implementation-ready design through developer interviews.
   - **Holistic review:** compare an existing codebase with developer-confirmed goals to
     find design defects and missing implementation.
   - **Documentation maintenance:** improve persistent agent guidance without a V-model.
4. Preserve useful material and user changes. Treat code and tests as evidence of current
   behavior, not proof of intended behavior.

Read [subagent playbooks](references/subagent-playbooks.md) only when delegation is
permitted and the selected workflow benefits from independent lanes.

Do not create or maintain a V-model for routine feature work, releases, or ordinary
documentation updates. Once a codebase has been implemented and holistically reviewed,
the cost and drift risk of a persistent parallel specification outweigh its value.

## Run an Initial Design

Read [discovery and interviews](references/discovery-and-interviews.md), then read
[V-model and traceability](references/v-model-and-traceability.md).

1. Before writing code, interview the developer in short rounds about users, scenarios,
   boundaries, failure behavior, constraints, non-goals, interfaces, and acceptance.
2. Draft and confirm a temporary `.agents/v-model/` that makes the rough prompt precise
   enough for independent agents to implement nonoverlapping parts.
3. Plan objective verification with the requirements. Keep implementation choices and
   working instructions in `.agents/context/`, not in normative records.
4. Develop the persistent routers and context while implementation proceeds.
5. Reconcile the implementation, verification evidence, and developer intent.
6. Move durable usage and development knowledge into agent documentation. Record any
   unfinished behavior there as brief, actionable current gaps.
7. Delete `.agents/v-model/` and every link or ID that depends on it before final handoff.

The V-model may be committed on a task branch so several agents can coordinate, but it
must not remain in the completed repository state.

## Run a Holistic Review

Read [discovery and interviews](references/discovery-and-interviews.md),
[V-model and traceability](references/v-model-and-traceability.md), and
[review and compaction](references/review-and-compaction.md).

1. Discover public behavior, source boundaries, tests, CI, and existing documentation
   read-only.
2. Interview the developer about intended users, outcomes, compatibility, exclusions,
   risk, and surprising behavior that evidence cannot classify.
3. Build a temporary V-model from confirmed goals and compare every layer with code and
   evidence. Report missing behavior, unintended behavior, weak boundaries, and missing
   verification without silently normalizing either side.
4. Improve persistent agent documentation with confirmed current usage, architecture,
   workflows, and concise unresolved gaps.
5. Complete the review or agreed corrections, then delete the V-model and its links.

For documentation maintenance without either bounded task, do not reconstruct a
V-model. Read [repository layout](references/repository-layout.md) and
[agent context documentation](references/agent-context-documentation.md) as needed.

## Build Durable Documentation

Use [repository layout](references/repository-layout.md) as the topology contract. Start
from `assets/templates/` selectively and replace every template token.
Read [agent context documentation](references/agent-context-documentation.md) when
creating, splitting, or compacting context topics.

Keep each `AGENTS.md` to inherited-scope deltas, local commands and rules, and links with
clear open conditions. Put detailed, implementation-facing learning, task, reference,
and explanation material in `.agents/context/`. Ensure these documents remain useful
after `.agents/v-model/` is removed.

When intent is uncertain, record the gap and ask the developer about intent or genuine
tradeoffs. Do not make an unconditional claim that repository evidence contradicts.

## Validate

Run the dependency-free, read-only linter from this skill directory with an explicit
V-model state:

```text
python3 scripts/lint_repository_docs.py REPOSITORY --v-model active \
  [--source-root PATH ...] [--json] [--fail-on-warn]

python3 scripts/lint_repository_docs.py REPOSITORY --v-model absent \
  [--source-root PATH ...] [--json] [--fail-on-warn]
```

Use `active` only during initial design, implementation coordination, or holistic
review. It requires, routes, and validates `.agents/v-model/`. Use `absent` for normal
repository life and final handoff; it rejects a retained V-model, stale links, and
confirmed ID references while flagging ambiguous IDs for review. Run `absent` before
declaring either bounded task complete.

Then confirm semantics the linter cannot prove: statements match developer intent,
commands work in their documented scope, links load only relevant context, cited tests
exercise claimed behavior, and unresolved gaps remain visible.

## Report

Report the workflow, code roots, durable documentation changed, developer confirmations,
design or implementation gaps, relevant linter results, V-model removal when applicable,
checks run, and checks not run.
