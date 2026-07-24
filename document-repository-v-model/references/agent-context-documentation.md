# Agent Context Documentation

Read this reference only when creating, migrating, splitting, reviewing, or compacting
`.agents/context/`. Adapt the four needs from [Diátaxis](https://diataxis.fr/) for agent retrieval; do not turn them into four mandatory directories.
This profile calls them **Guided learning**, **Task playbook**, **Reference**, and **Explanation**.

## Choose one retrieval need

| Need | Diátaxis form | The agent needs to | Include | Exclude |
| --- | --- | --- | --- | --- |
| Guided learning | [Tutorial](https://diataxis.fr/tutorials/) | Acquire an unfamiliar repository skill through a safe experience | One supported path, checkpoints, and expected observations | Production mutation, broad alternatives, and background essays |
| Task playbook | [How-to guide](https://diataxis.fr/how-to-guides/) | Complete a concrete repository task while already competent | Preconditions, goal-directed actions, branches, validation, and recovery | Teaching detours and embedded rationale |
| Reference | [Reference](https://diataxis.fr/reference/) | Look up exact facts about current machinery | Terse commands, mappings, interfaces, errors, limits, and source anchors | Workflow instruction and argumentative prose |
| Explanation | [Explanation](https://diataxis.fr/explanation/) | Understand why the implementation has its present shape | Mental models, rationale, alternatives, tradeoffs, and consequences | Step-by-step procedures and duplicated lookup tables |

Use the [Diátaxis compass](https://diataxis.fr/compass/): ask whether the agent is acting or understanding, then whether it is acquiring or applying knowledge. Guided learning is action plus acquisition; a Task playbook is action plus application.
Reference is cognition plus application, and Explanation is cognition plus acquisition.

Give each leaf one dominant need. Split only when a substantial section has a different open condition and would be useful independently. Link incidental facts or rationale instead of duplicating them.

## Route for selective loading

Use `.agents/index.md` as the entry point and keep specification routing visually
separate from working context:

```markdown
## Specification

- [V-model](v-model/index.md) — open when changing observable behavior or evidence.

## Working context

| Context | Need | Open when | Do not open when |
| --- | --- | --- | --- |
| [Release flow](context/releases.md) | Task playbook | Preparing or recovering a release | Editing local algorithms |
```

Keep context leaves topic-oriented and flat by default. Do not create empty category
directories. Following [complex-hierarchy guidance](https://diataxis.fr/complex-hierarchies/), add one subindex for a coherent product, domain, or workflow boundary when an index presents more than seven context choices or exceeds its router budget.
Permit at most one context-subindex hop from `.agents/index.md` to a leaf; a leaf-to-leaf
link does not make the destination routed. Apply the seven-choice budget to every index;
split an oversized domain into sibling subindexes rather than nesting another level.

A nested `AGENTS.md` should link directly to the relevant leaf when known rather than
forcing the agent through an index. Add `Scope` only when products or audiences differ;
preserve physical paths during classification and carry the four-part structure in `Need`.

## Write a context leaf

Start every leaf with this retrieval metadata:

```markdown
# Topic

- **Context need:** Guided learning
- **Open when:** ...
- **Do not open when:** ...
- **Related specification IDs:** SYS-001, SUB-002
- **Review when:** ...
```

Use `None — repository-only workflow` only when the topic genuinely has no product-specification relationship. Add anchors and unresolved questions when they help the agent verify freshness or act safely.

Shape the body for its need:

- **Guided learning:** State the learning outcome and safe prerequisites. Lead through
  one reproducible path with small checkpoints and expected observations. End with a
  completion check and next capability. Link optional alternatives or theory elsewhere.
- **Task playbook:** State the concrete objective, prerequisites, and constraints. Give
  actions in goal order, branch where repository state requires it, then cover
  validation, failure handling, rollback, or handoff. Assume baseline competence.
- **Reference:** Optimize for scanning with concise tables, lists, and exact current
  values. Follow the structure of the implementation being described and cite canonical
  source anchors. Describe facts; do not prescribe a task or argue for a design.
- **Explanation:** Begin with the question or mental model. Explain forces, rationale,
  alternatives, tradeoffs, history that still affects current work, and implications.
  Keep the topic bounded and link operational steps or exact facts elsewhere.

## Preserve the specification boundary

`.agents/v-model/` is the only normative product-specification tree. It must remain
understandable without context documents. A context Reference describes current
implementation facts; it does not define required product behavior.

When an implementation decision becomes externally observable, promote only the invariant
and its objective acceptance meaning into the V-model. Keep the chosen mechanism and
rationale in context, with links back to the affected specification IDs. If intent is
unresolved, record the uncertainty instead of promoting observed behavior.

## Migrate and review proportionally

For new material, create a leaf only for a recurring retrieval need supported by actual
repository work. During migration, inventory mixed prose, assign a dominant need, retain
useful anchors, and update inbound links atomically. Do not move or split content merely
to populate all four needs.

During review, verify that open conditions are distinct, every leaf is routed, body
shape matches its declared need, and links replace duplicated prose. Merge or split only
for retrieval, remove stale current state, and keep generated output and run logs outside
the live context tree.
