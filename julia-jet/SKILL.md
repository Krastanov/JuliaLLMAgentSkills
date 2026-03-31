---
name: julia-jet
description: Analyze Julia code with JET.jl for type errors, undefined references, and optimization failures. Use this skill when setting up or running JET analysis on Julia packages.
---

# JET.jl

Use this skill for all JET work. Keep the overview here and load the narrow
reference that matches the task.

## Warning

Use JET only on the latest stable Julia release. Nightly and pre-release Julia
versions often break JET because it depends on compiler internals.

## Environment Rule

- Prefer package-integrated JET runs via `Pkg.test(...; test_args=["jet"])` or
  the package's documented JET arguments.
- Avoid direct `test/runtests.jl` execution unless you are debugging the test
  router or worker behavior.
- If a JET failure appears after dependency churn, inspect stale
  `Manifest.toml` files in the package root, `test/`, and JET subprojects
  before blaming the analyzed code.

## Choose a Mode

- Start with `@report_opt` to find runtime dispatch and captured variables.
- Then use `@report_call` or `report_package` to find type-level errors.

## Quick Start

```julia
using JET

@report_opt sum(Any[1, 2, 3])
@report_call sum("julia")

using MyPackage
report_package(MyPackage; target_modules=[MyPackage])
report_file("my_script.jl")
```

## Filtering

```julia
@report_opt target_modules=(MyPackage,) my_function(args...)
```

Read JET stack traces from the bottom up: the bottom frame is the actual
problem site.

## References

- `references/config.md`
- `references/testing.md`
- `references/error-kinds.md`
- `references/fixing-dispatch.md`

## Related Skills

- `julia-perf` - performance work after dispatch cleanup
- `julia-tests` - test-suite integration patterns
