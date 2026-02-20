---
name: julia-term-apps
description: Build interactive TUI applications with Term.jl's App and Widget system. Use when creating interactive terminal apps with menus, buttons, text input, keyboard controls, and multi-widget layouts.
---

# Term.jl Interactive Apps

Build interactive TUI applications with App, widgets, keyboard input, and layouts.
Requires Term 2.0+.

## Quick Start

```julia
using Term
using Term.LiveWidgets

# Single-widget app
app = App(TextWidget("Hello, interactive world!"))
play(app)  # starts interactive session (q or Esc to quit)
```

## App Construction

### Single Widget

```julia
app = App(TextWidget("content"))
```

### Layout + Widgets

```julia
# Layout expression: name(height, width) with * (horizontal) / (vertical)
layout = :(a(10, 0.5) * b(10, 0.5))

widgets = Dict(
    :a => TextWidget("Left panel"; as_panel=true),
    :b => TextWidget("Right panel"; as_panel=true),
)

app = App(layout; widgets=widgets)
```

### Preview Without Interaction

```julia
frame(app)  # returns renderable showing current state
```

### App Options

| Kwarg | Description |
|-------|-------------|
| `width` | App width (default: terminal width) |
| `height` | App height (default: terminal height) |
| `expand` | Expand to fill terminal on resize |
| `transition_rules` | Manual widget navigation rules |

## Layout DSL

Same syntax as Compositor but with fractional widths for responsive sizing:

```julia
# Element: name(height, width)
# height: Int (lines), width: Int (cols) or Float64 (0-1 fraction)

# Two columns, equal width
:(a(20, 0.5) * b(20, 0.5))

# Header + two columns + footer
:((header(3, 1.0)) / (left(15, 0.3) * right(15, 0.7)) / (footer(3, 1.0)))

# Complex nested layout
:((a(10, 0.5) * b(10, 0.5)) / c(10, 1.0))
```

### Preview Layout (No Widgets)

```julia
layout = :((a(10, 0.5) * b(10, 0.5)) / c(5, 1.0))
App(layout) |> frame  # shows placeholders
```

## Built-in Widgets

### TextWidget

Display text, optionally in a panel:

```julia
TextWidget("Some text")
TextWidget("Paneled text"; as_panel=true)
```

### InputBox

Text input field. Captures keypresses when active:

```julia
InputBox()  # empty input box
```

Space, Enter, Del work as expected. Content available in `ib.input_text`.

### Button / ToggleButton

```julia
Button("Click me!")
Button("Run"; callback=my_function)  # callback called on press

ToggleButton("Toggle")  # stays pressed/unpressed
```

### SimpleMenu

Navigable option list (arrows to move, Enter to select):

```julia
SimpleMenu(["Option 1", "Option 2", "Option 3"])
SimpleMenu(options; active_style="bold", inactive_style="dim", layout=:vertical)
```

Returns selected index when Enter is pressed.

### ButtonsMenu

Like SimpleMenu but with button-styled options:

```julia
ButtonsMenu(["Save", "Load", "Quit"])
```

### MultiSelectMenu

Checkbox-style multi-selection (Space to toggle, Enter to confirm):

```julia
MultiSelectMenu(["Feature A", "Feature B", "Feature C"])
```

### Pager

Scrollable text viewer:

```julia
Pager("Very long text..."^1000)
Pager(text; height=20, width=60, line_numbers=true)
```

Navigation: arrows (line), `[`/`]` (page), Home/End.

### Gallery

Container showing one widget at a time (arrows to switch):

```julia
Gallery(
    [TextWidget("Page 1"), TextWidget("Page 2")];
    height=25, width=60, title="My Gallery"
)
```

## Keyboard Input

### KeyInput Types

Special keys for widget controls and transition rules:

| Type | Description |
|------|-------------|
| `ArrowUp()` | Up arrow |
| `ArrowDown()` | Down arrow |
| `ArrowLeft()` | Left arrow |
| `ArrowRight()` | Right arrow |
| `Enter()` | Enter/Return |
| `Esc()` | Escape |
| `SpaceBar()` | Space bar |
| `Del()` | Delete |
| `DelKey()` | Delete key variant |
| `HomeKey()` | Home |
| `EndKey()` | End |
| `PageUpKey()` | Page Up |
| `PageDownKey()` | Page Down |

### Controls Dict

Each widget has a `controls` dict mapping keys to handler functions:

```julia
# controls :: Dict{Union{KeyInput, Char}, Function}
# handler signature: fn(widget, key)

my_controls = Dict(
    ArrowDown() => next_item,
    ArrowUp() => prev_item,
    Enter() => select_item,
    Esc() => quit,
    'q' => quit,
    Char => handle_any_char,  # catch-all for character input
)
```

## Widget Navigation (Transition Rules)

### Auto-Inferred

App analyzes layout and creates arrow-key navigation automatically.

### Manual Transition Rules

For complex layouts, specify explicitly:

```julia
App(
    :(a(10, 0.2) * (b1(5, 0.2) / b2(5, 0.2)) * c(10, 0.2));
    widgets = Dict(
        :a  => TextWidget("Box 1"; as_panel=true),
        :b1 => TextWidget("Box 2.1"; as_panel=true),
        :b2 => TextWidget("Box 2.2"; as_panel=true),
        :c  => TextWidget("Box 3"; as_panel=true),
    ),
    transition_rules = Dict(
        ArrowRight() => Dict(:a => :b1, :b1 => :c, :b2 => :c),
        ArrowLeft()  => Dict(:c => :b1, :b1 => :a, :b2 => :a),
        ArrowDown()  => Dict(:b1 => :b2),
        ArrowUp()    => Dict(:b2 => :b1),
    )
)
```

Read as: "When ArrowRight pressed, if `:a` is active move to `:b1`".

## Custom Widgets

### Required Structure

```julia
mutable struct MyWidget <: AbstractWidget
    internals::WidgetInternals     # required: state, size, callbacks
    controls::AbstractDict          # required: keyboard handlers
    # ... your custom fields
end
```

### Required Methods

```julia
# Return renderable for display
function frame(w::MyWidget; kwargs...)::AbstractRenderable
    # build and return what should be shown
    Panel("content"; width=w.internals.measure.w)
end

# Handle layout resize
function on_layout_change(w::MyWidget, m::Measure)
    w.internals.measure = m
end
```

### Callbacks

Set in `WidgetInternals`:

| Callback | When called |
|----------|-------------|
| `on_draw` | Each time `frame()` is called |
| `on_activated` | Widget becomes active |
| `on_deactivated` | Widget loses focus |

### Tips

- Press `h` during `play()` to show help tooltip
- Active widget is visually highlighted (brighter)
- Only the active widget receives keyboard input
- Use `'q'` or `Esc()` controls for quitting

See `references/widget-api.md` for full interface details and
`references/app-examples.md` for complete examples.

## Related Skills

- `julia-term-layout` -- Compositor layout DSL (same expression syntax)
- `julia-term-renderables` -- Panel, Table, etc. used in widget `frame()`
- `julia-term-style` -- markup syntax for widget styling
