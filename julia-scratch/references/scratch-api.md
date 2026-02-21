# Scratch.jl API Reference

## Core Functions

### `get_scratch!(key::String)` / `get_scratch!(pkg::Module, key::String)`

Create or retrieve a scratch space directory. Returns the absolute path to the space.

- When called with a module/UUID, the space is namespaced to that package.
- When called with just a key, creates a global scratch space accessible by any package.

```julia
# With explicit module
path = get_scratch!(@__MODULE__, "my_cache")

# Global scratch space (no package ownership)
path = get_scratch!("global_cache")
```

### `@get_scratch!(key)`

Macro that automatically detects the calling module's UUID. Preferred over `get_scratch!`
in package code.

```julia
function __init__()
    global cache_dir = @get_scratch!("cache")
end
```

### `delete_scratch!(key; pkg_uuid)`

Delete a specific scratch space. Rarely needed since `Pkg.gc()` handles cleanup.

### `clear_scratchspaces!()`

Remove all scratch spaces across all packages. Use for freeing disk space.

### `clear_scratchspaces!(pkg)`

Remove all scratch spaces for a specific package only.

## Key Patterns

### Always Initialize in `__init__()`

Never store scratch paths as compile-time constants. Use `__init__()` for relocatability:

```julia
# WRONG - bakes absolute path into precompilation cache
const CACHE = @get_scratch!("data")

# RIGHT - resolves path at load time
const CACHE = Ref{String}()
function __init__()
    CACHE[] = @get_scratch!("data")
end
```

### Defensive Regeneration

Always handle the case where a scratch space has been cleared:

```julia
function ensure_data()
    dir = @get_scratch!("processed")
    if isempty(readdir(dir))
        regenerate_data(dir)
    end
    return dir
end
```

### Version Isolation

Use package version in key to prevent stale data across versions:

```julia
scratch_name = "cache-v$(pkg_version.major).$(pkg_version.minor)"
```

## Compatibility

- Works with Julia 1.0+.
- `Pkg.gc()` awareness of scratch spaces requires Julia 1.6+.
