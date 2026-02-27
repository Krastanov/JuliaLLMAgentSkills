---
name: julia-jet
description: Analyze Julia code with JET.jl for type errors, undefined references, and optimization failures. Use this skill when setting up or running JET analysis on Julia packages.
---

# JET.jl Static Analysis

JET.jl leverages Julia's compiler inference to detect type errors and
optimization failures *without running your code*. It analyzes all reachable
branches and call chains automatically.

**WARNING**: Use JET.jl only on the latest stable Julia release. Pre-release
versions and old releases may produce incorrect results or fail entirely,
because JET depends heavily on compiler internals that change between versions.

## Two Analysis Modes

| Mode | Entry points | Detects |
|------|-------------|---------|
| **Error analysis** | `@report_call`, `report_call`, `report_package` | `MethodError`, undefined refs, bad field access, `BoundsError` |
| **Optimization analysis** | `@report_opt`, `report_opt` | Runtime dispatch, captured variables, unresolvable calls |

**Use `@report_opt` first**, then `@report_call`. JET works best on
type-stable code — iron out dispatch issues before looking for type errors.

## Quick Start

```julia
using JET

# Check a single call for type errors
@report_call sum("julia")

# Check a single call for optimization issues
@report_opt sum(Any[1, 2, 3])

# Check an entire package
using MyPackage
report_package(MyPackage; target_modules=[MyPackage])
```

## Filtering Reports

Use `target_modules` to focus on your code and ignore dependency noise:

```julia
# Only report problems originating in MyPackage
@report_call target_modules=(MyPackage,) my_function(args...)

# Ignore problems from Base
@report_call ignored_modules=(Base,) my_function(args...)

# Match any frame in the call chain (not just the innermost)
@report_call ignored_modules=(AnyFrameModule(Base),) my_function(args...)
```

## Interpreting Output

JET prints a **stack trace for each detected problem**. Read bottom-to-top:

```
═════ 2 possible errors found ═════
┌ @ REPL[1]:1 sum(chars)
│┌ @ reducedim.jl:0 +(::Char, ::Char)
││ no matching method found `+(::Char, ::Char)`: ...
│└────────────────
│┌ @ reduce.jl:0 zero(::Type{Char})
││ no matching method found `zero(::Type{Char})`: ...
│└────────────────
```

- The **innermost frame** (bottom) shows the problematic call and the error kind
- Outer frames show **how JET reached** that call
- `x/y union split` means only some union members cause the error

## Working with Results Programmatically

```julia
result = @report_call my_function(args...)
reports = JET.get_reports(result)
length(reports)  # number of problems found

# Deduplicate reports that reach the same dispatch site
unique_reports = unique(JET.reportkey, reports)
```

## Reference

- **[Testing with JET](references/testing.md)** — Package-level test patterns and CI integration
- **[Configuration](references/config.md)** — All configuration options

## Related Skills

- `julia-jet-errors` — Error analysis details (`@report_call`, error kinds, fixes)
- `julia-jet-opt` — Optimization analysis details (`@report_opt`, dispatch, captures)
- `julia-perf` — Performance optimization workflow
- `julia-tests-write` — Writing tests (includes JET test template)
