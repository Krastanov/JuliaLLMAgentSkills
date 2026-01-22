---
name: julia-pkgextension
description: Build Julia package extensions (weak dependencies) for optional functionality. Use this skill when creating extensions that load conditionally based on trigger packages.
---

# Julia Package Extensions

Build package extensions (weak dependencies) to provide optional functionality that loads
only when users import the trigger package(s).

## Why Extensions?

1. **Minimal base package**: Users who don't need plotting don't pay for Makie compilation
2. **Clean dependencies**: Heavy packages stay optional
3. **Precompilation benefits**: Extensions precompile separately
4. **Type piracy prevention**: Methods involving external types live in extensions

**Tradeoff**: Extensions add complexity. Use them when the trigger dependency is heavy
(plotting, GPU, optimization solvers) or when the functionality is truly optional.

## Project.toml Configuration

```toml
[weakdeps]
Makie = "ee78f7c6-11fb-53f2-987a-cfe4a2b5a57a"
CUDA = "052768ef-5323-5732-b1bb-66c8b64840ba"

[extensions]
MyPackageMakieExt = "Makie"
MyPackageCUDAExt = "CUDA"
# Multiple triggers (loads when ALL are imported)
MyPackageOscarExt = ["Hecke", "Oscar"]

[compat]
Makie = "0.20, 0.21, 0.22, 0.23, 0.24"
```

## File Structure

```
MyPackage.jl/
├── Project.toml
├── src/
│   └── MyPackage.jl
└── ext/
    ├── MyPackageMakieExt/
    │   ├── MyPackageMakieExt.jl
    │   └── recipes.jl
    └── MyPackageCUDAExt.jl
```

**Naming convention**: `{PackageName}{TriggerDep}Ext`

## Extension Module Structure

```julia
# ext/MyPackageMakieExt.jl
module MyPackageMakieExt

using Makie
using MyPackage
using MyPackage: InternalType, internal_function

# Extend functions from main package
function MyPackage.plot_data(data::MyPackage.MyType)
    # Implementation using Makie
end

end # module
```

## Loading Extensions Programmatically

```julia
ext = Base.get_extension(MyPackage, :MyPackageHeckeExt)
if ext !== nothing
    # Extension is loaded
end
```

## Checklist

- [ ] Add weak dependencies to `[weakdeps]` section
- [ ] Add extension mapping to `[extensions]` section
- [ ] Add compat entries for weak dependencies
- [ ] Create extension module in `ext/` directory
- [ ] Use correct naming: `{Package}{Trigger}Ext`
- [ ] Import and extend functions from main package
- [ ] Load extensions in `docs/make.jl` for documentation
- [ ] Add tagged tests for extension functionality

## Reference

- **[Patterns](references/patterns.md)** - Extension patterns for plotting, GPU, multiple triggers
- **[WeakDepHelpers](references/weakdephelpers.md)** - User-friendly error messages for extensions
- **[Testing & Docs](references/testing.md)** - Testing extensions and documentation setup

## Related Skills

- `julia-docs` - Documentation setup including extensions
- `julia-tests-run` - Running tests with TestItemRunner
- `julia-tests-write` - Writing tests with tags
- `julia-makie-recipes` - Makie plot recipes
