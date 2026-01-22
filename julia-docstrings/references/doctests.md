# Doctests in Docstrings

Use doctests as **pedagogical examples** that are automatically tested for correctness.
They are not replacements for unit tests.

## Basic Doctest

```julia
"""
    double(x)

Return twice the value of `x`.

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

## Guidelines

- Use ` ```jldoctest ` code blocks with `julia>` prompts
- Whitespace is significant - match output exactly
- Use `[...]` to indicate truncated output
- Avoid `rand()` - use explicit RNG seeding if randomness needed
- Named doctests share state: ` ```jldoctest mytest `

## For Full Doctest Documentation

See the `julia-doctests` skill for:
- Named doctests (shared state)
- Setup and teardown
- Handling randomness with StableRNGs.jl
- Filters for non-deterministic output
- Testing exceptions
- Running doctests
