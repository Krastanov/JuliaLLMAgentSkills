# Julia Threading Patterns

## Startup and Threadpools

- Start with explicit thread counts: `julia --threads N` or `JULIA_NUM_THREADS=N`.
- Configure default/interactive pools: `julia --threads 3,1`.
- Check pools and placement:
  - `Threads.nthreads(:default)`
  - `Threads.nthreads(:interactive)`
  - `Threads.nthreadpools()`
  - `Threads.threadpool()`

GC thread configuration:
- `--gcthreads` (Julia >= 1.10)
- `JULIA_NUM_GC_THREADS`

## Data Parallel Loops

Use `Threads.@threads` on loop iteration spaces:

```julia
Threads.@threads for i in eachindex(a)
    a[i] = f(a[i])
end
```

`@threads` does not do reductions automatically; implement reduction safely with chunk-local state and final aggregation.

## Task-Based Parallel Work

Use `Threads.@spawn` for composable work units:

```julia
tasks = map(chunks) do chunk
    Threads.@spawn sum(chunk)
end
total = sum(fetch.(tasks))
```

Scheduling is nondeterministic; never depend on output order unless explicitly synchronized.

## Locks and Lockable

- Use `@lock lockobj expr` for short protected updates.
- Use `lock(lockobj) do ... end` for scoped locking.
- Use `Base.Lockable(value)` to couple lock and protected value.

Always ensure unlock in `finally` when locking manually.

## Atomics

- Use `Threads.Atomic{T}` for primitive shared values.
- Update with `Threads.atomic_add!` and related APIs.
- For structs, mark atomic fields with `@atomic` and use explicit orderings when needed.

Available orderings include `:monotonic`, `:acquire`, `:release`, `:acquire_release`, and `:sequentially_consistent`.

## Thread Safety Warnings

- Julia code must be data-race free; races can cause wrong answers or memory unsafety.
- Base collections need manual locking if concurrently modified.
- Task migration means `threadid()` can change when tasks yield.
- Avoid indexing shared state directly by `threadid()`.

## Additional Caveats

- `@threadcall` can offload blocking C calls but the called function must not callback into Julia.
- In long compute loops, use `GC.safepoint()` if GC starvation appears.
- Finalizers and global-state interactions require careful locking and design.
