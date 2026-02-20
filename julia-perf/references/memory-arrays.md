# Memory & Arrays

Source: https://docs.julialang.org/en/v1/manual/performance-tips/

## Pre-Allocate Outputs

Allocate once, reuse across iterations with mutating (`!`) functions.

```julia
# BAD — allocates a new array every iteration
function loopinc()
    y = 0
    for i = 1:10^5
        ret = xinc(i)       # allocates each time
        y += ret[2]
    end
    y
end

# GOOD — allocate once, mutate in-place
function loopinc_prealloc()
    ret = Vector{Int}(undef, 3000)
    y = 0
    for i = 1:10^5
        xinc!(ret, i)       # reuses buffer
        y += ret[2]
    end
    y
end
```

Typical improvement: ~30x speed, allocations drop from 200k to 2.

## Use Views Instead of Copies

Array slicing (`a[2:end-1]`) creates a copy. Use `view` or `@views` to avoid it.

```julia
# BAD — copies slice
fcopy(x) = sum(x[2:end-1])

# GOOD — zero-copy view
fview(x) = sum(@view x[2:end-1])

# GOOD — apply @views to a whole block
@views function process(x)
    a = x[1:100]
    b = x[101:end]
    sum(a) + sum(b)
end
```

For small arrays or single-use slices, copying may be faster due to contiguous
memory. Profile to decide.

## Access Arrays in Column-Major Order

Julia stores arrays column-major (first index varies fastest in memory).

```julia
# BAD — row-major traversal (cache-unfriendly)
for j = 1:n, i = 1:n    # j is outer loop
    out[j, i] = x[i]     # jumps in memory
end

# GOOD — column-major traversal
for j = 1:n, i = 1:n
    out[i, j] = x[i]     # sequential memory access
end
```

Rule: the **first** index should change in the **innermost** loop.

## Fuse Broadcasts with @. (More Dots)

Dot syntax fuses operations into a single loop, avoiding temporary arrays.

```julia
# BAD — allocates temporaries for each operation
f(x) = 3x.^2 + 4x + 7x.^3

# GOOD — single fused loop, one output array
fdot(x) = @. 3x^2 + 4x + 7x^3

# GOOD — in-place fused assignment
y .= @. 3x^2 + 4x + 7x^3
```

Typical improvement: ~10x speed, ~6x less memory on large arrays.

## Unfuse When Axis-Constant (Fewer Dots)

Pre-compute values that are constant along one axis instead of recomputing per
element.

```julia
x = rand(1000, 1000)
d = sum(abs2, x; dims=2)

# BAD — recomputes sqrt(d[i]) for every column element
x ./= sqrt.(d)

# GOOD — compute sqrt once per row, then divide
let s = sqrt.(d)
    x ./= s
end
```

## Copying Can Be Faster Than Views

When data is accessed repeatedly with irregular indices, copying to contiguous
memory improves cache performance.

```julia
A = randn(3000, 3000)
inds = shuffle(1:3000)[1:2000]

# Slower — non-contiguous access pattern
result = heavy_computation(view(A, inds, inds))

# Faster — contiguous copy despite allocation cost
result = heavy_computation(A[inds, inds])
```

## Consider StaticArrays.jl for Small Fixed-Size Arrays

For arrays with < ~100 elements and compile-time-known size:

```julia
using StaticArrays
v = SVector(1.0, 2.0, 3.0)
w = SVector(4.0, 5.0, 6.0)
norm(3v - w)   # no heap allocation, loop unrolling, register storage
```

## Multithreading and Linear Algebra

Avoid thread oversubscription when combining Julia threads with BLAS:

```bash
# Set BLAS to single-threaded when using Julia threads
OPENBLAS_NUM_THREADS=1 julia -t 4
```

```julia
using LinearAlgebra
BLAS.set_num_threads(1)   # or query with BLAS.get_num_threads()
```

Consider alternative backends: `MKL.jl` (Intel), `AppleAccelerate.jl` (macOS).
