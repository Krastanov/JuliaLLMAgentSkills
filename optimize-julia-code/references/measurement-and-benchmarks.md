# Measurement and Benchmarks

## Establish the baseline

Test the result before timing it. Choose inputs that represent the production sizes, shapes, and types. Record the Julia version, project environment, thread counts, and hardware when results must be compared later.

Warm the exact call once before measuring steady-state execution. A first call can include compilation:

```julia
result = target(args...)       # compile and verify
@time target(args...)         # coarse second-run check
```

Use `@time` to orient the investigation, not to support small performance claims.

## Use BenchmarkTools

Interpolate values from the surrounding scope so global lookup is not part of the benchmark:

```julia
using BenchmarkTools

x = rand(10_000)
@btime sum($x)
trial = @benchmark sum($x)
```

Use setup code and one evaluation per sample when the operation mutates its input:

```julia
@benchmark sort!(work) setup=(work = copy($x)) evals=1
```

Place setup work outside the measured expression. Verify that setup recreates the state the real call receives.

Use a `BenchmarkGroup` when the same performance contract needs repeated checks:

```julia
const SUITE = BenchmarkGroup()
SUITE["sum"] = @benchmarkable sum($x)
results = run(SUITE)
```

## Interpret conservatively

- Inspect the distribution, allocations, and samples; do not compare only one wall-clock observation.
- Compare in the same environment and on comparable hardware.
- Change one factor at a time, including thread counts and input layout.
- Treat small changes near machine noise as inconclusive.
- Benchmark all important input regimes; specialization, cache behavior, and algorithmic scaling can change the result.
- Keep a sequential or previous implementation until the replacement is verified and consistently faster.

## Sources

- [Julia performance tips](https://docs.julialang.org/en/v1/manual/performance-tips/)
- [BenchmarkTools manual](https://juliaci.github.io/BenchmarkTools.jl/stable/manual/)
