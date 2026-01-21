# Julia Package Development

Work with Julia packages in development mode: environment setup, dependency management,
compilation, and testing.

## Development Mode Setup

### Developing a Single Package

```julia
# In Julia REPL
using Pkg
Pkg.develop(path="/path/to/MyPackage.jl")

# Or from command line
julia -e 'using Pkg; Pkg.develop(path="/path/to/MyPackage.jl")'
```

### Multi-Package Development

When developing related packages together:

```julia
using Pkg
Pkg.develop(path="./QuantumOptics.jl")
Pkg.develop(path="./QuantumOpticsBase.jl")
Pkg.develop(path="./QuantumClifford.jl")
Pkg.develop(path="./QuantumSavory.jl")
```

This allows testing changes across multiple related packages simultaneously.

### Workspace Subprojects

Modern packages use workspaces for subprojects (docs, benchmarks, tests):

```toml
# Project.toml
[workspace]
projects = ["docs", "benchmark"]
```

Each subproject has its own `Project.toml`:

```toml
# docs/Project.toml
[deps]
Documenter = "e30172f5-a6a5-5a46-863b-614d45cd2de4"
MyPackage = "uuid-here"
```

## Common Pkg Commands

### Environment Management

```julia
using Pkg

# Activate a project
Pkg.activate(".")                    # Current directory
Pkg.activate("path/to/project")      # Specific path
Pkg.activate("docs")                 # Subproject

# Instantiate (resolve and install dependencies)
Pkg.instantiate()

# Update dependencies
Pkg.update()                         # All packages
Pkg.update("SpecificPackage")        # Single package

# Check status
Pkg.status()                         # Show installed packages
Pkg.status(mode=PKGMODE_PROJECT)     # Only direct dependencies
Pkg.status(mode=PKGMODE_MANIFEST)    # Include transitive deps
```

### Adding Dependencies

```julia
# Add a registered package
Pkg.add("PackageName")

# Add with version constraint
Pkg.add(name="PackageName", version="1.2")

# Add from URL
Pkg.add(url="https://github.com/Org/Package.jl")

# Add from local path (development mode)
Pkg.develop(path="../OtherPackage.jl")

# Add as weak dependency (for extensions)
# Edit Project.toml manually - no Pkg command for this
```

### Removing Dependencies

```julia
# Remove a package
Pkg.rm("PackageName")

# Remove from development mode (but keep as regular dep)
Pkg.free("PackageName")
```

### Pinning and Freeing

```julia
# Pin to current version (prevent updates)
Pkg.pin("PackageName")

# Unpin
Pkg.free("PackageName")
```

## Command Line Usage

Always use `--project` to specify the environment:

```bash
# Activate and run
julia --project=. -e 'using MyPackage'

# Use multiple threads (speeds up compilation)
julia -tauto --project=.

# Interactive with project
julia -tauto --project=. -i
```

## Running Tests

### Standard Test Command

```bash
# Run all tests
julia --project=. -e 'using Pkg; Pkg.test()'

# With threads (faster compilation)
julia -tauto --project=. -e 'using Pkg; Pkg.test()'
```

### Test Subproject

If tests have their own `test/Project.toml`:

```bash
# Instantiate test environment
julia --project=test -e 'using Pkg; Pkg.develop(PackageSpec(path=pwd())); Pkg.instantiate()'

# Run tests directly
julia --project=test test/runtests.jl

# With threads
julia -tauto --project=test test/runtests.jl
```

### Environment Variables for Tests

```bash
# Run JET static analysis tests
JET_TEST=true julia --project=. -e 'using Pkg; Pkg.test()'

# Run specific test categories (package-specific)
MYPACKAGE_PLOT_TEST=true julia --project=. -e 'using Pkg; Pkg.test()'
```

### TestItemRunner Pattern

Modern packages use TestItemRunner.jl for better test organization:

```julia
# test/runtests.jl
using MyPackage
using TestItemRunner

testfilter = ti -> begin
    exclude = Symbol[]
    if get(ENV, "JET_TEST", "") != "true"
        push!(exclude, :jet)
    end
    return all(!in(exclude), ti.tags)
end

@run_package_tests filter=testfilter
```

Individual test files use `@testitem`:

```julia
# test/test_feature.jl
@testitem "Feature tests" tags=[:feature] begin
    using MyPackage

    @test feature_function(1) == expected
end

@testitem "JET analysis" tags=[:jet] begin
    using JET
    using MyPackage

    @test_opt target_modules=[MyPackage] function_to_analyze()
end
```

## Compilation and Precompilation

### Force Recompilation

```julia
# Clear compiled cache for a package
using Pkg
Pkg.precompile()  # Precompile all packages

# Or delete the compiled cache manually
rm -rf ~/.julia/compiled/v1.XX/MyPackage
```

### Check Precompilation Status

```julia
using Pkg
Pkg.precompile()  # Will show what needs compilation
```

## Working with Extensions

### Loading Extensions in Development

Extensions load automatically when their trigger package is imported:

```julia
using MyPackage       # Base package
import Makie          # Triggers MyPackageMakieExt
```

### Testing Extensions

```julia
# Get extension module for testing
import SomeDep
const MyPackageExt = Base.get_extension(MyPackage, :MyPackageSomeDepExt)

# Now you can test extension functionality
@test MyPackageExt.extension_function() == expected
```

## Dependency Troubleshooting

### Resolve Conflicts

```julia
Pkg.resolve()  # Try to resolve dependency conflicts
```

### Clean Slate

```julia
# Remove Manifest and reinstall
rm("Manifest.toml")
Pkg.instantiate()
```

### Check What's Using a Package

```julia
Pkg.why("PackageName")  # Show dependency chain
```

### Garbage Collection

```julia
Pkg.gc()  # Remove unused packages from ~/.julia
```

## Quick Reference

| Task | Command |
|------|---------|
| Activate project | `Pkg.activate(".")` |
| Install deps | `Pkg.instantiate()` |
| Add package | `Pkg.add("Name")` |
| Remove package | `Pkg.rm("Name")` |
| Dev mode | `Pkg.develop(path="...")` |
| Exit dev mode | `Pkg.free("Name")` |
| Update all | `Pkg.update()` |
| Run tests | `Pkg.test()` |
| Show status | `Pkg.status()` |
| Precompile | `Pkg.precompile()` |

## Related Skills

- `julia-tests` - Detailed test setup and patterns (coming soon)
- `julia-docs` - Documentation setup
- `julia-ci` - CI/CD configuration (coming soon)
