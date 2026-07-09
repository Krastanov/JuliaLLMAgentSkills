---
name: optimize-julia-code
description: Measure and improve Julia runtime performance with BenchmarkTools, profiling and allocation tools, inference diagnosis, data-layout changes, and guarded low-level optimizations. Use when Julia code is slow, allocation-heavy, type-unstable, or needs a reproducible performance baseline or regression check.
---

# Optimize Julia Code

Optimize an observed workload, preserve its behavior, and remeasure every change.

## Workflow

1. Define representative inputs and record a correct baseline.
2. Establish repeatable timing and allocation measurements. Read [measurement-and-benchmarks.md](references/measurement-and-benchmarks.md).
3. Locate time or allocation hotspots before editing. Read [profiling-and-allocations.md](references/profiling-and-allocations.md).
4. Inspect inference and memory access only where measurements point. Read [inference-and-data-layout.md](references/inference-and-data-layout.md).
5. Apply annotations, concurrency, or specialized tooling only after simpler changes. Read [advanced-optimization.md](references/advanced-optimization.md).
6. Run correctness tests and the original measurement after each focused change. Keep only improvements that hold on representative inputs.

## Boundaries

- Separate first-call latency from steady-state runtime.
- Prefer algorithmic and data-movement improvements over syntax-level tweaks.
- Do not make argument types concrete merely for speed; Julia specializes on actual argument types.
- Do not add an optimization package without a measured bottleneck, a current compatibility check, and a benchmark against Base Julia.
- Report the workload, Julia version, thread configuration, inputs, and measurement method with performance conclusions.
