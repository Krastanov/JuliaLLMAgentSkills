---
name: julia-docs
description: Build documentation websites for Julia packages using Documenter.jl. Use this skill when setting up docs/, configuring make.jl, or writing documentation pages.
---

# Julia Documentation

Build documentation for Julia packages using Documenter.jl.

**Related skills:**
- `julia-docstrings` - Writing docstrings
- `julia-doctests` - Writing doctests
- `julia-doccitations` - Citations and bibliographies

## Create the Docs Environment

```julia
using Pkg
Pkg.activate("docs")
Pkg.add("Documenter")
Pkg.develop(path=pwd())
```

## Create docs/make.jl

```julia
using Documenter
using MyPackage

DocMeta.setdocmeta!(MyPackage, :DocTestSetup, :(using MyPackage); recursive=true)

makedocs(
    sitename = "MyPackage.jl",
    modules = [MyPackage],
    pages = [
        "Home" => "index.md",
        "Manual" => "manual.md",
        "API" => "API.md",
    ]
)

deploydocs(repo = "github.com/YourOrg/MyPackage.jl.git")
```

## Build Locally

```bash
julia --project=docs docs/make.jl
xdg-open docs/build/index.html  # Linux
```

## Reference

- **[Page Templates](references/templates.md)** - Landing, tutorial, API templates
- **[makedocs Options](references/makedocs-options.md)** - Doctests, extensions, format
- **[@-Block Reference](references/at-blocks.md)** - Doc blocks, cross-refs, admonitions, and other special syntax

## Checklist

- [ ] Docs env created via Pkg (`docs/Project.toml`)
- [ ] `docs/make.jl` includes all modules (including extensions)
- [ ] `deploydocs` configured in CI
