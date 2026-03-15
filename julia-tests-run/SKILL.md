---
name: julia-tests-run
description: Run Julia tests using the standard Test.jl library. Use this skill when running tests or configuring test infrastructure with Pkg.test and @testset.
---

# Running Julia Tests (Test.jl)

Run tests using the standard library `Test.jl`.
For TestItemRunner.jl, see `julia-testitem-run`.
For ParallelTestRunner.jl, see `julia-parallel-tests-run`.

## Quick Commands

```bash
# Standard test run
julia --project=. -e 'using Pkg; Pkg.test()'

# With multiple threads
julia -tauto --project=. -e 'using Pkg; Pkg.test()'

# Pass test arguments (Julia 1.9+)
julia --project=. -e 'using Pkg; Pkg.test(test_args=`integration`)'
```

## test/runtests.jl Structure

```julia
using MyPackage
using Test

@testset "MyPackage" begin
    include("test_core.jl")
    include("test_utils.jl")
end
```

## Conditional Test Loading

```julia
using MyPackage
using Test

@testset "MyPackage" begin
    include("test_core.jl")

    if get(ENV, "JET_TEST", "") == "true"
        include("test_jet.jl")
    end
    if VERSION >= v"1.10"
        include("test_aqua.jl")
        include("test_doctests.jl")
    end
    if !Sys.iswindows()
        include("test_unix.jl")
    end
end
```

## Test Project Setup

```julia
using Pkg
Pkg.activate("test")
Pkg.add(["Test", "Aqua", "Documenter"])
Pkg.develop(path=pwd())
```

## Reference

- **[Conditional Loading](references/conditional.md)** - Environment-based test selection

## Related Skills

- `julia-tests-write` - Writing tests with Test.jl
- `julia-testitem-run` - Running tests with TestItemRunner.jl
- `julia-parallel-tests-run` - Running tests with ParallelTestRunner.jl
