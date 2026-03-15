# Standard Test Files

## Aqua Tests

```julia
# test/test_aqua.jl
using Aqua
using MyPackage

@testset "Aqua" begin
    Aqua.test_all(MyPackage;
        ambiguities=false,  # Optional: skip ambiguity checks
    )
end
```

## JET Tests

```julia
# test/test_jet.jl
using JET
using Test
using MyPackage

@testset "JET" begin
    rep = JET.report_package(MyPackage; target_modules=[MyPackage])
    @show rep
    @test length(JET.get_reports(rep)) <= 5
    @test_broken length(JET.get_reports(rep)) == 0
end
```

## Doctests

```julia
# test/test_doctests.jl
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

@testset "Doctests" begin
    doctest(nothing, modules)
end
```

## Platform-Specific Tests

Conditionally included from runtests.jl (see `julia-tests-run`):

```julia
# test/test_gpu.jl
using CUDA
using Test
using MyPackage

@testset "CUDA" begin
    @test cuda_function() == expected
end
```

## Shared Test Utilities

```julia
# test/TestUtils.jl
module TestUtils
    export make_test_data, verify_result

    function make_test_data(n::Int)
        # Create reproducible test data
    end

    function verify_result(result)
        # Common verification logic
    end
end

# test/test_core.jl
include("TestUtils.jl")
using .TestUtils

@testset "Core" begin
    data = make_test_data(100)
    @test verify_result(process(data))
end
```
