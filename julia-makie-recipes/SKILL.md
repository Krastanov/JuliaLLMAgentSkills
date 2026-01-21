# Julia Makie Recipes

Create custom Makie plot types using recipes. Recipes enable reusable, themeable visualizations
that integrate seamlessly with Makie's ecosystem.

This skill focuses on creating recipes as package extensions. See `julia-pkgextension` for
extension setup.

## Recipe Types

### Type Recipes (Simple Conversions)

Convert custom types to existing plot types via `convert_arguments`:

```julia
# Convert MyType to work with heatmap
function Makie.convert_arguments(P::Type{<:Makie.Heatmap}, data::MyType)
    matrix = extract_matrix(data)
    return Makie.convert_arguments(P, matrix)
end
```

### Full Recipes (Custom Plot Types)

Create new plot functions with `@recipe` macro:

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
        # Attribute defaults
        attribute_name = default_value,
        another_attr = :default,
    )
end
```

**Generated automatically:**
- Type: `const PlotTypeName{ArgTypes} = Plot{plottypename, ArgTypes}`
- Functions: `plottypename(args...)` and `plottypename!(ax, args...)`
- Lowercase function name derived from type name

**Argument access in `plot!`:**
- `plot[:arg1]` or `plot.arg1` - Observable for argument
- `plot[:arg1][]` or `plot.arg1[]` - Current value

## Implementing plot!

```julia
function Makie.plot!(plot::CircuitPlot)
    # Access arguments (as Observables)
    circuit = plot[:circuit][]

    # Access attributes
    gw = plot.gatewidth[]

    # Draw using Makie primitives
    Makie.lines!(plot, xs, ys; color = plot.wirecolor)
    Makie.scatter!(plot, points; markersize = 10)
    Makie.poly!(plot, vertices; color = :blue)
    Makie.text!(plot, x, y; text = "label")

    return plot
end
```

**Key points:**
- First argument to primitives is `plot` (the recipe plot object)
- Access attributes with `plot.attribute[]` for current value
- Access attributes with `plot.attribute` (no `[]`) for Observable (reactive)
- Always `return plot`

## Complete Extension Example

### Project.toml Setup

```toml
# Main package Project.toml
[weakdeps]
Makie = "ee78f7c6-11fb-53f2-987a-cfe4a2b5a57a"

[extensions]
MyPackageMakieExt = "Makie"

[compat]
Makie = "0.20, 0.21, 0.22, 0.23, 0.24"
```

### Main Package Stubs

```julia
# src/plotting.jl (included in main module)

"""
    circuitplot(circuit; kwargs...)

Plot a quantum circuit. Requires Makie to be loaded.

See also: [`circuitplot!`](@ref), [`circuitplot_axis`](@ref)
"""
function circuitplot end

"""
    circuitplot!(ax, circuit; kwargs...)

Add a circuit plot to an existing axis.
"""
function circuitplot! end

"""
    circuitplot_axis(subfig, circuit; kwargs...)

Create a complete figure panel with circuit plot and configured axis.
Returns `(subfig, axis, plot)`.
"""
function circuitplot_axis end
```

### Extension Module

```julia
# ext/MyPackageMakieExt/MyPackageMakieExt.jl
module MyPackageMakieExt

using Makie
using MyPackage
using MyPackage: Circuit, affectedqubits, InternalType

# Import functions to extend
import MyPackage: circuitplot, circuitplot!, circuitplot_axis

# Define the recipe
Makie.@recipe(CircuitPlot, circuit) do scene
    Makie.Theme(;
        # Dimensions
        gatewidth = 0.8,
        qubitspacing = 1.0,
        # Colors
        wirecolor = :black,
        wirelinewidth = 1.0,
        gatecolor = Makie.RGB(0.2, 0.6, 0.2),
        measurementcolor = Makie.RGB(0.8, 0.2, 0.2),
        # Text
        fontsize = 0.5,
        textcolor = :white,
    )
end

