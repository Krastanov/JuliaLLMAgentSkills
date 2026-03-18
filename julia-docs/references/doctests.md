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

Documenter applies filters by running `replace` on the expected output and on the
actual output before comparing them. A filter does not need to match both sides;
if it matches only one side, that side is transformed and the other is left as-is.

Use a doctest-local filter when the scope should be one block:

````markdown
```jldoctest; filter = [r" \+ 0\.0im", r"slot = \d+\.(\d+)" => s"slot = Slot \1"]
julia> f()
...
```
````

Documenter also supports block-local setup and teardown, which is often the
cleanest option for inline docstrings:

````markdown
```jldoctest; setup = :(using ResumableFunctions: @resumable)
julia> @resumable function f()
           1
       end
f (generic function with 1 method)
```
````

If filter behavior is unclear, run doctests with `JULIA_DEBUG=Documenter` to
inspect the raw and filtered outputs.

## Common Pitfalls

- `raw"""` docstrings do not attach as documentation.
- In docstring regexes, write `\$` for an end-of-string anchor.
- Use character classes like `[(]` and `[0-9]` instead of backslash escapes.
- Set `ENV["LINES"]` and `ENV["COLUMNS"]` for stable pretty-printing output.
- Use `[...]` to truncate stack traces or long error output.
- Do not assume a filter must match both expected and actual output to take effect.
