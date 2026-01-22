# Advanced Doctests

## Table of Contents

- [Named Doctests (Shared State)](#named-doctests-shared-state)
- [Setup and Teardown](#setup-and-teardown)
- [Handling Randomness with StableRNGs.jl](#handling-randomness-with-stablerngsj)
- [Filters for Non-Deterministic Output](#filters-for-non-deterministic-output)
- [Testing Exceptions](#testing-exceptions)
- [Testing Package Extensions](#testing-package-extensions)
- [Output Suppression](#output-suppression)

## Named Doctests (Shared State)

Label doctests to share state across multiple blocks:

````julia
"""
```jldoctest myexample
julia> x = [1, 2, 3]
3-element Vector{Int64}:
 1
 2
 3
```

Some explanatory text here...

```jldoctest myexample
julia> sum(x)  # x is still defined from above
6
```
"""
````

All blocks with the same label share a module scope.

## Setup and Teardown

### Block-Level Setup

````markdown
```@meta
DocTestSetup = quote
    using MyPackage
    x = [1, 2, 3]
end
```

```jldoctest
julia> sum(x)
6
```

```@meta
DocTestTeardown = quote
    # cleanup code
end
```
````

### Inline Setup

````julia
```jldoctest; setup = :(using MyPackage)
julia> myfunction(1)
42
```
````

**Important**: Setup code re-runs for each doctest block. State is not shared unless
using named doctests.

## Handling Randomness with StableRNGs.jl

Never use `rand()` directly - output varies across Julia versions. Use StableRNGs.jl:

```julia
"""
# Examples
```jldoctest
julia> using StableRNGs

julia> rng = StableRNG(42);

julia> random_sample(rng, 3)
3-element Vector{Float64}:
 0.5557510873245796
 0.43710797460962514
 0.12174322140083723
```
"""
function random_sample(rng, n)
    rand(rng, n)
end
```

StableRNGs guarantees identical output across Julia versions, architectures, and operating systems.

## Filters for Non-Deterministic Output

### Global Filters

```julia
doctestfilters = [
    r"Ptr{0x[0-9a-f]+}",           # memory addresses
    r"\d+\.\d+ seconds",            # timing
    r"(MyPackage\.|)"               # optional module prefix
]

doctest(MyPackage; doctestfilters)
```

### Replacement Filters

```julia
doctestfilters = [
    r"[0-9]+ bytes" => s"N bytes"
]
```

### Block-Level Filters

````julia
```jldoctest; filter = r"[0-9\.]+ seconds"
julia> @elapsed sleep(0.1)
0.104 seconds
```
````

## Testing Exceptions

````julia
```jldoctest
julia> div(1, 0)
ERROR: DivideError: integer division error
[...]
```
````

- `[...]` indicates truncated output (stacktrace omitted)
- Error matching uses prefix comparison

## Testing Package Extensions

Load the extension and include it in the modules list:

```julia
@testitem "Doctests" begin
    using Documenter
    using MyPackage

    extensions = []

    # Load extension by importing its trigger package
    import SomeDependency
    const MyPackageSomeDependencyExt = Base.get_extension(MyPackage, :MyPackageSomeDependencyExt)
    push!(extensions, MyPackageSomeDependencyExt)

    # Conditional extensions
    @static if VERSION >= v"1.11"
        import AnotherDep
        const MyPackageAnotherDepExt = Base.get_extension(MyPackage, :MyPackageAnotherDepExt)
        push!(extensions, MyPackageAnotherDepExt)
    end

    # Set display size for consistent output
    ENV["LINES"] = 80
    ENV["COLUMNS"] = 80

    DocMeta.setdocmeta!(MyPackage, :DocTestSetup, :(using MyPackage); recursive=true)

    modules = [MyPackage, MyPackage.SubModule, extensions...]
    doctest(nothing, modules)
end
```

## Output Suppression

Hide output section in rendered docs while still testing:

````julia
```jldoctest; output = false
result = complex_calculation()
result == expected_value
# output
true
```
````
