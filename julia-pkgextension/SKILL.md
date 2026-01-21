---
name: julia-pkgextension
description: Build Julia package extensions (weak dependencies) for optional functionality. Use this skill when creating extensions that load conditionally based on trigger packages.
---

# Julia Package Extensions

Build package extensions (weak dependencies) to provide optional functionality that loads
only when users import the trigger package(s).

## Why Extensions?

Julia's multiple dispatch allows defining new methods for existing functions when new types
are introduced. Package extensions leverage this:

1. **Minimal base package**: Users who don't need plotting don't pay for Makie compilation
2. **Clean dependencies**: Heavy packages stay optional
3. **Precompilation benefits**: Extensions precompile separately; base package stays fast
4. **Type piracy prevention**: Methods involving external types live in extensions

**Tradeoff**: Extensions add complexity and require explicit loading. Use them when the
trigger dependency is heavy (plotting, GPU, optimization solvers) or when the functionality
is truly optional.

## Project.toml Configuration

```toml
name = "MyPackage"
uuid = "..."
version = "1.0.0"

[deps]
# Regular dependencies here

[weakdeps]
Makie = "ee78f7c6-11fb-53f2-987a-cfe4a2b5a57a"
CUDA = "052768ef-5323-5732-b1bb-66c8b64840ba"
Hecke = "3e1990a7-5d81-5526-99ce-9ba3ff248f21"
Oscar = "f1435218-dba5-11e9-1e4d-f1a5fab5fc13"

[extensions]
# Single trigger
MyPackageMakieExt = "Makie"
MyPackageCUDAExt = "CUDA"

# Multiple triggers (loads when ALL are imported)
MyPackageOscarExt = ["Hecke", "Oscar"]

[compat]
Makie = "0.20, 0.21, 0.22, 0.23, 0.24"
CUDA = "4.4.0, 5"
Hecke = "0.32 - 0.39"
Oscar = "1.1"
```

## File Structure

```
MyPackage.jl/
├── Project.toml
├── src/
│   ├── MyPackage.jl
│   └── ...
└── ext/
    ├── MyPackageMakieExt/
    │   ├── MyPackageMakieExt.jl    # Module definition
    │   ├── recipes.jl              # Plot recipes
    │   └── utils.jl                # Extension utilities
    └── MyPackageCUDAExt.jl         # Single-file extension
```

**Naming convention**: `{PackageName}{TriggerDep}Ext`

## Extension Module Structure

### Single-File Extension

```julia
# ext/MyPackageMakieExt.jl
module MyPackageMakieExt

using Makie
using MyPackage
using MyPackage: InternalType, internal_function  # Import internals to extend

# Extend functions from main package
function MyPackage.plot_data(data::MyPackage.MyType)
    # Implementation using Makie
end

# Define Makie recipes
@recipe(MyPlot, data) do scene
    # Recipe implementation
end

end # module
```

### Multi-File Extension

```julia
# ext/MyPackageMakieExt/MyPackageMakieExt.jl
module MyPackageMakieExt

using Makie
using MyPackage
using MyPackage: InternalType, internal_function

# Include implementation files
include("recipes.jl")
include("utils.jl")

end # module
```

### Extension with Exports (for Documentation)

When you need Documenter.jl to find types defined in extensions:

```julia
# ext/MyPackageHeckeExt/MyPackageHeckeExt.jl
module MyPackageHeckeExt

using Hecke
using MyPackage
using DocStringExtensions

# Export types so Documenter can find them
export SpecialCode, AnotherCode

include("codes.jl")
include("algorithms.jl")

end # module
```

## Extending Functions

### Pattern 1: Method Extension

Define methods in the main package, implement in extension:

