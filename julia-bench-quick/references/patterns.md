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