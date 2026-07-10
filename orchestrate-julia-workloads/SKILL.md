---
name: orchestrate-julia-workloads
description: Coordinate Julia tasks, channels, threads, external numerical-library threads, and subprocesses with explicit lifetimes and failure propagation. Use when building producer-consumer workflows, parallelizing CPU work, fixing races or deadlocks, controlling oversubscription, or automating external commands from Julia.
---

# Orchestrate Julia Workloads

Choose the smallest execution model that matches the work, then make task and process lifetimes explicit.

## Route the Work

- For cooperative jobs, I/O overlap, backpressure, or producer-consumer flows, read [tasks-and-channels.md](references/tasks-and-channels.md).
- For CPU parallelism, shared-memory safety, thread pools, or loop scheduling, read [threads-and-scheduling.md](references/threads-and-scheduling.md).
- For BLAS, MKL, FFT, or another library with its own worker pool, read [library-thread-control.md](references/library-thread-control.md).
- For `Cmd`, pipelines, process I/O, environments, or replacing shell glue, read [commands-and-processes.md](references/commands-and-processes.md).

## Core Rules

1. Keep a correct sequential implementation or test oracle.
2. Bound concurrency and buffering from resource limits, not only input size.
3. Enclose child work in a scope that waits and propagates failures.
4. Give each task ownership of mutable state; synchronize truly shared state.
5. Avoid stacking Julia threads, library threads, and process workers without measuring the total resource use.
6. Test success, failure, cancellation or interruption, empty input, and constrained concurrency.
7. Measure representative workloads before retaining a parallel implementation.
