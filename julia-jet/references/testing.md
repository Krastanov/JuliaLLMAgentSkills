# Testing with JET

## Preferred Invocation

For package-integrated JET tests, prefer
`Pkg.test("MyPackage"; test_args=["jet"])`. That route lets Pkg build the test
environment before the JET file runs and avoids many stale-manifest problems.

Set `JULIA_PKG_SERVER_REGISTRY_PREFERENCE=eager` or
`ENV["JULIA_PKG_SERVER_REGISTRY_PREFERENCE"] = "eager"` before `Pkg`
operations in this workspace.

If JET behaves differently across machines or only in CI, do not inspect
`Manifest.toml` directly. Run `Pkg.update()` and `Pkg.resolve()` in the
relevant package and JET environments first. If recurrent issues remain,
delete the relevant `Manifest.toml` file and regenerate it with
`Pkg.instantiate()` before treating it as a real JET regression.

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
nightly/pre-release Julia versions. If JET should not live in the main test
environment, prefer a dedicated test subproject that is activated from
`test/runtests.jl`, and invoke that route through `Pkg.test(...; test_args=["jet"])`:

```julia
if ARGS == ["jet"]
    using Pkg
    Pkg.activate(joinpath(@__DIR__, "projects", "jet"))
    Pkg.instantiate()
    include("test_jet.jl")
else
    include("test_main.jl")
end
```

### Key Points

1. **Prefer `Pkg.test(...; test_args=["jet"])`** — let Pkg manage the test env first
2. **Use a dedicated JET subproject when needed** — avoid mutating the active test env ad hoc
3. **Run only JET tests on the JET route** — avoid mixing the full suite with JET
4. **Do not inspect manifests directly** — run `Pkg.update()` and
   `Pkg.resolve()` first, then delete and regenerate the relevant manifest if
   recurrent environment issues remain
