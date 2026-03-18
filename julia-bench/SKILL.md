---
name: julia-bench
description: Benchmark Julia code with BenchmarkTools.jl and AirspeedVelocity.jl. Use when running quick benchmarks, writing benchmark suites, comparing results, or setting up benchmark CI.
---

# Julia Benchmarks

Use this skill for all Julia benchmarking work. Pick the workflow first, then
open only the matching reference file.

## Choose a Workflow

- Quick ad-hoc timing during development:
  `references/quick-patterns.md`
- Writing a benchmark suite:
  `references/suite-patterns.md`
- Full suite example:
  `references/suite-example.md`
- Comparing saved benchmark results:
  `references/comparison.md`
- Benchmark CI with AirspeedVelocity.jl:
  `references/ci.md`

## Quick Commands

```julia
using BenchmarkTools

v = rand(1000)
@btime sum($v)
@btime sort!(x) setup=(x=copy($v))
```

```bash
julia -tauto --project=benchmark -e 'include("benchmark/benchmarks.jl"); run(SUITE)'
julia -tauto --project=benchmark -e 'include("benchmark/benchmarks.jl"); tune!(SUITE); run(SUITE)'
```

## Notes

- Use `$` interpolation in BenchmarkTools unless you deliberately want to time
  global lookup.
- Use `setup=` and usually `evals=1` for mutating benchmarks.
- Use a benchmark subproject for repeatable suites and CI.

## Related Skills

- `julia-perf` - performance diagnosis and optimization before benchmarking
- `julia-package-dev` - package workflows around benchmark environments

