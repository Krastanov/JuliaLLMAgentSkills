---
name: julia-tests-write
description: Write tests for Julia packages using the standard Test.jl library including @testset, Aqua, JET, and doctests. Use this skill when adding or organizing tests.
---

# Writing Julia Tests (Test.jl)

Write tests using `@testset` and `@test` from the standard `Test` library.
For TestItemRunner.jl patterns, see `julia-testitem-write`.

## Project Structure

```
MyPackage.jl/
├── test/
│   ├── Project.toml       # Created via Pkg
│   ├── runtests.jl        # Test runner with includes
│   ├── test_core.jl       # Core functionality tests
│   ├── test_aqua.jl       # Code quality checks
│   └── test_jet.jl        # Static analysis
```

## Basic Tests

```julia
# test/test_core.jl
using Test
using MyPackage

@testset "Core functionality" begin
    @test myfunction(1) == expected_value
    @test_throws ArgumentError myfunction(-1)
end
```

## Key Test Macros

| Macro | Purpose |
|-------|---------|
| `@test expr` | Assert expression is true |
| `@test_throws E expr` | Assert expression throws E |
| `@test_broken expr` | Known failure (passes = error) |
| `@test_skip expr` | Skip this test |
| `@test_warn r"pattern" expr` | Assert warning is emitted |
| `@test_logs (:warn,) expr` | Assert log messages |
| `@testset "name" begin ... end` | Group tests |
| `@testset for x in vals ... end` | Parameterized tests |
| `@inferred f(x)` | Assert return type is inferred |

## Nested Test Sets

```julia
@testset "MyPackage" begin
    @testset "Feature A" begin
        @test feature_a(1) == 2
    end
    @testset "Feature B" begin
        @test feature_b("x") == "xx"
    end
end
```

## Standard Test Files

### Aqua (test/test_aqua.jl)

```julia
using Aqua
using MyPackage

@testset "Aqua" begin
    Aqua.test_all(MyPackage; ambiguities=false)
end
```

### JET (test/test_jet.jl)

```julia
using JET
using Test
using MyPackage

@testset "JET" begin
    rep = JET.report_package(MyPackage; target_modules=[MyPackage])
    @show rep
    @test length(JET.get_reports(rep)) <= 5
    @test_broken length(JET.get_reports(rep)) == 0
end
```

### Doctests (test/test_doctests.jl)

```julia
using Documenter
using MyPackage

@testset "Doctests" begin
    DocMeta.setdocmeta!(MyPackage, :DocTestSetup, :(using MyPackage); recursive=true)
    doctest(MyPackage; manual=false)
end
```

## Reference

- **[Standard Tests](references/standard-tests.md)** - Aqua, JET, doctests, extensions templates

## Related Skills

- `julia-tests-run` - Running tests with Pkg.test
- `julia-testitem-write` - Writing tests with TestItemRunner.jl
- `julia-doctests` - Doctest configuration
- `julia-jet` - JET.jl analysis overview
