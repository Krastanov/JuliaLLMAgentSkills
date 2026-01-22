# Quick Benchmark Patterns

## Interpolation ($)

Always interpolate variables to avoid measuring global variable access:

```julia
# Good - measures only the function
v = rand(1000)
@btime sum($v)

# Bad - includes global lookup overhead
@btime sum(v)
```

## Setup for Mutating Functions

Use `setup` to get fresh data each run:

```julia
v = rand(1000)

# Good - fresh copy each iteration
@btime sort!(x) setup=(x=copy($v))

# Bad - sorts already-sorted array after first run
@btime sort!($v)
```

## Avoiding Compilation in Results

Run benchmarks twice - first run includes compilation:

```julia
v = rand(1000)
@btime sum($v)  # Includes compilation
@btime sum($v)  # Pure runtime measurement
```

Or use `@benchmark` for more samples:

```julia
@benchmark sum($v)  # Multiple samples, compilation amortized
```

## Type Stability Checks

Combine with `@code_warntype` for performance analysis:

```julia
@code_warntype f(x)  # Check type stability first
@btime f($x)         # Then measure performance
```

## Memory Allocation

`@btime` shows allocations - zero is ideal for hot paths:

```julia
@btime sum($v)
# Output: 1.234 μs (0 allocations: 0 bytes)
```

## Comparing Alternatives

```julia
v = rand(1000)

println("sum:")
@btime sum($v)

println("reduce:")
@btime reduce(+, $v)

println("manual loop:")
@btime begin
    s = zero(eltype($v))
    for x in $v
        s += x
    end
    s
end
```

## BenchmarkTools vs Chairmarks

| Feature | BenchmarkTools | Chairmarks |
|---------|---------------|------------|
| Interpolation | Manual (`$`) | Automatic |
| Load time | ~2s | ~0.1s |
| Statistics | Detailed | Minimal |
| Comparison | Separate calls | Built-in |
| Best for | Thorough analysis | Quick checks |
