# ParallelTestRunner.jl

Use this reference when the suite is organized as independent test files run in
parallel worker processes.

## Quick Commands

```bash
julia --project test/runtests.jl
julia --project test/runtests.jl --verbose --jobs=4
julia --project test/runtests.jl integration core
julia --project test/runtests.jl --list
```

## `Pkg.test` Integration

```julia
using Pkg
Pkg.test("MyPackage"; test_args=`--verbose --jobs=4`)
Pkg.test("MyPackage"; test_args=`integration`)
```

## Minimal `runtests.jl`

```julia
using MyPackage
using ParallelTestRunner

runtests(MyPackage, ARGS)
```

## CLI Flags

- `--help`
- `--list`
- `--verbose`
- `--quickfail`
- `--jobs=N`
- positional test-name prefixes

## When To Open More

- For isolated file layout and migration from include-based tests:
  `references/parallel-files.md`
- For custom workers and init code:
  `references/parallel-advanced.md`

