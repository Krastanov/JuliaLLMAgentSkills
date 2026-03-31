# Conditional Test Loading

Prefer reaching these branches through `Pkg.test(...)` or CI rather than by
calling `test/runtests.jl` directly. If conditional dependencies live in their
own subproject, activate and instantiate that subproject instead of trusting an
old manifest.

## Environment-Based Dependencies

```julia
# test/runtests.jl
using Pkg

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
end
```

## System-Based Checks

```julia
using InteractiveUtils
versioninfo(; verbose=true)

Oscar_flag = false
GPU_flag = false

# Oscar only supported on x86_64 *NIX
if Sys.iswindows() || Sys.ARCH != :x86_64
    @info "Skipping Oscar tests"
else
    Oscar_flag = VERSION >= v"1.11"
end

# GPU tests only on *NIX
if !Sys.iswindows()
    GPU_flag = get(ENV, "GPU_TEST", "") != ""
end
```

## Conditional Include Pattern

```julia
using MyPackage
using Test

@testset "MyPackage" begin
    include("test_core.jl")

    if get(ENV, "JET_TEST", "") == "true"
        include("test_jet.jl")
    end

    if Oscar_flag
        include("test_oscar.jl")
    end

    if GPU_flag
        include("test_gpu.jl")
    end

    if VERSION >= v"1.10"
        include("test_aqua.jl")
        include("test_doctests.jl")
    end
end
```
