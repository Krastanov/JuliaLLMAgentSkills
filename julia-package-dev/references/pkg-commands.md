# Pkg Commands Reference

## Environment Management

```julia
using Pkg

Pkg.activate(".")                    # Current directory
Pkg.activate("path/to/project")      # Specific path
Pkg.activate("docs")                 # Subproject

Pkg.instantiate()                    # Resolve and install

Pkg.update()                         # All packages
Pkg.update("SpecificPackage")        # Single package

Pkg.status()                         # Show installed
```

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

### Clean Slate

```julia
rm("Manifest.toml")
Pkg.instantiate()
```

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
Pkg.activate("./dev")
Pkg.develop(path="./QuantumOptics.jl")
Pkg.develop(path="./QuantumClifford.jl")
Pkg.develop(path="./QuantumSavory.jl")
```

## Workspace Subprojects

Create subprojects with Pkg in their own environments:

```julia
Pkg.activate("docs")
Pkg.add("Documenter")

Pkg.activate("benchmark")
Pkg.add("BenchmarkTools")
```
