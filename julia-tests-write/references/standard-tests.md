# Standard Test Files

## Aqua Tests

```julia
# test/test_aqua.jl
using Test

@testset "Aqua" begin
    using Aqua
    using MyPackage

    Aqua.test_all(MyPackage;
        ambiguities=false,  # Optional: skip ambiguity checks
    )
end
```

## JET Tests

```julia
# test/test_jet.jl
using Test

@testset "JET" begin
    using JET
    using MyPackage

    rep = JET.report_package(MyPackage, target_modules=[MyPackage])
    @show rep # print detected issues
    @test length(JET.get_reports(rep)) <= 5 # nonzero, in case there are some unresolved issues
    @test_broken length(JET.get_reports(rep)) == 0 # broken test, in case there are some unresolved issues
end
```

## Doctests

```julia
# test/test_doctests.jl
using Test

@testset "Doctests" begin
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

## Platform-Specific Tests

Guard optional tests with explicit environment flags and platform checks in
`test/runtests.jl`, then include the files or run `@testset` conditionally.

```julia
# test/test_gpu.jl
using Test

@testset "CUDA tests" begin
    using CUDA
    using MyPackage

    @test cuda_function() works
end
```

```julia
# test/test_oscar.jl
using Test

@testset "Oscar tests" begin
    using Oscar
    using MyPackage

    @test oscar_function() works
end
```

```julia
# test/runtests.jl
using Test

if get(ENV, "GPU_TEST", "") == "cuda" && !Sys.iswindows()
    include("test_gpu.jl")
end

if !Sys.iswindows() && Sys.ARCH == :x86_64 && VERSION >= v"1.11"
    include("test_oscar.jl")
end
```

## Setup and Teardown

```julia
using Test

@testset "With setup" begin
    using MyPackage

    # Setup runs once per test set
    data = load_test_data()

    @test process(data) == expected
    @test validate(data)
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
```

```julia
# test/test_core.jl
using Test

@testset "Core" begin
    include("TestUtils.jl")
    using .TestUtils

    data = make_test_data(100)
    @test verify_result(process(data))
end
```
