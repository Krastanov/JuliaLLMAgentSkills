---
name: julia-async
description: Build and troubleshoot asynchronous Julia code using Task, schedule/wait, Channels, producer-consumer patterns, and task/event coordination. Use this skill when implementing non-blocking workflows, background jobs, inter-task communication, or Task-based orchestration in Julia.
---

# Julia Async

Use Julia `Task` and `Channel` primitives for concurrent workflows that cooperate through yielding and waiting.

## Task Lifecycle Pattern

Create task work with `@task` or `Task`, then schedule and wait:

```julia
t = @task begin
    sleep(0.1)
    println("done")
end

schedule(t)
wait(t)
```

For immediate scheduling, use `Threads.@spawn` and `fetch`/`wait` on the returned task handle.

## Producer-Consumer with Channels

Use `Channel` when tasks need explicit handoff and buffering:

```julia
function producer(c::Channel)
    for n in 1:4
        put!(c, n)
    end
end

for x in Channel(producer)
    @show x
end
```

Apply bounded channel capacities (`Channel{T}(sz)`) to control backpressure.

## Error Handling and Robust Wiring

- Use `errormonitor(task)` for visibility of task failures.
- Prefer `bind(channel, task)` when channel lifetime and failure propagation should be linked.
- Use `take!`, `put!`, `fetch`, `isready`, `close` according to channel state semantics.

## Event Waiting Model

Remember that `wait` is the core blocking primitive:
- `wait(task)` for task completion.
- `wait(process)` for process exit.
- `wait(condition)`/`notify(condition)` for condition synchronization.

Most switching is scheduler-managed; avoid low-level `yieldto` unless implementing advanced control flow.

## Reference

- `references/task-channel-patterns.md` - task/channel recipes and safety notes

## Related Skills

- `julia-threads` - multi-threaded execution and synchronization
- `julia-external-cmd` - subprocess orchestration with tasks and pipelines
