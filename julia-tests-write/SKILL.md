---
name: julia-tests-write
description: Write tests for Julia packages using TestItemRunner.jl patterns including Aqua, JET, and doctests. Use this skill when adding or organizing tests.
---

# Writing Julia Tests

Write tests for Julia packages using TestItemRunner.jl with support for
tagging, code quality checks, and static analysis.

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
Pkg.add(["Test", "TestItemRunner", "Aqua", "JET"])
Pkg.develop(path=pwd())
```

## Basic Test Item

```julia
@testitem "Core functionality" begin
    using MyPackage

    @test myfunction(1) == expected_value
    @test_throws ArgumentError myfunction(-1)
end
```

## Tagged Test Item

```julia
@testitem "Advanced feature" tags=[:advanced] begin
    using MyPackage

    @test advanced_function() works
end
```

## Common Tags

| Tag | Purpose |
|-----|---------|
| `:jet` | JET static analysis |
| `:aqua` | Aqua code quality |
| `:doctests` | Documentation tests |
| `:cuda` | CUDA GPU tests |
| `:plotting` | Visualization tests |
| `:core` | Core functionality |

## Standard Test Files

### Aqua Tests (test/test_aqua.jl)

```julia
@testitem "Aqua" tags=[:aqua] begin
    using Aqua
    using MyPackage

    Aqua.test_all(MyPackage;
        ambiguities=false,  # Optional: skip ambiguity checks
    )
end
```

### JET Tests (test/test_jet.jl)

```julia
@testitem "JET" tags=[:jet] begin
    using JET
    using Test
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
- `julia-doctests` - Doctest configuration
