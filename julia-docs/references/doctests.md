# Doctests

Use doctests as user-facing examples that are also checked automatically by
Documenter.jl.

## Basic Pattern

````julia
"""
    double(x)

Return twice the value of `x`.

# Examples
```jldoctest
julia> double(2)
4
```
"""
double(x) = 2x
````

## Test-Suite Hook

```julia
using Documenter
using Test
using MyPackage

ENV["LINES"] = 80
ENV["COLUMNS"] = 80

DocMeta.setdocmeta!(MyPackage, :DocTestSetup, :(using MyPackage); recursive=true)

@testset "Doctests" begin
    doctest(MyPackage; manual=false)
end
```

## Core Rules

- Use ````jldoctest`` blocks for executable examples.
- Match whitespace and output exactly.
- Prefer deterministic examples.
- Use `StableRNGs.jl` instead of raw `rand()` output.
- Use named doctests only when blocks really need shared state.

## Named Doctests

````markdown
```jldoctest myexample
julia> x = [1, 2, 3]
3-element Vector{Int64}:
 1
 2
 3
```

```jldoctest myexample
julia> sum(x)
6
```
````

## Filters

```julia
doctestfilters = [
    r"Ptr{0x[0-9a-f]+}",
    r"[0-9]+ bytes" => s"N bytes",
    r"(MyPackage\.|)",
]

doctest(MyPackage; doctestfilters)
```

Documenter only applies a filter when it matches both the expected and actual
output. For version-specific output, make the varying part optional.

## Common Pitfalls

- `raw"""` docstrings do not attach as documentation.
- In docstring regexes, write `\$` for an end-of-string anchor.
- Use character classes like `[(]` and `[0-9]` instead of backslash escapes.
- Set `ENV["LINES"]` and `ENV["COLUMNS"]` for stable pretty-printing output.
- Use `[...]` to truncate stack traces or long error output.
