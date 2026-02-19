# Task and Channel Patterns

## Task Creation and Scheduling

- Create with `Task(() -> work())` or `@task work()`.
- Start with `schedule(task)`.
- Block until done with `wait(task)`.
- Check state with `istaskstarted(task)` and `istaskdone(task)`.
- For fire-and-wait style, use `t = Threads.@spawn work(); fetch(t)`.

## Channel Basics

- Create untyped/bounded channel: `Channel(32)`.
- Create typed/bounded channel: `Channel{MyType}(64)`.
- Write with `put!(c, x)`.
- Read with `take!(c)`.
- Read without removal using `fetch(c)`.
- Check availability with `isready(c)`.
- Close with `close(c)` when no further writes are expected.

## Blocking Semantics

- `take!` blocks on empty channel.
- `put!` blocks on full channel.
- `take!`/`fetch` can still return queued values after close.
- `put!` on closed channel throws `InvalidStateException`.

## Producer-Consumer Pattern

```julia
const jobs = Channel{Int}(32)
const results = Channel{Tuple{Int,Float64}}(32)

function worker()
    for id in jobs
        t = rand()
        sleep(t)
        put!(results, (id, t))
    end
end
```

Launch workers with `errormonitor(Threads.@spawn worker())`.

## Failure Propagation

- `errormonitor(task)` logs unexpected failures.
- `bind(ch, task)` is often more robust: it links task and resource lifetimes and propagates failure.

## Scheduler and Events

- `wait` is the general event wait API.
- `wait` on `Condition` queues tasks; `notify` wakes waiters.
- Explicitly created tasks are scheduler-independent until scheduled or waiting on scheduler-managed events.

## Low-Level Operations

- `yieldto` is the primitive task switch operation.
- Prefer structured primitives (`wait`, `Channel`, `schedule`) over direct `yieldto`.
- Use `task_local_storage` for task-scoped key-value state.
