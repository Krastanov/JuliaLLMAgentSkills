---
name: julia-package-dev
description: Create and develop Julia packages in local environments, including package bootstrapping, multi-package workspaces, package extensions, and Pkg apps. Use when starting a package or managing package environments, dependencies, structure, and related development workflows.
---

# Julia Package Development

Use this skill for package-oriented Julia work: bootstrapping a package,
local environments, multi-package workspaces, extensions, and Pkg apps.

## Starting a Package

### PkgTemplates.jl

```julia
using PkgTemplates

t = Template(;
    user = "YourGitHubUsername",
    authors = "Your Name <your@email.com>",
    plugins = [
        Git(; manifest=false),
        GitHubActions(; extra_versions=["1.10", "nightly"]),
        Codecov(),
        Documenter{GitHubActions}(),
        License(; name="MIT"),
    ],
)

t("MyPackage")
```

### Minimal Start

```julia
using Pkg
Pkg.generate("MyPackage")
```

Then add dependencies and create `docs/` and `test/` subprojects with Pkg.

### Bootstrap Checklist

- [ ] Package created with `PkgTemplates` or `Pkg.generate`
- [ ] `src/MyPackage.jl` exposes the public API
- [ ] `test/` and `docs/` environments exist
- [ ] CI workflows are added
- [ ] Required secrets such as `CODECOV_TOKEN` and `DOCUMENTER_KEY` are configured

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
