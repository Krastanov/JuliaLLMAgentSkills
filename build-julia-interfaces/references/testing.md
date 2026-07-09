# Test Julia Interfaces Simply

Keep domain behavior outside the interface. Test it directly, then add one focused adapter
test. Use dependency injection through ordinary arguments and `IO`; do not build a mocking
framework for global `ARGS`, `stdin`, `stdout`, terminal state, or Makie internals.

## CLI Logic

```julia
using Test

@testset "greet CLI" begin
    out = IOBuffer()
    err = IOBuffer()

    @test run_cli(["Ada"]; out, err) == 0
    @test String(take!(out)) == "Hello, Ada\n"

    @test run_cli(String[]; out, err) == 2
    @test occursin("usage:", String(take!(err)))
end
```

Call Comonicon command functions as ordinary Julia functions for behavioral tests. Add a
real command invocation only to verify parsing, packaging, or installation. Put that smoke
test in its own file; use `orchestrate-julia-workloads` for safe subprocess mechanics.

## Term Output and Layout

```julia
using Test, Term
using Term.LiveWidgets

@test occursin("ready", string(Panel("ready"; title="Status")))

widget = TextWidget("Hello"; as_panel=true)
rendered = string(frame(widget))
@test occursin("Hello", rendered)
```

Test `frame`, not `play`, in the normal suite. Keep a manual interactive check for raw-mode,
resize, focus, and keyboard behavior when those features matter.

## Makie Recipe Smoke Test

```julia
using CairoMakie, Test
import Makie

fig = Figure()
ax = Axis(fig[1, 1])
plot = curveplot!(ax, 1:3, [1.0, 4.0, 2.0])

Makie.update!(plot; arg2=[2.0, 1.0, 3.0])

mktempdir() do dir
    path = joinpath(dir, "recipe.png")
    save(path, fig)
    @test filesize(path) > 0
end
```

Update positional inputs through `arg1`, `arg2`, and so on; recipe argument names such as
`x` and `y` name converted nodes for use inside the recipe.

Prefer a structural/render smoke test to pixel snapshots. Add reference-image comparison
only when exact visual output is part of the public contract.

## Run Independent Files with ParallelTestRunner

Place independent interface areas in separate files such as `test/cli.jl`, `test/term.jl`,
and `test/makie.jl`, then prefer ParallelTestRunner:

```julia
# test/runtests.jl
using MyPackage
using ParallelTestRunner

runtests(MyPackage, ARGS)
```

Run through Pkg so the intended test environment is active:

```julia
using Pkg
Pkg.test("MyPackage"; test_args=["--jobs=4"])
Pkg.test("MyPackage"; test_args=["cli"])
```

Each test file runs in an isolated module on one of the runner's reusable worker processes.
Do not rely on state established by a different file, and keep files large enough that
scheduling and worker startup do not dominate.

## Sources

- [Julia Test standard library](https://docs.julialang.org/en/v1/stdlib/Test/)
- [ParallelTestRunner stable API](https://juliatesting.github.io/ParallelTestRunner.jl/stable/api/)
- [ParallelTestRunner advanced usage](https://juliatesting.github.io/ParallelTestRunner.jl/stable/advanced/)
- [Makie recipe documentation](https://docs.makie.org/stable/documentation/recipes/)
- [Term live apps](https://fedeclaudi.github.io/Term.jl/stable/live/app_intro/)
