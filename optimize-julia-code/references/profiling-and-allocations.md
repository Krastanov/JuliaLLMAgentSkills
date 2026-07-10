# Profiling and Allocations

## Profile execution time

Compile the workload, clear old samples, and collect enough work for a useful statistical profile:

```julia
using Profile

target(args...)                     # warm up
Profile.clear()
@profile for _ in 1:100
    target(args...)
end
Profile.print()
Profile.print(format=:flat, sortedby=:count)
```

Read the call tree before editing a line with many samples: an expensive child call contributes samples to its callers. Increase the repeated work when the profile has too few samples. Use `C=true` in `Profile.print` when time may be inside C or Fortran code.

On Julia 1.12 or later, use `Profile.@profile_walltime` for task-heavy workloads where waiting and synchronization matter. The regular CPU profiler samples running threads and can miss blocked tasks.

## Measure allocations

Start with totals after warmup:

```julia
target(args...)
bytes = @allocated target(args...)
count = @allocations target(args...)
```

Use the allocation profiler to find allocation sites:

```julia
using Profile

target(args...)
Profile.Allocs.clear()
Profile.Allocs.@profile sample_rate=0.01 target(args...)
allocs = Profile.Allocs.fetch()
Profile.Allocs.print(stdout, allocs)
```

Tune `sample_rate` to collect a useful sample without overwhelming the workload. A sampled allocation profile counts allocation events uniformly; it does not necessarily rank sites by total bytes unless every allocation is recorded.

Use `--track-allocation=user` only when the allocation profiler is insufficient. Warm up, call `Profile.clear_malloc_data()`, run the workload again, then inspect the generated `.mem` files. Remember that allocation tracking changes code generation.

## Diagnose before reducing

- Distinguish required output allocation from avoidable temporary allocation.
- Check whether allocations come from type uncertainty, captured variables, conversions, slicing, or repeated buffer creation.
- Preallocate only when a buffer can be reused safely and the measurement shows value.
- Do not trade correctness, alias safety, or a clear public API for an insignificant allocation reduction.

## Sources

- [Julia profiling manual](https://docs.julialang.org/en/v1/manual/profile/)
- [Profile standard-library reference](https://docs.julialang.org/en/v1/stdlib/Profile/)
