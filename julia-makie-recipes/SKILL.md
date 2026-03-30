---
name: julia-makie-recipes
description: "Define plot attributes, implement argument conversion, add default themes, and register custom plot types using Makie @recipe macro for reusable, themeable visualizations. Use this skill when creating custom plots in Julia, implementing Makie recipes, building plotting extensions, or converting custom types to Makie primitives."
---

# Julia Makie Recipes

Create custom Makie plot types using recipes. This skill assumes recipes live
in package extensions (see `julia-package-dev`).

## Type Recipes (Conversions)

```julia
function Makie.convert_arguments(P::Type{<:Makie.Heatmap}, data::MyType)
    matrix = extract_matrix(data)
    return Makie.convert_arguments(P, matrix)
end
```

## Full Recipes (Custom Plots)

```julia
Makie.@recipe(CircuitPlot, circuit) do scene
    Makie.Theme(;
        gatewidth = 0.8,
        wirecolor = :black,
    )
end
```

## Implement plot!

```julia
function Makie.plot!(plot::CircuitPlot)
    circuit = plot[:circuit][]
    Makie.lines!(plot, xs, ys; color = plot.wirecolor)
    Makie.scatter!(plot, points; markersize = 10)
    return plot
end
```

## Notes

- Pass the recipe plot object as the first argument to primitives.
- Use `plot.attr[]` for the current value and `plot.attr` for Observables.

## Checklist

- [ ] Add Makie as a weak dep via Pkg (`pkg> add --weak Makie`)
- [ ] Add `[extensions]` mapping for `{Package}MakieExt`
- [ ] Create stub functions in the main package (with docstrings)
- [ ] Implement the recipe and `Makie.plot!` in the extension
- [ ] Test with CairoMakie and GLMakie
- [ ] Verify: `using CairoMakie, MyPkg; circuitplot(test_data)` renders without errors

## Reference

- **[Complete Examples](references/examples.md)** - Full extension example with recipes
- **[Patterns](references/patterns.md)** - Attributes, reactivity, axis configuration

## Related Skills

- `julia-package-dev` - Package extension setup
- `julia-docs` - Documenting extension functionality
