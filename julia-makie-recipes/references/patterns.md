# Recipe Patterns

## Table of Contents

- [Attribute Patterns](#attribute-patterns)
- [Reactive Updates with Observables](#reactive-updates-with-observables)
- [Alternative @recipe Syntax](#alternative-recipe-syntax)
- [Specializing by Argument Type](#specializing-by-argument-type)
- [Axis Configuration Patterns](#axis-configuration-patterns)
- [Color Definitions](#color-definitions)

## Attribute Patterns

### Theme Inheritance

```julia
Makie.@recipe(MyPlot, data) do scene
    Makie.Theme(;
        colormap = Makie.@inherit colormap :viridis,
        linewidth = 2,
    )
end
```

## Reactive Updates with Observables

For plots that update when data changes:

```julia
function Makie.plot!(plot::MyPlot)
    points = Makie.Observable(Point2f[])
    colors = Makie.Observable(Float64[])

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

    update_plot(plot[:data][])
    Makie.Observables.onany(update_plot, plot[:data])

    Makie.scatter!(plot, points; color = colors)

    return plot
end
```

## Alternative @recipe Syntax

```julia
Makie.@recipe(
    function (scene)
        Makie.Theme(;
            xzcomponents = :together,
            colormap = :viridis,
        )
    end,
    StabilizerPlot,
    stabilizer
)

function Makie.plot!(plot::StabilizerPlot)
    s = plot[:stabilizer][]
    # ... implementation
end
```

## Specializing by Argument Type

```julia
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

## Color Definitions

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
