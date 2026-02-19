---
name: julia-toml
description: Parse and write TOML in Julia using the TOML standard library (TOML.jl), including parse/tryparse APIs, ParserError handling, Parser reuse, and TOML.print serialization options. Use this skill when reading or generating TOML config files such as Project.toml, Manifest snippets, or other TOML-based settings.
---

# Julia TOML

Use `TOML` stdlib APIs to parse TOML safely and serialize Julia data back to TOML.

## Parse TOML

Use throwing APIs when malformed TOML should fail fast:

```julia
using TOML
cfg = TOML.parse(text)
cfg2 = TOML.parsefile("config.toml")
```

Use non-throwing APIs when parse errors should be handled explicitly:

```julia
res = TOML.tryparse(text)
if res isa TOML.ParserError
    # handle parser error
end
```

For high-volume parsing of many small TOML files, reuse `TOML.Parser()` to reduce allocations.

## Handle Parse Errors

`TOML.ParserError` includes useful fields for diagnostics:
- `pos` for failing byte position.
- `table` for partially parsed data.
- `type` for parser error category.

When errors need user-facing feedback, report file path + position + nearby source.

## Write TOML

Use `TOML.print` for serialization:

```julia
TOML.print(io, data)
```

Control key ordering when needed:

```julia
TOML.print(io, data; sorted=true, by=length)
```

For custom structs, pass `to_toml` converter that maps unsupported values to supported TOML types.

## Type Constraints to Remember

`TOML.print` supports values that map to TOML primitives/tables, including dict-like tables, integers/floats, booleans, and `Dates.Date`, `Dates.Time`, `Dates.DateTime` (subject to TOML stdlib conversion constraints).

## Reference

- `references/toml-api-patterns.md` - parse/tryparse/print API behavior and examples

## Related Skills

- `julia-package-dev` - package workflows using TOML files
- `julia-yaml` - analogous workflow for YAML serialization
