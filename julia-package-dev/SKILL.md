---
name: julia-package-dev
description: Develop Julia packages in local environments, including multi-package workspaces, package extensions, and Pkg apps. Use when managing package environments, dependencies, package structure, and related development workflows.
---

# Julia Package Development

Use this skill for package-oriented Julia development: local environments,
multi-package workspaces, extensions, and Pkg apps.

## Core Workflow

```julia
using Pkg

Pkg.activate("./dev")
Pkg.develop(path="./MyPackage.jl")
using MyPackage
```

Prefer environments over mutating the global default environment.

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

### Interactive Development

```julia
using Revise
Pkg.activate("./dev")
Pkg.develop(path="./MyPackage.jl")
using MyPackage
```

### Shared Workspace

```julia
using Pkg
Pkg.activate("quantum-dev")
Pkg.develop(path="./QuantumInterface.jl")
Pkg.develop(path="./QuantumSavory.jl")
```

### Logging

```julia
@debug "Debug message"
@info "Informational message"
@warn "Warning message"
@error "Error message"
```

## Notes

- Use `julia-tests` for test execution and organization.
- Use `julia-docs` for docs setup and doctests.
- Use `julia-comonicon` when you need a richer CLI than Pkg apps provide.

## Related Skills

- `julia-tests`
- `julia-docs`
- `julia-scratch`

