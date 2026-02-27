# JET Configuration Reference

All configurations are passed as keyword arguments to any JET entry point.

## Result Filtering

| Option | Default | Description |
|--------|---------|-------------|
| `target_modules` | `nothing` | Only report problems from these modules |
| `ignored_modules` | `nothing` | Hide problems from these modules |

Both accept an iterable of module specifiers:

```julia
# Module object — matches innermost frame in module or submodules
target_modules=(MyPkg,)

# AnyFrameModule — matches if ANY frame in the chain is in the module
ignored_modules=(AnyFrameModule(Base),)
```

## Error Analysis Options (`@report_call`, `report_package`)

| Option | Default | Description |
|--------|---------|-------------|
| `mode` | `:basic` | Analysis mode: `:basic`, `:sound`, or `:typo` |
| `ignore_missing_comparison` | `false` | Ignore `missing` from comparison operators |
| `ignore_throws` | `false` | Ignore `throw` calls and propagated exceptions |

`report_package` defaults: `ignore_missing_comparison=true`, `ignore_throws=true`.

**Modes:**

- `:basic` — default, reports common problems (not exhaustive)
- `:sound` — strict, guarantees no runtime errors if clean
- `:typo` — minimal, only undefined refs and bad field access

## Optimization Analysis Options (`@report_opt`)

| Option | Default | Description |
|--------|---------|-------------|
| `skip_noncompileable_calls` | `true` | Skip dispatch analysis in non-concrete calls |
| `function_filter` | `f -> true` | Predicate to skip analysis of specific functions |

```julia
# Ignore runtime dispatch inside println (intentionally dynamic)
@report_opt function_filter=(@nospecialize(f) -> f !== println) my_function(args...)
```

## Print Options

| Option | Default | Description |
|--------|---------|-------------|
| `sourceinfo` | `:default` | Path display: `:full`, `:default`, `:compact`, `:minimal`, `:none` |
| `print_inference_success` | `true` | Print message when no errors found |

## Configuration File

Place a `.JET.toml` in your project directory. JET searches upward from the
analyzed file:

```toml
# .JET.toml
ignore_missing_comparison = true
ignore_throws = true
```

Keyword arguments override file settings.
