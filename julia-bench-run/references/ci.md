# Benchmark CI Configuration

## AirspeedVelocity GitHub Action

### Basic Setup

```yaml
# .github/workflows/benchmark.yml
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

### With Tuning

```yaml
steps:
  - uses: MilesCranmer/AirspeedVelocity.jl@action-v1
    with:
      julia-version: '1'
      tune: 'true'  # More accurate but slower
```

### Specific Groups

```yaml
steps:
  - uses: MilesCranmer/AirspeedVelocity.jl@action-v1
    with:
      julia-version: '1'
      benchmark-filter: 'core'  # Only run core group
```

## Manual CI Setup

If you need more control:

```yaml
name: Benchmarks
on:
  pull_request:
    branches: [master, main]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: julia-actions/setup-julia@v2
        with:
          version: '1'
      - uses: julia-actions/cache@v2

      - name: Run benchmarks
        run: |
          julia --project=benchmark -e '
            using Pkg
            Pkg.instantiate()
            include("benchmark/benchmarks.jl")
            results = run(SUITE)
            # Process results as needed
          '
```

## Buildkite

```yaml
# .buildkite/pipeline.yml
steps:
  - label: "Benchmarks"
    plugins:
      - JuliaCI/julia#v1:
          version: "1"
    commands:
      - julia --project=benchmark -e '
          using Pkg; Pkg.instantiate();
          include("benchmark/benchmarks.jl");
          run(SUITE)'
    agents:
      queue: "benchmarks"  # Use dedicated benchmark runners
```
