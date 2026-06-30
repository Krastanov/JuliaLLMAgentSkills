# Lightweight Threading with Polyester.jl

Julia's standard `Base.Threads.@threads` incurs a small but non-trivial overhead when scheduling tasks. For tight loops that complete very quickly, this task-spawning overhead can dominate execution time, neutralizing the benefits of multithreading. 

`Polyester.jl` provides `@batch`, an alternative that implements lightweight, low-overhead threading. It achieves this static scheduling by keeping a dedicated static pool of threads awake and synchronizing them directly using atomics, bypassing Julia's standard task scheduler entirely.

## Using `@batch`

Use `@batch for i in ...` instead of `@threads` for inner loops where iteration bodies are extremely fast.

### Crucial Caveats
- **Slicing creates views**: `Polyester.@batch` moves arrays to threads by turning them into `StrideArraysCore.PtrArray`s. This means that under a `@batch` loop, array slices will automatically create `view`s by default! You may want to start Julia with `--check-bounds=yes` while debugging.
- **No thread pinning**: Polyester uses regular Julia threads, governed by `JULIA_NUM_THREADS`. It does **not** pin threads to specific CPU-cores. To guarantee threads run on specific cores, use a tool like `ThreadPinning.jl`.

### Configuration and Keywords

#### `per=cores` vs `per=threads`
By default, `@batch` uses `per=cores`, meaning it limits execution to up to 1 thread per physical CPU core (e.g., skipping hyperthreads). This default exists because LoopVectorization.jl (a major Polyester consumer) performs optimally with 1 thread per physical core. If you explicitly want to utilize all logical threads, use `@batch per=threads for ...`.

#### `minbatch`
The `minbatch` argument allows you to specify a minimum number of loop iterations per thread, effectively capping the number of threads spawned for small arrays. For example, `minbatch=n` means it will use at most `number_of_iterations ÷ n` threads. 
```julia
# With 10,000 items, minbatch=2500 ensures only 4 threads are used.
@batch minbatch=2500 for i in eachindex(y, x)
    y[i] = a * x[i] + y[i]
end
```

#### `threadlocal`
You can define local storage for each thread without incurring allocations. Polyester will return a vector containing each of the local storages at the end of the loop block.
```julia
# Optionally define the type (e.g. ::Float16)
let
    @batch threadlocal=rand(10:99)::Float16 for i in 1:100
        # Use `threadlocal` safely inside the loop
        threadlocal += i
    end
    println(threadlocal) # e.g. Float16[83.0, 90.0, 27.0, 65.0]
end
```

#### `reduction`
The `reduction` keyword enables zero-allocation reductions of an already initialized `isbits` variable. It supports tuples of associative operations with their starting variables.
```julia
y1 = 0
y2 = 1
@batch reduction=((+, y1), (*, y2)) for i in 1:9
    y1 += i
    y2 *= i
end
```

### Disabling for Nested Parallelism

When running many repetitions of a Polyester-multithreaded function (e.g., in an embarrassingly parallel problem where an outer loop repeatedly executes an inner function that contains `@batch`), it is highly beneficial to disable Polyester's inner threading to avoid task oversubscription.

This is done using the `Polyester.disable_polyester_threads()` context manager. 
**Crucial Rule**: Call this manager *once* outside the `Base.Threads.@threads` loop, not inside it, to avoid unnecessary overhead.

```julia
# DO THIS: Fast!
Polyester.disable_polyester_threads() do
    @threads for i in 1:N
        func_with_batch()
    end
end

# DO NOT DO THIS: Unnecessary overhead inside the loop
@threads for i in 1:N
    Polyester.disable_polyester_threads() do
        func_with_batch()
    end
end
```

---

## Ecosystem Packages Built on Polyester

These packages provide high-level APIs that use Polyester under the hood for low-overhead multithreading. 

- **FastBroadcast.jl**: Provides `@..` for parallel broadcasts. Note that threading is **not** enabled by default; use `@.. thread=true` to enable it. *Warning: on small arrays, `@.. thread=true` can be much slower than standard `@..` due to task overhead. Always benchmark!*
- **Strided.jl**: Provides `@strided` to easily parallelize array operations, broadcasts, and `permutedims` over strided arrays. Strided automatically decides whether threading is beneficial based on the array size, or you can manually control it via `Strided.set_num_threads(n)`.
- **LoopVectorization.jl**: Provides `@tturbo` (or `@turbo thread=true` / `@turbo thread=n`) to combine SIMD vectorization with lightweight Polyester-style multithreading.
