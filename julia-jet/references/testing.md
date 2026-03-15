# Testing with JET

## Package-Level Test Pattern

Use `report_package` in a `@testset` with a threshold test
and `@test_broken` for the aspirational zero-report goal:

```julia
# test/test_jet.jl
using JET
using Test
using MyPackage

@testset "JET checks" begin
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
@testset "JET checks" begin
    using JET, Test, MyPackage, MyPackageCore
    rep = JET.report_package(MyPackage;
        target_modules=[MyPackage, MyPackageCore])
    @show rep
    @test length(JET.get_reports(rep)) <= 5
    @test_broken length(JET.get_reports(rep)) == 0
end
```

## Single-Call Tests

Use `@test_call` and `@test_opt` for targeted assertions:

```julia
using JET, MyPackage

@testset "Critical path is type-stable" begin
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

## CI Considerations

- Control JET tests via environment variable (e.g. `JET_TEST=true`) and
  conditionally include them in runtests.jl
- JET analysis can be slow — consider running only on main or in a separate CI job
- JET results depend on Julia version — pin to a specific stable release

## Conditional JET Loading (Required Pattern)

**IMPORTANT**: JET depends on Julia compiler internals and frequently breaks on
nightly/pre-release Julia versions. **Never add JET to `test/Project.toml`
directly.** Instead, add it conditionally in `test/runtests.jl`:

```julia
if get(ENV, "JET_TEST", "") == "true"
    using Pkg
    Pkg.add("JET")
    include("test_jet.jl")
else
    @info "Skipping JET tests -- must be explicitly enabled."
end
```

### Key Points

1. **Do NOT list JET in `test/Project.toml`** — causes resolution failures on Julia nightly
2. **Use `Pkg.add("JET")` conditionally** — only when `JET_TEST=true`
3. **When `JET_TEST` is true, run ONLY JET tests** — avoid running the full suite alongside JET
