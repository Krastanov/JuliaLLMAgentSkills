---
name: julia-docstrings
description: Write Julia docstrings using DocStringExtensions.jl and SciML conventions. Use this skill when documenting functions, types, and modules in Julia packages.
---

# Julia Docstrings

Write high-quality Julia docstrings following SciML conventions and using DocStringExtensions.jl.

## Core Philosophy

- **Docstrings are for users, not developers**
- Do NOT include implementation details (e.g., "uses pattern matching")
- Focus on: what it does, arguments, return values, and usage examples
- Implementation notes belong in code comments, not docstrings

## What to Document

- All **exported** functions (required)
- Most modules, types, and public functions
- Prefer documenting accessor functions over fields (documented fields become public API)
- Avoid documenting commonly overloaded methods (`==`, `show`, etc.)

## DocStringExtensions.jl Abbreviations

Always add `using DocStringExtensions` to modules with docstrings.

### For Types

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

### For Functions

```julia
"""
$TYPEDSIGNATURES

Brief description of what this function does.
"""
function foo(x::Int, y::String) end
```

### Quick Reference

| Abbreviation | Use For | Output |
|--------------|---------|--------|
| `$TYPEDEF` | Types | Full type signature |
| `$TYPEDFIELDS` | Types | Fields with types and docs |
| `$FIELDS` | Types | Fields with docs (no types) |
| `$TYPEDSIGNATURES` | Functions | Signatures with types |
| `$SIGNATURES` | Functions | Signatures without types |
| `$FUNCTIONNAME` | Functions | Just the name |
| `$EXPORTS` | Modules | List of exports |

## Formatting Rules

- **Line width**: Wrap at 92 characters
- **Indentation**: Continuation lines indented with 4 spaces
- **Blank lines**: Add between headings and content for longer sections

```julia
# Good - wrapped and indented
"""
# Keywords
- `definition::AbstractString`: Name of the job definition to use. Defaults to the
    definition used within the current instance.
"""
```

## See Also Blocks

Use liberally to help users discover related functionality:

```julia
"""
...

See also: [`EntanglementTracker`](@ref), [`SwapperProt`](@ref)
"""
```

## LaTeX in Docstrings

Use `@doc doc"""..."""` for docstrings containing LaTeX:

```julia
@doc doc"""
    eigenvalue(A)

Compute eigenvalues ``\lambda_i`` of matrix ``A`` where ``A v_i = \lambda_i v_i``.
"""
function eigenvalue(A) end
```

## Reference

- **[Templates](references/templates.md)** - Complete function, type, and module templates
- **[Doctests](references/doctests.md)** - Guidelines for doctest examples
