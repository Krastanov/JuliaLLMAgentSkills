---
name: julia-testitem-write
description: Write Julia @testitem tests that are easy to run from the command line and easy to filter by tags, names, and files. Use when adding or refactoring test items for TestItemRunner.jl workflows.
---

# Writing Filter-Friendly `@testitem` Tests

Write `@testitem`s so subset runs are predictable in CI and agent workflows.

## Required Practices

1. Give each test item a stable, descriptive name (no timestamps or random IDs).
2. Use a small, consistent tag taxonomy (e.g. `:core`, `:integration`, `:slow`, `:some_feature`).
3. Keep each test item self-contained; never depend on execution order.
4. Group related test items in coherent files so filename filtering is useful.

`@testset` can be nested inside of a `@testitem`

## Example Pattern

```julia
@testitem "fft real input" tags=[:core, :fft] begin
    using MyPackage
    @test myfft([1.0, 0.0]) == [1.0, 1.0]
end

@testitem "fft large random input" tags=[:slow, :fft] begin
    using MyPackage
    x = randn(1_000_000)
    @test length(myfft(x)) == length(x)
end
```

## Default Imports

`@testitem` includes `using Test` and `using YourPackage` by default.
If you set `default_imports=false`, add imports manually inside the block.
Either way, you should always include the imports anyway, no matter the default,
to help human users when they interactively work with the tests.

## Related Skills

- `julia-testitem-run` - CLI execution and filtering patterns
- `julia-tests-write` - Broader Julia test templates
- `julia-tests-run` - General runner setup
