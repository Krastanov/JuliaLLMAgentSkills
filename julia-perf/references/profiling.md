# Profiling & Diagnosis

Source: https://docs.julialang.org/en/v1/manual/performance-tips/

## Step-by-Step Diagnosis

### 1. Benchmark with @time / @btime

```julia
# Always run twice — first call includes compilation
@time my_function(args)   # compilation + execution
@time my_function(args)   # actual performance

# For accurate measurement use BenchmarkTools
using BenchmarkTools
@btime my_function($args)
```

Key metrics to watch:
- **Time** — absolute and relative to expectation.
- **Allocations** — unexpected allocations signal type instability or
  unnecessary copying. Zero allocations is ideal for inner loops.
- **GC time** — high GC% means excessive allocation pressure.

### 2. Identify Type Instability with @code_warntype

```julia
@code_warntype my_function(args)
```

Reading the output:
- Concrete types (`Float64`, `Int64`) → good.
- `Any` or `Union{T1, T2, ...}` → type instability, fix it.
- `Union{Nothing, T}` / `Union{Missing, T}` (yellow) → often acceptable
  (small union optimization).

Common causes of instability:
| Symptom | Fix |
|---|---|
| Function returns different types | Use `zero(x)`, `oftype(x, val)` |
| Variable changes type in loop | Initialize with correct type |
| Accessing `Array{Any}` elements | Use typed arrays or assert `a[i]::T` |
| Struct field is abstract | Parameterize the struct |
| Captured closure variable | Use `let` block or type annotation |

### 3. Profile Execution Time

```julia
using Profile

@profile my_function(args)
Profile.print(noisefloor=2.0)  # suppress noise

# Visual profilers
using ProfileView
@profview my_function(args)

# Flame graph
using PProf
@profile my_function(args)
pprof()
```

### 4. Track Allocations

```bash
julia --track-allocation=user script.jl
```

```julia
# In script.jl:
using MyPackage
my_function(args)                # warm up (compile)
Profile.clear_malloc_data()      # reset counters
my_function(args)                # measure
```

This produces `.mem` files alongside source files showing bytes allocated per
line.

### 5. Automated Analysis with JET.jl

```julia
using JET

@report_opt my_function(args)    # optimization analysis
@report_call my_function(args)   # type-level bug detection
```

JET performs abstract interpretation to detect type instabilities and potential
errors without running the code.

## Quick Diagnosis Checklist

Run these in order on any slow function:

```julia
using BenchmarkTools, JET

# 1. How slow is it?
@btime target_function($args)

# 2. Type stable?
@code_warntype target_function(args)

# 3. Automated check
@report_opt target_function(args)

# 4. Where is time spent?
@profview target_function(args)   # requires ProfileView
```

## Common Patterns and Fixes

### Unexpected Allocations in a Loop

```julia
# Problem: allocations inside hot loop
for i in 1:n
    result = compute(data[i])     # allocates each iteration
end

# Fix 1: Pre-allocate buffer
buf = similar(data[1])
for i in 1:n
    compute!(buf, data[i])        # mutate pre-allocated buffer
end

# Fix 2: Use views instead of slices
for i in 1:n
    v = @view data[:, i]          # no copy
    process(v)
end
```

### Type-Unstable Struct

```julia
# Problem
struct Simulation
    state::AbstractArray          # abstract field
    dt::Real                      # abstract field
end

# Fix
struct Simulation{S<:AbstractArray, T<:Real}
    state::S
    dt::T
end
```

### Global Variable Performance

```julia
# Problem — type unknown, prevents optimization
data = load_file("input.dat")
function process()
    sum(data)                     # data could be anything
end

# Fix 1 — const
const data = load_file("input.dat")

# Fix 2 — pass as argument (preferred)
function process(data)
    sum(data)
end

# Fix 3 — type assert at use site
function process()
    sum(data::Vector{Float64})
end
```
