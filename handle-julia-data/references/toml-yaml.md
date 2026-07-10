# TOML and YAML

Prefer TOML for Julia-owned configuration. Use YAML when interoperability or an existing
format requires it. Parse into plain data, validate the expected shape, and convert into a
typed application structure near the boundary.

## TOML Standard Library

```julia
using TOML

config = TOML.parsefile("config.toml")

result = TOML.tryparse(text)
if result isa TOML.ParserError
    error(sprint(showerror, result))
end
```

Reuse `TOML.Parser()` only after measurement shows that repeatedly parsing many small inputs
matters. `ParserError` exposes documented location and partial-result information, but
`showerror` is usually the simplest user-facing diagnostic.

Write supported TOML-compatible values through an `IO`:

```julia
open("config.toml", "w") do io
    TOML.print(io, config; sorted=true)
end
```

`TOML.print` accepts dictionaries, vectors, strings, integer/float values representable by
TOML, booleans, and `Dates.Date`, `Dates.Time`, and `Dates.DateTime`. Supply a conversion
function only for a small, explicit custom type mapping.

Use Pkg APIs to add/remove dependencies and change compat. Never generate or edit a
`Manifest.toml` as generic TOML; it is Pkg-managed state.

## YAML.jl

```julia
import YAML

config = YAML.load_file("config.yaml"; dicttype=Dict{String,Any})
YAML.write_file("generated.yaml", config)
```

The default mapping type is `Dict{Any,Any}`. Prefer `Dict{String,Any}` for ordinary config.
Choose `OrderedDict` only when source order is a real requirement and its dependency is
already justified.

### Consume Multiple Documents While the File Is Open

In YAML.jl 0.4.16, `load_all_file` returns a lazy iterator after its internal `open do`
scope has closed, so iteration can stop after the first document. Use this form instead:

```julia
documents = open("multi.yaml", "r") do io
    collect(YAML.load_all(io))
end
```

`YAML.load_all(text)` is also safe when the complete input is already a string.

### Respect YAML.jl Semantics

- Anchors and aliases can preserve shared object identity; do not assume a deep copy.
- Timestamp scalars become `Dates.Date` or `Dates.DateTime`. Version 0.4.16 supports
  fractional seconds to millisecond precision but does not apply numeric timezone offsets;
  quote timezone-sensitive values and parse them with an appropriate time-zone library.
- Custom read constructors exist, but do not introduce tag machinery unless the input
  contract requires it. The writer does not reproduce custom tags or source formatting.
- Verify a round trip by comparing parsed values. Comments, scalar style, quoting, anchors,
  and whitespace are not preserved textually.

## Sources

- [Julia TOML standard-library reference](https://docs.julialang.org/en/v1/stdlib/TOML/)
- [Pkg project and manifest guidance](https://pkgdocs.julialang.org/v1/toml-files/)
- [YAML.jl 0.4.16 README](https://github.com/JuliaData/YAML.jl/blob/v0.4.16/README.md)
- [YAML.jl 0.4.16 loader source](https://github.com/JuliaData/YAML.jl/blob/v0.4.16/src/YAML.jl)
- [YAML.jl 0.4.16 timestamp constructor](https://github.com/JuliaData/YAML.jl/blob/v0.4.16/src/constructor.jl)
- [YAML.jl custom-constructor and dictionary tests](https://github.com/JuliaData/YAML.jl/blob/v0.4.16/test/runtests.jl)
