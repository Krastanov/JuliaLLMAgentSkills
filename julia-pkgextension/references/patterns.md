# Extension Patterns

## Table of Contents

- [Plotting Extension (Makie)](#plotting-extension-makie)
- [GPU Extension (CUDA)](#gpu-extension-cuda)
- [Multiple Trigger Extension](#multiple-trigger-extension)
- [Method Extension Pattern](#method-extension-pattern)
- [Type Definition in Extension](#type-definition-in-extension)
- [Multi-File Extension](#multi-file-extension)

## Plotting Extension (Makie)

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

## GPU Extension (CUDA)

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

## Multiple Trigger Extension

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

## Method Extension Pattern

Define methods in the main package, implement in extension:

```julia
# src/MyPackage.jl
module MyPackage
function plot_data end  # Declare function (can be empty)
export plot_data
end

# ext/MyPackageMakieExt.jl
module MyPackageMakieExt
using Makie, MyPackage

function MyPackage.plot_data(data::MyPackage.MyType)
    fig = Figure()
    ax = Axis(fig[1,1])
    # ... plotting code
    return fig
end
end
```

## Type Definition in Extension

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

## Multi-File Extension

```julia
# ext/MyPackageMakieExt/MyPackageMakieExt.jl
module MyPackageMakieExt

using Makie
using MyPackage
using MyPackage: InternalType, internal_function

include("recipes.jl")
include("utils.jl")

end # module
```

## PrecompileTools in Extensions

```julia
module MyPackageMakieExt

using PrecompileTools

@setup_workload begin
    using Makie, MyPackage
    @compile_workload begin
        data = MyPackage.example_data()
        MyPackage.plot_data(data)
    end
end

end
```
