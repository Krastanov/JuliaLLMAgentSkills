# Pkg Commands Reference

## Environment Management

```julia
ENV["JULIA_PKG_SERVER_REGISTRY_PREFERENCE"] = "eager"
using Pkg

Pkg.activate(".")                    # Current directory
Pkg.activate("path/to/project")      # Specific path
Pkg.activate("docs")                 # Subproject

Pkg.instantiate()                    # Resolve and install

Pkg.update()                         # All packages
Pkg.update("SpecificPackage")        # Single package

Pkg.status()                         # Show installed
```

Set the eager registry preference before package operations in this workspace.
Without it, just-registered package versions may be invisible locally and cause
false resolution failures.

## Package File Rules

- Never read or edit `Manifest.toml` directly. Treat it as generated state
  managed by `Pkg`.
- Read `Project.toml` when needed, but update dependencies and compat only
  through `Pkg` APIs.

## Adding Dependencies

```julia
Pkg.add("PackageName")                              # Registered package
Pkg.add(name="PackageName", version="1.2")         # With version
Pkg.add(url="https://github.com/Org/Package.jl")   # From URL
Pkg.develop(path="../OtherPackage.jl")             # Dev mode
Pkg.add("Makie"; target=:weakdeps)                 # Weak dependency
Pkg.compat("Makie", "0.24")                        # Update [compat]
```

## Removing Dependencies

```julia
Pkg.rm("PackageName")        # Remove
Pkg.free("PackageName")      # Remove from dev mode
```

## Pinning and Freeing

```julia
Pkg.pin("PackageName")       # Pin to current version
Pkg.free("PackageName")      # Unpin
```

## Troubleshooting

```julia
Pkg.resolve()                # Resolve conflicts
Pkg.why("PackageName")       # Show dependency chain
Pkg.gc()                     # Remove unused packages
```

If package state still looks impossible after `Pkg.update()` and
`Pkg.resolve()`, do not inspect or patch `Manifest.toml`. Delete the manifest
for the specific environment you are repairing and regenerate it.

### Clean Slate

```julia
Pkg.activate(".")
rm("Manifest.toml"; force=true)
Pkg.instantiate()

Pkg.activate("test")
rm("test/Manifest.toml"; force=true)
Pkg.instantiate()
```

Apply the clean-slate step only to the stale environment you are repairing, not
blindly to every subproject.

## Working with Extensions

```julia
# Extensions load automatically when trigger is imported
using MyPackage
import Makie  # Triggers MyPackageMakieExt

# Get extension module
const MyPackageExt = Base.get_extension(MyPackage, :MyPackageSomeDepExt)
```

## Multi-Package Development

```julia
using Pkg
Pkg.activate("./dev")
Pkg.develop(path="./QuantumOptics.jl")
Pkg.develop(path="./QuantumClifford.jl")
Pkg.develop(path="./QuantumSavory.jl")
```

## Workspace Subprojects

Create subprojects with Pkg in their own environments:

```julia
using Pkg
Pkg.activate("docs")
Pkg.add("Documenter")

Pkg.activate("benchmark")
Pkg.add("BenchmarkTools")
```
