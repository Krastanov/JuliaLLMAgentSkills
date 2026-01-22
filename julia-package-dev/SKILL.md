---
name: julia-package-dev
description: Work with Julia packages in development mode including environment setup, dependency management, and testing. Use this skill when developing Julia packages.
---

# Julia Package Development

Work with Julia packages in development mode: environment setup, dependency management,
compilation, and debugging.

## Environments vs Packages

Julia's `Project.toml` serves two distinct purposes:

1. **Environments**: Self-contained workspaces for tracking dependencies
2. **Packages**: Reusable libraries with `src/` folders and module definitions

**Key distinction**:
- You **activate** environments
- You **develop** (dev) packages into environments
- Never activate a package directly

## Development Mode Setup

```julia
# Create/activate a development environment
using Pkg
Pkg.activate("./dev")

# Add your package in development mode
Pkg.develop(path="./MyPackage.jl")

# Now you can use it
using MyPackage
```

## Interactive Development with Revise.jl

Revise.jl automatically tracks source file changes and reloads them.

```julia
# In startup.jl (~/.julia/config/startup.jl)
try
    using Revise
catch e
    @warn "Error initializing Revise"
end
```

```julia
using Revise
Pkg.activate("./dev")
Pkg.develop(path="./MyPackage.jl")
using MyPackage

# Make changes to src/MyPackage.jl
# Changes are automatically reloaded!
```

## Common Pkg Commands

```julia
using Pkg

Pkg.activate(".")               # Activate project
Pkg.instantiate()               # Install deps
Pkg.add("PackageName")          # Add package
Pkg.rm("PackageName")           # Remove package
Pkg.develop(path="...")         # Dev mode
Pkg.free("PackageName")         # Exit dev mode
Pkg.update()                    # Update all
Pkg.test()                      # Run tests
Pkg.status()                    # Show status
Pkg.precompile()                # Precompile
```

## Logging vs Printing

Prefer logging macros over `println`:

```julia
@debug "Debug message"
@info "Informational message"
@warn "Warning message" x
@error "Error message"
```

Enable debug messages:
```bash
JULIA_DEBUG=MyPackage julia --project=.
```

## Quick Reference

| Task | Command |
|------|---------|
| Activate project | `Pkg.activate(".")` |
| Install deps | `Pkg.instantiate()` |
| Dev mode | `Pkg.develop(path="...")` |
| Exit dev mode | `Pkg.free("Name")` |

## Reference

- **[Pkg Commands](references/pkg-commands.md)** - Complete Pkg command reference
- **[Debugging](references/debugging.md)** - Infiltrator.jl, Debugger.jl, code exploration

## Related Skills

- `julia-tests-run` - Running tests
- `julia-tests-write` - Writing tests
- `julia-multipackage` - Multi-package workflows
