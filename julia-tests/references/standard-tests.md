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
    using JET
    using MyPackage

    @test_opt target_modules=[MyPackage] myfunction(1)
    @test_call target_modules=[MyPackage] myfunction(1)
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
