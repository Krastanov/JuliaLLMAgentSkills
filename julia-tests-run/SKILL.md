---
name: julia-tests-run
description: Run Julia tests with filtering, conditional loading, and environment-based selection. Use this skill when running tests or configuring test infrastructure.
---

# Running Julia Tests

Run tests for Julia packages with support for filtering, conditional loading,
and environment-based test selection using TestItemRunner.jl.

## Quick Commands

```bash
# Standard test run
julia --project=. -e 'using Pkg; Pkg.test()'

# With threads (recommended)
julia -tauto --project=. -e 'using Pkg; Pkg.test()'

# Run specific test categories
JET_TEST=true julia --project=. -e 'using Pkg; Pkg.test()'
GPU_TEST=cuda julia --project=. -e 'using Pkg; Pkg.test()'
```

## Test Project Setup

### test/Project.toml

```toml
[deps]
Aqua = "4c88cf16-eb10-579e-8560-4a9242c79595"
Documenter = "e30172f5-a6a5-5a46-863b-614d45cd2de4"
JET = "c3a54625-cd67-489e-a8e7-0a5a0ff4e31b"
MyPackage = "your-package-uuid"
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

## Common Tags

| Tag | Purpose |
|-----|---------|
| `:jet` | JET static analysis |
| `:aqua` | Aqua code quality |
| `:doctests` | Documentation tests |
| `:cuda` | CUDA GPU tests |
| `:plotting` | Visualization tests |

## Reference

- **[Conditional Loading](references/conditional.md)** - Environment-based test selection
- **[CI Integration](references/ci.md)** - Running tests in CI pipelines

## Related Skills

- `julia-tests-write` - Writing tests
- `julia-ci-github` - GitHub Actions CI
- `julia-ci-buildkite` - Buildkite CI
