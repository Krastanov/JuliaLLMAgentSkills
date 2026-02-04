# Comparing Benchmark Results

## Save and Load Results

```julia
using BenchmarkTools

# Run and save baseline
results_baseline = run(SUITE)
BenchmarkTools.save("baseline.json", results_baseline)

# Later, load baseline
baseline = BenchmarkTools.load("baseline.json")[1]
```

## Compare Results

```julia
# Run new benchmarks
results_new = run(SUITE)

# Compare using minimum (most stable)
judgment = judge(minimum(results_new), minimum(baseline))

# View results
println(judgment)
```

## Understanding Judgments

```julia
# Judgment categories
# - :improvement - new is faster
# - :regression  - new is slower
# - :invariant   - no significant change

# Access specific benchmark
judgment["core"]["process"]

# Filter regressions
regressions(judgment)

# Filter improvements
improvements(judgment)
```

## Tolerance Settings

```julia
# Default: 5% tolerance
judge(new, old)

# Stricter: 1% tolerance
judge(new, old; time_tolerance=0.01)

# Looser: 10% tolerance
judge(new, old; time_tolerance=0.10)
```

## Comparison Script

```julia
# compare.jl
using BenchmarkTools

include("benchmark/benchmarks.jl")

# Load baseline
baseline = BenchmarkTools.load("baseline.json")[1]

# Run current
current = run(SUITE)

# Compare
judgment = judge(minimum(current), minimum(baseline))

# Report
println("=== Regressions ===")
for (name, j) in leaves(regressions(judgment))
    println("  $name: $(ratio(j).time)x slower")
end

println("\n=== Improvements ===")
for (name, j) in leaves(improvements(judgment))
    println("  $name: $(ratio(j).time)x faster")
end
```

## Best Practices

1. **Use minimum** for comparison (more reliable than mean)
2. **Run on consistent hardware** for valid comparisons
3. **Close other applications** during benchmarking
4. **Use multiple samples** (default behavior)
5. **Set reasonable tolerance** based on noise level
