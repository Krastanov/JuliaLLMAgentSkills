# Additional Testing Tools

## ReferenceTests.jl

Compare outputs against stored reference files:

```julia
@testitem "Reference tests" begin
    using ReferenceTests

    result = generate_output()
    @test_reference "references/expected.txt" result
end
```

## LocalCoverage.jl

Analyze code coverage locally without CI:

```julia
using LocalCoverage

# Generate coverage report
generate_coverage("MyPackage")

# Open HTML report
open_coverage()
```

## Standard Library Test Module

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

## Common Test Macros

```julia
@test expr                  # Test expression is true
@test_throws E expr         # Test that E is thrown
@test_logs (:warn,) expr    # Test log output
@test_broken expr           # Known broken test
@test_skip expr             # Skip this test

@testset "name" begin       # Group tests
    # tests...
end

@inferred f(x)              # Test type stability
```

## Best Practices

1. **Use TestItemRunner** for modern, organized tests
2. **Tag all tests** for selective running
3. **Conditionally install** heavy dependencies
4. **Check platform/version** before loading platform-specific code
5. **Print thread info** at test start for debugging
6. **Keep JET tests separate** - they're slow and need explicit enabling
7. **Use `@static if`** for compile-time platform checks
