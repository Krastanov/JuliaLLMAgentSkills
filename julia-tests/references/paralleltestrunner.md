# ParallelTestRunner.jl

Use this reference when the suite is organized as independent test files run in
parallel worker processes.

## Default Rule

- Prefer `Pkg.test("MyPackage"; test_args=...)` over direct
  `julia --project test/runtests.jl ...` invocations.
- Use direct `runtests.jl` execution mainly when debugging the runner itself,
  worker init code, or CLI parsing.
- If workers fail unexpectedly, inspect `Manifest.toml` files in the package
  root, `test/`, and test subprojects. Stale manifests often show up as
  worker-only failures.

## Preferred Commands

```julia
using Pkg
Pkg.test("MyPackage"; test_args=`--verbose --jobs=4`)
Pkg.test("MyPackage"; test_args=`integration`)
```

## Direct Runner Debugging

```bash
julia --project test/runtests.jl
julia --project test/runtests.jl --verbose --jobs=4
julia --project test/runtests.jl integration core
julia --project test/runtests.jl --list
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
