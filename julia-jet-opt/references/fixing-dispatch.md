# Fixing Runtime Dispatch

Common patterns for eliminating runtime dispatch detected by `@report_opt`.

## Non-Const Globals

```julia
# BAD — runtime dispatch on every access
threshold = 0.5
f(x) = x > threshold ? x : zero(x)

# GOOD — const global
const THRESHOLD = 0.5
f(x) = x > THRESHOLD ? x : zero(x)

# GOOD — pass as argument
f(x, threshold) = x > threshold ? x : zero(x)
```

## Untyped Containers

```julia
# BAD — Any elements cause dispatch
data = Any[1, 2.0, 3]
sum_data() = sum(data)

# GOOD — concrete element types
data = [1.0, 2.0, 3.0]
sum_data() = sum(data)
```

## Captured Variables in Closures

When a variable is captured *and reassigned*, Julia boxes it:

```julia
# BAD — r is reassigned and captured → boxed
function make_mult(r::Int)
    if r < 0; r = -r; end
    x -> x * r
end

# GOOD — let block snapshots the value
function make_mult(r::Int)
    if r < 0; r = -r; end
    let r = r
        x -> x * r
    end
end

# GOOD — type-annotate the captured variable
function make_mult(r0::Int)
    r::Int = r0 < 0 ? -r0 : r0
    x -> x * r
end
```

## Abstract Fields in Structs

```julia
# BAD — abstract field type
struct Wrapper
    value  # implicitly ::Any
end
f(w::Wrapper) = w.value + 1  # dispatch on Any

# GOOD — parametric type
struct Wrapper{T}
    value::T
end
f(w::Wrapper) = w.value + 1  # specialized per T
```

## Union Return Types

```julia
# BAD — returns Int or Float64 depending on value
pos(x) = x < 0 ? 0 : x

# GOOD — consistent return type
pos(x) = x < 0 ? zero(x) : x
```

## Function-Typed Arguments

Julia doesn't specialize on `Function` by default:

```julia
# BAD — f is not specialized
apply(f, x) = f(x)

# GOOD — type parameter forces specialization
apply(f::F, x) where {F} = f(x)
```

## Using `target_modules` to Triage

When `@report_opt` returns many reports, focus on your code first:

```julia
@report_opt target_modules=(MyPackage,) my_function(args...)
```

Reports from dependencies are usually intentional design choices (like
`println` using dynamic dispatch). Only investigate them if they're in
your hot path.

## Using `function_filter` to Skip Known-Dynamic Functions

```julia
# Skip dispatch analysis for println and show
@report_opt function_filter=(@nospecialize(f) -> f !== println && f !== show) my_function(args...)
```

## Verification Workflow

After fixing a dispatch issue:

1. Re-run `@report_opt` to confirm it's gone
2. Run `@btime` to verify the performance improved
3. Optionally check with `@code_warntype` for deeper understanding
