---
name: julia-bench-write
description: Write benchmark suites for Julia packages using BenchmarkTools.jl. Use this skill when creating organized, reproducible benchmark suites.
---

# Writing Julia Benchmark Suites

Write organized benchmark suites for Julia packages using BenchmarkTools.jl
with reproducible data and grouped benchmarks.

## Project Structure

```
MyPackage.jl/
├── Project.toml           # Must include benchmark in workspace
├── benchmark/
│   ├── Project.toml       # Benchmark dependencies
│   └── benchmarks.jl      # Benchmark suite definition
```

## Workspace Configuration

```toml
# Project.toml
[workspace]
projects = ["docs", "benchmark"]
```

## Benchmark Dependencies

### benchmark/Project.toml

```toml
[deps]
BenchmarkTools = "6e4b80f9-dd63-53aa-95a3-0cdb28fa8baf"
MyPackage = "your-package-uuid"
StableRNGs = "860ef19b-820b-49d6-a774-d7a799459cd3"
```

## Basic Suite Structure

### benchmark/benchmarks.jl

```julia
using BenchmarkTools
using MyPackage
using StableRNGs

const SUITE = BenchmarkGroup()
rng = StableRNG(42)

# Pre-create constant test data
const test_data = generate_data(rng, 1000)

# Define benchmarks
SUITE["operations"] = BenchmarkGroup()
SUITE["operations"]["process"] = @benchmarkable process($test_data)
SUITE["inplace"]["modify"] = @benchmarkable modify!(d) setup=(d=copy($test_data)) evals=1
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

- `julia-bench-quick` - Quick impromptu benchmarks
- `julia-bench-run` - Running benchmark suites
