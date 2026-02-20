# Annotations & Tweaks

Source: https://docs.julialang.org/en/v1/manual/performance-tips/

## Performance Annotations

### @inbounds — Remove Bounds Checks

Skips array bounds checking. Use **only** when indices are provably valid.

```julia
# Safe loop — use eachindex for correct bounds
@inbounds for i in eachindex(x)
    s += x[i]
end
```

### @fastmath — Aggressive Float Optimization

Allows reordering of floating-point operations. May change numerical results.
Ignores inf/nan semantics.

```julia
@fastmath y = x^2 + 2x + 1
```

### @simd — Vectorize Independent Iterations

Asserts that loop iterations are independent and can be reordered/vectorized.

```julia
@simd for i in eachindex(x, y)
    x[i] += y[i]
end
```

### Combined Usage

```julia
function fast_dot(x, y)
    s = zero(eltype(x))
    @fastmath @inbounds @simd for i in eachindex(x, y)
        s += x[i] * y[i]
    end
    s
end
```

Typical improvement: ~9x for dot products vs no annotations.

### Safety Notes

- `@inbounds` — undefined behavior if indices are wrong; never use on
  user-supplied indices without validation.
- `@fastmath` — breaks IEEE 754 edge cases; avoid for code that handles
  inf/nan or requires strict reproducibility.
- `@simd` — incorrect if iterations have dependencies (e.g., `x[i] = x[i-1] + 1`).

## Miscellaneous Tweaks

### Avoid Unnecessary Containers

```julia
# BAD
sum([x, y, z])

# GOOD
x + y + z
```

### Use Specialized Math Functions

```julia
# BAD
abs(z)^2         # allocates intermediate for complex z

# GOOD
abs2(z)           # direct computation

# BAD
floor(x / y)

# GOOD
fld(x, y)         # floor division
div(x, y)         # truncating division
cld(x, y)         # ceiling division
```

### Avoid String Interpolation for I/O

```julia
# BAD — allocates intermediate string
println(file, "$a $b")

# GOOD — writes directly
println(file, a, " ", b)
```

### Use Lazy Strings for Conditional Messages

```julia
# BAD — always materializes the string
@warn "deprecated for type $(typeof(x))"

# GOOD — only materializes when displayed
@warn lazy"deprecated for type $(typeof(x))"
```

### Fix Deprecation Warnings

Deprecated functions add runtime overhead for warning bookkeeping. Replace them
immediately.

### Subnormal Numbers

Flushing subnormal floats to zero can yield ~1.5x speedup on some hardware:

```julia
set_zero_subnormals(true)
```

Trade-off: breaks `x - y == 0 ⟹ x == y`. Use only when subnormals are
irrelevant to your computation.

## Precompilation and Latency

### Reduce Time to First Execution

Use `PrecompileTools.jl` to cache compiled code:

```julia
using PrecompileTools

@compile_workload begin
    # Representative usage
    my_function(typical_args)
end
```

### Reduce Package Load Time

- Minimize dependencies; use package extensions for optional interop.
- Avoid expensive work in `__init__()`.
- Diagnose with `@time_imports using MyPackage`.

### Parallel Execution I/O

Use `@sync` + `Threads.@spawn` for one network round-trip per worker:

```julia
responses = Vector{Any}(undef, nworkers())
@sync for (idx, pid) in enumerate(workers())
    Threads.@spawn responses[idx] = remotecall_fetch(foo, pid, args...)
end
```
