---
name: julia-package-init
description: Create new Julia packages with modern infrastructure including tests, documentation, and CI. Use this skill when starting a new Julia package from scratch.
---

# Julia Package Initialization

Create a new Julia package with tests, docs, and CI scaffolding.

## Quick Start (PkgTemplates.jl)

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

## Manual Minimal Init

```julia
using Pkg
Pkg.generate("MyPackage")
```

Use Pkg to add dependencies and create subprojects (`docs/`, `test/`).

## Secrets

- `CODECOV_TOKEN` for coverage uploads (from codecov.io)
- `DOCUMENTER_KEY` for doc deployment (`DocumenterTools.genkeys()`)

## Initialization Checklist

- [ ] Package created via PkgTemplates or `Pkg.generate`
- [ ] `src/MyPackage.jl` exports the public API
- [ ] `test/` and `docs/` subprojects created via Pkg
- [ ] CI workflows added (`ci.yml`, `TagBot.yml`)
- [ ] Secrets added to GitHub

## Related Skills

- `julia-tests-run` - Test runner setup
- `julia-tests-write` - Writing tests
- `julia-docs` - Documentation setup
