---
name: julia-tests
description: Set up and organize tests for Julia packages using TestItemRunner.jl with conditional loading and tagging. Use this skill when configuring test infrastructure.
---

# Julia Tests

Set up and organize tests for Julia packages using TestItemRunner.jl with support for
conditional loading, tagging, and environment-based test selection.

## Project Structure

```
MyPackage.jl/
├── test/
│   ├── Project.toml       # Test dependencies
│   ├── runtests.jl        # Test runner with filtering
│   ├── test_core.jl       # Core functionality tests
│   ├── test_aqua.jl       # Code quality checks
│   └── test_jet.jl        # Static analysis
```

## Test Dependencies

### test/Project.toml

```toml
[deps]
Aqua = "4c88cf16-eb10-579e-8560-4a9242c79595"
Documenter = "e30172f5-a6a5-5a46-863b-614d45cd2de4"
JET = "c3a54625-cd67-489e-a8e7-0a5a0ff4e31b"
Test = "8dfed614-e22c-5e08-85e1-65c5234f0b40"
TestItemRunner = "f8b46487-2199-4994-9208-9a1283c18c0a"
```

## Test Runner with Filtering

### test/runtests.jl

```julia
using MyPackage
using TestItemRunner

testfilter = ti -> begin
    exclude = Symbol[]
    if get(ENV, "JET_TEST", "") != "true"
        push!(exclude, :jet)
    end
    if !(VERSION >= v"1.10")
        push!(exclude, :doctests)
        push!(exclude, :aqua)
    end
    return all(!in(exclude), ti.tags)
end

println("Starting tests with $(Threads.nthreads()) threads...")

@run_package_tests filter=testfilter
```

## Test Item Pattern

### Basic Test Item

```julia
@testitem "Core functionality" begin
    using MyPackage

    @test myfunction(1) == expected_value
end
```

### Tagged Test Item

```julia
@testitem "Advanced feature" tags=[:advanced] begin
    using MyPackage

    @test advanced_function() works
end
```

## Common Tags

| Tag | Purpose |
|-----|---------|
| `:jet` | JET static analysis |
| `:aqua` | Aqua code quality |
| `:doctests` | Documentation tests |
| `:cuda` | CUDA GPU tests |
| `:plotting` | Visualization tests |

## Running Tests

```bash
julia --project=. -e 'using Pkg; Pkg.test()'           # All tests
julia -tauto --project=. -e 'using Pkg; Pkg.test()'    # With threads
JET_TEST=true julia --project=. -e 'using Pkg; Pkg.test()'  # JET only
```

## Reference

- **[Standard Tests](references/standard-tests.md)** - Aqua, JET, doctests setup
- **[Conditional Loading](references/conditional.md)** - Environment-based test selection
- **[Additional Tools](references/tools.md)** - ReferenceTests, LocalCoverage

## Related Skills

- `julia-doctests` - Doctest configuration
- `julia-ci-github` - CI configuration
