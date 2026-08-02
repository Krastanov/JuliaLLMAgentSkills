# Agent Context Documentation

Read this reference when creating, splitting, reviewing, or compacting
`.agents/context/`. Adapt the four needs from [Diátaxis](https://diataxis.fr/) for agent
retrieval; do not turn them into mandatory directories.

## Choose one retrieval need

| Need | The agent needs to | Include | Exclude |
| --- | --- | --- | --- |
| Guided learning | Acquire an unfamiliar repository skill through a safe experience | One supported path, checkpoints, expected observations | Production mutation, broad alternatives, background essays |
| Task playbook | Complete a concrete task while already competent | Preconditions, actions, branches, validation, recovery | Teaching detours, embedded rationale |
| Reference | Look up exact facts about current machinery | Commands, mappings, interfaces, errors, limits, source anchors | Workflow instruction, argumentative prose |
| Explanation | Understand why the implementation has its present shape | Mental models, rationale, alternatives, tradeoffs, consequences | Step-by-step procedures, duplicated lookup tables |

Use the [Diátaxis compass](https://diataxis.fr/compass/) to distinguish acting from
understanding and acquiring from applying knowledge. Give each leaf one dominant need.
Split only when another section has a distinct open condition and is useful by itself.

## Route for selective loading

Use `.agents/index.md` as the persistent entry point:

```markdown
| Context | Need | Open when | Do not open when |
| --- | --- | --- | --- |
| [Release flow](context/releases.md) | Task playbook | Preparing or recovering a release | Editing local algorithms |
```

Keep leaves topic-oriented and flat by default. Add one subindex for a coherent product,
domain, or workflow boundary when an index presents more than seven choices or exceeds
its router budget. Permit at most one subindex hop from `.agents/index.md` to a leaf.

A nested `AGENTS.md` should link directly to the relevant leaf when known. During an
initial design or holistic review, `.agents/index.md` may also link to the temporary
V-model. Remove that link with the V-model at task completion.

## Write a context leaf

Start every leaf with retrieval metadata:

```markdown
# Topic

- **Context need:** Guided learning
- **Open when:** ...
- **Do not open when:** ...
- **Review when:** ...
- **Known gaps:** None
```

`Known gaps` is optional. Use it for a short, actionable statement of unfinished current
behavior, including unfinished work transferred from a temporary V-model. Do not retain
V-model IDs or reproduce the discarded specification.

Shape the body for its need:

- **Guided learning:** State the learning outcome and safe prerequisites. Lead through
  one reproducible path with checkpoints and expected observations. End with a
  completion check and next capability.
- **Task playbook:** State the objective, prerequisites, and constraints. Give actions in
  goal order, branch where repository state requires it, then cover validation, failure
  handling, rollback, or handoff.
- **Reference:** Optimize for scanning with concise tables, lists, exact values, and
  canonical source anchors. Describe facts; do not prescribe a task or argue for a
  design.
- **Explanation:** Begin with the question or mental model. Explain forces, rationale,
  alternatives, tradeoffs, and implications. Link operational steps and exact facts.

## Keep context durable

Describe how to use the project as it exists and how to develop it further. Keep current
commands, implementation decisions, architecture, source anchors, and rationale here.
Avoid coupling persistent context to a temporary V-model.

When a V-model is active, use it to sharpen the docs, but keep the docs understandable
without it. Before deleting the V-model, transfer only durable knowledge and concise
unresolved gaps. Avoid copying detailed requirements, trace tables, or temporary review
status into context.

## Review proportionally

Create a leaf only for a recurring retrieval need supported by real repository work.
During review, verify that open conditions are distinct, every leaf is routed, body
shape matches its declared need, and links replace duplicated prose. Merge or split only
for retrieval, remove stale current state, and keep generated output outside the live
context tree.
