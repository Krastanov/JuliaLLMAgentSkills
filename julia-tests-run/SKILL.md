---
name: julia-tests-run
description: Run Julia tests with filtering, conditional loading, and environment-based selection. Use this skill when running tests or configuring test infrastructure.
---

# Running Julia Tests

Run tests for Julia packages with support for filtering, conditional loading,
and environment-based test selection using TestItemRunner.jl.
For `@testitem`-specific CLI filtering patterns, use `julia-testitem-run`.

## Quick Commands

```bash
# Standard test run
julia -tauto --project=. -e 'using Pkg; Pkg.test()'
```

## Test Project Setup

```julia
using Pkg
Pkg.activate("test")
Pkg.add(["Test", "TestItemRunner", "Aqua", "JET", "Documenter"])
Pkg.develop(path=pwd())
```

## Test Runner with Filtering

### test/runtests.jl

```julia
using MyPackage
using TestItemRunner

testfilter = ti -> begin
    exclude = Symbol[]
    if get(ENV, "JET_TEST", "") != "true"
        push!(exclude, :jet)
    end
    if !(VERSION >= v"1.10")
        push!(exclude, :doctests)
        push!(exclude, :aqua)
    end
    return all(!in(exclude), ti.tags)
end

println("Starting tests with $(Threads.nthreads()) threads...")

@run_package_tests filter=testfilter
```

### Common Tags

| Tag | Purpose |
|-----|---------|
| `:jet` | JET static analysis |
| `:aqua` | Aqua code quality |
| `:doctests` | Documentation tests |
| `:cuda` | CUDA GPU tests |
| `:plotting` | Visualization tests |

## Reference

- **[Conditional Loading](references/conditional.md)** - Environment-based test selection

## Related Skills

- `julia-tests-write` - Writing tests
- `julia-testitem-run` - Dedicated `@testitem` filtering workflows
- `julia-testitem-write` - Writing filter-friendly `@testitem`s
