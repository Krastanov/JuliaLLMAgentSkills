# Test.jl and `Pkg.test`

Use this reference for the default Julia test workflow with `Test.jl`.

Prefer `Pkg.test(...)` even when working inside the package checkout. It should
be the default package-validation path, and it is much less sensitive to stale
environment state than running `test/runtests.jl` directly.

Set the eager registry preference before `Pkg` operations in this workspace:
`JULIA_PKG_SERVER_REGISTRY_PREFERENCE=eager` in the shell or
`ENV["JULIA_PKG_SERVER_REGISTRY_PREFERENCE"] = "eager"` in Julia.

If resolution or loading looks wrong, do not inspect `Manifest.toml`
directly. Run `Pkg.update()` and `Pkg.resolve()` in the relevant environment
first. If recurrent issues remain, delete the relevant `Manifest.toml` file and
regenerate it with `Pkg.instantiate()`.

## Quick Commands

```bash
julia --project=. -e 'using Pkg; Pkg.test()'
julia -tauto --project=. -e 'using Pkg; Pkg.test()'
julia --project=. -e 'using Pkg; Pkg.test(; test_args=["integration"])'
```

## Minimal `runtests.jl`

```julia
using MyPackage
using Test

@testset "MyPackage" begin
    include("test_core.jl")
    include("test_utils.jl")
end
```

## Test Project Setup

```julia
using Pkg
Pkg.activate("test")
Pkg.add(["Test", "Aqua", "Documenter"])
Pkg.develop(path=pwd())
```

## When To Open More

- For conditional includes and environment-based setup:
  `references/conditional.md`
- For Aqua, JET, doctests, and shared test helpers:
  `references/standard-tests.md`