function Makie.plot!(plot::CircuitPlot)
    circuit = plot[:circuit][]

    if isempty(circuit)
        return plot
    end

    gw = plot.gatewidth[]
    qs = plot.qubitspacing[]

    # Draw qubit wires
    all_qubits = affectedqubits(circuit)
    for q in minimum(all_qubits):maximum(all_qubits)
        y = q * qs
        Makie.lines!(plot, [0.5, length(circuit) + 0.5], [y, y];
            color = plot.wirecolor[],
            linewidth = plot.wirelinewidth[]
        )
    end

    # Draw gates
    for (idx, op) in enumerate(circuit)
        qubits = affectedqubits(op)
        x_center = idx
        y_min = minimum(qubits) * qs - 0.3 * qs
        y_max = maximum(qubits) * qs + 0.3 * qs

        # Rectangle for gate
        Makie.poly!(plot,
            Makie.Point2f[
                (x_center - gw/2, y_min),
                (x_center + gw/2, y_min),
                (x_center + gw/2, y_max),
                (x_center - gw/2, y_max)
            ];
            color = plot.gatecolor[],
            strokecolor = :black,
            strokewidth = 1
        )

        # Gate label
        Makie.text!(plot, x_center, (y_min + y_max) / 2;
            text = gate_label(op),
            align = (:center, :center),
            fontsize = plot.fontsize[],
            color = plot.textcolor[],
            markerspace = :data
        )
    end

    return plot
end

# Convenience function for complete figure
function circuitplot_axis(subfig, circuit::Circuit; kwargs...)
    ax = Makie.Axis(subfig[1, 1])
    p = circuitplot!(ax, circuit; kwargs...)

    Makie.hidedecorations!(ax)
    Makie.hidespines!(ax)
    ax.aspect = Makie.DataAspect()

    # Set axis limits
    if !isempty(circuit)
        all_qubits = affectedqubits(circuit)
        Makie.xlims!(ax, 0, length(circuit) + 1)
        Makie.ylims!(ax, minimum(all_qubits) - 0.5, maximum(all_qubits) + 0.5)
    end

    return (subfig, ax, p)
end

end # module
```

## Attribute Patterns

### Theme Inheritance

```julia
Makie.@recipe(MyPlot, data) do scene
    Makie.Theme(;
        # Inherit from scene theme with fallback
        colormap = Makie.@inherit colormap :viridis,
        # Direct default
        linewidth = 2,
    )
end
```

### Color Definitions

```julia
# Named colors
color = :red
color = :black

# RGB values
color = Makie.RGB(0.2, 0.6, 0.2)
color = Makie.RGBA(0.2, 0.6, 0.2, 0.8)

# Categorical colormap
colormap = Makie.cgrad([
    :lightgray,
    Makie.RGB(27/255, 158/255, 119/255),
    Makie.RGB(217/255, 95/255, 2/255),
], 3, categorical = true)
```

## Reactive Updates with Observables

For plots that update when data changes:

```julia
function Makie.plot!(plot::MyPlot)
    # Create Observable containers
    points = Makie.Observable(Point2f[])
    colors = Makie.Observable(Float64[])

    # Update function
    function update_plot(data)
        empty!(points[])
        empty!(colors[])
        for item in data
            push!(points[], compute_position(item))
            push!(colors[], compute_color(item))
        end
        Makie.notify(points)
        Makie.notify(colors)
    end

    # Initial population
    update_plot(plot[:data][])

    # Register for updates
    Makie.Observables.onany(update_plot, plot[:data])

    # Create graphics
    Makie.scatter!(plot, points; color = colors)

    return plot
end
```

## Alternative @recipe Syntax

For more complex setups:

```julia
# Separate type name from arguments
Makie.@recipe(
    function (scene)
        Makie.Theme(;
            xzcomponents = :together,
            colormap = :viridis,
        )
    end,
    StabilizerPlot,      # Type name
    stabilizer           # Argument name
)

function Makie.plot!(plot::StabilizerPlot)
    s = plot[:stabilizer][]
    # ... implementation
