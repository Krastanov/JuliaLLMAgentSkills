---
name: julia-testitem-write
description: Write Julia @testitem tests that are easy to run from the command line and easy to filter by tags, names, and files. Use when adding or refactoring test items for TestItemRunner.jl workflows.
---

# Writing `@testitem` Tests

Write `@testitem`s for predictable subset runs in CI and agent workflows.

## Required Practices

1. Stable, descriptive names (no timestamps or random IDs).
2. Small, consistent tag taxonomy (`:core`, `:integration`, `:slow`, `:feature_name`).
3. Self-contained items — never depend on execution order.
4. Group related items in coherent files for filename filtering.

## Basic Pattern

```julia
@testitem "fft real input" tags=[:core, :fft] begin
    using MyPackage
    @test myfft([1.0, 0.0]) == [1.0, 1.0]
end

@testitem "fft large random" tags=[:slow, :fft] begin
    using MyPackage
    x = randn(1_000_000)
    @test length(myfft(x)) == length(x)
end
```

## Nesting `@testset` Inside `@testitem`

```julia
@testitem "Matrix operations" tags=[:core] begin
    using MyPackage
    @testset "addition" begin
        @test mat_add(A, B) == expected
    end
    @testset "multiplication" begin
        @test mat_mul(A, B) == expected
    end
end
```

## Default Imports

`@testitem` auto-imports `Test` and your package by default.
Always include explicit imports anyway — it helps when running interactively.

## Common Tags

| Tag | Purpose |
|-----|---------|
| `:jet` | JET static analysis |
| `:aqua` | Aqua code quality |
| `:doctests` | Documentation tests |
| `:cuda` | CUDA GPU tests |
| `:core` | Core functionality |
| `:slow` | Long-running tests |

## Standard Test Items

### Aqua

```julia
@testitem "Aqua" tags=[:aqua] begin
    using Aqua
    using MyPackage
    Aqua.test_all(MyPackage; ambiguities=false)
end
```

### JET

```julia
@testitem "JET" tags=[:jet] begin
    using JET, Test, MyPackage
    rep = JET.report_package(MyPackage; target_modules=[MyPackage])
    @show rep
    @test length(JET.get_reports(rep)) <= 5
    @test_broken length(JET.get_reports(rep)) == 0
end
```

### Doctests

```julia
@testitem "Doctests" tags=[:doctests] begin
    using Documenter, MyPackage
    DocMeta.setdocmeta!(MyPackage, :DocTestSetup, :(using MyPackage); recursive=true)
    doctest(MyPackage; manual=false)
end
```

## Related Skills

- `julia-testitem-run` - CLI execution and filtering patterns
- `julia-tests-write` - Standard Test.jl patterns
