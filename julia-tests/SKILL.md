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
julia -tauto --project=test -e 'using TestItemRunner; TestItemRunner.run_tests("test")'
julia --project test/runtests.jl --verbose --jobs=4
```

## Writing Tests

- Standard `@testset` organization and common support files:
  `references/standard-tests.md`
- Writing filter-friendly `@testitem`s:
  `references/testitem.md`
- Writing file-per-test suites for ParallelTestRunner.jl:
  `references/parallel-files.md`

## Common Structure

```text
test/
├── Project.toml
├── runtests.jl
├── test_core.jl
├── test_aqua.jl
├── test_jet.jl
└── test_doctests.jl
```

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

