---
name: julia-package-dev
description: Create and develop Julia packages in local environments, including package bootstrapping, multi-package workspaces, package extensions, and Pkg apps. Use when starting a package or managing package environments, dependencies, structure, and related development workflows.
---

# Julia Package Development

Use this skill for package-oriented Julia work: bootstrapping a package,
local environments, multi-package workspaces, extensions, and Pkg apps.

## Core Workflow

```julia
using Pkg

Pkg.activate("./dev")
Pkg.develop(path="./MyPackage.jl")
using MyPackage
```

Prefer environments over mutating the global default environment.

- Prefer `Pkg.test(...)` over directly executing `test/runtests.jl` when
  validating a package checkout.
- If dependency resolution behaves impossibly, inspect stale `Manifest.toml`
  files in the package root, `test/`, `docs/`, and custom subprojects before
  editing compat or source code.

## Multi-Repo Rule

- In a workspace with sibling repos, if compat or registry resolution blocks
  testing, first `Pkg.develop(path=...)` the local dependency checkouts already
  present, preferably on their current `master`/`main`.
- Do this before chasing registry lag or editing compat blindly.

## Pick a Topic

- Pkg commands and dependency management:
  `references/pkg-commands.md`
- Interactive debugging and exploration:
  `references/debugging.md`
- Multi-package development and release flow:
  `references/multipackage-git-workflow.md`
- Package extension patterns:
  `references/extension-patterns.md`
- Testing and documenting extensions:
  `references/extension-testing.md`
- User-facing extension error hints:
  `references/weakdephelpers.md`
- Pkg app scaffolding and CLI patterns:
  `references/pkg-app-patterns.md`

## Common Tasks

### Shared Workspace

```julia
using Pkg
Pkg.activate("quantum-dev")
Pkg.develop(path="./QuantumInterface.jl")
Pkg.develop(path="./QuantumSavory.jl")
```

## Notes

- Use `julia-tests` for test execution and organization.
- Use `julia-docs` for docs setup and doctests.
- Use `julia-comonicon` when you need a richer CLI than Pkg apps provide.

## Related Skills

- `julia-tests`
- `julia-docs`
- `julia-scratch`
