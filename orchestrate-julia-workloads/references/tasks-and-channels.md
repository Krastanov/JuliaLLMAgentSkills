# Tasks and Channels

## Keep child tasks structured

Use `@sync` to wait for lexically enclosed tasks and collect their failures. Use `fetch` when the result is needed:

```julia
results = Vector{Int}(undef, length(items))

@sync for (i, item) in pairs(items)
    Threads.@spawn results[i] = work(item)
end
```

Prefer `Threads.@spawn` in reusable libraries even when the work is mostly waiting; `@async` creates sticky tasks and can inhibit migration of the parent task. Use `@async` only when deliberate local, single-thread scheduling is part of the design.

Attach `errormonitor` to intentionally detached tasks so failures are visible. Prefer a structured parent scope over detachment whenever the caller owns the work.

Avoid low-level `schedule` and `yieldto` for ordinary orchestration. Scheduling an arbitrary task that has already started is unsafe without a protocol that establishes ownership.

## Use channels for handoff and backpressure

Choose a concrete element type and a bounded capacity:

```julia
jobs = Channel{Job}(32) do ch
    for job in source
        put!(ch, job)
    end
end

@sync for _ in 1:nworkers
    Threads.@spawn for job in jobs
        handle(job)
    end
end
```

The `Channel(f, size)` constructor binds the producer task to the channel and closes the channel when the task terminates. Use `bind(channel, task)` when constructing them separately and when waiters should receive producer failures.

Treat `isready` and `isopen` as momentary observations, not synchronization guarantees. Prefer blocking `put!`, `take!`, iteration, `wait`, or a clearly owned state transition.

Size buffers to express acceptable queued work. An unbounded accumulation moved behind a channel is still unbounded resource use.

## Design failure behavior

- Let unexpected child failures reach the owning scope.
- Close producer-owned channels exactly once.
- Do not bind one channel to multiple producers without accounting for the rule that the first terminating bound task closes it.
- Avoid swallowing `CompositeException` or `TaskFailedException`; add context and preserve the cause.
- Ensure consumers finish when producers close normally and fail when producers terminate exceptionally.

## Sources

- [Julia asynchronous-programming manual](https://docs.julialang.org/en/v1/manual/asynchronous-programming/)
- [Julia task and channel reference](https://docs.julialang.org/en/v1/base/parallel/)
