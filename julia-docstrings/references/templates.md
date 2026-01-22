# Docstring Templates

## Table of Contents

- [Type Template](#type-template)
- [Function Template (Exported Functions)](#function-template-exported-functions)
- [Multiple Method Signatures](#multiple-method-signatures)
- [Module Template](#module-template)
- [Docstring Placement](#docstring-placement)

## Type Template

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

## Function Template (Exported Functions)

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

## Multiple Method Signatures

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

## Module Template

```julia
"""
Module description here.

$EXPORTS
"""
module MyModule

using DocStringExtensions

# ... module contents ...

end
```

## Docstring Placement

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
