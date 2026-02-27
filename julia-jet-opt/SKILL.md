---
name: julia-jet-opt
description: Detect optimization failures in Julia code with JET.jl (@report_opt, @test_opt). Use this skill when finding and fixing runtime dispatch, captured variables, and type instabilities.
---

# JET Optimization Analysis

Detect runtime dispatch, captured variables, and other optimization failures
using `@report_opt` and `@test_opt`. Unlike `@code_warntype`, JET
automatically descends the entire call graph.

**WARNING**: Use JET.jl only on the latest stable Julia release.

## Quick Start

```julia
using JET

# Report optimization issues for a call
@report_opt sum(Any[1, 2, 3])

# Focus on your code only (ignore deps)
@report_opt target_modules=(MyPackage,) my_function(args...)
```

## What It Detects

### Runtime Dispatch

The compiler can't resolve the method at compile time and must look it up
at runtime. Caused by type instability.

```julia
n = rand(Int)  # non-const global
sumup(f) = (s = 0; for i in 1:n; s += f(i); end; s)

@report_opt sumup(sin)
# runtime dispatch detected: f(%N::Any)::Any
```

**Fix:** Pass the value as an argument or declare `const`:

```julia
sumup(f, n) = (s = 0; for i in 1:n; s += f(i); end; s)
@report_opt sumup(sin, 100)  # clean
```

### Captured Variables

Closures that capture reassigned variables create heap-allocated "boxes",
preventing optimization:

```julia
function abmult(r::Int)
    if r < 0
        r = -r  # r is now a captured, reassigned variable
    end
    f = x -> x * r
    return f
end
@report_opt abmult(42)
# captured variable `r` detected
```

**Fix:** Use a `let` block to snapshot the value:

```julia
function abmult(r::Int)
    if r < 0
        r = -r
    end
    f = let r = r
        x -> x * r
    end
    return f
end
@report_opt abmult(42)  # clean
```

### Non-Const Global Variables

Any read from a non-const global is type-unstable:

```julia
config = Dict(:verbose => true)
f() = config[:verbose] ? println("hi") : nothing
@report_opt f()  # runtime dispatch on config access
```

**Fix:** Use `const` or pass as argument.

## Filtering Noise

### `target_modules` — Focus on Your Code

```julia
# Ignore dispatch inside println, which is intentionally dynamic
@report_opt target_modules=(@__MODULE__,) compute(30)
```

### `function_filter` — Skip Specific Functions

```julia
# Skip analysis of calls to println
@report_opt function_filter=(@nospecialize(f) -> f !== println) my_function(args...)
```

### `skip_noncompileable_calls` (default: `true`)

By default, JET skips dispatch analysis inside calls that can't be
compiled with concrete types (since Julia's runtime dispatch handles
those). Set to `false` to be stricter:

```julia
@report_opt skip_noncompileable_calls=false my_function(args...)
```

## Test Integration

```julia
using Test, JET

@test_opt target_modules=(MyPackage,) my_function(1, 2.0)
@test_opt broken=true my_unstable_function(args...)

@testset "Type stability" begin
    @test_opt my_function(1)      # should pass
    @test_opt my_function(1, 2.0) # should pass
end
```

## Working with Reports

```julia
report = @report_opt my_function(args...)
rpts = JET.get_reports(report)

# Deduplicate reports reaching the same dispatch site
urpts = unique(JET.reportkey, rpts)
```

## Relationship to `@code_warntype`

| Feature | `@code_warntype` | `@report_opt` |
|---------|-----------------|---------------|
| Scope | Single function | Entire call graph |
| Output | Full IR (noisy) | Only problems |
| Depth | Shallow | Recursive |
| Use for | Understanding inference | Finding all dispatch |

Use `@report_opt` to *find* problems, then `@code_warntype` to *understand*
them in detail if needed.

## Reference

- **[Fixing Dispatch](references/fixing-dispatch.md)** — Patterns for eliminating runtime dispatch

## Related Skills

- `julia-jet` — Overview and quick start
- `julia-jet-errors` — Error analysis (`@report_call`)
- `julia-perf` — Performance optimization workflow
- `julia-bench-quick` — Benchmarking to verify fixes
