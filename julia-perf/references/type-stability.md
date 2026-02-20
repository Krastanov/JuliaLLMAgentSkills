# Type Stability

Source: https://docs.julialang.org/en/v1/manual/performance-tips/

## What Is Type Stability?

A function is type-stable when the return type depends only on the **types** of
its arguments, not on their **values**. The compiler can then specialize the
calling code.

```julia
# BAD — returns Int or typeof(x) depending on value
pos(x) = x < 0 ? 0 : x

# GOOD — return type always matches input type
pos(x) = x < 0 ? zero(x) : x
pos(x) = x < 0 ? oftype(x, 0) : x
```

Use `zero(x)`, `oneunit(x)`, `oftype(x, val)` to preserve types.

## Diagnosing with @code_warntype

```julia
@code_warntype f(3.2)
```

In the output:
- Concrete types (e.g. `Float64`) → good.
- `Union{...}` or `Any` → type instability, fix it.
- `Union` with `Nothing`/`Missing` shown in yellow → often acceptable.

## Don't Change Variable Types Inside Functions

```julia
# BAD — x starts as Int, becomes Float64
function foo()
    x = 1
    for i = 1:10
        x /= rand()
    end
    x
end

# GOOD — initialize with correct type
function foo()
    x = 1.0
    for i = 1:10
        x /= rand()
    end
    x
end
```

Alternatives: use `x::Float64 = 1`, or `one(Float64)`, or initialize from the
first iteration.

## Function Barriers (Kernel Functions)

When a type is unknown at a call site but fixed once resolved, push the hot loop
into a separate function so the compiler can specialize it.

```julia
# BAD — loop runs with uncertain element type
function strange_twos(n)
    a = Vector{rand(Bool) ? Int64 : Float64}(undef, n)
    for i = eachindex(a)
        a[i] = 2
    end
    a
end

# GOOD — compiler specializes fill_twos! for each concrete array type
function fill_twos!(a)
    for i = eachindex(a)
        a[i] = 2
    end
end

function strange_twos(n)
    a = Vector{rand(Bool) ? Int64 : Float64}(undef, n)
    fill_twos!(a)
    a
end
```

This pattern is essential when handling data loaded from files or external
sources where the element type is determined at runtime.

## Annotate Values from Untyped Locations

Add type assertions when extracting from `Any` containers:

```julia
function foo(a::Array{Any,1})
    x = a[1]::Int32      # assert known type
    b = x + 1
end
```

Use `convert(T, val)::T` when the value might need conversion.

## Captured Variables in Closures

Closures that capture reassigned variables create heap-allocated "boxes".

```julia
# BAD — r is boxed
function abmult(r::Int)
    if r < 0; r = -r; end
    f = x -> x * r
    return f
end

# GOOD — let block avoids boxing
function abmult(r::Int)
    if r < 0; r = -r; end
    f = let r = r
        x -> x * r
    end
    return f
end
```

Alternative: declare the captured variable with a type annotation (`r::Int = r0`).

## When Julia Avoids Specializing

By default Julia does **not** specialize on `Type`, `Function`, or `Vararg`
arguments. Force specialization with type parameters:

```julia
# Won't specialize on t
f(t) = ones(t, 10)

# Will specialize
g(::Type{T}) where T = ones(T, 10)

# Won't specialize on f
apply(f, x) = f(x)

# Will specialize
apply(f::F, x) where {F} = f(x)

# Won't specialize on length
f(x::Int...) = tuple(x...)

# Will specialize
g(x::Vararg{Int, N}) where {N} = tuple(x...)
```
