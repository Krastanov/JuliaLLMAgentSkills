# TOML.jl API Patterns

## Parse APIs

Throwing variants:

```julia
using TOML
table = TOML.parse(text_or_io)
table = TOML.parsefile(path)
```

Non-throwing variants:

```julia
res = TOML.tryparse(text_or_io)
res = TOML.tryparsefile(path)
if res isa TOML.ParserError
    # inspect error
end
```

## Reusable Parser

For repeatedly parsing many small TOML inputs:

```julia
p = TOML.Parser()
a = TOML.parse(p, text_a)
b = TOML.parsefile(p, path_b)
```

`Parser()` reuse can reduce repeated parser setup overhead.

## ParserError Fields

`TOML.ParserError` exposes:
- `pos`: position where parse failed.
- `table`: partial result parsed before failure.
- `type`: parser error type/category.

Use these fields to produce clear diagnostics.

## Serialization with TOML.print

Basic:

```julia
TOML.print(io, data)
```

Sorted table keys:

```julia
TOML.print(io, data; sorted=true, by=length)
```

Custom conversion for unsupported structs:

```julia
TOML.print(io, data) do x
    x isa MyType ? Dict("a" => x.a, "b" => x.b) : x
end
```

## Supported Value Shapes

`TOML.print` supports TOML-compatible structures such as:
- dictionary-like tables
- integers and floating-point values (convertible to TOML numeric constraints)
- booleans
- `Dates.Date`, `Dates.Time`, `Dates.DateTime`
- arrays/arrays-of-tables composed of supported values

## Source

- TOML.jl docs: `https://julialang.github.io/TOML.jl/dev/`