end
```

## Specializing by Argument Type

Handle different input types differently:

```julia
# General recipe
Makie.@recipe(DataPlot, data) do scene
    Makie.Theme(; colormap = :viridis)
end

# Specialize for 2D arrays
const DataPlot2D = DataPlot{Tuple{<:AbstractMatrix}}

function Makie.plot!(plot::DataPlot2D)
    Makie.heatmap!(plot, plot[:data][])
    return plot
end

# Specialize for 3D arrays
const DataPlot3D = DataPlot{Tuple{<:AbstractArray{<:Any, 3}}}

function Makie.plot!(plot::DataPlot3D)
    Makie.volume!(plot, plot[:data][])
    return plot
end
```

## Helper Functions Pattern

Keep helper functions in the extension:

```julia
module MyPackageMakieExt

# ... recipe definition ...

# Helper: determine color based on type
function gate_color(op, plot)
    if is_measurement(op)
        return plot.measurementcolor[]
    elseif is_rotation(op)
        return plot.rotationcolor[]
    else
        return plot.defaultcolor[]
    end
end

# Helper: generate label
function gate_label(op)
    # ... logic ...
end

# Use in plot!
function Makie.plot!(plot::CircuitPlot)
    for op in plot[:circuit][]
        color = gate_color(op, plot)
        label = gate_label(op)
        # ... draw ...
    end
    return plot
end

end
```

## Axis Configuration Patterns

### Basic Configuration

```julia
function myplot_axis(subfig, data; kwargs...)
    ax = Makie.Axis(subfig[1, 1])
    p = myplot!(ax, data; kwargs...)

    Makie.hidedecorations!(ax)
    Makie.hidespines!(ax)
    ax.aspect = Makie.DataAspect()

    return (subfig, ax, p)
end
```

### With Colorbar

```julia
function myplot_axis(subfig, data; colorbar=true, kwargs...)
    ax = Makie.Axis(subfig[1, 1])
    p = myplot!(ax, data; kwargs...)

    Makie.hidedecorations!(ax)
    Makie.hidespines!(ax)
    ax.aspect = Makie.DataAspect()

    if colorbar
        Makie.Colorbar(subfig[1, 2], p,
            ticks = (0:3, ["I", "X", "Z", "Y"]),
            vertical = true
        )
    end

    return (subfig, ax, p)
end
```

### With Interactivity

```julia
function myplot_axis(ax::Makie.AbstractAxis, data; datainspector=true, kwargs...)
    p = myplot!(ax, data; kwargs...)

    ax.aspect = Makie.DataAspect()
    Makie.hidedecorations!(ax)
    Makie.hidespines!(ax)

    if datainspector
        Makie.DataInspector(ax.parent)
    end

    return (ax.parent, ax, p)
end
```

## Makie Primitives Reference

| Primitive | Use Case |
|-----------|----------|
| `lines!` | Continuous lines, wires |
| `linesegments!` | Disconnected line segments |
| `scatter!` | Points, markers |
| `poly!` | Filled polygons, rectangles |
| `text!` | Labels, annotations |
| `heatmap!` | 2D color grids |
| `mesh!` | 3D surfaces |

## Checklist

- [ ] Add Makie to `[weakdeps]` and `[extensions]` in Project.toml
- [ ] Create stub functions in main package (with docstrings)
- [ ] Import stub functions in extension: `import MyPackage: plotfunc`
- [ ] Define recipe with `Makie.@recipe`
- [ ] Implement `Makie.plot!` method
- [ ] Access arguments as `plot[:argname][]`
- [ ] Access attributes as `plot.attrname[]`
- [ ] Always `return plot` from `plot!`
- [ ] Create `_axis` convenience function for complete figures
- [ ] Test with CairoMakie and GLMakie

## Related Skills

- `julia-pkgextension` - Package extension setup
- `julia-docs` - Documenting extension functionality
- `julia-tests` - Testing with tagged test items
