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
├── Project.toml
├── test/
│   ├── Project.toml       # Test dependencies
│   ├── runtests.jl        # Test runner with filtering
│   ├── test_core.jl       # Core functionality tests
│   ├── test_advanced.jl   # Advanced feature tests
│   ├── test_doctests.jl   # Doctest runner
│   ├── test_aqua.jl       # Code quality checks
│   └── test_jet.jl        # Static analysis
└── src/
    └── MyPackage.jl
```

## Test Dependencies

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

# Filter tests based on environment variables and system capabilities
testfilter = ti -> begin
    exclude = Symbol[]

    # JET tests only when explicitly enabled
    if get(ENV, "JET_TEST", "") != "true"
        push!(exclude, :jet)
    end

    # Version-gated tests
    if !(VERSION >= v"1.10")
        push!(exclude, :doctests)
        push!(exclude, :aqua)
    end

    return all(!in(exclude), ti.tags)
end

println("Starting tests with $(Threads.nthreads()) threads out of `Sys.CPU_THREADS = $(Sys.CPU_THREADS)`...")

@run_package_tests filter=testfilter
```

## Conditional Dependency Loading

### Based on Environment Variables

```julia
# test/runtests.jl
using Pkg

# Install optional test dependencies based on ENV
if get(ENV, "PLOT_TEST", "") == "true"
    Pkg.add(["GLMakie", "CairoMakie"])
end

if get(ENV, "JET_TEST", "") == "true"
    Pkg.add("JET")
end

if get(ENV, "GPU_TEST", "") == "cuda"
    Pkg.add("CUDA")
elseif get(ENV, "GPU_TEST", "") == "rocm"
    Pkg.add("AMDGPU")
elseif get(ENV, "GPU_TEST", "") == "opencl"
    Pkg.add(["pocl_jll", "OpenCL"])
end

# Load common GPU dependencies
if get(ENV, "GPU_TEST", "") in ["cuda", "rocm", "opencl"]
    Pkg.add(["Adapt", "GPUArraysCore", "GPUArrays", "KernelAbstractions"])
end
```

### Based on System Checks

```julia
# test/runtests.jl
using InteractiveUtils
versioninfo(; verbose=true)

# Platform-specific flags
Oscar_flag = false
GPU_flag = false

# Oscar only supported on x86_64 *NIX
if Sys.iswindows() || Sys.ARCH != :x86_64
    @info "Skipping Oscar tests -- only supported on x86_64 *NIX platforms."
else
    Oscar_flag = VERSION >= v"1.11"
    !Oscar_flag && @info "Skipping Oscar tests -- not tested on Julia < 1.11"
end

# GPU tests only on *NIX
if Sys.iswindows()
    @info "Skipping GPU tests -- only executed on *NIX platforms."
else
    GPU_flag = get(ENV, "GPU_TEST", "") != ""
end

# Conditionally install packages
using Pkg
Oscar_flag && Pkg.add("Oscar")
GPU_flag && Pkg.add("CUDA")
```

### Combined Filter Function

```julia
testfilter = ti -> begin
    exclude = Symbol[]

    # JET-only mode
    if get(ENV, "JET_TEST", "") == "true"
        return :jet in ti.tags
    else
        push!(exclude, :jet)
    end

    # Platform exclusions
    if !Oscar_flag
        push!(exclude, :oscar_required)
    end

    if !GPU_flag
        push!(exclude, :cuda)
        push!(exclude, :gpu)
    end

    # Version exclusions
    if !(VERSION >= v"1.10")
        push!(exclude, :doctests)
        push!(exclude, :aqua)
    end

    # Architecture exclusions
    if !(Base.Sys.islinux() && Int === Int64)
        push!(exclude, :bitpack)
    end

    return all(!in(exclude), ti.tags)
end
```

## Test Item Pattern

### Basic Test Item

```julia
# test/test_core.jl
@testitem "Core functionality" begin
    using MyPackage

    @test myfunction(1) == expected_value
    @test myfunction(2) == other_value
end
```

### Tagged Test Item

```julia
# test/test_advanced.jl
@testitem "Advanced feature" tags=[:advanced] begin
    using MyPackage

    @test advanced_function() works
end
```

### Platform-Specific Tests

```julia
# test/test_gpu.jl
@testitem "CUDA tests" tags=[:cuda, :gpu] begin
    using CUDA
    using MyPackage

    @test cuda_function() works
end

@testitem "Oscar tests" tags=[:oscar_required] begin
    using Oscar
    using MyPackage

    @test oscar_function() works
end
```

## Standard Test Files

### test/test_aqua.jl

```julia
@testitem "Aqua" tags=[:aqua] begin
    using Aqua
    using MyPackage

    Aqua.test_all(MyPackage;
        ambiguities=false,  # Optional: skip ambiguity checks
    )
end
```

