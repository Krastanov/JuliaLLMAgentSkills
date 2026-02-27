# JET Error Kinds Reference

## `no matching method found`

Runtime would throw `MethodError`. Most common JET finding.

```julia
f(x::Integer) = x + 1
g(x) = f(x)
@report_call g(1.0)
# ═════ 1 possible error found ═════
# ┌ @ REPL:1 f(x)
# │ no matching method found `f(::Float64)`
```

**Fix:** Add the missing method or correct the argument types.

## `no matching method found (x/y union split)`

Only some members of a union type cause a `MethodError`. Typically from
functions returning `Union{T, Nothing}` (like `findfirst`, `match`,
`tryparse`, dictionary `get`).

```julia
function find_next(v, target)
    i = findfirst(==(target), v)
    v[i + 1]  # i could be nothing
end
```

**Fix approaches (choose one):**

1. **Handle the nothing case** — add an `if` check:
   ```julia
   i = findfirst(==(target), v)
   i === nothing && return nothing
   v[i + 1]
   ```

2. **Typeassert** — when you know nothing is impossible for valid input:
   ```julia
   i = findfirst(==(target), v)::Int
   v[i + 1]
   ```
   Typeasserts also improve performance (compiler gets better type info).

3. **Use `something()`** — convert nothing to a default:
   ```julia
   i = something(findfirst(==(target), v), 0)
   ```

## Union fields on mutable structs

Julia doesn't prove that loading the same mutable field twice returns the
same object. So even with an `if` check, the second load is still a union:

```julia
mutable struct Foo
    x::Union{Int, Nothing}
end

# BAD — x.x in the else branch is still Union{Int, Nothing}
f(x) = x.x === nothing ? nothing : x.x + 1

# GOOD — assign to local variable, compiler narrows the type
f(x) = (y = x.x; y === nothing ? nothing : y + 1)
```

## `X is not defined`

An undefined name is referenced. Causes:
- Typo in function/variable name
- Missing `using`/`import`
- Name exists but is not in scope

## `type T has no field F`

Accessing a nonexistent field. Usually a typo:

```julia
struct Point
    x::Float64
    y::Float64
end
f(p) = p.z  # no field z
```

## `BoundsError: Attempt to access T at index [i]`

Only detected when both container size and index are known at compile time.
Typically with tuples (whose length is part of the type):

```julia
get_fourth(x) = x[4]
@report_call get_fourth((1,2,3))  # detected
@report_call get_fourth([1,2,3])  # NOT detected (array length unknown)
```

## `may throw [...]`

- **`:basic` mode** — only reported when a function *always* throws uncaught
- **`:sound` mode** — reported when a function *may* throw

```julia
f(x) = x isa Integer ? throw("bad") : nothing
@report_call f(1)              # reported (always throws for Int)
@report_call mode=:sound f(1)  # also reported
```
