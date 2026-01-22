# Conditional Test Loading

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

## Combined Filter Function

```julia
testfilter = ti -> begin
    exclude = Symbol[]

    # JET-only mode
    if get(ENV, "JET_TEST", "") == "true"
        return :jet in ti.tags
    else
        push!(exclude, :jet)
    end

    # Platform exclusions
    if !Oscar_flag
        push!(exclude, :oscar_required)
    end
    if !GPU_flag
        push!(exclude, :cuda, :gpu)
    end

    # Version exclusions
    if !(VERSION >= v"1.10")
        push!(exclude, :doctests, :aqua)
    end

    return all(!in(exclude), ti.tags)
end
```

## Test Categories Pattern

```julia
testfilter = ti -> begin
    exclude = Symbol[]

    if get(ENV, "TEST_CATEGORY", "") == "base"
        return (:core in ti.tags) && all(!in(exclude), ti.tags)
    elseif get(ENV, "TEST_CATEGORY", "") == "encoding"
        return (:encoding in ti.tags) && all(!in(exclude), ti.tags)
    end

    return all(!in(exclude), ti.tags)
end
```
