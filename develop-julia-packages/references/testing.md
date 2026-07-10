# Testing Julia Packages

Use `Test` for assertions. Choose one runner from repository evidence, with ParallelTestRunner as the default for a file-split suite.

## Select the Runner

1. **ParallelTestRunner.jl**: prefer for package suites split across independent `.jl` files. It discovers files, evaluates each in a fresh sandbox module on a pool of worker processes, and accepts file filters.
2. **TestItemRunner.jl**: preserve when the repository already defines `@testitem` blocks. Do not migrate a functioning test-item suite solely for uniformity.
3. **Sequential Test.jl**: keep for a tiny suite or behavior that intentionally requires one process and explicit ordering.

Do not combine runners without a demonstrated need.

Preserve another established runner unless migration is requested or required for the change. For a new file-oriented suite, choose ParallelTestRunner; do not introduce TestItemRunner unless `@testitem` is already part of the repository.

## Configure ParallelTestRunner

Declare `ParallelTestRunner` in the supported test environment. A minimal `test/runtests.jl` is:

```julia
using PackageName
using ParallelTestRunner

runtests(PackageName, ARGS)
```

Run through Pkg:

```julia
using Pkg
Pkg.test()
```

Pass runner arguments without editing tests:

```julia
Pkg.test(; test_args=`--verbose --jobs=4 parser`)
```

Useful direct commands include `julia --project test/runtests.jl --list` and `julia --project test/runtests.jl parser` when that invocation matches the repository's environment layout.

ParallelTestRunner discovers every `.jl` file recursively under `test/` except `runtests.jl`. It evaluates each test file in a temporary module on a worker, and a worker process may be reused for later files. Therefore:

- import `Test`, the package, and directly used dependencies in each file, or supply intentional `init_code`;
- do not rely on another test file having run;
- do not share mutable globals, ports, paths, random streams, or process state between files; module isolation does not reset process-wide state;
- do not place `TestUtils.jl` under automatic discovery and assume it is ignored; use package helpers, intentional `init_code`, or an explicitly filtered test suite;
- keep each file safe to run alone.

Use `--jobs=1` only to diagnose order or resource contention, not to hide isolation defects.

## Write Stable Tests

- Test public behavior and important invariants rather than implementation trivia.
- Use `@test_throws` for expected failures, `@test_logs` for Julia log records, and `isapprox` with justified tolerances for floating-point results.
- Use `mktempdir` for filesystem fixtures and close files, sockets, tasks, and channels.
- Use explicit local RNG objects. Add StableRNGs only when the stream must remain identical across Julia releases; a seeded Julia RNG is often enough within a supported release.
- Give concurrent tests unique resources and bounded waits.
- Keep slow/network/external-service tests opt-in according to existing runner arguments or CI jobs.

Do not mutate the active test environment. In particular, never call `Pkg.add`, `Pkg.develop`, `Pkg.instantiate`, or registry operations from tests. Declare dependencies before the run.

## Keep Test Doubles Simple

Prefer, in order:

1. a pure helper tested directly;
2. an injected callable, IO, path, clock value, or small interface;
3. `IOBuffer`, `mktempdir`, a local server, or a lightweight fake type;
4. a real small dependency in an isolated fixture.

Avoid mocking frameworks, global method replacement, and changes to another package's methods. A test seam should improve the production design, not reproduce Julia dispatch at runtime.

## Preserve Existing Test Items

When `@testitem` is already present, keep the existing `TestItemRunner` entry point and tags. Each item should import what it uses and avoid global state. Do not invent universal tag names; follow repository policy.

## Sources

- [ParallelTestRunner quick start and CLI](https://juliatesting.github.io/ParallelTestRunner.jl/stable/)
- [ParallelTestRunner API and isolation model](https://juliatesting.github.io/ParallelTestRunner.jl/stable/api/)
- [ParallelTestRunner advanced setup](https://juliatesting.github.io/ParallelTestRunner.jl/stable/advanced/)
- [Julia Test standard library](https://docs.julialang.org/en/v1/stdlib/Test/)
- [Pkg package testing and test dependencies](https://pkgdocs.julialang.org/v1/creating-packages/#Adding-tests-to-the-package)
- [TestItems/TestItemRunner guide](https://www.julia-vscode.org/docs/stable/userguide/testitems/)
