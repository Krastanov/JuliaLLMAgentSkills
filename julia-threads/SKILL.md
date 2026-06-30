---
name: julia-threads
description: Implement and debug Julia multithreading with Threads.@threads, Threads.@spawn, threadpools, locks, atomics, and race-avoidance patterns. Use this skill when parallelizing CPU work, configuring Julia thread counts, fixing data races, or handling thread-specific caveats such as task migration.
---

# Julia Threads

Use Julia `Base.Threads` tools to parallelize CPU work while preserving thread safety.

## Start Julia with the Right Thread Configuration

Use CLI flags or env vars before launch:

```bash
julia --threads 4
export JULIA_NUM_THREADS=4
```

Check runtime layout:

```julia
Threads.nthreads(:default)
Threads.nthreads(:interactive)
Threads.threadid()
```

Use threadpools for responsiveness and interactive tasks.

## Pick the Execution Primitive

- Use `Threads.@threads [schedule]` for parallel loops over iteration spaces.
  - `:dynamic` (default): Distributes chunks dynamically. Best for uniform workloads.
  - `:greedy` (Julia 1.11+): Tasks greedily take the next value. Excellent for non-uniform workloads and non-indexable iterators.
  - `:static`: Divides iterations equally with exactly one task per thread. Discouraged in library code as it cannot be nested or called outside thread 1.
- Use `Threads.@spawn` for task-based parallel decomposition.
- Use `@spawn :interactive ...` for latency-sensitive tasks.
- Use `Polyester.@batch` for lightweight multithreaded loops with significantly lower task-spawning overhead than `@threads`, making it ideal for tight loops.
- Leverage ecosystem packages built on Polyester for low-overhead multithreading: `Strided.jl` (multithreaded array views), `FastBroadcast.jl` (`@.. thread=true` for non-allocating parallel broadcast), and `LoopVectorization.jl` (`@tturbo` for multithreaded SIMD vectorization).

For reduction-style work, avoid shared mutable accumulators; split work into independent chunks and combine results after `fetch`.

## Enforce Data-Race Freedom

Treat race freedom as a hard requirement:
- Protect shared mutable state with `ReentrantLock`, `@lock`, or `lock(... do ...)`.
- Prefer `Base.Lockable` to bind lock + protected object.
- Use `Threads.Atomic` / `atomic_*` for primitive shared counters and similar patterns.
- Use per-field atomics (`@atomic`, `@atomicswap`, `@atomicreplace`, `@atomiconce`) when field-level ordering is required.

## Numeric Libraries (BLAS, FFTW, MKL)

When mixing Julia's native multithreading with external threaded libraries, you must manually manage thread counts to avoid **oversubscription**. If calling these libraries inside a natively threaded region, set their thread count to `1` (e.g., `BLAS.set_num_threads(1)`).

## Handle Migration and Runtime Caveats

- Do not assume `threadid()` stays constant inside a task.
- Avoid per-thread buffers indexed by `threadid()` unless migration constraints are handled.
- Expect `@spawn` scheduling order to be nondeterministic.
- Insert `GC.safepoint()` in long compute-bound loops if needed to prevent GC starvation.
- Avoid parallel top-level `include`/`eval` of types/modules/methods.

## Reference

- `references/threading-patterns.md` - thread setup, safety, and synchronization patterns
- `references/polyester.md` - lightweight threading with Polyester.jl and related ecosystem packages
- `references/numeric-libraries.md` - managing thread counts in BLAS, MKL, and FFTW

## Related Skills

- `julia-async` - task/channel concurrency and event scheduling
- `julia-tests` - validating threaded behavior in tests
