---
name: julia-parallel-tests-write
description: Write tests for ParallelTestRunner.jl with file-per-test isolation, automatic discovery, and shared utilities. Use this skill when writing tests for packages that use ParallelTestRunner.jl.
---

# Writing Tests for ParallelTestRunner.jl

Write standard `Test.jl` tests organized as independent files. Each file runs
in an isolated module — no shared state between files.

## Project Structure

```
MyPackage.jl/
├── test/
│   ├── Project.toml         # Must include ParallelTestRunner
│   ├── runtests.jl          # Runner (see julia-parallel-tests-run)
│   ├── test_core.jl         # One file per test group
│   ├── test_utils.jl
│   ├── test_aqua.jl
│   ├── test_jet.jl
│   └── subdir/
│       └── test_feature.jl  # Subdirs are auto-discovered
```

## Test File Format

Each file is a standalone script using `Test.jl`:

```julia
# test/test_core.jl
using Test
using MyPackage

@testset "Core functionality" begin
    @test myfunction(1) == expected
    @test_throws ArgumentError myfunction(-1)
end
```

## Key Rules

1. **No `include` statements** — each file is discovered and run automatically
2. **Self-contained** — each file must import its own dependencies
3. **No shared state** — files run in isolated modules on separate workers
4. **File = test unit** — `runtests.jl` is excluded from discovery; all other
   `.jl` files in `test/` are included

## Migration from include-based Tests

Remove `include()` calls from `runtests.jl`. Each test file must add its own
`using` statements since it runs in an isolated module:

```julia
# Before (runtests.jl): include("test_core.jl")
# After (runtests.jl):
using MyPackage
using ParallelTestRunner
runtests(MyPackage, ARGS)

# test/test_core.jl must have:
using Test
using MyPackage
# ... tests ...
```

## Balancing Test Files

For optimal parallelism, split large test files into smaller ones of roughly
equal duration. The runner uses historical timing data to balance load.

## Related Skills

- `julia-parallel-tests-run` - Running tests with ParallelTestRunner.jl
- `julia-tests-write` - Standard Test.jl patterns
