---
name: julia-term-layout
description: Compose and arrange Term.jl renderables with stacking, alignment, grid, and Compositor layouts. Use when arranging panels side-by-side, creating grids, or building expression-based layouts.
---

# Term.jl Layout

Arrange renderables with stacking operators, alignment, grid, and Compositor.

## Stacking Operators

`*` stacks horizontally (side by side), `/` stacks vertically (one above another).
Both return a generic `Renderable`.

```julia
using Term: Panel

# Horizontal
Panel(width=20) * Panel(width=20)

# Vertical
Panel(width=20) / Panel(width=20)

# Complex expressions
p = Panel(width=10, height=3)
(p * p * p) / (p * p)
```

### Measure Rules
- `*`: width = sum of widths, height = max height
- `/`: width = max width, height = sum of heights

## hstack / vstack

Functions equivalent to `*` and `/`, with optional `pad` kwarg:

```julia
using Term: Panel
using Term.Layout: vstack, hstack

p = Panel(height=4, width=12)

# With padding (spacing between elements)
hstack(p, p, p, p; pad=4)     # 4-column gap between panels
vstack(p, p, p; pad=1)         # 1-line gap between panels
```

## Alignment

Equalize widths before stacking by padding left/right:

```julia
using Term: Panel
using Term.Layout: leftalign!, center!, rightalign!

p1 = Panel(height=3, width=20)
p2 = Panel(height=3, width=40)
p3 = Panel(height=3, width=60)

# Mutating versions (modify renderables in-place)
center!(p1, p2, p3)        # pad to equal width, centered
leftalign!(p1, p2, p3)     # pad to equal width, left-aligned
rightalign!(p1, p2, p3)    # pad to equal width, right-aligned

# Then stack
vstack(p1, p2, p3)
```

### Shorthand: Justify + Stack in One Call

```julia
using Term: Panel
using Term.Layout: lvstack, cvstack, rvstack

p1 = Panel(height=3, width=20)
p2 = Panel(height=3, width=40)
p3 = Panel(height=3, width=60)

rvstack(p1, p2, p3)  # right-align + vstack
cvstack(p1, p2, p3)  # center + vstack
lvstack(p1, p2, p3)  # left-align + vstack
```

## Layout Elements

### Spacer

Empty space of a given size:

```julia
using Term.Layout: Spacer

s = Spacer(3, 10)  # height=3, width=10
Panel(width=10) * s * Panel(width=10)
```

### hLine / vLine

Horizontal and vertical lines with optional title:

```julia
using Term.Layout: hLine, vLine

hLine(40; style="blue", box=:HEAVY)
hLine(40, "Section Title"; style="bold")
vLine(10; style="dim")
```

### PlaceHolder

Labeled placeholder for layout prototyping:

```julia
using Term.Layout: PlaceHolder

ph = PlaceHolder(5, 20)  # height, width
print(ph)
```

## Padding Functions

```julia
using Term.Layout: pad, vertical_pad

# Horizontal padding
padded = pad("text", 10, 5)       # 10 left, 5 right
padded = pad(Panel(width=20), 5)   # 5 on each side

# Vertical padding
padded = vertical_pad(Panel(width=20), 2)  # 2 lines top and bottom
```

## Grid

Arrange renderables in a grid layout:

```julia
using Term: Panel
using Term.Grid: grid

panels = [Panel(height=6, width=12) for _ in 1:8]

# Auto layout
grid(panels)

# With padding
grid(panels; pad=2)              # uniform padding
grid(panels; pad=(8, 1))         # (hpad, vpad)

# Aspect ratio
grid(panels; aspect=1)           # square-ish grid

# Explicit layout
grid(panels; layout=(2, 4))                    # 2 rows, 4 cols
grid(panels; layout=(3, nothing))              # 3 rows, auto cols
grid(panels; layout=(3, 4), show_placeholder=true)  # show empty cells

# Expression layout -- use _ for empty cells
grid(panels[1:6]; layout=:((a * _ * b) / (_ * _ * c * d) / (_ * e * f)))

# Repeated elements
grid(panels[1:2]; layout=:((x * _ * x) / (_ * _ * y * y)))
```

## Compositor

Expression-based layout with named, sized placeholders. Supports `update!` to
replace placeholders with real content.

```julia
using Term: Panel
using Term.Compositors: Compositor, update!

# Basic layout -- elements are Name(height, width)
layout = :(A(5, 45) * B(5, 45))
comp = Compositor(layout)

# Pass initial content
panel = Panel(height=5, width=45, style="green")
comp = Compositor(layout; B=panel)

# Update content later
update!(comp, :A, Panel(height=5, width=45, title="Updated"))
comp  # display updated compositor

# Fractional widths (0.0-1.0 = fraction of available space)
layout = :(A(20, $(0.75)) * B(20, $(0.25)))
Compositor(layout)

# Complex layouts with vstack/hstack
layout = :(
    vstack(
        A(5, 40), B(5, 40),
        hstack(C(5, 18), D(5, 18); pad=4);
        pad=1
    )
)
Compositor(layout)

# Build complex layouts from sub-expressions
left = :(vstack(A(5, 40), B(5, 40); pad=1))
right = :(vstack(C(5, 40), D(5, 40); pad=1))
layout = :(($left * E(10, 5) * $right) / F(5, 85))
Compositor(layout)
```

See `references/compositor-dsl.md` for full DSL syntax.

### Key Compositor Notes

- **Not a Renderable** -- Compositor cannot be stacked with `*`/`/` or nested in
  Panel. It's a separate display object.
- **Size matters** -- `update!` content must match the size specified in the layout
  expression, or Compositor will warn.
- **Interpolation** -- Use `$` to compose sub-expressions into larger layouts.

## Related Skills

- `julia-term-renderables` -- Panel, Table, Tree to arrange in layouts
- `julia-term-apps` -- App uses Compositor-style layout DSL for widgets
