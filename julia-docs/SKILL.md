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

## Philosophy

- **Document at the highest level possible**: Document interfaces and abstract types rather than every method/subtype
- **Tutorials before reference**: Users need the "90% use case" before API details
- **Opinionated tutorials**: Show complete workflows with specific tool choices
- **Variable names matter**: If you use `u0`, everyone will copy it
- **Summarize before details**: Every page should summarize before diving in

## Project Structure

```
MyPackage.jl/
├── Project.toml              # Must include [workspace] entry
├── docs/
│   ├── Project.toml          # Documentation dependencies
│   ├── make.jl               # Build script
│   └── src/
│       ├── index.md          # Landing page
│       ├── manual.md         # Getting started tutorial
│       └── API.md            # API reference
└── src/
    └── MyPackage.jl
```

## Quick Setup

### 1. Add workspace entry to Project.toml

```toml
[workspace]
projects = ["docs"]
```

### 2. Create docs/Project.toml

```toml
[deps]
Documenter = "e30172f5-a6a5-5a46-863b-614d45cd2de4"

[compat]
Documenter = "1"
```

### 3. Create docs/make.jl

```julia
using Documenter
using MyPackage

DocMeta.setdocmeta!(MyPackage, :DocTestSetup, :(using MyPackage); recursive=true)

makedocs(
    sitename = "MyPackage.jl",
    modules = [MyPackage],
    format = Documenter.HTML(),
    doctest = false,
    warnonly = [:missing_docs, :linkcheck],
    pages = [
        "MyPackage.jl" => "index.md",
        "Manual" => "manual.md",
        "API" => "API.md",
    ]
)

deploydocs(repo = "github.com/YourOrg/MyPackage.jl.git")
```

**For packages with extensions**: See [make.jl with Extensions](references/makedocs-options.md#packages-with-extensions)

## Building Documentation

```bash
# Install dependencies and build
julia --project=docs -e 'using Pkg; Pkg.develop(PackageSpec(path=pwd())); Pkg.instantiate()'
julia --project=docs docs/make.jl

# View locally
xdg-open docs/build/index.html  # Linux
```

### Live Preview with LiveServer.jl

```bash
julia --project=docs -e 'using Pkg; Pkg.add("LiveServer")'
julia --project=docs -e 'include("docs/make.jl"); using LiveServer; serve(dir="docs/build")'
```

## Page Organization (Diataxis Framework)

| Type | Purpose | Content |
|------|---------|---------|
| **Tutorials** | Learning-oriented | Step-by-step lessons for beginners |
| **How-To Guides** | Task-oriented | Solutions to specific problems |
| **Explanations** | Understanding-oriented | Background and context |
| **Reference** | Information-oriented | Technical descriptions (API docs) |

Order in navigation: Tutorials -> How-To -> Explanations -> Reference

## Reference Documentation

- **[Page Templates](references/templates.md)** - Templates for landing pages, tutorials, and API pages
- **[makedocs Options](references/makedocs-options.md)** - Quality assurance, doctests, and format options
- **[@-Block Reference](references/at-blocks.md)** - Docstring blocks, cross-references, code examples, admonitions

## Checklist

- [ ] `Project.toml` has `[workspace]` entry including `"docs"`
- [ ] `docs/Project.toml` includes all dependencies (including extension triggers)
- [ ] `docs/make.jl` includes all modules (including extensions!)
- [ ] `DocMeta.setdocmeta!` configured for doctests
- [ ] `warnonly = [:missing_docs, :linkcheck]` set appropriately
- [ ] Landing page has quick start example
- [ ] Tutorial covers the "90% use case"
- [ ] API pages organized by concept, not alphabetically
- [ ] Extensions documented in separate API sections
- [ ] Cross-references use `@ref` links
- [ ] `deploydocs` configured for CI
