# YAML.jl API Patterns

## Load APIs

Single document:

```julia
import YAML
obj = YAML.load(yaml_text)
obj = YAML.load_file("config.yml")
```

All documents from stream/file:

```julia
docs = YAML.load_all(yaml_text)
docs = YAML.load_all_file("config.yml")
```

## Dictionary Type Customization

Default mapping type is `Dict{Any,Any}`. Override with `dicttype`:

```julia
YAML.load_file("x.yml"; dicttype=Dict{Symbol,Any})
YAML.load_file("x.yml"; dicttype=OrderedDict{String,Any})
YAML.load_file("x.yml"; dicttype=()->DefaultDict{String,Any}(missing))
```

Use:
- `Dict{Symbol,Any}` for symbol-key workflows.
- `OrderedDict` when key order matters.
- `DefaultDict` when missing-key defaults are useful.

## Write APIs

Emit YAML from Julia structures:

```julia
yaml_str = YAML.write(data)
YAML.write_file("out.yml", data)
```

Formatting details may differ from input while preserving content.

## Type and Structure Notes

- YAML scalars map into Julia values (including numbers and timestamp-like values) according to parser rules.
- Anchors and aliases are supported, including reference behavior described in the README.

## Known Limitations (per README)

- Writing does not support extra constructors/tags in the same way reading can.
- Sexigesimal numbers are not implemented.
- Fractions of seconds in timestamps are not implemented.
- Specific timezone offsets in timestamps are not implemented.
- Application-specific tags are not implemented.

## Source

- YAML.jl README: `https://github.com/JuliaData/YAML.jl/blob/master/README.md`
