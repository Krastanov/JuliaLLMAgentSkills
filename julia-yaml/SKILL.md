---
name: julia-yaml
description: Parse and write YAML in Julia with YAML.jl, including load/load_file/load_all APIs, dictionary type customization, anchors/aliases behavior, and write/write_file emission. Use this skill when reading YAML configs, converting YAML to Julia structures, or generating YAML outputs from Julia data.
---

# Julia YAML

Use `YAML.jl` to load YAML documents into Julia types and emit Julia data as YAML.

## Load YAML Documents

Single-document parse:

```julia
import YAML
obj = YAML.load(yaml_string)
obj2 = YAML.load_file("config.yml")
```

Multi-document parse:

```julia
docs = YAML.load_all(yaml_string)
docs2 = YAML.load_all_file("multi.yml")
```

## Control Dictionary Type

By default, mappings parse as `Dict{Any,Any}`. Pass `dicttype` to control output:

```julia
YAML.load_file("a.yml"; dicttype=Dict{Symbol,Any})
YAML.load_file("a.yml"; dicttype=OrderedDict{String,Any})
YAML.load_file("a.yml"; dicttype=()->DefaultDict{String,Any}(missing))
```

Use `OrderedDict` when key order should be preserved from source YAML.

## Write YAML

Emit to string/IO or file:

```julia
yaml_text = YAML.write(data)
YAML.write_file("out.yml", data)
```

When round-tripping, verify semantic structure, not exact formatting (layout/quoting style may differ).

## YAML Semantics Notes

- Anchors and references are supported per package README behavior.
- Numeric and timestamp-like scalars are parsed into Julia values according to YAML.jl rules.
- Keep current package limitations in mind when relying on advanced YAML features.

## Reference

- `references/yaml-api-patterns.md` - load/dump APIs, `dicttype`, and caveats

## Related Skills

- `julia-toml` - analogous workflow for TOML data
- `julia-package-dev` - package workflows where YAML may appear in tooling/config
