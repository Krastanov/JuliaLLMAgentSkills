# Threads and Scheduling

## Choose threads for CPU work

Configure thread counts before launch with `--threads` or `JULIA_NUM_THREADS`, then inspect the actual pools:

```julia
Threads.nthreads(:default)
Threads.nthreads(:interactive)
Threads.threadpoolsize()
```

Use `Threads.@spawn` for a small task graph with explicit results. Use `Threads.@threads` for independent loop iterations when coarse loop scheduling fits the workload.

## Select a loop schedule

- Use the default or `:dynamic` for indexable work whose iteration costs are roughly uniform. It uses a bounded number of tasks and contiguous iteration regions.
- Use `:greedy` for uneven work or iterators that are not indexable. Require Julia 1.11 or later.
- Avoid `:static` in new library code unless fixed thread assignment is an explicit compatibility requirement. It cannot be nested freely or called from an arbitrary worker thread.

Treat schedule choice as a benchmark variable. Do not rely on iteration order or a stable assignment of work to threads.

## Enforce race freedom

- Make every loop iteration independently forward-progressing.
- Do not communicate between `@threads` iterations with blocking channels.
- Write to disjoint output locations, return per-task results, or protect shared mutation with a lock or atomic operation.
- Release a lock in the same iteration that acquired it; prefer `lock(lock_object) do ... end` or `@lock` for exception safety.
- Protect Base collections when any concurrent task mutates them.
- Do not index buffers by `threadid()` unless the code deliberately uses a schedule that pins the task. Tasks can migrate after yielding.
- Avoid parallel top-level `include`, `eval`, and method or type definition.

Prefer partitioning work and combining task-local results over a shared accumulator.

## Use Polyester only after measurement

Keep Base threading as the default. Consider `Polyester.@batch` only when a representative BenchmarkTools result shows that Base scheduling overhead materially limits a small, independent loop. Before adopting it:

1. Verify current Julia and package compatibility.
2. Check Polyester's array, view, bounds-checking, and scheduling semantics for the kernel.
3. Compare sequential, Base-threaded, and Polyester implementations across relevant sizes and thread counts.
4. Retain the clearer Base path when the improvement is small or unstable.

Do not generalize one microbenchmark to other element types, CPUs, memory layouts, or nested workloads.

## Sources

- [Julia multi-threading manual](https://docs.julialang.org/en/v1/manual/multi-threading/)
- [Julia `Base.Threads` reference](https://docs.julialang.org/en/v1/base/multi-threading/)
- [Polyester repository and documented `@batch` semantics](https://github.com/JuliaSIMD/Polyester.jl)
