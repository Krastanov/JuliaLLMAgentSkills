# Fast Loop and Array Libraries

For extremely hot, compute-bound code, Julia's standard abstractions (like broadcast or native array views) can sometimes leave performance on the table due to compiler optimization limits or memory access patterns. The following ecosystem packages provide highly optimized macro-based alternatives.

## LoopVectorization.jl (`@turbo`)

`LoopVectorization.jl` transforms standard `for` loops and array operations into highly optimized SIMD (Single Instruction, Multiple Data) instructions, utilizing AVX-512, AVX2, or NEON depending on the architecture. 

While LLVM/Julia natively generates optimal SIMD instructions for the main body of a loop, it struggles significantly with loop remainders (the "tails" of the array that don't fit perfectly into the SIMD register width). LoopVectorization's greatest performance benefit comes from handling these tails far more efficiently than standard `@simd`.

### Usage and Examples
Prefix a `for` loop or broadcast statement with `@turbo`:

```julia
function mydotavx(a, b)
    s = 0.0
    @turbo for i ∈ eachindex(a,b)
        s += a[i]*b[i]
    end
    s
end
```

When dealing with arrays that have a leading dimension of size 1 (i.e., broadcasting across rows), you can wrap them in `LowDimArray` so the macro can optimize accordingly:
```julia
using LoopVectorization
ldad = LowDimArray{(false,true,true)}(d)
@turbo @. E = exp(A - b' + ldad) * c
```

### Requirements & Limitations (Nasal Demons Warning!)
Misusing LoopVectorization can have severe consequences. Like `@inbounds`, misusing it can lead to segfaults and memory corruption. **You must guarantee the following when using `@turbo`:**

1. **No Bounds Checking**: `@turbo` does not perform any bounds checking. You must ensure you are not indexing an array out of bounds.
2. **No Empty Iteration Spaces**: Iterating over an empty loop (such as `for i ∈ eachindex(Float64[])`) is undefined behavior and will likely result in out-of-bounds memory accesses.
3. **No Specific Execution Order**: `@turbo` can and will re-order operations and loops inside its scope. The code's correctness cannot depend on a particular order (e.g., you cannot implement `cumsum` with `@turbo`).
4. **No Multiple Same-Level Loops**: You are not using multiple loops at the same level within nested loops.
5. **Iteration Space**: It currently only supports rectangular iteration spaces (not triangular or ragged). Inner loop iterations cannot be a function of outer loop variables.
6. **No Branches/Allocations**: Loop bodies cannot contain branching (`if` statements) or allocations.
7. **No kwargs**: `@turbo` does not support passing kwargs to function calls inside its block (e.g., `@turbo round.(A; digits=3)` throws a `TypeError`). Work around this by wrapping the call in an anonymous function or struct beforehand:
   ```julia
   struct KwargCall{F,T} f::F; x::T end
   @inline (f::KwargCall)(args...) = f.f(args...; f.x...)
   f = KwargCall(round, (digits = 3,));
   @turbo f.(rand(10))
   ```

### The StructArray Trick (Complex Numbers & Structs)
Because `@turbo` leverages low-level knowledge of how primitive types (like `Float64` or `Int`) are handled by CPU registers, it **cannot** natively handle arrays of structs (such as `Array{Complex{Float64}}`).
To vectorize code involving complex numbers or custom numeric structs, use **`StructArrays.jl`** to transform your Array-of-Structs (AoS) into a Struct-of-Arrays (SoA). 
```julia
using StructArrays

# Create a StructArray which separates the real and imaginary parts into their own arrays:
A = StructArray(randn(ComplexF64, M, K))

# You can now apply @turbo on the underlying arrays of primitives independently:
@turbo for i in eachindex(A)
    A.re[i] += 1.0
    A.im[i] -= 1.0
end
```
This pattern extends to other numeric structs like dual numbers or `DoubleFloats`.

### Vectorized Convenience Functions
LoopVectorization exports highly optimized mapping alternatives:
- **`vmap` / `vmap!`**: Directly vectorized (SIMD) versions of `map` and `map!`.
- **`vmapnt` / `vmapnt!`**: Like `vmap`, but uses **non-temporal (streaming) stores** when writing to the destination array. This explicitly prevents the CPU from pulling the destination memory into the cache hierarchy, preserving cache space for other data. It yields major performance increases for massive arrays whose written values won't be read back again soon.
- **`vmapntt!`**: Multithreaded + non-temporal `map!`.

*(Threading note: Can be multithreaded using `@tturbo` or `@turbo thread=true` (or `thread=8`)).*

---

## FastBroadcast.jl (`@..`)

`FastBroadcast.jl` exports `@..`, a drop-in replacement for standard broadcast (`@.`) that compiles the expression directly into simple `for` loops that are significantly easier for the LLVM compiler to optimize.

### Usage and Examples
```julia
using FastBroadcast

function fast_foo9(a, b, c, d, e, f, g, h, i)
    @.. a = b + 0.1 * (0.2c + 0.3d + 0.4e + 0.5f + 0.6g + 0.6h + 0.6i)
    nothing
end
```

### Performance Benefits
- **Avoids Temporaries**: Standard broadcasting can sometimes trigger intermediate allocations when evaluating complex, deeply nested expressions with many arguments. `@..` reliably fuses the entire expression into a single allocation-free loop.
- **Faster Compilation**: Because it directly generates a `for` loop instead of deeply nested internal broadcast machinery types, the time-to-first-execution (TTFX) and compiler latency are drastically reduced.

*(Threading note: Can be multithreaded using `@.. thread=true`).*

---

## Strided.jl (`@strided`)

`Strided.jl` provides cache-friendly, highly optimized manipulations for arrays with arbitrary strides. While Julia's Base operations assume column-major contiguous memory, `Strided.jl` makes no assumptions (e.g., stride 1 along the first dimension, or monotonically increasing strides) and excels when memory is non-contiguous (e.g., transposed arrays, reshaped views).

Currently, Strided.jl methods are restricted to array data in main memory and do not support GPUs.

### Usage and Examples
Wrap operations like broadcasts, reductions, or `permutedims` in `@strided`:

```julia
using Strided

A = randn(4000, 4000); B = similar(A);

# Cache misses on A' make Base slow (e.g. 145 ms)
B .= (A .+ A') ./ 2

# Strided reorganizes memory access to be cache-friendly (e.g. 56 ms)
@strided B .= (A .+ A') ./ 2

# Massive improvements on non-contiguous array multiplication (2.4 ms -> 1.4 ms)
@strided B .= 3 .* A'

# Multidimensional permutations are much faster (5.2 ms -> 2.2 ms)
@strided permutedims!(B, A, (4,3,2,1))
```

### Key Functions and Configuration
- **`@strided`**: The main macro. Reorganizes the memory access pattern of the enclosed expression to avoid massive performance cliffs associated with non-contiguous memory access.
- **`StridedView(A)`**: The foundational structured type (provided by `StridedViews.jl`) that wraps a contiguous array. It is device-agnostic and guarantees downstream functions utilize cache-aware algorithms.
- **`sreshape` / `sview`**: Strided-specific equivalents to `reshape` and `view` that ensure the result remains properly typed for Strided's algorithms without unnecessary allocations.

*(Threading note: Can be multithreaded; `@strided` enables it automatically for large arrays).*
