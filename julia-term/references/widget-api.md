# Widget API Reference

Full `AbstractWidget` interface for building custom Term.jl widgets.

## AbstractWidget Interface

### Required Struct Fields

```julia
mutable struct MyWidget <: AbstractWidget
    internals::WidgetInternals     # manages state, size, callbacks
    controls::AbstractDict          # Dict{Union{KeyInput, Char}, Function}
    # ... custom fields
end
```

### Required Methods

```julia
# Render the widget -- called each frame
frame(w::MyWidget; kwargs...)::AbstractRenderable

# Handle resize -- called when app layout changes
on_layout_change(w::MyWidget, m::Measure)
```

### Typical on_layout_change

```julia
on_layout_change(w::MyWidget, m::Measure) = w.internals.measure = m
```

## WidgetInternals

Managed by the App framework. Key fields:

| Field | Type | Description |
|-------|------|-------------|
| `measure` | `Measure` | Current widget size (height, width) |
| `on_draw` | `Union{Nothing, Function}` | Called each frame |
| `on_activated` | `Union{Nothing, Function}` | Called when widget gains focus |
| `on_deactivated` | `Union{Nothing, Function}` | Called when widget loses focus |
| `active` | `Bool` | Whether widget is currently focused |

## Controls Dict

Maps keyboard input to handler functions:

```julia
controls = Dict{Union{KeyInput, Char}, Function}(
    ArrowUp()   => my_up_handler,
    ArrowDown() => my_down_handler,
    Enter()     => my_select_handler,
    Esc()       => quit,
    'q'         => quit,
    Char        => my_char_handler,  # catch-all for any character
)
```

### Handler Signature

```julia
function my_handler(widget::MyWidget, key::Union{KeyInput, Char})
    # modify widget state
    # return nothing (or :stop to halt event propagation)
end
```

### Special Return Values

- `nothing` -- normal, continue processing
- `:stop` -- stop propagating this key event to other widgets
- Any other value -- collected by the app as a return value (used by menus)

## Widget Lifecycle

1. Widget constructed with initial state
2. App calls `frame(widget)` to render display
3. Active widget receives keyboard input via `controls`
4. `on_activated`/`on_deactivated` called on focus changes
5. `on_layout_change` called if terminal resizes

## Quit Function

Standard quit handler (provided by Term):

```julia
quit(w::AbstractWidget, ::Union{Esc, Char}) = :quit
```

Include in controls to allow exiting the app.

## Active State

Widgets should render differently when active vs inactive:

```julia
function frame(w::MyWidget; kwargs...)
    style = w.internals.active ? "bold blue" : "dim"
    Panel("content"; style=style, width=w.internals.measure.w)
end
```
