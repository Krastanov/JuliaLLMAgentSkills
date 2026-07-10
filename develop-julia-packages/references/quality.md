# Package Quality Checks

Quality tools supplement behavioral tests. Add or run them only through declared test or quality environments and keep repository-specific configuration.

## Use a Proportional Sequence

1. Run the focused behavioral tests.
2. Run the full package suite.
3. Run Aqua for package hygiene.
4. Run targeted JET analysis for concrete, important calls; run package-wide JET checks only when supported and useful.
5. Collect coverage when the repository reports it.

Do not turn every tool into a blocking check in every Julia-version job. Version-sensitive tools often belong in one compatible quality job.

## Aqua

Declare Aqua as a test dependency with a compat bound. A default check is:

```julia
using Aqua
using PackageName

Aqua.test_all(PackageName)
```

The defaults check areas such as ambiguities, exports, unbound type parameters, stale dependencies, test-project consistency, compat, piracy, and persistent tasks. Prefer defaults. Add a narrow, documented exclusion only after confirming a finding is intentional; do not disable whole categories to reduce noise.

With ParallelTestRunner, place Aqua in its own discovered file and make it self-contained.

## JET

JET releases are closely tied to Julia compiler versions; the current JET v0.11 series supports Julia 1.12. Use a JET release compatible with the quality job's Julia version rather than forcing it into the minimum-version matrix.

Start from a representative concrete entry point:

```julia
using JET
using PackageName

@report_opt PackageName.transform(input)
@report_call PackageName.transform(input)
```

Use `@report_opt` to address inference problems before interpreting cascades from `@report_call`. Package-wide `report_package(PackageName)` is less precise because generic method signatures contain less type information. When supported by the pinned JET version, `JET.test_package(PackageName)` integrates package analysis with `Test`.

Do not enforce a report-count threshold: one fixed report can be replaced by a different regression without changing the count. Do not use `@test_broken` as a permanent zero-report assertion; an unexpected pass is an error by design. Prefer concrete `@test_call`/`@test_opt` checks or a small reviewed allowlist tied to stable findings.

Treat "No errors detected" as evidence only for inferable callees reached from the analyzed entry point, not proof that the package is error-free.

## Coverage

Collect coverage through the package test interface:

```julia
using Pkg
Pkg.test(; coverage = true)
```

Use the repository's existing LocalCoverage, Coverage, Codecov, or Coveralls flow to process results. Avoid adding multiple processors. Coverage identifies unexecuted lines; it does not establish assertion quality.

For local HTML reports, use LocalCoverage only if already declared or intentionally adopted, and follow its current `generate_coverage`/`genhtml` workflow. In CI, `julia-actions/julia-processcoverage` produces `lcov.info` from Julia coverage files.

## Keep Failures Actionable

- Reproduce tool failures under the same Julia and dependency versions as CI.
- Separate a tool compatibility failure from a finding in package code.
- Pin a reasonable compat range for test-only tools.
- Record why any exclusion exists and keep it narrower than the reported method or dependency.

## Sources

- [Aqua stable documentation](https://juliatesting.github.io/Aqua.jl/stable/)
- [JET tutorial and package-analysis limitations](https://aviatesk.github.io/JET.jl/stable/tutorial/)
- [JET compatibility and limitations](https://aviatesk.github.io/JET.jl/)
- [JET error-analysis test integration](https://aviatesk.github.io/JET.jl/stable/jetanalysis/)
- [Julia Test behavior for `@test_broken`](https://docs.julialang.org/en/v1/stdlib/Test/#Broken-Tests)
- [Pkg test and coverage API](https://pkgdocs.julialang.org/v1/api/#Pkg.test)
- [LocalCoverage.jl](https://github.com/JuliaCI/LocalCoverage.jl)
- [julia-processcoverage](https://github.com/julia-actions/julia-processcoverage)
