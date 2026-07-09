# Inference and Data Layout

## Inspect inference at the hot call

Run inference tools on the concrete call identified by profiling:

```julia
@code_warntype target(args...)
```

Trace important values from the first uncertain result into the hot kernel. Red output is a diagnostic lead, not proof of a performance bug; small unions and cold paths may be harmless.

Use a function barrier when dynamic setup chooses types or shapes:

```julia
function outer(raw)
    prepared = prepare(raw)          # dynamic boundary
    return kernel(prepared)          # specialized hot function
end
```

When the project already uses JET, use `@report_opt` after checking that the installed JET release supports the active Julia release. Treat reports outside the measured path as lower priority.

## Keep storage inferable

- Parameterize hot struct fields instead of storing them as `Any`, `Function`, or a broad abstract type when the concrete field type is stable per object.
- Prefer concretely typed containers for homogeneous hot data.
- Keep return types inferable across hot control-flow branches when practical.
- Avoid changing a hot local variable among unrelated types.
- Annotate a value taken from genuinely untyped storage only when its runtime type is known.

Do not add concrete argument annotations as a performance ritual. Julia normally specializes a method for the actual argument types. Use argument annotations for dispatch, correctness, or clarity, and accept the most general interface the algorithm supports. Avoid return-type annotations merely for speed; they convert the result rather than fixing unstable computation.

## Improve data movement

- Traverse dense arrays in memory order; for Julia matrices, vary the first index fastest.
- Preallocate repeated outputs when reuse is safe and measured.
- Use views to avoid copies when subsequent access remains efficient.
- Copy an irregular or noncontiguous view when repeated contiguous computation repays the copy.
- Fuse broadcasts to remove temporaries, but unfuse a repeated subexpression when recomputing it costs more than materializing it once.
- Prefer a simpler algorithm or less data movement before changing representation.

Benchmark layout changes across realistic sizes. A layout that helps one kernel can hurt another or increase compilation and memory costs.

## Sources

- [Julia performance tips: type inference and arrays](https://docs.julialang.org/en/v1/manual/performance-tips/)
- [Julia functions: argument-type declarations](https://docs.julialang.org/en/v1/manual/functions/#Argument-type-declarations)
- [JET tutorial](https://aviatesk.github.io/JET.jl/stable/tutorial/)
