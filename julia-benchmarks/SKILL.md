---
name: julia-benchmarks
description: Set up performance benchmarking for Julia packages using BenchmarkTools.jl and AirspeedVelocity.jl. Use this skill when adding benchmarks or CI performance tracking.
---

# Julia Benchmarks

Set up performance benchmarking for Julia packages using BenchmarkTools.jl and
AirspeedVelocity.jl for CI integration.

## Quick Measurements

### BenchmarkTools.jl @btime

```julia
using BenchmarkTools

v = rand(1000)
@btime sum($v)          # Interpolate with $ to avoid global overhead
@btime sort!(x) setup=(x=copy($v))  # Fresh data each run
```

### Chairmarks.jl (Lightweight Alternative)

```julia
using Chairmarks

v = rand(1000)
@b sum(v)               # Automatic interpolation
@b sort!(x) setup=(x=copy($v))
```

## Project Structure

```
MyPackage.jl/
├── Project.toml           # Must include benchmark in workspace
├── benchmark/
│   ├── Project.toml       # Benchmark dependencies
│   └── benchmarks.jl      # Benchmark suite definition
└── .github/workflows/
    └── benchmark.yml      # CI workflow
```

## Workspace Configuration

```toml
# Project.toml
[workspace]
projects = ["docs", "benchmark"]
```

## Benchmark Suite

### benchmark/benchmarks.jl

```julia
using BenchmarkTools
using MyPackage
using StableRNGs

const SUITE = BenchmarkGroup()
rng = StableRNG(42)

const test_data = generate_data(rng, 1000)

SUITE["operations"] = BenchmarkGroup()
SUITE["operations"]["process"] = @benchmarkable process($test_data)
SUITE["inplace"]["modify"] = @benchmarkable modify!(d) setup=(d=copy($test_data)) evals=1
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

## Running Locally

```bash
julia -tauto --project=benchmark -e '
    include("benchmark/benchmarks.jl")
    run(SUITE)'
```

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `@benchmarkable f($x)` | Pure function |
| `@benchmarkable f!(y) setup=(y=copy(x)) evals=1` | Mutating function |
| `SUITE["group"]["name"]` | Organization |
| `StableRNG(seed)` | Reproducible random |

## Reference

- **[Patterns](references/patterns.md)** - Benchmark patterns and best practices
- **[Complete Example](references/example.md)** - Full benchmark suite example

## Related Skills

- `julia-ci-github` - GitHub Actions configuration
- `julia-tests-run` - Running tests
