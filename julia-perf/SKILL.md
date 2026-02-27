---
name: julia-perf
description: Optimize Julia code for performance. Use this skill when diagnosing slow code, reducing allocations, fixing type instabilities, or applying performance best practices.
---

# Julia Performance Optimization

Diagnose and fix performance issues in Julia code following the official
[Performance Tips](https://docs.julialang.org/en/v1/manual/performance-tips/).

## Diagnosis Workflow

1. **Profile first** — identify the actual bottleneck before optimizing.
2. **Check type stability** — run `@code_warntype` on hot functions.
3. **Measure allocations** — use `@time`/`@btime` to find unexpected allocations.
4. **Apply targeted fixes** — use the references below for specific patterns.

```julia
using BenchmarkTools, Profile

# Step 1: Measure
@btime my_function($args)

# Step 2: Check type stability
@code_warntype my_function(args)

# Step 3: Profile
@profile my_function(args)
Profile.print(noisefloor=2.0)

# Step 4: Track allocations
julia --track-allocation=user -e 'using MyPkg; my_function(args); Profile.clear_malloc_data(); my_function(args)'
```

## Top Rules

1. **Put hot code in functions** — never at global/script scope.
2. **Avoid untyped globals** — use `const` or pass as arguments.
3. **Use concrete types everywhere** — in structs, containers, return values.
4. **Pre-allocate and mutate** — use `!` functions to reuse buffers.
5. **Access arrays in column-major order** — first index varies fastest.
6. **Fuse broadcasts** — use `@.` or dot syntax to avoid temporaries.

## Reference

- **[Type Stability](references/type-stability.md)** — Type inference, stable returns, function barriers
- **[Structs & Dispatch](references/structs-dispatch.md)** — Concrete fields, parametric types, Val
- **[Memory & Arrays](references/memory-arrays.md)** — Pre-allocation, views, column-major, broadcasting
- **[Annotations & Tweaks](references/annotations-tweaks.md)** — @inbounds, @fastmath, @simd, misc tips
- **[Profiling & Diagnosis](references/profiling.md)** — @code_warntype, profiling, allocation tracking

## Related Skills

- `julia-jet` - JET.jl static analysis overview
- `julia-jet-opt` - Detect runtime dispatch with `@report_opt`
- `julia-bench-quick` - Quick ad-hoc benchmarks with @btime
- `julia-bench-write` - Writing benchmark suites
- `julia-bench-run` - Running benchmark suites
