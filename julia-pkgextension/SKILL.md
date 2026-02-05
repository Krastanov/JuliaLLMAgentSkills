---
name: julia-pkgextension
description: Build Julia package extensions (weak dependencies) for optional functionality. Use this skill when creating extensions that load conditionally based on trigger packages.
---

# Julia Package Extensions

Build package extensions (weak dependencies) for optional functionality that
loads when trigger packages are imported.

## Add Weak Dependencies (Pkg)

```julia
using Pkg
Pkg.activate(".")
Pkg.add("Makie"; target=:weakdeps)
Pkg.add("CUDA"; target=:weakdeps)
Pkg.compat("Makie", "0.20, 0.21, 0.22, 0.23, 0.24")
```

Add extension mappings in `Project.toml`:

```toml
[extensions]
MyPackageMakieExt = "Makie"
MyPackageCUDAExt = "CUDA"
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

- [ ] Add weak deps and compat via Pkg
- [ ] Add `[extensions]` mapping
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
