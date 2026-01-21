# Julia Docstrings

Write high-quality Julia docstrings following SciML conventions and using DocStringExtensions.jl.

## Core Philosophy

- **Docstrings are for users, not developers**
- Do NOT include implementation details (e.g., "uses pattern matching", "implemented via recursion")
- Focus on: what it does, arguments, return values, and usage examples
- Implementation notes belong in code comments, not docstrings

## What to Document

- All **exported** functions (required)
- Most modules, types, and public functions
- Prefer documenting accessor functions over fields (documented fields become public API)
- Avoid documenting commonly overloaded methods (`==`, `show`, etc.)
- Document the function, not individual methods, unless behavior differs significantly

## DocStringExtensions.jl

Always add `using DocStringExtensions` to modules with docstrings. Use these abbreviations
to reduce boilerplate:

### For Types (structs)

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

- `$TYPEDEF` - Inserts the full type signature (e.g., `struct MyType{T} <: AbstractType`)
- `$TYPEDFIELDS` - Lists all fields with types and their docstrings
- `$FIELDS` - Lists fields without type annotations

### For Functions

```julia
"""
$TYPEDSIGNATURES

Brief description of what this function does.
"""
function foo(x::Int, y::String)
    ...
end
```

- `$SIGNATURES` - Method signatures without types: `foo(x, y)`
- `$TYPEDSIGNATURES` - Method signatures with types: `foo(x::Int, y::String)`
- `$FUNCTIONNAME` - Just the function name (useful for `$FUNCTIONNAME(args...)`)

### For Modules

```julia
"""
Module description here.

$EXPORTS
"""
module MyModule
```

- `$EXPORTS` - Bulleted list of all exported names
- `$IMPORTS` - List of imported modules

## Docstring Templates

### Type Template

```julia
"""
$TYPEDEF

My super awesome array wrapper!

$TYPEDFIELDS

See also: [`RelatedType`](@ref), [`related_function`](@ref)
"""
struct MyArray{T, N} <: AbstractArray{T, N}
    "stores the array being wrapped"
    data::AbstractArray{T, N}
    "stores metadata about the array"
    metadata::Dict
end
```

### Function Template (Exported Functions)

```julia
"""
    mysearch(array::MyArray{T}, val::T; verbose=true) where {T} -> Int

Search the `array` for `val`. Returns the index where `val` is found.

# Arguments
- `array::MyArray{T}`: the array to search
- `val::T`: the value to search for

# Keywords
- `verbose::Bool=true`: print progress details

# Returns
- `Int`: the index where `val` is located in the `array`

# Throws
- `NotFoundError`: if `val` is not found in `array`

See also: [`myfilter`](@ref), [`myfind`](@ref)
"""
function mysearch(array::MyArray{T}, val::T; verbose=true) where {T}
    ...
end
```

### Multiple Method Signatures

When a function has many arguments or multiple dispatch patterns:

```julia
"""
    Manager(max_workers; kwargs...)
    Manager(min_workers:max_workers; kwargs...)
    Manager(min_workers, max_workers; kwargs...)

A cluster manager which spawns workers.

# Arguments
- `min_workers::Int`: minimum workers to spawn (throws if not met)
- `max_workers::Int`: requested number of workers to spawn

# Keywords
- `definition::AbstractString`: name of the job definition to use. Defaults to the
    definition used within the current instance.
- `name::AbstractString`: ...
"""
function Manager end
```

## Formatting Rules

- **Line width**: Wrap docstring lines at 92 characters
- **Indentation**: Continuation lines for bullet points indented with 4 spaces
- **Blank lines**: Add blank line between headings and content for longer sections
- **Consistency**: Be consistent with whitespace within a single docstring

```julia
# Good - wrapped and indented
"""
# Keywords
- `definition::AbstractString`: Name of the job definition to use. Defaults to the
    definition used within the current instance.
"""

# Bad - aligned to colon
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

## Doctests

Use doctests as **pedagogical examples** that are automatically tested for correctness.
They are not replacements for unit tests.

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

Guidelines for doctests:
- Use ` ```jldoctest ` code blocks with `julia>` prompts
- Whitespace is significant - match output exactly
- Use `[...]` to indicate truncated output
- Avoid `rand()` - use explicit RNG seeding if randomness needed
- Named doctests share state: ` ```jldoctest mytest `

## LaTeX in Docstrings

Use the `@doc` macro with `doc"""` for docstrings containing LaTeX:

```julia
@doc doc"""
    eigenvalue(A)

Compute the eigenvalues ``\lambda_i`` of matrix ``A`` where ``A v_i = \lambda_i v_i``.
"""
function eigenvalue(A) end
```

## Where Docstrings Can Be Placed

Julia supports docstrings in many locations:

```julia
"Document a function"
function f(x) end

"Document a method"
f(x::Int) = x

"Document a macro"
macro m(x) end

"Document an abstract type"
abstract type MyAbstract end

"Document a struct"
struct MyStruct
    "Document a field"
    x::Int
    "Document another field"
    y::String
end

"Document a module"
module MyModule end

"Document a constant"
const MY_CONST = 42

"Document a global variable"
global my_var = 1

"Document multiple bindings at once"
a, b
```

## Quick Reference

| Abbreviation | Use For | Output |
|--------------|---------|--------|
| `$TYPEDEF` | Types | Full type signature |
| `$TYPEDFIELDS` | Types | Fields with types and docs |
| `$FIELDS` | Types | Fields with docs (no types) |
| `$TYPEDSIGNATURES` | Functions | Signatures with types |
| `$SIGNATURES` | Functions | Signatures without types |
| `$FUNCTIONNAME` | Functions | Just the name |
| `$EXPORTS` | Modules | List of exports |
| `$METHODLIST` | Functions | All methods with locations |