### test/test_jet.jl

```julia
@testitem "JET" tags=[:jet] begin
    using JET
    using MyPackage

    @test_opt target_modules=[MyPackage] myfunction(1)
    @test_call target_modules=[MyPackage] myfunction(1)
end
```

### test/test_doctests.jl

```julia
@testitem "Doctests" tags=[:doctests] begin
    using Documenter
    using MyPackage

    # Load extensions if needed
    import SomeDep
    const MyPackageExt = Base.get_extension(MyPackage, :MyPackageSomeDepExt)

    # Set display size for consistent output
    ENV["LINES"] = 80
    ENV["COLUMNS"] = 80

    DocMeta.setdocmeta!(MyPackage, :DocTestSetup, :(using MyPackage); recursive=true)

    modules = [MyPackage, MyPackageExt]
    doctest(nothing, modules)
end
```

See the `julia-doctests` skill for more details.

## Test Categories Pattern

For large test suites, split into categories:

```julia
# test/runtests.jl
testfilter = ti -> begin
    exclude = Symbol[]

    # Category-based test selection
    if get(ENV, "TEST_CATEGORY", "") == "base"
        return (:core in ti.tags) && all(!in(exclude), ti.tags)
    elseif get(ENV, "TEST_CATEGORY", "") == "encoding"
        return (:encoding in ti.tags) && all(!in(exclude), ti.tags)
    elseif get(ENV, "TEST_CATEGORY", "") == "decoding"
        return (:decoding in ti.tags) && all(!in(exclude), ti.tags)
    else
        # Default: exclude category tests, run everything else
        push!(exclude, :core)
        push!(exclude, :encoding)
        push!(exclude, :decoding)
    end

    return all(!in(exclude), ti.tags)
end
```

## Running Tests

```bash
# Run all tests
julia --project=. -e 'using Pkg; Pkg.test()'

# With threads (faster)
julia -tauto --project=. -e 'using Pkg; Pkg.test()'

# Run JET tests only
JET_TEST=true julia --project=. -e 'using Pkg; Pkg.test()'

# Run specific category
TEST_CATEGORY=encoding julia --project=. -e 'using Pkg; Pkg.test()'

# Run plotting tests
PLOT_TEST=true julia --project=. -e 'using Pkg; Pkg.test()'

# Run GPU tests
GPU_TEST=cuda julia --project=. -e 'using Pkg; Pkg.test()'
```

## Common Tags

| Tag | Purpose |
|-----|---------|
| `:jet` | JET static analysis |
| `:aqua` | Aqua code quality |
| `:doctests` | Documentation tests |
| `:cuda` | CUDA GPU tests |
| `:rocm` | ROCm GPU tests |
| `:opencl` | OpenCL tests |
| `:plotting` | Visualization tests |
| `:examples` | Example code tests |
| `:oscar_required` | Requires Oscar.jl |

## Best Practices

1. **Use TestItemRunner** for modern, organized tests
2. **Tag all tests** for selective running
3. **Conditionally install** heavy dependencies
4. **Check platform/version** before loading platform-specific code
5. **Print thread info** at test start for debugging
6. **Keep JET tests separate** - they're slow and need explicit enabling
7. **Use `@static if`** for compile-time platform checks

## Quick Reference

```julia
# Basic test item
@testitem "Name" begin ... end

# Tagged test item
@testitem "Name" tags=[:tag1, :tag2] begin ... end

# Run with filter
@run_package_tests filter=testfilter

# Environment check
get(ENV, "VAR", "") == "value"

# Platform check
Sys.iswindows()
Sys.islinux()
Sys.ARCH == :x86_64

# Version check
VERSION >= v"1.10"

# Conditional Pkg.add
condition && Pkg.add("Package")
```

## Additional Testing Tools

### ReferenceTests.jl

Compare outputs against stored reference files:

```julia
@testitem "Reference tests" begin
    using ReferenceTests

    result = generate_output()
    @test_reference "references/expected.txt" result
end
```

### LocalCoverage.jl

Analyze code coverage locally without CI:

```julia
using LocalCoverage

# Generate coverage report
generate_coverage("MyPackage")

# Open HTML report
open_coverage()
```

### Standard Library Test Module

For simple cases without TestItemRunner:

```julia
# test/runtests.jl
using Test
using MyPackage

@testset "MyPackage Tests" begin
    @testset "Basic functionality" begin
        @test myfunction(1) == expected
        @test_throws ErrorType badfunction()
    end

    @testset "Edge cases" begin
        @test isempty(myfunction([]))
    end
end
```

## Related Skills

- `julia-doctests` - Doctest configuration
- `julia-ci-github` - CI configuration
- `julia-ci-buildkite` - Buildkite configuration
