---
name: julia-docstrings
description: Write Julia docstrings using DocStringExtensions.jl and SciML conventions. Use this skill when documenting functions, types, and modules in Julia packages.
---

# Julia Docstrings

Write user-facing docstrings using DocStringExtensions.jl and SciML-style
conventions.

## Core Rules

- Describe behavior, arguments, return values, and examples.
- Avoid implementation details (put those in code comments).
- Document exported functions, public types, and key modules.

## Use DocStringExtensions

Add `using DocStringExtensions` and use the macros for signatures and fields.

```julia
"""
$TYPEDEF

Brief description of what this type represents.

$TYPEDFIELDS
"""
@kwdef struct MyType
    "description of field a"
    a::Int
    "description of field b"
    b::String
end
```

```julia
"""
$TYPEDSIGNATURES

Brief description of what this function does.
"""
function foo(x::Int, y::String) end
```

## Notes

- Add a short "See also" list for discoverability.
- Use `@doc doc"""..."""` for LaTeX-heavy docstrings.

## Reference

- **[Templates](references/templates.md)** - Function, type, and module templates
- **[Doctests](references/doctests.md)** - Doctest guidance
