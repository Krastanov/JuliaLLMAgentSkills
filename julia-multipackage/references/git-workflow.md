# Git Workflow for Multi-Package Changes

## Create Feature Branches in All Affected Packages

```bash
cd QuantumClifford.jl
git checkout -b feature/new-api

cd ../QuantumSavory.jl
git checkout -b feature/adapt-to-new-api
```

## Make Changes and Test Together

```bash
julia -e '
    using Pkg
    Pkg.activate("temp-test")
    Pkg.develop(path="./QuantumClifford.jl")
    Pkg.develop(path="./QuantumSavory.jl")
    Pkg.test("QuantumSavory")
'
```

## Create PRs in Dependency Order

1. First PR: Changes to the dependency (QuantumClifford)
2. Wait for merge and release
3. Second PR: Changes to dependent package (QuantumSavory)

## Managing Compat Bounds

Use Pkg to update compat entries after the dependency is released:

```julia
using Pkg
Pkg.activate(".")
Pkg.compat("QuantumClifford", "0.12")
```

Bump the dependency version before release as part of the standard release flow.

## Testing Unreleased Dependencies

```yaml
# CI: Test against unreleased branch
- run: |
    julia -e '
      using Pkg
      Pkg.add(url="https://github.com/Org/Dependency.jl", rev="feature-branch")
      Pkg.test()
    '
```

## Tips

1. **Keep upstream remotes**: Use `upstream` for main repo, `origin` for fork
2. **Pull before work**: Always `git pull` on all packages before starting
3. **Test bidirectionally**: Test both dependency and dependent packages
4. **Coordinate releases**: Plan release order for breaking changes
5. **Document cross-package changes**: Note in PRs when changes span packages
