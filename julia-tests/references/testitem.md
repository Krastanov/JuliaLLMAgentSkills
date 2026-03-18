# Writing `@testitem` Tests

Use this reference when designing tests for TestItemRunner.jl workflows.

## Required Practices

1. Use stable, descriptive names.
2. Use a small, consistent tag set.
3. Make each test item self-contained.
4. Group related items into coherent files.

## Basic Pattern

```julia
@testitem "fft real input" tags=[:core, :fft] begin
    using MyPackage
    @test myfft([1.0, 0.0]) == [1.0, 1.0]
end
```

## Standard Tags

- `:core`
- `:slow`
- `:jet`
- `:aqua`
- `:doctests`
- `:feature_name`

## Notes

- Include explicit imports even though `@testitem` can auto-import some names.
- Put JET, Aqua, and doctest checks in their own tagged items so they remain easy
  to filter in CI and local runs.

