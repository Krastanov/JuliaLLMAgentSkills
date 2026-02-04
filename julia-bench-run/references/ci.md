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