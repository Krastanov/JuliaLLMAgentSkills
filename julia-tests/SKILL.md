---
name: julia-tests
description: Run and write Julia tests with Test.jl, TestItemRunner.jl, and ParallelTestRunner.jl. Use when organizing test suites, choosing a test runner, or filtering package tests.
---

# Julia Tests

Use this skill for all Julia testing work. Choose the runner first, then load
only the matching reference file.

## Choose a Runner

- Standard `Test.jl` and `Pkg.test()`: open `references/testjl.md`
- `@testitem` suites with TestItemRunner.jl: open `references/testitemrunner.md`
- File-per-test suites with ParallelTestRunner.jl: open `references/paralleltestrunner.md`

## Quick Commands

```bash
julia -tauto --project=. -e 'using Pkg; Pkg.test()'
julia -tauto --project=. -e 'using Pkg; Pkg.test(; test_args=["integration"])'
julia -tauto --project=. -e 'using Pkg; Pkg.test(; test_args=["--verbose", "--jobs=4"])'
```

## Default Rule

- Prefer `Pkg.test(...)` over directly executing `test/runtests.jl`; `Pkg.test`
  activates the intended test environment and usually handles manifest updates
  more reliably.
- If tests fail in ways that do not match the current source, inspect checked-in
  `Manifest.toml` files in the package root, `test/`, and custom test
  subprojects. Stale manifests or broken path pins often cause fake failures.

## Resolve First

- If tests hit unreleased compat or registry lag in a multi-repo checkout,
  `Pkg.develop(path=...)` the local sibling repos into the active env before
  debugging the tests themselves.

## Writing Tests

- Standard `@testset` organization and common support files:
  `references/standard-tests.md`
- Writing filter-friendly `@testitem`s:
  `references/testitem.md`
- Writing file-per-test suites for ParallelTestRunner.jl:
  `references/parallel-files.md`

## Extra References

- Conditional loading and environment-based test selection:
  `references/conditional.md`
- Local code coverage checks and reports with LocalCoverage.jl:
  `references/localcoverage.md`
- Advanced ParallelTestRunner.jl setup:
  `references/parallel-advanced.md`

## Notes

- Keep doctest authoring and Documenter-specific setup under `julia-docs`.
- Keep JET-specific analysis workflow under `julia-jet`.
- Prefer one top-level testing skill and a few narrow reference files over many
  sibling skills.
