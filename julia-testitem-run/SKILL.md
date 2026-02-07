---
name: julia-testitem-run
description: Run Julia @testitem tests from the command line with TestItemRunner.jl, including reliable filtering by tags, names, and filenames for CI or agentic workflows. Use when asked to run only a subset of test items.
---

# Running `@testitem` Tests (CLI)

Use direct command-line filters for one-off agent runs. Avoid a large
environment-variable router unless a project already has one.

## Minimal Runner

```bash
julia -tauto --project=. -e 'using Pkg; Pkg.test()'
julia -tauto --project=test -e 'using TestItemRunner; TestItemRunner.run_tests("test")'
```

## CLI Filtering Invocations

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

## Filtering Rules to Keep Correct

1. Treat tags as `Symbol`s, not strings.
2. Match filenames with regex or `endswith` because `ti.filename` is a full path.
3. Keep filter expressions pure and quick; they run once per discovered test item.
4. Use `filter` and `verbose` consistently in both `run_tests` and `@run_package_tests`.

## Related Skills

- `julia-testitem-write` - Write filter-friendly `@testitem`s
- `julia-tests-run` - General Julia test execution patterns
- `julia-tests-write` - General test organization and templates
