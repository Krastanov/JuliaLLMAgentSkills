---
name: julia-bench-run
description: Run benchmark suites locally and in CI using AirspeedVelocity.jl. Use this skill when running benchmarks or setting up CI performance tracking.
---

# Running Julia Benchmark Suites

Run benchmark suites locally and in CI using BenchmarkTools.jl and
AirspeedVelocity.jl.

## Run Locally

```bash
julia -tauto --project=benchmark -e 'include("benchmark/benchmarks.jl"); run(SUITE)'
julia -tauto --project=benchmark -e 'include("benchmark/benchmarks.jl"); run(SUITE["core"])'
julia -tauto --project=benchmark -e 'include("benchmark/benchmarks.jl"); tune!(SUITE); run(SUITE)'
```

## Compare Results

```julia
results_old = run(SUITE)
BenchmarkTools.save("baseline.json", results_old)

results_new = run(SUITE)
judge(median(results_new), median(results_old))
```

## Reference

- **[CI Configuration](references/ci.md)** - Complete AirspeedVelocity workflows
- **[Comparison](references/comparison.md)** - Comparing benchmark results

## Related Skills

- `julia-bench-quick` - Quick impromptu benchmarks
- `julia-bench-write` - Writing benchmark suites
- `julia-ci-github` - GitHub Actions configuration
