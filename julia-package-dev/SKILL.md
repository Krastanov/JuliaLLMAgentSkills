---
name: julia-package-dev
description: Work with Julia packages in development mode including environment setup, dependency management, and testing. Use this skill when developing Julia packages.
---

# Julia Package Development

Work with Julia packages in development mode: environment setup, dependency management,
compilation, and testing.

## Environments vs Packages

Julia's `Project.toml` serves two distinct purposes:

1. **Environments**: Self-contained workspaces (like Python's virtualenv) for tracking dependencies
2. **Packages**: Reusable libraries with `src/` folders and module definitions

**Key distinction**:
- You **activate** environments
- You **develop** (dev) packages into environments
- Never activate a package directly — activate an environment, then `dev` the package into it

## Development Mode Setup

### Developing a Single Package

Create a development environment and add your package to it:

```julia
# Create/activate a development environment
using Pkg
Pkg.activate("./dev")  # or any folder name

# Add your package in development mode
Pkg.develop(path="./MyPackage.jl")

# Now you can use it
using MyPackage
```

Or from command line:

```bash
julia --project=./dev -e 'using Pkg; Pkg.develop(path="./MyPackage.jl")'
```

### Multi-Package Development

When developing related packages together, add them all to the same environment:

```julia
using Pkg
Pkg.activate("./dev")  # Shared development environment
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

## Interactive Development with Revise.jl

Revise.jl automatically tracks source file changes and reloads them without restarting Julia.
It's so essential that many developers wish it were part of the core language.

### Basic Revise Workflow

```julia
# In your startup.jl (~/.julia/config/startup.jl)
try
    using Revise
catch e
    @warn "Error initializing Revise"
end
```

Then develop interactively:

```julia
using Revise
using Pkg
Pkg.activate("./dev")
Pkg.develop(path="./MyPackage.jl")
using MyPackage

# Make changes to src/MyPackage.jl
# Changes are automatically reloaded!
myfunction(args)  # Uses updated code
```

### For Scripts (Not Packages)

Use `includet` to track script files:

```julia
using Revise
Revise.includet("myscript.jl")  # Track changes and auto-reload
```

For one-time execution without tracking:

```julia
include("myscript.jl")  # No change tracking
```

## Logging vs Printing

Prefer logging macros over `println` — they're more versatile:

```julia
@debug "Debug message"         # Suppressed by default
@info "Informational message"  # Standard output
@warn "Warning message" x      # Shows variable name and value
@error "Error message"         # Error-level logging
```

Benefits:
- Automatic variable name display
- Source line numbers
- Filtering by module and severity
- Works well with multithreaded code
- Can redirect to files

Enable debug messages:

```bash
JULIA_DEBUG=MyPackage julia --project=.
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
# Edit Project.toml manually to move a dependency to a weak dependency - no Pkg command for this
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
```

## Running Tests

### Standard Test Command

```bash
# Run all tests
julia --project=. -e 'using Pkg; Pkg.test("PackageName")'
```

### Environment Variables for Tests

```bash
# Run specific test categories (package-specific)
MYPACKAGE_PLOT_TEST=true julia --project=. -e 'using Pkg; Pkg.test("PackageName")'
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
using Pkg
Pkg.precompile()  # Precompile all packages
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

# Now you can test extension functionality that is not exposed in the main package namespace
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

## Debugging

### Infiltrator.jl (Lightweight)

Minimal performance impact, sets breakpoints in your code:

```julia
using Infiltrator

function myfunction(n)
    @infiltrate  # Breakpoint here
    # ...
end
```

In the infiltrate REPL:
- `@exfiltrate x y` - Save variables to global `safehouse`
- `@continue` - Resume execution

### Debugger.jl (Full Stepping)

Step through any code, including external functions:

```julia
using Debugger
@enter myfunction(args)
```

Debugger commands:
- `n` - Next step
- `` ` `` - Enter evaluation mode to inspect variables
- `c` - Continue

## Code Exploration

```julia
using InteractiveUtils

@which exp(1)              # Find method definition location
supertypes(Int64)          # Show type hierarchy
methodswith(MyType)        # Find methods for a type
versioninfo()              # System info (useful for bug reports)
```

## Related Skills

- `julia-tests` - Test setup and patterns
- `julia-docs` - Documentation setup
- `julia-ci-github` - GitHub Actions CI
- `julia-ci-buildkite` - Buildkite CI
- `julia-multipackage` - Multi-package workflows
