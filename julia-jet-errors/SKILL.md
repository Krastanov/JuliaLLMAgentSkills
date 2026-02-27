---
name: julia-jet-errors
description: Detect type errors in Julia code with JET.jl's error analysis (@report_call, report_package). Use this skill when diagnosing MethodErrors, undefined references, or bad field access detected by JET.
---

# JET Error Analysis

Detect type-level errors statically using `@report_call`, `report_call`,
and `report_package`. JET analyzes all reachable branches — it can find
errors that no single test run would trigger.

**WARNING**: Use JET.jl only on the latest stable Julia release.

## Entry Points

```julia
using JET

# Analyze a specific call (most precise)
@report_call my_function(1, "hello")
report_call(my_function, (Int, String))

# Analyze an entire package (less precise, uses method signatures)
using MyPackage
report_package(MyPackage; target_modules=[MyPackage])

# Analyze a script file
report_file("my_script.jl")
```

## Error Kinds and How to Fix Them

### `no matching method found`

A function is called with types that have no matching method.

```julia
f(x::Integer) = x + 1
g(x) = f(x)
@report_call g(1.0)  # MethodError: no f(::Float64)
```

**Fix:** Add the missing method or correct the calling code.

### `no matching method found (x/y union split)`

A union type where *some* members cause a `MethodError`. Most common with
functions that return `Union{T, Nothing}`.

```julia
function pos_after_tab(v::AbstractArray{UInt8})
    p = findfirst(isequal(UInt8('\t')), v)
    p + 1  # ERROR: p could be nothing
end
```

**Fix option 1 — handle the nothing case:**

```julia
function pos_after_tab(v::AbstractArray{UInt8})
    p = findfirst(isequal(UInt8('\t')), v)
    p === nothing && return nothing
    p + 1
end
```

**Fix option 2 — typeassert when nothing is impossible:**

```julia
function pos_after_tab(v::AbstractArray{UInt8})
    p = findfirst(isequal(UInt8('\t')), v)::Integer
    p + 1
end
```

Typeasserts also improve performance by giving the compiler better type info.

### Union fields on mutable structs

Julia can't prove that two loads of the same mutable field return the same
value. Assign to a local variable first:

```julia
# BAD — JET reports error even with the if-check
mutable struct Foo
    x::Union{Int, Nothing}
end
f(foo) = foo.x === nothing ? nothing : foo.x + 1

# GOOD — local variable lets the compiler narrow the type
f(foo) = (y = foo.x; y === nothing ? nothing : y + 1)
```

### `X is not defined`

An undefined name is used. Usually a typo or a missing import.

### `type T has no field F`

A field access uses a nonexistent field name. Usually a typo.

### `may throw [...]`

In `:basic` mode, only reported when a function *always* throws uncaught.
In `:sound` mode, reported when a function *may* throw.

## Analysis Modes

```julia
# Default — common errors, good for general development
@report_call my_function(args...)

# Sound — strict, guarantees no runtime errors if clean
@report_call mode=:sound my_function(args...)

# Typo — minimal, only undefined refs and bad field access
@report_call mode=:typo my_function(args...)
```

## Test Integration

```julia
using Test, JET

# Assert a call is error-free (works like @test)
@test_call target_modules=(MyPackage,) my_function(args...)

# With type signature instead of values
test_call(my_function, (Int, String); target_modules=(MyPackage,))

# Mark known issues
@test_call broken=true my_function(args...)
```

## Limitations

- JET analyzes *types*, not *values* — it may report errors on unreachable
  branches if the branch condition depends on values
- JET cannot see past type instabilities — fix dispatch issues first
  (use `@report_opt`)
- `report_package` uses method signatures which are often very generic,
  producing more false positives than targeted `@report_call`

## Reference

- **[Error Kinds](references/error-kinds.md)** — Complete error catalog with examples

## Related Skills

- `julia-jet` — Overview and quick start
- `julia-jet-opt` — Optimization analysis (`@report_opt`)
- `julia-perf` — Performance optimization (type stability, profiling)
- `julia-tests-write` — Test templates including JET
