# Local Coverage with `LocalCoverage.jl`

Use this reference when the task is about local coverage percentages, HTML
coverage reports, `coverage/lcov.info`, or enforcing a minimum coverage target.

## Tooling Environment

Prefer a helper environment so `LocalCoverage` does not become a package
dependency:

```julia
using Pkg
Pkg.activate(temp=true)
Pkg.add("LocalCoverage")
Pkg.develop(path=pwd())
using LocalCoverage
```

If `LocalCoverage` is already available in the current environment, run from
`julia --project=.` and skip the setup above.

## Default Workflow

```julia
cov = generate_coverage("MyPackage")
```

- This runs `Pkg.test(; coverage=true)` for the package.
- It processes the generated `*.cov` files and writes `coverage/lcov.info`.
- Pass `test_args=["integration"]` or similar when the package already filters
  tests through `Pkg.test(...)`.

## HTML Report

`html_coverage` shells out to `genhtml`, so install `lcov` first.

```julia
cov = generate_coverage("MyPackage")
html_coverage(cov; dir="coverage/html", open=false)
```

Open `coverage/html/index.html` in the package checkout.

## Threshold Check

```julia
report_coverage_and_exit("MyPackage"; target_coverage=90)
```

- Exit code `0` means the target was met.
- Exit code `1` means the target was missed.
- Use `print_gaps=true` when the task is to identify uncovered lines.

## Reuse Existing Coverage Data

If another command already generated `*.cov` files, avoid rerunning tests:

```julia
cov = generate_coverage("MyPackage"; run_test=false)
```

## Scope Control

For partial reports, limit coverage processing to specific folders or files:

```julia
cov = generate_coverage("MyPackage";
    folder_list=["src", "ext"],
    file_list=["examples/demo.jl"],
)
```
