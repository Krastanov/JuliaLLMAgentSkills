---
name: julia-multipackage
description: Work with multiple inter-related Julia packages simultaneously, managing dependencies across packages and testing changes together. Use this skill when developing packages that depend on each other.
---

# Julia Multi-Package Development

Work with multiple inter-related Julia packages simultaneously, managing dependencies
across packages and testing changes together.

## When to Use Multi-Package Development

- Developing a package alongside its dependencies
- Working on packages in the same ecosystem (e.g., QuantumClifford + QuantumSavory)
- Testing changes across package boundaries
- Coordinating breaking changes across packages

## Setting Up a Development Environment

### Create a Shared Environment

```julia
# Create a new environment for multi-package work
using Pkg
Pkg.activate("quantum-dev")  # or any name

# Develop all related packages
Pkg.develop(path="./QuantumInterface.jl")
Pkg.develop(path="./QuantumClifford.jl")
Pkg.develop(path="./QuantumSavory.jl")
Pkg.develop(path="./BPGates.jl")
```

### Command Line Setup

```bash
# Create environment and develop packages
julia -e '
    using Pkg
    Pkg.activate("quantum-dev")
    Pkg.develop(path="./QuantumInterface.jl")
    Pkg.develop(path="./QuantumClifford.jl")
    Pkg.develop(path="./QuantumSavory.jl")
    Pkg.instantiate()
'
```

## Directory Structure

Typical multi-package workspace:

```
workspace/
├── quantum-dev/           # Shared dev environment
│   ├── Project.toml
│   └── Manifest.toml
├── QuantumInterface.jl/
├── QuantumClifford.jl/
├── QuantumSavory.jl/
├── BPGates.jl/
└── PBCCompiler.jl/
```

## Testing Changes Across Packages

### Test Downstream Package with Local Changes

```bash
# Test QuantumSavory with local QuantumClifford changes
julia --project=$(mktemp -d) -e '
    using Pkg
    Pkg.develop(path="./QuantumClifford.jl")  # Local changes
    Pkg.add("QuantumSavory")                    # Released version
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

## Buildkite Downstream Testing

Automatically test downstream packages in CI:

```yaml
# .buildkite/pipeline.yml
steps:
  - label: "Downstream Tests - {{matrix.PACKAGE}}"
    plugins:
      - JuliaCI/julia#v1:
          version: "1"
    command:
      - julia --project=$(mktemp -d) -e '
        using Pkg;
        pkg"dev .";
        Pkg.add("{{matrix.PACKAGE}}");
        Pkg.build("{{matrix.PACKAGE}}");
        Pkg.test("{{matrix.PACKAGE}}");'
    matrix:
      setup:
        PACKAGE: ["QuantumSavory", "BPGates", "QuantumSymbolics"]
```

## Git Workflow for Multi-Package Changes

### 1. Create Feature Branches in All Affected Packages

```bash
# For each package that needs changes
cd QuantumClifford.jl
git checkout -b feature/new-api

cd ../QuantumSavory.jl
git checkout -b feature/adapt-to-new-api
```

### 2. Make Changes and Test Together

```bash
# Develop both packages
julia -e '
    using Pkg
    Pkg.activate("temp-test")
    Pkg.develop(path="./QuantumClifford.jl")
    Pkg.develop(path="./QuantumSavory.jl")
    Pkg.test("QuantumSavory")
'
```

### 3. Create PRs in Dependency Order

1. First PR: Changes to the dependency (QuantumClifford)
2. Wait for merge and release
3. Update downstream package's compat bounds
4. Second PR: Changes to dependent package (QuantumSavory)

## Managing Compat Bounds

When making breaking changes:

### In the Dependency

```toml
# QuantumClifford.jl/Project.toml
version = "0.12.0"  # Bump major/minor for breaking changes
```

### In the Dependent Package

```toml
# QuantumSavory.jl/Project.toml
[compat]
QuantumClifford = "0.12"  # Update after release
```

## Testing Unreleased Dependencies

### Using Branch in CI

```yaml
# Test against unreleased branch
- run: |
    julia -e '
      using Pkg
      Pkg.add(url="https://github.com/Org/Dependency.jl", rev="feature-branch")
      Pkg.test()
    '
```

### Local Development with Specific Commits

```julia
using Pkg
Pkg.develop(url="https://github.com/Org/Dependency.jl", rev="abc123")
```

## Common Patterns

### Check Which Version is Active

```julia
using Pkg
Pkg.status()  # Shows all packages and whether they're dev'd
```

### Free a Package from Dev Mode

```julia
Pkg.free("PackageName")  # Returns to registered version
```

### Update to Latest Registered Version

```julia
Pkg.free("PackageName")
Pkg.update("PackageName")
```

### Temporarily Test with Released Version

```julia
# Save current state
Pkg.activate("backup-env")
Pkg.instantiate()

# Test with released version
Pkg.activate("test-env")
Pkg.add("Dependency")  # Released version
Pkg.test("MyPackage")

# Return to dev environment
Pkg.activate("backup-env")
```

## Tips for Multi-Package Work

1. **Keep upstream remotes**: Use `upstream` for the main repo, `origin` for your fork
2. **Pull before work**: Always `git pull` on all packages before starting
3. **Test bidirectionally**: Test both the dependency and dependent packages
4. **Coordinate releases**: Plan the release order for breaking changes
5. **Document cross-package changes**: Note in PRs when changes span packages
6. **Use consistent environments**: Share environment setup scripts with collaborators

## Environment Script Example

Create a setup script for your workspace:

```bash
#!/bin/bash
# setup-quantum-dev.sh

mkdir -p workspace && cd workspace

# Clone all packages
git clone https://github.com/QuantumSavory/QuantumInterface.jl.git
git clone https://github.com/QuantumSavory/QuantumClifford.jl.git
git clone https://github.com/QuantumSavory/QuantumSavory.jl.git

# Set up development environment
julia -e '
    using Pkg
    Pkg.activate("quantum-dev")
    Pkg.develop(path="./QuantumInterface.jl")
    Pkg.develop(path="./QuantumClifford.jl")
    Pkg.develop(path="./QuantumSavory.jl")
    Pkg.instantiate()
    println("Environment ready! Activate with: julia --project=quantum-dev")
'
```

## Quick Reference

| Task | Command |
|------|---------|
| Develop package | `Pkg.develop(path="./Pkg.jl")` |
| Exit dev mode | `Pkg.free("Pkg")` |
| Check status | `Pkg.status()` |
| Test package | `Pkg.test("Pkg")` |
| Update all | `Pkg.update()` |
| Create temp env | `Pkg.activate(mktempdir())` |

## Related Skills

- `julia-package-dev` - Single package development
- `julia-github` - Git and PR workflows
- `julia-ci-buildkite` - Downstream testing in CI
