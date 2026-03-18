# Test.jl and `Pkg.test`

Use this reference for the default Julia test workflow with `Test.jl`.

## Quick Commands

```bash
julia --project=. -e 'using Pkg; Pkg.test()'
julia -tauto --project=. -e 'using Pkg; Pkg.test()'
julia --project=. -e 'using Pkg; Pkg.test(test_args=`integration`)'
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

