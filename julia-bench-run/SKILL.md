---
name: julia-bench-run
description: Run benchmark suites locally and in CI using AirspeedVelocity.jl. Use this skill when running benchmarks or setting up CI performance tracking.
---

# Running Julia Benchmark Suites

Run benchmark suites locally and in CI using BenchmarkTools.jl and
AirspeedVelocity.jl for performance tracking.

## Running Locally

```bash
# Run all benchmarks
julia -tauto --project=benchmark -e '
    include("benchmark/benchmarks.jl")
    run(SUITE)'

# Run specific group
julia -tauto --project=benchmark -e '
    include("benchmark/benchmarks.jl")
    run(SUITE["core"])'

# Tune and run (more accurate but slower)
julia -tauto --project=benchmark -e '
    include("benchmark/benchmarks.jl")
    tune!(SUITE)
    run(SUITE)'
```

## CI with AirspeedVelocity

### .github/workflows/benchmark.yml

```yaml
name: Benchmarks
on:
  pull_request_target:
    branches: [master, main]

permissions:
  pull-requests: write

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: MilesCranmer/AirspeedVelocity.jl@action-v1
        with:
          julia-version: '1'
          tune: 'false'
```

## Comparing Results

```julia
# Save baseline
results_old = run(SUITE)
BenchmarkTools.save("baseline.json", results_old)

# After changes, compare
results_new = run(SUITE)
judge(median(results_new), median(results_old))
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `run(SUITE)` | Run all benchmarks |
| `run(SUITE["group"])` | Run specific group |
| `tune!(SUITE)` | Auto-tune parameters |
| `judge(new, old)` | Compare results |

## Reference

- **[CI Configuration](references/ci.md)** - Complete CI workflow examples
- **[Comparison](references/comparison.md)** - Comparing benchmark results

## Related Skills

- `julia-bench-quick` - Quick impromptu benchmarks
- `julia-bench-write` - Writing benchmark suites
- `julia-ci-github` - GitHub Actions configuration
