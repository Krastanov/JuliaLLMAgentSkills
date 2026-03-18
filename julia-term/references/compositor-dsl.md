# Compositor DSL Reference

Full syntax for `Compositor` layout expressions.

## Element Syntax

```julia
Name(height, width)
```

- `Name`: single or multi-character identifier (e.g. `A`, `header`, `sidebar`)
- `height`: `Int` (number of terminal lines)
- `width`: `Int` (columns) or `Float64` fraction `0.0 < w < 1.0` (fraction of
  available width)

### Examples

```julia
A(10, 40)         # 10 lines, 40 columns
B(10, $(0.5))     # 10 lines, half available width
C(5, $(0.33))     # 5 lines, one-third width
```

## Operators

- `*` -- horizontal stacking (side by side)
- `/` -- vertical stacking (one above another)
- Parentheses for grouping

```julia
# A left of B
:(A(5, 40) * B(5, 40))

# A above B
:(A(5, 80) / B(5, 80))

# Complex: (A beside B) above C
:((A(5, 40) * B(5, 40)) / C(5, 80))
```

## Using hstack/vstack in Expressions

For padding control:

```julia
:(vstack(A(5, 40), B(5, 40); pad=1))
:(hstack(A(5, 40), B(5, 40); pad=4))

# Nested
:(vstack(
    A(5, 40),
    B(5, 40),
    hstack(C(5, 18), D(5, 18); pad=4);
    pad=1
))
```

## Expression Interpolation

Build complex layouts from sub-expressions:

```julia
col1 = :(vstack(A(5, 40), B(5, 40); pad=1))
col2 = :(vstack(C(5, 40), D(5, 40); pad=1))
divider = :(E(10, 3))

full_layout = :(($col1 * $divider * $col2) / Footer(3, 83))
```

## Fractional Sizing

Use interpolated `Float64` for responsive widths:

```julia
# Must interpolate the float
layout = :(A(20, $(0.7)) * B(20, $(0.3)))
```

Heights must always be `Int`.

## Compositor Lifecycle

```julia
using Term.Compositors: Compositor, update!

# 1. Define layout
layout = :(Header(3, 80) / (Sidebar(15, 20) * Main(15, 60)) / Footer(3, 80))

# 2. Create compositor (optionally pass initial content)
comp = Compositor(layout; Header=Panel("My App"; width=80, height=3))

# 3. Update placeholders
update!(comp, :Main, Panel("Content"; width=60, height=15))
update!(comp, :Sidebar, Tree(Dict("a" => 1)))

# 4. Display
comp  # shows the composed layout

# 5. Continue updating as needed
update!(comp, :Footer, Panel("Status: OK"; width=80, height=3))
```

## Size Constraints

- Content passed to `update!` should match the declared (height, width)
- Mismatched sizes produce a warning and may cause visual misalignment
- Use `fit=false` on Panels to enforce exact sizing:

```julia
update!(comp, :Main, Panel("text"; width=60, height=15, fit=false))
```
