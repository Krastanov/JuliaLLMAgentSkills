---
name: julia-doctests
description: Configure and write doctests for Julia packages using Documenter.jl. Use this skill when adding testable code examples to docstrings or setting up doctest infrastructure.
---

# Julia Doctests

Write and test doctests - executable code examples embedded in docstrings that are
automatically verified for correctness.

## Purpose

Doctests serve as **pedagogical examples** that are automatically tested:
- They teach users how to use your API with real, working code
- They catch documentation rot when APIs change
- They are **NOT** replacements for unit tests - keep them simple and illustrative

## Two Doctest Formats

### REPL Examples

```julia
"""
    double(x)

# Examples
```jldoctest
julia> double(2)
4

julia> double(3.5)
7.0
```
"""
double(x) = 2x
```

### Script Examples

````julia
"""
# Examples
```jldoctest
a, b = 2, 3
println("Sum: ", a + b)
# output
Sum: 5
```
"""
````

## Module-Level Setup

Apply setup to all docstrings in a module:

```julia
using Documenter

DocMeta.setdocmeta!(
    MyPackage,
    :DocTestSetup,
    :(using MyPackage; using MyPackage.SubModule);
    recursive=true
)

doctest(MyPackage)
```

## Running Doctests

### In Test Suite

```julia
@testitem "Doctests" begin
    using Documenter
    using MyPackage

    DocMeta.setdocmeta!(MyPackage, :DocTestSetup, :(using MyPackage); recursive=true)
    doctest(MyPackage; manual=false)
end
```

### Fix Mode

Automatically update outdated doctest output:

```julia
doctest(MyPackage; fix=true)
```

## Quick Reference

| Feature | Syntax |
|---------|--------|
| REPL example | ` ```jldoctest ` with `julia>` prompts |
| Script example | ` ```jldoctest ` with `# output` separator |
| Named/shared | ` ```jldoctest mylabel ` |
| Setup | `DocMeta.setdocmeta!(Mod, :DocTestSetup, expr)` |
| Filter | `doctest(...; doctestfilters=[r"pattern"])` |
| Fix output | `doctest(...; fix=true)` |
| Truncated output | `[...]` |
| Stable randomness | `StableRNG(seed)` from StableRNGs.jl |

## Reference

- **[Advanced Topics](references/advanced.md)** - Named doctests, filters, StableRNGs, testing extensions
- **[Common Pitfalls](references/pitfalls.md)** - Whitespace sensitivity, module prefixes, display size
