---
name: julia-tests-write
description: Write tests for Julia packages using the standard library Test, including Aqua, JET, and doctests. Use this skill when adding or organizing tests.
---

# Writing Julia Tests

Write tests for Julia packages using the standard library `Test`, with support
for code quality checks and static analysis. If a repository already uses
`@testitem`, treat that as a separate setup (optional, not preferred) and see
`julia-retestitems-run` plus `julia-testitem-write`.

## Project Structure

```
MyPackage.jl/
├── test/
│   ├── Project.toml       # Created via Pkg
│   ├── runtests.jl        # Test runner with filtering
│   ├── test_core.jl       # Core functionality tests
│   ├── test_aqua.jl       # Code quality checks
│   └── test_jet.jl        # Static analysis
```

## Test Environment

```julia
using Pkg
Pkg.activate("test")
Pkg.add(["Test", "Aqua", "JET", "Documenter"])
Pkg.develop(path=pwd())
```

## Basic Test Set

```julia
using Test

@testset "Core functionality" begin
    using MyPackage

    @test myfunction(1) == expected_value
    @test_throws ArgumentError myfunction(-1)
end
```

## Additional Test Set

```julia
@testset "Advanced feature" begin
    using MyPackage

    @test advanced_function() works
end
```

## Standard Test Files

### Aqua Tests (test/test_aqua.jl)

```julia
using Test

@testset "Aqua" begin
    using Aqua
    using MyPackage

    Aqua.test_all(MyPackage;
        ambiguities=false,  # Optional: skip ambiguity checks
    )
end
```

### JET Tests (test/test_jet.jl)

```julia
using Test

@testset "JET" begin
    using JET
    using MyPackage

    rep = JET.report_package(MyPackage, target_modules=[MyPackage])
    @show rep # print detected issues
    @test length(JET.get_reports(rep)) <= 5 # nonzero, in case there are some unresolved issues
    @test_broken length(JET.get_reports(rep)) == 0 # broken test, in case there are some unresolved issues
end
```

## Reference

- **[Standard Tests](references/standard-tests.md)** - Aqua, JET, doctests templates

## Related Skills

- `julia-tests-run` - Running tests
- `julia-retestitems-run` - Optional `@testitem` runner patterns
- `julia-testitem-write` - Optional `@testitem` authoring patterns
- `julia-doctests` - Doctest configuration
- `julia-jet` - JET.jl analysis overview and configuration
