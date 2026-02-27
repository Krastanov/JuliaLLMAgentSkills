# Testing with JET

## Package-Level Test Pattern

Use `report_package` in a `@testitem` with `:jet` tag. Use a threshold test
with `@test_broken` for the aspirational zero-report goal:

```julia
# test/test_jet.jl
@testitem "JET checks" tags=[:jet] begin
    using JET
    using Test
    using MyPackage

    rep = JET.report_package(MyPackage; target_modules=[MyPackage])
    @show rep
    @test length(JET.get_reports(rep)) <= 5
    @test_broken length(JET.get_reports(rep)) == 0
end
```

**Pattern explained:**

- `target_modules=[MyPackage]` — filters out noise from dependencies
- `@show rep` — prints all detected issues so CI logs show what's wrong
- `@test length(...) <= N` — enforces a ceiling that ratchets down over time
- `@test_broken length(...) == 0` — documents the goal without failing CI

When you fix issues, lower the threshold. When you hit zero, replace both
lines with `@test length(JET.get_reports(rep)) == 0`.

## Multi-Module Packages

If your package re-exports or tightly couples with another module, include
both in `target_modules`:

```julia
@testitem "JET checks" tags=[:jet] begin
    using JET
    using Test
    using MyPackage
    using MyPackageCore

    rep = JET.report_package(MyPackage;
        target_modules=[MyPackage, MyPackageCore])
    @show rep
    @test length(JET.get_reports(rep)) <= 5
    @test_broken length(JET.get_reports(rep)) == 0
end
```

## Single-Call Tests

Use `@test_call` and `@test_opt` for targeted assertions in unit tests:

```julia
@testitem "Critical path is type-stable" tags=[:jet] begin
    using JET
    using MyPackage

    @test_call target_modules=(MyPackage,) critical_function(1, 2.0)
    @test_opt target_modules=(MyPackage,) critical_function(1, 2.0)
end
```

`@test_call` and `@test_opt` support `broken=true` and `skip=true`:

```julia
@test_call broken=true my_function(args...)  # known issue, don't fail CI
@test_opt skip=true my_function(args...)     # skip entirely
```

## Workload-Based Analysis

For more precise analysis than `report_package`, write a function that
exercises your package with concrete types:

```julia
function exercise_mypkg()
    data = MyPkg.load_data("test.csv")
    result = MyPkg.process(data)
    MyPkg.save(result, tempname())
end

@test_call target_modules=(MyPkg,) exercise_mypkg()
```

This gives JET concrete types to work with, producing fewer false positives
than the generic signatures that `report_package` infers.

## CI Considerations

- Tag JET tests with `:jet` and control them via environment variable
  (e.g. `JET_TEST`) so they can be skipped on platforms where they're slow
- JET analysis can be slow on large packages — consider running only on
  the main branch or in a separate CI job
- JET results depend on the Julia version — pin to a specific stable release
