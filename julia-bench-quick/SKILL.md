---
name: julia-bench-quick
description: Run quick impromptu benchmarks using @btime or @b macros. Use this skill for ad-hoc performance measurements during development.
---

# Quick Julia Benchmarks

Run quick, impromptu benchmarks during development using BenchmarkTools.jl or
Chairmarks.jl for ad-hoc performance measurements.

## BenchmarkTools.jl (@btime)

The standard benchmarking tool with detailed statistics.

```julia
using BenchmarkTools

v = rand(1000)
@btime sum($v)          # Interpolate with $ to avoid global overhead
```

### In-Place Operations

Use `setup` for functions that modify their input:

```julia
v = rand(1000)
@btime sort!(x) setup=(x=copy($v))  # Fresh copy each run
```

### Comparing Implementations

```julia
v = rand(1000)
@btime sum($v)
@btime reduce(+, $v)
```

## Chairmarks.jl (@b)

Lightweight alternative with automatic interpolation and faster startup.

```julia
using Chairmarks

v = rand(1000)
@b sum(v)               # Automatic interpolation (no $ needed)
@b sort!(x) setup=(x=copy($v))
```

### Comparison Mode

```julia
@b sum(v) reduce(+, v)  # Compare two expressions
```

## Quick Reference

| Tool | Macro | Interpolation | Best For |
|------|-------|---------------|----------|
| BenchmarkTools | `@btime` | Manual (`$`) | Detailed stats |
| Chairmarks | `@b` | Automatic | Quick checks |

## Common Patterns

```julia
# Pure function
@btime f($x)

# Mutating function
@btime f!(y) setup=(y=copy($x))

# Multiple arguments
@btime f($x, $y, $z)

# Keyword arguments
@btime f($x; kwarg=$val)
```

## Reference

- **[Patterns](references/patterns.md)** - Common benchmarking patterns and pitfalls

## Related Skills

- `julia-bench-write` - Writing benchmark suites
- `julia-bench-run` - Running benchmark suites