```julia
# src/MyPackage.jl
module MyPackage

# Declare function (can be empty or have base methods)
function plot_data end

export plot_data
end

# ext/MyPackageMakieExt.jl
module MyPackageMakieExt
using Makie, MyPackage

# Add method for extension-specific functionality
function MyPackage.plot_data(data::MyPackage.MyType)
    fig = Figure()
    ax = Axis(fig[1,1])
    # ... plotting code
    return fig
end

end
```

### Pattern 2: Type Definition in Extension

Define types that only exist when extension is loaded:

```julia
# ext/MyPackageHeckeExt.jl
module MyPackageHeckeExt
using Hecke, MyPackage

# New type only available with Hecke
struct LPCode <: MyPackage.AbstractCode
    # fields using Hecke types
end

# Methods for the new type
MyPackage.encode(code::LPCode, data) = # ...

end
```

## Error Hints with WeakDepHelpers.jl

Provide helpful error messages when users call functions without loading the extension:

### Setup in Main Package

```julia
# src/MyPackage.jl
module MyPackage

using WeakDepHelpers: WeakDepCache, method_error_hint_callback,
    @declare_struct_is_in_extension, @declare_method_is_in_extension

export LPCode, special_algorithm  # Export names even though defined in extension

const WEAKDEP_METHOD_ERROR_HINTS = WeakDepCache()

function __init__()
    if isdefined(Base.Experimental, :register_error_hint)
        Base.Experimental.register_error_hint(MethodError) do io, exc, argtypes, kwargs
            method_error_hint_callback(WEAKDEP_METHOD_ERROR_HINTS, io, exc, argtypes, kwargs)
        end
    end
end

end
```

### Declare Extension Types and Methods

```julia
# src/extension_stubs.jl (included in main module)
using WeakDepHelpers: @declare_struct_is_in_extension, @declare_method_is_in_extension

const hecke_docstring = "Implemented in extension requiring Hecke.jl."

# Declare types implemented in extensions
@declare_struct_is_in_extension MyPackage LPCode :MyPackageHeckeExt (:Hecke,) hecke_docstring
@declare_struct_is_in_extension MyPackage GeneralizedBicycle :MyPackageHeckeExt (:Hecke,) hecke_docstring

# Declare functions implemented in extensions
@declare_method_is_in_extension MyPackage.WEAKDEP_METHOD_ERROR_HINTS special_algorithm (:Hecke,) hecke_docstring
```

### User Experience

Without Hecke loaded:
```julia
julia> using MyPackage
julia> LPCode(args...)
ERROR: `LPCode` depends on the package(s) `Hecke` but you have not installed or
imported them yet. Immediately after an `import Hecke`, `LPCode` will be available.
```

After loading Hecke:
```julia
julia> import Hecke
julia> LPCode(args...)  # Works!
```

## Loading Extensions Programmatically

### Check if Extension is Loaded

```julia
ext = Base.get_extension(MyPackage, :MyPackageHeckeExt)
if ext !== nothing
    # Extension is loaded, can use its functionality
end
```

### Get Extension Module

```julia
import Hecke  # Triggers extension loading
const MyPackageHeckeExt = Base.get_extension(MyPackage, :MyPackageHeckeExt)

# Now can access extension internals
MyPackageHeckeExt.internal_extension_function()
```

## Testing Extensions

### In Test Suite

```julia
# test/test_hecke_extension.jl
@testitem "Hecke extension" tags=[:hecke] begin
    using Hecke
    using MyPackage

    # Get extension module for testing internals
    const HeckeExt = Base.get_extension(MyPackage, :MyPackageHeckeExt)

    @test LPCode(args...) isa MyPackage.AbstractCode
    @test HeckeExt.internal_function() == expected
end
```

### Conditional Test Loading

```julia
# test/runtests.jl
using TestItemRunner

testfilter = ti -> begin
    exclude = Symbol[]
    # Skip Hecke tests if not available or too slow for CI
    if get(ENV, "HECKE_TEST", "") != "true"
        push!(exclude, :hecke)
    end
    return all(!in(exclude), ti.tags)
end

@run_package_tests filter=testfilter
```

