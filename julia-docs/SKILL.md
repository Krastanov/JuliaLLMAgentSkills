---
name: julia-docs
description: Build Julia package documentation with Documenter.jl, including docstrings, doctests, and citations. Use when setting up docs/, configuring make.jl, or writing documentation content.
---

# Julia Documentation

Use this skill for the full documentation workflow: docs site setup, docstrings,
doctests, and citations.

## Quick Start

```julia
using Pkg
Pkg.activate("docs")
Pkg.add("Documenter")
Pkg.develop(path=pwd())
```

```julia
using Documenter
using MyPackage

DocMeta.setdocmeta!(MyPackage, :DocTestSetup, :(using MyPackage); recursive=true)

makedocs(
    sitename = "MyPackage.jl",
    modules = [MyPackage],
    pages = ["Home" => "index.md", "API" => "api.md"],
)
```

```bash
julia -tauto --project=docs docs/make.jl
```

## What Lives Here

- Documentation site structure and `docs/make.jl`
- Docstring conventions and templates
- Doctest authoring and Documenter-specific setup
- Citations and bibliography integration

Run doctests via `julia-tests`; use this skill for how to write and configure
them.

## References

- `references/page-templates.md`
- `references/docstring-templates.md`
- `references/doctests.md`
- `references/makedocs-options.md`
- `references/at-blocks.md`
- `references/citations-examples.md`

## Checklist

- [ ] `docs/Project.toml` exists and includes doc dependencies
- [ ] `docs/make.jl` loads all relevant modules and extensions
- [ ] `DocMeta.setdocmeta!` is configured for doctests
- [ ] Inline doctest filters use Documenter's `filter = ...` syntax when the scope should be a single block
- [ ] Docstring-specific setup uses block `setup = ...` or module-level `DocMeta`, not ad hoc assumptions
- [ ] `JULIA_DEBUG=Documenter` is used when filter behavior is unclear
- [ ] Citation setup is added if the docs cite papers or books
