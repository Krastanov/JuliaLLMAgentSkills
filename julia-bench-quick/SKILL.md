---
name: julia-bench-quick
description: Run quick impromptu benchmarks using @btime macro. Use this skill for ad-hoc performance measurements during development.
---

# Quick Julia Benchmarks

Run short, ad-hoc benchmarks during development.

## BenchmarkTools (@btime)

```julia
using BenchmarkTools

v = rand(1000)
@btime sum($v)
@btime sort!(x) setup=(x=copy($v))
```

## Notes

- Interpolate with `$` in BenchmarkTools.
- Use `setup` for mutating functions.

## Reference

- **[Patterns](references/patterns.md)** - Interpolation, setup, comparison patterns

## Related Skills

- `julia-bench-write` - Writing benchmark suites
- `julia-bench-run` - Running benchmark suites
