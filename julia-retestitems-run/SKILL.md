---
name: julia-retestitems-run
description: Run Julia @testitem tests with ReTestItems.jl, including parallel runs and filtering by tags, names, and paths. Use this skill when executing or narrowing @testitem subsets.
---

# Running `@testitem` Tests with ReTestItems.jl

ReTestItems.jl is the preferred runner for `@testitem` suites. It keeps the same
`@testitem` organization but provides better CLI filtering and parallel
execution. Use `julia-testitem-write` for authoring patterns.

## Quickstart

```bash
# Run the full test suite from the test environment
julia -tauto --project=test -e 'using ReTestItems; runtests()'
```

`runtests` discovers test files ending with `_test.jl` or `_tests.jl` in the
active project.

## Run Specific Files or Directories

```bash
julia -tauto --project=test -e 'using ReTestItems; runtests("test/Database/")'
julia -tauto --project=test -e 'using ReTestItems; runtests("test/foo_test.jl", "test/bar_tests.jl")'
```

## Filter by Name or Tags

```bash
# Exact name
julia -tauto --project=test -e 'using ReTestItems; runtests("test/"; name="issue-123")'

# Regex name match
julia -tauto --project=test -e 'using ReTestItems; runtests("test/"; name=r"^issue")'

# Tags (all tags must be present)
julia -tauto --project=test -e 'using ReTestItems; runtests("test/"; tags=[:regression, :fast])'

# Combine tags + name
julia -tauto --project=test -e 'using ReTestItems; runtests("test/"; tags=:regression, name=r"^issue")'
```

## Parallel Runs

```bash
# Use worker processes for parallel test-item execution
julia -tauto --project=test -e 'using ReTestItems; runtests("test/"; nworkers=4)'

# Set threads per worker process
julia -tauto --project=test -e 'using ReTestItems; runtests("test/"; nworkers=4, nworker_threads=2)'
```

Notes:
1. `nworkers=0` (default) runs sequentially on the current process.
2. `nworkers=1` runs sequentially in a new process.
3. `nworkers>=2` runs in parallel across worker processes.
4. ReTestItems uses distributed processes (not multithreading) for parallel runs.

## Logging and Fail-Fast

```bash
# Only show logs for failing/erroring items (default in non-interactive runs)
julia -tauto --project=test -e 'using ReTestItems; runtests("test/"; logs=:issues)'

# Stop scheduling new test-items after the first failure
julia -tauto --project=test -e 'using ReTestItems; runtests("test/"; failfast=true)'

# Stop within each test-item at the first failing test
julia -tauto --project=test -e 'using ReTestItems; runtests("test/"; testitem_failfast=true)'
```

## Failures First

```bash
# Run previous failures first (default is true)
julia -tauto --project=test -e 'using ReTestItems; runtests("test/"; failures_first=true)'
```

## Related Skills

- `julia-testitem-write` - `@testitem` authoring patterns (runner-agnostic)
- `julia-tests-run` - General Julia test execution patterns
- `julia-tests-write` - Test organization templates
- `julia-testitem-run` - Legacy TestItemRunner.jl runner patterns
