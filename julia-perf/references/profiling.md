# Profiling & Diagnosis

Source: https://docs.julialang.org/en/v1/manual/performance-tips/

Agents cannot use interactive viewers, GUI visualizers (ProfileView, PProf), or
REPL displays. Always export profile data to flat `.txt` files (`format=:flat`,
wide `displaysize`) or parse `Profile.fetch()` / `Profile.Allocs.fetch()`
programmatically.

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

### 3. CPU Sampling Profiler (`Profile.@profile`)

Identifies the most time-consuming operations in compute-bound code. Export a
flat, tabular summary to a file for parsing:

```julia
using Profile

my_function(args)         # 1. force compilation first
Profile.clear()           # 2. clear stale samples

@profile my_function(args)  # 3. collect

# 4. export flat table — wide displaysize prevents truncation
open("profile_results.txt", "w") do io
    Profile.print(IOContext(io, :displaysize => (24, 1000)), format=:flat)
end
```

Then read `profile_results.txt` and find the functions with the highest sample
counts.

**Hierarchical (JSON) export.** For a structured call tree instead of a flat
list, build a `FlameGraphs.flamegraph()`, map its nodes into plain `Dict`s, and
write them with `JSON.json(dict)` to a file for programmatic analysis.

### 4. Wall-time Profiler (`Profile.@profile_walltime`)

Samples all tasks regardless of scheduling state. Use it for IO-heavy work or
to diagnose contention on synchronization primitives (tasks waiting on
`Channel`s or locks).

```julia
using Profile

my_function(args)         # force compilation
Profile.clear()

@profile_walltime my_function(args)

open("walltime_profile_results.txt", "w") do io
    Profile.print(IOContext(io, :displaysize => (24, 1000)), format=:flat)
end
```

Extremely short-lived tasks may appear as `failed_to_sample_task_fun` or
`failed_to_stop_thread_fun`.

### 5. Track Allocations

The allocation profiler records the stack trace and type of each allocation and
returns natively structured data:

```julia
using Profile

my_function(args)         # force compilation
Profile.Allocs.clear()

# sample_rate: 0.01 = 1%, 1.0 = every allocation. Aim for 1k–10k samples.
Profile.Allocs.@profile sample_rate=0.01 my_function(args)

prof = Profile.Allocs.fetch()
sort!(prof.allocs, by = a -> a.size, rev = true)

open("allocation_results.txt", "w") do io
    for alloc in prof.allocs[1:min(10, end)]
        println(io, "Size: $(alloc.size), Type: $(alloc.type)")
        # alloc.stacktrace holds the frames if needed
    end
end
```

Samples are drawn uniformly across allocations (not weighted by size) unless
`sample_rate = 1`. For a coarse view, `GC.enable_logging(true)` logs GC events
to `stderr`. Line-level data is also available via
`julia --track-allocation=user script.jl`, which writes `.mem` files next to
each source file (warm up once, then `Profile.clear_malloc_data()` before the
measured call).

### 6. Automated Analysis with JET.jl

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
using BenchmarkTools, JET, Profile

# 1. How slow is it?
@btime target_function($args)

# 2. Type stable?
@code_warntype target_function(args)

# 3. Automated check
@report_opt target_function(args)

# 4. Where is time spent? (export to file, then read it)
target_function(args); Profile.clear()
@profile target_function(args)
open("profile_results.txt", "w") do io
    Profile.print(IOContext(io, :displaysize => (24, 1000)), format=:flat)
end
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

## General Best Practices

1. **Force JIT compilation** — run the function once before profiling, or the
   profile captures the compiler instead of the target code.
2. **Clear buffers** — `Profile.clear()` / `Profile.Allocs.clear()` before each
   collection to avoid merging with stale data.
3. **Export, don't display** — never use interactive viewers, GUI visualizers,
   or REPL prints. Write wide `.txt` files (`format=:flat`), parse
   `fetch()` results directly, or export JSON.
