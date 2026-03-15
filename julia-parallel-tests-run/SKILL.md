---
name: julia-parallel-tests-run
description: Run Julia tests in parallel with ParallelTestRunner.jl including automatic discovery, CLI args, filtering, and worker configuration. Use this skill when running tests with ParallelTestRunner.jl.
---

# Running Tests with ParallelTestRunner.jl

Run test files in parallel across isolated worker processes with automatic
discovery and load balancing.

## Quick Commands

```bash
# Standard run
julia --project test/runtests.jl

# Verbose with job count
julia --project test/runtests.jl --verbose --jobs=4

# Run specific tests (prefix match)
julia --project test/runtests.jl integration core

# List available tests
julia --project test/runtests.jl --list

# Quick fail on first error
julia --project test/runtests.jl --quickfail
```

## Via Pkg.test

```julia
using Pkg
Pkg.test("MyPackage"; test_args=`--verbose --jobs=4`)
Pkg.test("MyPackage"; test_args=`integration`)
```

## Minimal runtests.jl

```julia
using MyPackage
using ParallelTestRunner

runtests(MyPackage, ARGS)
```

## CLI Options

| Flag | Purpose |
|------|---------|
| `--help` | Show usage |
| `--list` | List all test files |
| `--verbose` | Show start times and details |
| `--quickfail` | Stop on first failure |
| `--jobs=N` | Number of worker processes |
| `TESTS...` | Filter tests by name prefix |

## Reference

- **[Advanced](references/advanced.md)** - Custom workers, init code, filtering

## Related Skills

- `julia-parallel-tests-write` - Writing tests for ParallelTestRunner.jl
- `julia-tests-run` - Standard Test.jl execution
