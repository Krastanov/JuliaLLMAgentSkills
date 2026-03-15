---
name: julia-testitem-run
description: Run Julia @testitem tests from the command line with TestItemRunner.jl, including reliable filtering by tags, names, and filenames for CI or agentic workflows. Use when asked to run only a subset of test items.
---

# Running `@testitem` Tests (CLI)

Run tests written with `@testitem` using TestItemRunner.jl.

## Minimal Runner

```bash
julia -tauto --project=. -e 'using Pkg; Pkg.test()'
julia -tauto --project=test -e 'using TestItemRunner; TestItemRunner.run_tests("test")'
```

## CLI Filtering

```bash
# Include only one tag
julia -tauto --project=test -e 'using TestItemRunner; TestItemRunner.run_tests("test"; filter=ti->(:core in ti.tags))'

# Exclude one tag
julia -tauto --project=test -e 'using TestItemRunner; TestItemRunner.run_tests("test"; filter=ti->(!(:skipci in ti.tags)))'

# Filter by test item name
julia -tauto --project=test -e 'using TestItemRunner; TestItemRunner.run_tests("test"; filter=ti->occursin(r"fft.*edge", ti.name))'

# Filter by filename + tag
julia -tauto --project=test -e 'using TestItemRunner; TestItemRunner.run_tests("test"; filter=ti->(endswith(ti.filename, "test_fft.jl") && !(:slow in ti.tags)))'
```

## runtests.jl with Tag Filtering

```julia
using MyPackage
using TestItemRunner

testfilter = ti -> begin
    exclude = Symbol[]
    if get(ENV, "JET_TEST", "") == "true"
        return :jet in ti.tags  # JET-only mode
    else
        push!(exclude, :jet)
    end
    if !(VERSION >= v"1.10")
        push!(exclude, :doctests, :aqua)
    end
    return all(!in(exclude), ti.tags)
end

@run_package_tests filter=testfilter
```

## Test Project Setup

```julia
using Pkg
Pkg.activate("test")
Pkg.add(["Test", "TestItemRunner", "Aqua", "JET", "Documenter"])
Pkg.develop(path=pwd())
```

## Filtering Rules

1. Tags are `Symbol`s, not strings.
2. `ti.filename` is a full path — use `endswith` or regex.
3. Filter functions must be pure and fast (run once per discovered item).
4. Use `filter` kwarg in both `run_tests` and `@run_package_tests`.

## Related Skills

- `julia-testitem-write` - Write filter-friendly `@testitem`s
- `julia-tests-run` - Standard Test.jl execution
