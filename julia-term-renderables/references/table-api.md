# Table API Reference

Full kwargs for `Term.Tables.Table`.

## Constructor

```julia
Table(data; kwargs...)
```

`data` can be: `Matrix`, `Dict`, or any Tables.jl-compatible object.

## Kwargs

### Box and Style

| Kwarg | Type | Default | Description |
|-------|------|---------|-------------|
| `box` | `Symbol` | theme `tb_box` (`:MINIMAL_HEAVY_HEAD`) | Box type |
| `style` | `String` | theme `tb_style` (`"#9bb3e0"`) | Box border style |

### Header

| Kwarg | Type | Default | Description |
|-------|------|---------|-------------|
| `header` | `Vector{String}` | auto from data | Column header labels |
| `header_style` | `String` or `Vector{String}` | theme `tb_header` | Header style(s) |
| `header_justify` | `Symbol` or `Vector{Symbol}` | `:center` | Header alignment(s) |

### Columns

| Kwarg | Type | Default | Description |
|-------|------|---------|-------------|
| `columns_style` | `String` or `Vector{String}` | theme `tb_columns` | Column style(s) |
| `columns_justify` | `Symbol` or `Vector{Symbol}` | `:center` | Column alignment(s) |
| `vertical_justify` | `Symbol` | `:top` | Vertical alignment (`:top`, `:center`, `:bottom`) |

### Footer

| Kwarg | Type | Default | Description |
|-------|------|---------|-------------|
| `footer` | `Vector{String}` or `Function` | none | Footer labels or aggregation function |
| `footer_style` | `String` or `Vector{String}` | theme `tb_footer` | Footer style(s) |
| `footer_justify` | `Symbol` or `Vector{Symbol}` | `:center` | Footer alignment(s) |

### Padding

| Kwarg | Type | Default | Description |
|-------|------|---------|-------------|
| `hpad` | `Int` | `2` | Horizontal padding around cell content |
| `vpad` | `Int` | `0` | Vertical padding around cell content |

## Per-Column Styling

Pass a `Vector` instead of a single value to style columns independently:

```julia
Table(data;
    header_style=["bold green", "dim red"],
    columns_style=["bold", "italic"],
    columns_justify=[:right, :left],
)
```

Single values apply to all columns.

## Footer Functions

Pass a `Function` to compute footer values from each column:

```julia
Table(data; footer=sum)     # sum of each column
Table(data; footer=length)  # count per column
```

## Renderable Cell Content

Table cells can contain renderables (Panel, PlaceHolder, etc.):

```julia
using Term.Layout: PlaceHolder

ph = PlaceHolder(3, 12)
data = Dict("col1" => [ph, ph], "col2" => [ph, ph])
Table(data; vertical_justify=:bottom)
```
