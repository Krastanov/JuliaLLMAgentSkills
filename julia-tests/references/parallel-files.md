# Writing Tests for ParallelTestRunner.jl

Each discovered test file runs in an isolated module. Design files as
independent units.

## Structure

```text
test/
├── Project.toml
├── runtests.jl
├── test_core.jl
├── test_utils.jl
└── subdir/test_feature.jl
```

## Rules

1. Do not use `include()` to build the suite.
2. Every test file must import its own dependencies.
3. Do not rely on shared mutable state across files.
4. Split very large test files into smaller files for better worker balance.

## Minimal File

```julia
using Test
using MyPackage

@testset "Core functionality" begin
    @test myfunction(1) == expected
    @test_throws ArgumentError myfunction(-1)
end
```

