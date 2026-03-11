---
name: julia-tests-run
description: Run Julia tests with the standard library Test, including conditional loading and environment-based selection. Use this skill when running tests or configuring test infrastructure.
---

# Running Julia Tests

Run tests for Julia packages using the standard library `Test`, with optional
conditional loading and environment-based selection.
If a repository already uses `@testitem`, treat that as a separate setup and
use `julia-retestitems-run` (optional, not preferred).

## Quick Commands

```bash
# Standard test run
julia -tauto --project=. -e 'using Pkg; Pkg.test()'

# Run the test project directly
julia -tauto --project=test -e 'include("test/runtests.jl")'
```

## Test Project Setup

```julia
using Pkg
Pkg.activate("test")
Pkg.add(["Test", "Aqua", "JET", "Documenter"])
Pkg.develop(path=pwd())
```

## Test Runner with Conditional Loading

### test/runtests.jl

```julia
using MyPackage
using Test

# Only include optional tests when explicitly enabled
if get(ENV, "JET_TEST", "") == "true"
    include("test_jet.jl")
end
if get(ENV, "DOCTESTS", "") == "true"
    include("test_doctests.jl")
end

println("Starting tests with $(Threads.nthreads()) threads...")

include("test_core.jl")
include("test_aqua.jl")
```

## Reference

- **[Conditional Loading](references/conditional.md)** - Environment-based test selection

## Related Skills

- `julia-tests-write` - Writing tests
- `julia-retestitems-run` - Optional `@testitem` runner patterns
- `julia-testitem-write` - Optional `@testitem` authoring patterns