## Documenting Extensions

Extensions require special handling in `docs/make.jl`. See the `julia-docs` skill for details.

### Load Extensions Before Building Docs

```julia
# docs/make.jl
using Documenter
using MyPackage

# Load extension triggers
import Hecke
const MyPackageHeckeExt = Base.get_extension(MyPackage, :MyPackageHeckeExt)

import Makie
const MyPackageMakieExt = Base.get_extension(MyPackage, :MyPackageMakieExt)

# Include all modules
makedocs(
    modules = [MyPackage, MyPackageHeckeExt, MyPackageMakieExt],
    # ...
)
```

### Document Extension API Separately

```markdown
# Extension API

## Hecke Extension

Requires `Hecke.jl` to be loaded.

```@autodocs
Modules = [MyPackageHeckeExt]
Private = false
```
```

## Precompilation Considerations

### Why Extensions Help Precompilation

1. **Separate precompilation**: Each extension precompiles independently
2. **Conditional loading**: Users only pay compilation cost when they need it
3. **Smaller base package**: Core functionality compiles faster

### PrecompileTools in Extensions

```julia
# ext/MyPackageMakieExt.jl
module MyPackageMakieExt

using PrecompileTools

@setup_workload begin
    using Makie, MyPackage
    @compile_workload begin
        # Precompile common extension operations
        data = MyPackage.example_data()
        MyPackage.plot_data(data)
    end
end

end
```

### Cache Invalidation

Extensions recompile when:
- The main package changes
- Any trigger dependency changes
- Julia version changes

Keep extensions focused to minimize recompilation cascades.

## Common Patterns

### Plotting Extension (Makie)

```julia
module MyPackageMakieExt

using Makie
using MyPackage

# Plot recipe
@recipe(CircuitPlot, circuit) do scene
    Attributes(
        gatecolor = :blue,
        wirecolor = :black,
    )
end

function Makie.plot!(p::CircuitPlot)
    circuit = p.circuit[]
    # Draw circuit elements
    return p
end

# Convenience function
function MyPackage.circuitplot(circuit; kwargs...)
    fig = Figure()
    ax = Axis(fig[1,1])
    circuitplot!(ax, circuit; kwargs...)
    return fig
end

end
```

### GPU Extension (CUDA)

```julia
module MyPackageCUDAExt

using CUDA
using MyPackage

# GPU-accelerated method
function MyPackage.process(data::CuArray)
    # CUDA implementation
end

# Adapt rule for custom types
import Adapt
Adapt.adapt_structure(to::CUDA.KernelAdaptor, x::MyPackage.MyType) = # ...

end
```

### Multiple Trigger Extension

```julia
# Loads only when BOTH Oscar AND Hecke are imported
module MyPackageOscarExt

using Oscar  # Depends on Hecke
using Hecke
using MyPackage

# Functionality requiring both packages
struct HomologicalProduct <: MyPackage.AbstractCode
    # Uses types from both Oscar and Hecke
end

end
```

## Checklist

- [ ] Add weak dependencies to `[weakdeps]` section
- [ ] Add extension mapping to `[extensions]` section
- [ ] Add compat entries for weak dependencies
- [ ] Create extension module in `ext/` directory
- [ ] Use correct naming: `{Package}{Trigger}Ext`
- [ ] Import and extend functions from main package
- [ ] Export types that Documenter needs to find
- [ ] Add WeakDepHelpers stubs for user-friendly errors (optional)
- [ ] Register method error hints in `__init__` (optional)
- [ ] Load extensions in `docs/make.jl` for documentation
- [ ] Add tagged tests for extension functionality
- [ ] Update CI to conditionally run extension tests

## Related Skills

- `julia-docs` - Documentation setup including extensions
- `julia-tests` - Testing with TestItemRunner and tags
- `julia-package-dev` - Package development basics
