# Conditional Test Loading

These patterns show how to gate optional tests using environment variables
and platform checks with the standard library `Test`.
If a repository already uses `@testitem`, prefer ReTestItems.jl for running
those tests (see `julia-retestitems-run`).

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

## Conditional Includes

```julia
# test/runtests.jl
using Test

include("test_core.jl")
include("test_aqua.jl")

if get(ENV, "JET_TEST", "") == "true"
    include("test_jet.jl")
end

if get(ENV, "DOCTESTS", "") == "true"
    include("test_doctests.jl")
end
```
