# Repository Layout

Use this reference when creating or migrating the documentation tree, declaring code
roots, or deciding where nested routers and topic files belong.

## Contents

- [Why this layout](#why-this-layout)
- [Default topology](#default-topology)
- [Declare code roots](#declare-code-roots)
- [Keep routers small](#keep-routers-small)
- [Route repository context](#route-repository-context)
- [Keep specification separate](#keep-specification-separate)
- [Use the templates selectively](#use-the-templates-selectively)
- [Exclude transient material](#exclude-transient-material)

## Why this layout

[OpenAI’s harness-engineering guidance](https://openai.com/index/harness-engineering/)
describes a short `AGENTS.md` as a map into structured repository knowledge, with
progressive disclosure and mechanical checks for cross-links and drift. Apply that
pattern here with `.agents/` as the selectively loaded knowledge tree. The exact
directory name is this profile’s convention, not an OpenAI product requirement.

## Default topology

```text
AGENTS.md
<code-root>/AGENTS.md
<meaningful-subsystem>/AGENTS.md
.agents/
├── index.md
├── context/
│   └── <topic>.md
└── v-model/
    ├── index.md
    ├── 01-stakeholder-outcomes.md
    ├── 02-system-requirements.md
    ├── 03-subsystem-contracts.md
    ├── 04-component-contracts.md
    └── verification.md
```

Treat this as a default, not a demand for empty files. Create the complete V-model
profile, but add context topics and nested routers only for information and boundaries
that exist.

## Declare code roots

- Require `src/AGENTS.md` whenever `src/` exists.
- For a nonstandard or polyglot repository, list every actual code root in the root
  router and create an equivalent router in each one. Examples include `app/`, `gui/`,
  `packages/`, `cmd/`, or a repository root that contains executable code directly.
- Pass the same roots to the linter with repeated `--source-root` options. Do not invent
  a `src/` directory just to satisfy the profile.
- Treat an independently built frontend, backend, library, plugin, or service as a
  likely code root when its manifest and workflow are distinct.

## Keep routers small

Every `AGENTS.md` contains only:

1. Its scope and inherited-scope deltas.
2. Commands that are valid in that scope.
3. Local rules or invariants that directly guide work.
4. Links to canonical topic or specification documents, with an explicit “open when”
   condition.

Do not restate architecture, requirement records, rationale, history, or long testing
guides. Do not ask an agent to read `.agents/` recursively. A nested router overrides or
adds to inherited guidance; it does not copy the parent.

Add a nested router only when a directory is a meaningful subsystem, module, ownership
boundary, or distinct development workflow. File count alone is not a boundary. A stable
interface, separate release unit, different toolchain, or different validation command
is stronger evidence.

## Route repository context

Make `.agents/index.md` the repository-wide router. Link directly to context leaves when
the relevant leaf is known, and give every link explicit “open when” and “do not open
when” conditions. Keep names aligned to an agent's retrieval task rather than
organizational history.

When creating, classifying, splitting, or reviewing context, read
[agent context documentation](agent-context-documentation.md). It defines four
agent-facing retrieval needs and the adaptive rules for adding subindexes without
forcing four category directories. Keep the tree flat until a real product, domain, or
workflow boundary makes another routing hop useful. Never ask an agent to preload a
category or recursively read `.agents/context/`.

## Keep specification separate

`.agents/v-model/` is the only normative product-specification tree in this profile.
Keep it understandable without opening `.agents/context/`. Section-level context links
may supply essential background, but must not carry normative meaning.

For a large layer, replace its canonical Markdown file with a same-named directory:

```text
.agents/v-model/03-subsystem-contracts/
├── index.md
├── storage.md
└── transport.md
```

The directory index routes to shards. Keep record IDs unique repository-wide. Apply the
same file-or-directory form to `verification` when verification records need sharding.

For independently released products in one repository, make `.agents/v-model/index.md`
route to one complete profile per product:

```text
.agents/v-model/
├── index.md
├── product-a/
│   ├── index.md
│   └── <all four layers plus verification>
└── product-b/
    ├── index.md
    └── <all four layers plus verification>
```

Do not combine products merely because they share a repository. Do not split one product
merely because it uses several languages.

## Use the templates selectively

- `assets/templates/AGENTS-root.md`: root router.
- `assets/templates/AGENTS-source.md`: code-root or meaningful-boundary router.
- `assets/templates/context-topic.md`: one context leaf, shaped for its retrieval need.
- `assets/templates/v-model/`: a complete small single-product profile.

Copy, rename, and fill only what the repository needs. Replace all `{{TOKEN}}` values.
Preserve existing useful prose by moving it to the correct canonical home and replacing
the old copy with a link.

## Exclude transient material

Keep generated reports, large CSV/JSON exports, images, database files, recordings, and
run logs outside the live `.agents/` tree. Link to a durable evidence location instead.
Retain current status and durable references in `verification.md`, not copied console
output. Rely on Git history for obsolete prose unless a short retirement record is
needed for compatibility.
