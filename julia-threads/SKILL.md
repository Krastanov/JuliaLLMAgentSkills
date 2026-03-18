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

- Use `Threads.@threads` for parallel loops over iteration spaces.
- Use `Threads.@spawn` for task-based parallel decomposition.
- Use `@spawn :interactive ...` for latency-sensitive tasks.

For reduction-style work, avoid shared mutable accumulators; split work into independent chunks and combine results after `fetch`.

## Enforce Data-Race Freedom

Treat race freedom as a hard requirement:
- Protect shared mutable state with `ReentrantLock`, `@lock`, or `lock(... do ...)`.
- Prefer `Base.Lockable` to bind lock + protected object.
- Use `Threads.Atomic` / `atomic_*` for primitive shared counters and similar patterns.
- Use per-field atomics (`@atomic`, `@atomicswap`, `@atomicreplace`, `@atomiconce`) when field-level ordering is required.

## Handle Migration and Runtime Caveats

- Do not assume `threadid()` stays constant inside a task.
- Avoid per-thread buffers indexed by `threadid()` unless migration constraints are handled.
- Expect `@spawn` scheduling order to be nondeterministic.
- Insert `GC.safepoint()` in long compute-bound loops if needed to prevent GC starvation.
- Avoid parallel top-level `include`/`eval` of types/modules/methods.

## Reference

- `references/threading-patterns.md` - thread setup, safety, and synchronization patterns

## Related Skills

- `julia-async` - task/channel concurrency and event scheduling
- `julia-tests` - validating threaded behavior in tests
