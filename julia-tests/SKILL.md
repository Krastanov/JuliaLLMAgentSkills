---
name: julia-tests
description: "Run and write Julia tests with Test.jl, TestItemRunner.jl, and ParallelTestRunner.jl — including writing @testitem blocks, configuring parallel execution, filtering test subsets, and debugging test failures. Use when organizing test suites, choosing a test runner, filtering package tests, or interpreting test output."
---

# Julia Tests

Use this skill for all Julia testing work. Choose the runner first, then load
only the matching reference file.

## Workflow

1. **Choose a runner** (see below)
2. **Write tests** using the matching reference
3. **Run** with the appropriate command
4. **Interpret output**: look for `Test Failed` lines — the file path and line number point to the failing assertion. Fix and re-run.
5. **Verify**: all tests pass with zero failures before committing

## Choose a Runner

- Standard `Test.jl` and `Pkg.test()`: open `references/testjl.md`
- `@testitem` suites with TestItemRunner.jl: open `references/testitemrunner.md`
- File-per-test suites with ParallelTestRunner.jl: open `references/paralleltestrunner.md`

## Quick Commands

```bash
julia -tauto --project=. -e 'using Pkg; Pkg.test()'
julia -tauto --project=test -e 'using TestItemRunner; TestItemRunner.run_tests("test")'
julia --project test/runtests.jl --verbose --jobs=4
```

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
- Advanced ParallelTestRunner.jl setup:
  `references/parallel-advanced.md`

## Notes

- Keep doctest authoring and Documenter-specific setup under `julia-docs`.
- Keep JET-specific analysis workflow under `julia-jet`.
- Prefer one top-level testing skill and a few narrow reference files over many
  sibling skills.
