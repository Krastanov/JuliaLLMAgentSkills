# Structs & Dispatch

Source: https://docs.julialang.org/en/v1/manual/performance-tips/

## Use Concrete Types in Struct Fields

Abstract field types prevent the compiler from knowing the memory layout.

```julia
# BAD — field type is abstract
struct MyType
    a::AbstractFloat
end

# BAD — untyped field defaults to Any
struct MyType
    a
end

# GOOD — parametric struct, concrete at instantiation
struct MyType{T<:AbstractFloat}
    a::T
end
# MyType(3.2) → MyType{Float64}
```

Never instantiate with abstract parameters: `MyType{AbstractFloat}(3.2)` loses
all benefits.

## Use Concrete Types in Container Fields

```julia
# BAD — abstract container
struct Wrapper
    a::Array
end

# BAD — abstract container element parameter only
struct Wrapper{T}
    a::AbstractVector{T}
end

# GOOD — fully parametric container
struct Wrapper{A<:AbstractVector}
    a::A
end
# Wrapper(1:10) → Wrapper{UnitRange{Int64}}
```

## Avoid Containers with Abstract Element Types

```julia
# BAD — stores boxed pointers, no SIMD, poor cache behavior
a = Real[]
push!(a, 1); push!(a, 2.0); push!(a, π)

# GOOD — contiguous memory, SIMD-friendly
a = Float64[]
push!(a, 1); push!(a, 2.0); push!(a, π)
```

## Use Multiple Dispatch Instead of Branching on Types

```julia
# BAD — runtime type check
function mynorm(A)
    if isa(A, Vector)
        return sqrt(real(dot(A, A)))
    elseif isa(A, Matrix)
        return maximum(svdvals(A))
    end
end

# GOOD — dispatch selects method at compile time
mynorm(x::Vector) = sqrt(real(dot(x, x)))
mynorm(A::Matrix) = maximum(svdvals(A))
```

## Val: Values as Type Parameters

Pass compile-time-known values via `Val` to enable specialization:

```julia
# BAD — N only known at runtime
function array3(fillval, N)
    fill(fillval, ntuple(d -> 3, N))
end

# GOOD — N is a type parameter, known at compile time
function array3(fillval, ::Val{N}) where N
    fill(fillval, ntuple(d -> 3, Val(N)))
end

array3(5.0, Val(2))
```

`Val` only helps when the argument is a literal or already in the type domain.
Wrapping a runtime variable in `Val(n)` does **not** help and can make things
worse.

### Correct usage — N comes from a type parameter

```julia
function filter3(A::AbstractArray{T,N}) where {T,N}
    kernel = array3(1, Val(N))
    filter(A, kernel)
end
```

### Incorrect usage — N is still a runtime value

```julia
function call_array3(fillval, n)
    A = array3(fillval, Val(n))  # Val wraps runtime value — no benefit
end
```

## Don't Abuse Dispatch for Combinatorial Types

```julia
# Potentially harmful — generates method per Make×Model combination
struct Car{Make, Model}
    year::Int
end
```

Only encode values as type parameters when:
1. Expensive per-instance computation benefits from specialization.
2. The total number of combinations is small and bounded.
3. You store homogeneous collections (`Vector{Car{:Honda,:Accord}}`).
