# Complete Benchmark Example

## benchmark/Project.toml

```toml
[deps]
BenchmarkTools = "6e4b80f9-dd63-53aa-95a3-0cdb28fa8baf"
MyPackage = "your-package-uuid"
StableRNGs = "860ef19b-820b-49d6-a774-d7a799459cd3"
```

## benchmark/benchmarks.jl

```julia
using BenchmarkTools
using MyPackage
using MyPackage: internal_function, InternalType
using StableRNGs

const SUITE = BenchmarkGroup()

# Reproducible random data
rng = StableRNG(42)

# Helper functions to create test data
function make_small_data(n::Int)
    return MyType(rand(rng, n))
end

function make_large_data(n::Int)
    return MyType(rand(rng, n))
end

# Pre-create constant test data
const small_data = make_small_data(100)
const large_data = make_large_data(1000)

# Core operations benchmarks
SUITE["core"] = BenchmarkGroup(["core"])
SUITE["core"]["process_small"] = @benchmarkable process($small_data)
SUITE["core"]["process_large"] = @benchmarkable process($large_data)

# Scaling benchmarks
SUITE["scaling"] = BenchmarkGroup(["scaling"])
for n in [10, 100, 1000]
    SUITE["scaling"]["$n"] = @benchmarkable process(d) setup=(d=make_small_data($n)) evals=1
end

# In-place operations (use evals=1 and setup)
SUITE["inplace"] = BenchmarkGroup(["inplace"])
SUITE["inplace"]["modify_100"] = @benchmarkable modify!(d) setup=(d=make_small_data(100)) evals=1
SUITE["inplace"]["modify_1000"] = @benchmarkable modify!(d) setup=(d=make_large_data(1000)) evals=1

# Algorithm variants
SUITE["algorithms"] = BenchmarkGroup(["algorithms"])
SUITE["algorithms"]["v1_100"] = @benchmarkable algorithm_v1(d) setup=(d=make_small_data(100)) evals=1
SUITE["algorithms"]["v2_100"] = @benchmarkable algorithm_v2(d) setup=(d=make_small_data(100)) evals=1
```

## Running Benchmarks

```bash
# Run all benchmarks
julia -tauto --project=benchmark -e '
    include("benchmark/benchmarks.jl")
    run(SUITE)'

# Run specific group
julia -tauto --project=benchmark -e '
    include("benchmark/benchmarks.jl")
    run(SUITE["core"])'

# Tune and run (more accurate but slower)
julia -tauto --project=benchmark -e '
    include("benchmark/benchmarks.jl")
    tune!(SUITE)
    run(SUITE)'
```
