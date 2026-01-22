---
name: julia-makie-recipes
description: Create custom Makie plot types using recipes for reusable, themeable visualizations. Use this skill when implementing plot recipes in Makie extensions.
---

# Julia Makie Recipes

Create custom Makie plot types using recipes. Recipes enable reusable, themeable visualizations
that integrate seamlessly with Makie's ecosystem.

This skill focuses on creating recipes as package extensions. See `julia-pkgextension` for
extension setup.

## Recipe Types

### Type Recipes (Simple Conversions)

Convert custom types to existing plot types:

```julia
function Makie.convert_arguments(P::Type{<:Makie.Heatmap}, data::MyType)
    matrix = extract_matrix(data)
    return Makie.convert_arguments(P, matrix)
end
```

### Full Recipes (Custom Plot Types)

```julia
Makie.@recipe(CircuitPlot, circuit) do scene
    Makie.Theme(;
        gatewidth = 0.8,
        wirecolor = :black,
    )
end
```

## @recipe Macro Syntax

```julia
Makie.@recipe(PlotTypeName, arg1, arg2, ...) do scene
    Makie.Theme(;
        attribute_name = default_value,
    )
end
```

**Generated automatically:**
- Type: `const PlotTypeName{ArgTypes} = Plot{plottypename, ArgTypes}`
- Functions: `plottypename(args...)` and `plottypename!(ax, args...)`

## Implementing plot!

```julia
function Makie.plot!(plot::CircuitPlot)
    circuit = plot[:circuit][]  # Get argument value

    # Access attributes
    gw = plot.gatewidth[]

    # Draw using Makie primitives
    Makie.lines!(plot, xs, ys; color = plot.wirecolor)
    Makie.scatter!(plot, points; markersize = 10)
    Makie.poly!(plot, vertices; color = :blue)
    Makie.text!(plot, x, y; text = "label")

    return plot  # Always return plot!
end
```

**Key points:**
- First argument to primitives is `plot` (the recipe plot object)
- Access attributes with `plot.attribute[]` for current value
- Access attributes with `plot.attribute` (no `[]`) for Observable (reactive)

## Makie Primitives Reference

| Primitive | Use Case |
|-----------|----------|
| `lines!` | Continuous lines, wires |
| `linesegments!` | Disconnected line segments |
| `scatter!` | Points, markers |
| `poly!` | Filled polygons, rectangles |
| `text!` | Labels, annotations |
| `heatmap!` | 2D color grids |

## Checklist

- [ ] Add Makie to `[weakdeps]` and `[extensions]` in Project.toml
- [ ] Create stub functions in main package (with docstrings)
- [ ] Import stub functions in extension
- [ ] Define recipe with `Makie.@recipe`
- [ ] Implement `Makie.plot!` method
- [ ] Always `return plot` from `plot!`
- [ ] Create `_axis` convenience function for complete figures
- [ ] Test with CairoMakie and GLMakie

## Reference

- **[Complete Examples](references/examples.md)** - Full extension example with recipes
- **[Patterns](references/patterns.md)** - Attributes, reactivity, axis configuration

## Related Skills

- `julia-pkgextension` - Package extension setup
- `julia-docs` - Documenting extension functionality
