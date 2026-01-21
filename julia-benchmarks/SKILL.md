# Julia Benchmarks

Set up performance benchmarking for Julia packages using BenchmarkTools.jl and
AirspeedVelocity.jl for CI integration.

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

### Project.toml

```toml
[workspace]
projects = ["docs", "benchmark"]
```

### benchmark/Project.toml

```toml
[deps]
BenchmarkTools = "6e4b80f9-dd63-53aa-95a3-0cdb28fa8baf"
MyPackage = "your-package-uuid"
StableRNGs = "860ef19b-820b-49d6-a774-d7a799459cd3"
```

Add any additional dependencies needed for benchmarks.

## Benchmark Suite

### benchmark/benchmarks.jl

```julia
using BenchmarkTools
using MyPackage
using StableRNGs

const SUITE = BenchmarkGroup()

# Use StableRNGs for reproducible benchmarks
rng = StableRNG(42)

# Create test data outside benchmarks
const test_data_small = generate_data(rng, 100)
const test_data_large = generate_data(rng, 10000)

# Organize benchmarks in groups
SUITE["operations"] = BenchmarkGroup(["operations"])

# Basic benchmarks
SUITE["operations"]["small"] = @benchmarkable process($test_data_small)
SUITE["operations"]["large"] = @benchmarkable process($test_data_large)

# Benchmarks with setup (fresh data each run)
SUITE["mutating"] = BenchmarkGroup(["mutating"])
SUITE["mutating"]["inplace"] = @benchmarkable modify!(data) setup=(data=copy(test_data_small)) evals=1

# Nested groups
SUITE["algorithms"] = BenchmarkGroup(["algorithms"])
SUITE["algorithms"]["v1"] = BenchmarkGroup(["v1"])
SUITE["algorithms"]["v1"]["100"] = @benchmarkable algorithm_v1(n) setup=(n=100)
SUITE["algorithms"]["v1"]["1000"] = @benchmarkable algorithm_v1(n) setup=(n=1000)
```

## Benchmark Patterns

### In-Place Operations

Use `evals=1` and `setup` for functions that modify state:

```julia
SUITE["inplace"]["modify"] = @benchmarkable modify!(arr) setup=(arr=zeros(1000)) evals=1
```

### Interpolation

Use `$` to interpolate variables (avoids global variable overhead):

```julia
const data = generate_data()
SUITE["process"] = @benchmarkable process($data)
```

### Size Scaling

Benchmark across different input sizes:

```julia
for n in [10, 100, 1000, 10000]
    SUITE["scale"]["$n"] = @benchmarkable algorithm(data) setup=(data=generate($n))
end
```

### Direction/Mode Comparison

```julia
SUITE["traversal"]["direction"] = BenchmarkGroup(["direction"])
SUITE["traversal"]["direction"]["right"] = @benchmarkable process(c, :right) setup=(c=make_data(100)) evals=1
SUITE["traversal"]["direction"]["left"] = @benchmarkable process(c, :left) setup=(c=make_data(100)) evals=1
```

## Running Benchmarks Locally

```bash
# Run all benchmarks
julia -tauto --project=benchmark -e '
    include("benchmark/benchmarks.jl")
    run(SUITE)'

# Run specific group
julia -tauto --project=benchmark -e '
    include("benchmark/benchmarks.jl")
    run(SUITE["operations"])'

# Tune and run (more accurate but slower)
julia -tauto --project=benchmark -e '
    include("benchmark/benchmarks.jl")
    tune!(SUITE)
    run(SUITE)'
```

## CI with AirspeedVelocity (Recommended)

AirspeedVelocity.jl provides the simplest and most modern CI benchmark integration.

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

This automatically:
- Runs benchmarks on both PR branch and base branch
- Compares results and detects regressions
- Posts a comment on the PR with the comparison table

### Options

```yaml
- uses: MilesCranmer/AirspeedVelocity.jl@action-v1
  with:
    julia-version: '1'      # Julia version to use
    tune: 'false'           # Whether to tune benchmarks (slower but more accurate)
    # Additional options available in AirspeedVelocity docs
```

## Complete Example

### benchmark/benchmarks.jl

```julia
using BenchmarkTools
using MyPackage
using MyPackage: internal_function, InternalType
using StableRNGs

const SUITE = BenchmarkGroup()

# Reproducible random data
rng = StableRNG(42)

# Helper functions to create test data
function make_small_data(n::Int)
    # Create data structure of size n
    return MyType(rand(rng, n))
end

function make_large_data(n::Int)
    return MyType(rand(rng, n))
end

# Pre-create constant test data
const small_data = make_small_data(100)
const large_data = make_large_data(1000)

# Core operations benchmarks
SUITE["core"] = BenchmarkGroup(["core"])
SUITE["core"]["process_small"] = @benchmarkable process($small_data)
SUITE["core"]["process_large"] = @benchmarkable process($large_data)

# Scaling benchmarks
SUITE["scaling"] = BenchmarkGroup(["scaling"])
for n in [10, 100, 1000]
    SUITE["scaling"]["$n"] = @benchmarkable process(d) setup=(d=make_small_data($n)) evals=1
end

# In-place operations (use evals=1 and setup)
SUITE["inplace"] = BenchmarkGroup(["inplace"])
SUITE["inplace"]["modify_100"] = @benchmarkable modify!(d) setup=(d=make_small_data(100)) evals=1
SUITE["inplace"]["modify_1000"] = @benchmarkable modify!(d) setup=(d=make_large_data(1000)) evals=1

# Algorithm variants
SUITE["algorithms"] = BenchmarkGroup(["algorithms"])
SUITE["algorithms"]["v1_100"] = @benchmarkable algorithm_v1(d) setup=(d=make_small_data(100)) evals=1
SUITE["algorithms"]["v2_100"] = @benchmarkable algorithm_v2(d) setup=(d=make_small_data(100)) evals=1
```

## Best Practices

1. **Use StableRNGs** for reproducible random data across runs
2. **Create test data outside benchmarks** using `const` globals
3. **Use `evals=1`** for mutating functions
4. **Use `setup=`** for fresh data each evaluation
5. **Interpolate with `$`** to avoid global variable overhead
6. **Group related benchmarks** for organization
7. **Benchmark multiple sizes** to catch scaling issues
8. **Use descriptive group/benchmark names** for clear reports

## When to Add Benchmarks

Add benchmarks for:
- New compilation passes or transformations
- New algorithms or data structures
- Functions that process data at scale
- Performance-critical code paths
- Any code where performance regressions would be problematic

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `@benchmarkable f($x)` | Pure function, interpolate constant input |
| `@benchmarkable f!(y) setup=(y=copy(x)) evals=1` | Mutating function |
| `SUITE["group"]["subgroup"]` | Nested organization |
| `run(SUITE)` | Run all benchmarks |
| `tune!(SUITE)` | Calibrate timing parameters |
| `StableRNG(seed)` | Reproducible random numbers |

## Related Skills

- `julia-ci-github` - GitHub Actions configuration
- `julia-ci-buildkite` - Buildkite configuration
- `julia-tests` - Test setup and patterns
