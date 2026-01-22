# Complete Extension Example

## Project.toml Setup

```toml
[weakdeps]
Makie = "ee78f7c6-11fb-53f2-987a-cfe4a2b5a57a"

[extensions]
MyPackageMakieExt = "Makie"

[compat]
Makie = "0.20, 0.21, 0.22, 0.23, 0.24"
```

## Main Package Stubs

```julia
# src/plotting.jl (included in main module)

"""
    circuitplot(circuit; kwargs...)

Plot a quantum circuit. Requires Makie to be loaded.
"""
function circuitplot end

"""
    circuitplot!(ax, circuit; kwargs...)

Add a circuit plot to an existing axis.
"""
function circuitplot! end

"""
    circuitplot_axis(subfig, circuit; kwargs...)

Create a complete figure panel with circuit plot.
Returns `(subfig, axis, plot)`.
"""
function circuitplot_axis end
```

## Extension Module

```julia
# ext/MyPackageMakieExt/MyPackageMakieExt.jl
module MyPackageMakieExt

using Makie
using MyPackage
using MyPackage: Circuit, affectedqubits

import MyPackage: circuitplot, circuitplot!, circuitplot_axis

Makie.@recipe(CircuitPlot, circuit) do scene
    Makie.Theme(;
        gatewidth = 0.8,
        qubitspacing = 1.0,
        wirecolor = :black,
        wirelinewidth = 1.0,
        gatecolor = Makie.RGB(0.2, 0.6, 0.2),
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

function circuitplot_axis(subfig, circuit::Circuit; kwargs...)
    ax = Makie.Axis(subfig[1, 1])
    p = circuitplot!(ax, circuit; kwargs...)

    Makie.hidedecorations!(ax)
    Makie.hidespines!(ax)
    ax.aspect = Makie.DataAspect()

    if !isempty(circuit)
        all_qubits = affectedqubits(circuit)
        Makie.xlims!(ax, 0, length(circuit) + 1)
        Makie.ylims!(ax, minimum(all_qubits) - 0.5, maximum(all_qubits) + 0.5)
    end

    return (subfig, ax, p)
end

end # module
```
