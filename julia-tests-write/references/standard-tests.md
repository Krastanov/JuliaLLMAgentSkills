# Standard Test Files

## Aqua Tests

```julia
# test/test_aqua.jl
@testitem "Aqua" tags=[:aqua] begin
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
@testitem "JET" tags=[:jet] begin
@testitem "JET" tags=[:jet] begin
    using JET
    using Test
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

## Platform-Specific Tests

These need appropriate handling in runtests.jl in order to have them filtered by tags

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

## Setup and Teardown

```julia
@testitem "With setup" begin
    using MyPackage

    # Setup runs once per test item
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

# test/test_core.jl
@testitem "Core" begin
    include("TestUtils.jl")
    using .TestUtils

    data = make_test_data(100)
    @test verify_result(process(data))
end
```
