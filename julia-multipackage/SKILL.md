---
name: julia-multipackage
description: Work with multiple inter-related Julia packages simultaneously, managing dependencies across packages and testing changes together. Use this skill when developing packages that depend on each other.
---

# Julia Multi-Package Development

Work with multiple inter-related Julia packages simultaneously, managing dependencies
across packages and testing changes together.

## When to Use

- Developing a package alongside its dependencies
- Working on packages in the same ecosystem
- Testing changes across package boundaries
- Coordinating breaking changes across packages

## Setting Up a Shared Environment

```julia
using Pkg
Pkg.activate("quantum-dev")

Pkg.develop(path="./QuantumInterface.jl")
Pkg.develop(path="./QuantumClifford.jl")
Pkg.develop(path="./QuantumSavory.jl")
```

## Directory Structure

```
workspace/
├── quantum-dev/           # Shared dev environment
│   ├── Project.toml
│   └── Manifest.toml
├── QuantumInterface.jl/
├── QuantumClifford.jl/
└── QuantumSavory.jl/
```

## Testing Changes Across Packages

### Test Downstream Package with Local Changes

```bash
julia --project=$(mktemp -d) -e '
    using Pkg
    Pkg.develop(path="./QuantumClifford.jl")  # Local changes
    Pkg.add("QuantumSavory")                   # Released version
    Pkg.test("QuantumSavory")
'
```

### Test with All Local Packages

```bash
julia --project=quantum-dev -e '
    using Pkg
    Pkg.test("QuantumSavory")  # Uses all dev'd packages
'
```

## Quick Reference

| Task | Command |
|------|---------|
| Develop package | `Pkg.develop(path="./Pkg.jl")` |
| Exit dev mode | `Pkg.free("Pkg")` |
| Check status | `Pkg.status()` |
| Test package | `Pkg.test("Pkg")` |
| Create temp env | `Pkg.activate(mktempdir())` |

## Reference

- **[Git Workflow](references/git-workflow.md)** - Branching and PR strategies for multi-package changes
- **[CI Testing](references/ci-testing.md)** - Buildkite downstream testing configuration

## Related Skills

- `julia-package-dev` - Single package development
- `julia-github` - Git and PR workflows
- `julia-ci-buildkite` - Downstream testing in CI
