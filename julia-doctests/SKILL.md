---
name: julia-doctests
description: Configure and write doctests for Julia packages using Documenter.jl. Use this skill when adding testable code examples to docstrings or setting up doctest infrastructure.
---

# Julia Doctests

Write executable examples in docstrings and verify them with Documenter.jl.

## Doctest Formats

Use REPL-style prompts for interactive examples:

````julia
"""
# Examples
```jldoctest
julia> double(2)
4
```
"""
double(x) = 2x
````

Use script-style blocks for multiline output:

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

## Set Up and Run

```julia
using Documenter
DocMeta.setdocmeta!(MyPackage, :DocTestSetup, :(using MyPackage); recursive=true)
doctest(MyPackage)
```

## In the Test Suite

```julia
@testitem "Doctests" begin
    using Documenter
    using MyPackage
    DocMeta.setdocmeta!(MyPackage, :DocTestSetup, :(using MyPackage); recursive=true)
    doctest(MyPackage; manual=false)
end
```

## Reference

- **[Advanced Topics](references/advanced.md)** - Filters, named blocks, StableRNGs
- **[Common Pitfalls](references/pitfalls.md)** - Whitespace, module prefixes, display size
