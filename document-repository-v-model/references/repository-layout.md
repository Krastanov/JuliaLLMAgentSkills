# Repository Layout

Use this reference when creating or reorganizing agent-facing documentation, declaring
code roots, or deciding where nested routers and context topics belong.

## Contents

- [Persistent topology](#persistent-topology)
- [Temporary V-model](#temporary-v-model)
- [Declare code roots](#declare-code-roots)
- [Keep routers small](#keep-routers-small)
- [Route repository context](#route-repository-context)
- [Use the templates selectively](#use-the-templates-selectively)
- [Exclude transient material](#exclude-transient-material)

## Persistent topology

Use a short `AGENTS.md` as a map into selectively loaded repository knowledge. Keep the
normal repository state independent of any V-model:

```text
AGENTS.md
<code-root>/AGENTS.md
<meaningful-subsystem>/AGENTS.md
.agents/
├── index.md
└── context/
    └── <topic>.md
```

This applies the progressive-disclosure pattern described by
[OpenAI's harness-engineering guidance](https://openai.com/index/harness-engineering/).
The `.agents/` directory is this skill's convention, not an OpenAI requirement. Create
only context topics and nested routers supported by real retrieval needs and boundaries.

## Temporary V-model

Add `.agents/v-model/` only during an initial design before code or a holistic codebase
review:

```text
.agents/v-model/
├── index.md
├── 01-stakeholder-outcomes.md
├── 02-system-requirements.md
├── 03-subsystem-contracts.md
├── 04-component-contracts.md
└── verification.md
```

While it is active, link it from `.agents/index.md` with a clear temporary open
condition. A task branch may carry it for multi-agent coordination. Before completing
the implementation or review:

1. Transfer current usage, architecture, commands, and development knowledge into
   durable context.
2. Rewrite unfinished requirements as brief, actionable gaps in the relevant context
   topic or issue tracker; do not retain orphaned V-model IDs.
3. Remove links to the V-model, then delete `.agents/v-model/`.
4. Run the linter with `--v-model absent`.

Do not recreate this tree for routine changes or maintain it as a parallel description
of an established, reviewed codebase.

For a large active profile, replace a layer file with a same-named directory containing
`index.md` and topic shards. For independently released products, place one complete
profile per product under `.agents/v-model/` and route to them from its index. Keep IDs
unique repository-wide.

## Declare code roots

- Require `src/AGENTS.md` whenever `src/` exists.
- For a nonstandard or polyglot repository, list every actual code root in the root
  router and create an equivalent router in each one. Examples include `app/`, `gui/`,
  `packages/`, `cmd/`, or a repository root containing executable code directly.
- Pass the same roots to the linter with repeated `--source-root` options. Do not invent
  `src/` merely to satisfy the profile.
- Treat an independently built frontend, backend, library, plugin, or service as a
  likely code root when its manifest and workflow are distinct.

## Keep routers small

Every `AGENTS.md` contains only:

1. Its scope and inherited-scope deltas.
2. Commands valid in that scope.
3. Local rules or invariants that directly guide work.
4. Links to canonical context with an explicit open condition.

Do not restate architecture, rationale, history, or long testing guides. Do not ask an
agent to read `.agents/` recursively. Add a nested router only for a meaningful
subsystem, ownership boundary, release unit, toolchain, or development workflow.

## Route repository context

Make `.agents/index.md` the repository-wide router. Link directly to a context leaf when
known, with explicit "open when" and "do not open when" conditions. Name topics for an
agent's retrieval task rather than organizational history.

Read [agent context documentation](agent-context-documentation.md) when creating,
classifying, splitting, or reviewing context. Keep the tree flat until a real product,
domain, or workflow boundary requires one additional routing hop. Never preload a
category or recursively read `.agents/context/`.

## Use the templates selectively

- `assets/templates/AGENTS-root.md`: persistent root router.
- `assets/templates/AGENTS-source.md`: persistent code-root or boundary router.
- `assets/templates/context-topic.md`: persistent context leaf.
- `assets/templates/v-model/`: temporary small single-product profile.

Copy, rename, and fill only what the repository needs. Replace all `{{TOKEN}}` values.
Move useful existing prose to its canonical home and replace duplicate copies with
links.

## Exclude transient material

Keep generated reports, large data exports, images, database files, recordings, and run
logs outside `.agents/`. Link to durable evidence instead. Rely on Git history for
obsolete prose unless compatibility work needs a short retirement note.
