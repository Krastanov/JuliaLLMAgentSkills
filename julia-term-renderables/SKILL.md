---
name: julia-term-renderables
description: Create visual building blocks with Term.jl including Panel, Table, Tree, Dendogram, and Annotation. Use when creating bordered boxes, data tables, tree views, or annotated text.
---

# Term.jl Renderables

Build visual terminal elements: Panel, TextBox, Table, Tree, Dendogram, Annotation.

## RenderableText

Styled text with controlled width. Applies markup automatically.

```julia
using Term: RenderableText

rt = RenderableText("{bold red}Hello!"; width=40)
print(rt)  # markup applied, text wrapped to 40 cols
```

## Panel

Bordered box around content. The most-used renderable.

```julia
using Term: Panel

# Basic panel
print(Panel("Hello world"))

# Full options
Panel(
    "{red}styled content{/red}";
    title="My Title",
    title_style="bold green",
    title_justify=:center,        # :left (default), :center, :right
    subtitle="footer",
    subtitle_style="dim",
    subtitle_justify=:right,
    style="gold1 bold",           # box border style
    box=:ROUNDED,                 # box type (see references/box-types.md)
    width=60,
    height=10,
    fit=true,                     # true: expand to fit content; false: truncate
    padding=(2, 2, 0, 0),        # (left, right, top, bottom)
    justify=:left,                # content justify: :left, :center, :right
    background="on_black",        # background color for content area
)

# Empty panel (no content)
Panel(; width=20, height=5, style="blue")

# Panel with renderable content
Panel(
    Panel(width=18, style="green"),
    Panel(width=18, style="red");
    title="nested!", fit=true
)
```

### Key Panel kwargs

| Kwarg | Type | Default | Description |
|-------|------|---------|-------------|
| `fit` | `Bool` | `false` | Expand panel to fit content |
| `width` | `Int` | `default_width()` | Panel width in columns |
| `height` | `Int` | `2` | Panel height in lines |
| `padding` | `NTuple{4}` | `(2,2,0,0)` | Left, right, top, bottom |
| `justify` | `Symbol` | `:left` | Content alignment |
| `style` | `String` | theme `line` | Box border markup style |
| `box` | `Symbol` | theme `box` | Box type (`:ROUNDED`, `:HEAVY`, etc.) |
| `title` | `String/Nothing` | `nothing` | Top title text |
| `title_style` | `String/Nothing` | `nothing` | Title markup style |
| `title_justify` | `Symbol` | `:left` | Title position |
| `subtitle` | `String/Nothing` | `nothing` | Bottom subtitle text |
| `subtitle_style` | `String/Nothing` | `nothing` | Subtitle markup style |
| `subtitle_justify` | `Symbol` | `:left` | Subtitle position |
| `background` | `String/Nothing` | `nothing` | e.g. `"on_black"`, `"on_#202020"` |

## TextBox

Panel without visible border. Same kwargs as Panel (width, height, padding, justify,
title).

```julia
using Term: TextBox

TextBox("Long text here"^10; title="TEXT", width=40, fit=false)
```

## @nested_panels

Auto-sets width of nested Panel() calls to fit nicely:

```julia
using Term: @nested_panels

@nested_panels Panel(
    Panel(
        Panel(; title="deep", style="blue");
        title="deeper", style="green");
    title="outer", style="red"
)
```

Only works with literal `Panel()` calls in the macro expression.

## Table

Styled tables from matrices, dicts, or Tables.jl-compatible data.

```julia
using Term.Tables: Table

# From matrix
data = hcat(1:3, rand(Int8, 3))
Table(data)

# From Dict
data = Dict(:Parameter => [:alpha, :beta], :Value => [1, 2])
Table(data;
    header=["Param", "Val"],
    header_style="bold white on_black",
    header_justify=[:right, :left],
    columns_style=["bold white", "dim"],
    columns_justify=[:right, :left],
    footer=["", "2 params"],
    footer_style="bold green",
    footer_justify=[:right, :left],
    box=:SIMPLE,
    style="#9bb3e0",
    hpad=3,
    vpad=1,
)

# Function as footer (applied per-column)
Table(data; footer=sum)

# Renderables as cell content
Table(Dict("col1" => [Panel(width=12)], "col2" => [Panel(width=12)]);
    vertical_justify=:bottom
)
```

See `references/table-api.md` for full kwargs.

## Tree

Hierarchical data visualization using AbstractTrees.jl.

```julia
using Term.Trees: Tree
using Term: typestree

# From Dict (nested dicts = nested branches)
data = Dict(
    "config" => Dict("debug" => true, "level" => 3),
    "name" => "myapp",
    "tags" => (1, 2, 3),
)
print(Tree(data))

# Style with theme
using Term: Theme
tree = Tree(data;
    theme=Theme(tree_keys="yellow", tree_pair="red_light"),
    guides=:asciitree,  # guide style
    title="Config",
)
print(tree)

# From expressions and arrays
Tree(:(print, (:x, :(y+1)))) |> print
Tree([1, [2, [:a, :b]]]) |> print

# Type hierarchy tree
typestree(AbstractFloat)
```

Guide styles: `:standardtree` (default), `:asciitree`, `:boldtree`, or custom
`AbstractTrees.TreeCharSet`.

## Dendogram

Top-down hierarchical visualization (trunk with leaves).

```julia
using Term.Dendograms: Dendogram, link

# Simple dendogram
dendo = Dendogram("root", "leaf1", "leaf2", "leaf3")
print(dendo)

# Nested via link()
d1 = Dendogram("first", [1, 2])
d2 = Dendogram("second", [:a, :b])
print(link(d1, d2; title="combined"))

# Deep nesting
print(link(d1, link(d2, d2; title="inner"); title="outer"))
```

## Annotation

Annotate substrings of text with explanatory panels below.

```julia
using Term.Annotations: Annotation

# Basic annotation -- pairs of substring => explanation
Annotation(
    "This function returns the result",
    "function" => "a callable object",
    "result" => "the computed output"
)

# With style on annotation
Annotation(
    "styled annotations",
    "styled" => ("markup style applied", "bold red")
)

# Combine with Panel
Panel(
    Annotation("my code example", "code" => "source text");
    title="Annotated", fit=true
)
```

## Box Types

All available box symbols for Panel, Table, hLine, vLine:

`:NONE`, `:ASCII`, `:ASCII2`, `:ASCII_DOUBLE_HEAD`, `:SQUARE`,
`:SQUARE_DOUBLE_HEAD`, `:MINIMAL`, `:MINIMAL_HEAVY_HEAD`,
`:MINIMAL_DOUBLE_HEAD`, `:SIMPLE`, `:SIMPLE_HEAD`, `:SIMPLE_HEAVY`,
`:HORIZONTALS`, `:ROUNDED`, `:HEAVY`, `:HEAVY_EDGE`, `:HEAVY_HEAD`,
`:DOUBLE`, `:DOUBLE_EDGE`

See `references/box-types.md` for visual examples.

## Composing Renderables

All renderables work with stacking operators and layout functions:

```julia
using Term: Panel

# Horizontal stack
Panel(width=20) * Panel(width=20)

# Vertical stack
Panel(width=20) / Panel(width=20)

# Inside other renderables
Panel(Tree(Dict("a" => 1)); fit=true, title="tree in panel")
```

## Related Skills

- `julia-term-style` -- markup syntax and themes used by all renderables
- `julia-term-layout` -- stacking, grid, Compositor for arranging renderables
