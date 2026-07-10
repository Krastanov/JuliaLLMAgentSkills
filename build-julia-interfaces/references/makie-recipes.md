# Makie 0.24 Recipes

Choose a type recipe when a custom type can become arguments of an existing plot. Choose a
full recipe only when the visualization combines plots or needs its own attributes and plot
function.

## Type Conversion

```julia
function Makie.convert_arguments(P::Type{<:Makie.Scatter}, data::MyPoints)
    points = Makie.Point2f.(data.x, data.y)
    return Makie.convert_arguments(P, points)
end
```

`convert_arguments` must return a tuple; delegating to Makie's existing conversion preserves
the plot's canonical argument format. Prefer a conversion trait such as `Makie.PointBased`
when the same conversion is valid for a documented family of plots.

## Full Reactive Recipe

Target Makie 0.24's recipe syntax and ComputeGraph:

```julia
Makie.@recipe CurvePlot (x, y) begin
    color = :steelblue
    linewidth = 2
end

function Makie.plot!(plot::CurvePlot)
    Makie.map!(plot.attributes, [:x, :y], :points) do x, y
        return Makie.Point2f.(x, y)
    end

    Makie.lines!(
        plot,
        plot.points;
        color=plot.color,
        linewidth=plot.linewidth,
    )
    return plot
end
```

Pass graph nodes such as `plot.points` and `plot.color` to child plots. Do not unwrap inputs
with `[]`, build concrete children from the snapshot, and then claim the recipe is reactive.
When several derived arrays must change together, produce them in one computation so a child
never observes mismatched lengths.

Use `Makie.preferred_axis_type` or `Makie.preferred_axis_attributes` only when the recipe has
a real axis requirement. Let callers configure an ordinary `Axis` otherwise.

## Put Package Recipes in Extensions

For optional plotting support:

1. Define and document empty public plotting functions in the main package.
2. Add Makie as a weak dependency and map a package extension to it.
3. Import the public functions and implement the recipe in the extension.
4. Depend on Makie, not a particular backend, in the extension.
5. Set compat only for versions actually tested. Do not copy a broad list of Makie minors.
6. Test with CairoMakie as the deterministic headless backend; add GLMakie testing only when
   backend-specific interactive behavior matters.

Do not add pre-0.24 Observable mutation code to a new recipe. It remains a compatibility
technique for an already-supported older Makie release and can introduce synchronization
problems that ComputeGraph avoids.

## Sources

- [Makie stable recipe documentation](https://docs.makie.org/stable/documentation/recipes/)
- [Makie conversion pipeline](https://docs.makie.org/stable/explanations/conversion_pipeline.html)
- [Makie Observables and the 0.24 ComputeGraph note](https://docs.makie.org/stable/explanations/observables.html)
- [Pkg package extensions](https://pkgdocs.julialang.org/v1/creating-packages/#Conditional-loading-of-code-in-packages-(Extensions))
