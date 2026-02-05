---
name: julia-package-dev
description: Work with Julia packages in development mode including environment setup, dependency management, and testing. Use this skill when developing Julia packages.
---

# Julia Package Development

Work with Julia packages in development mode: environments, dependencies, and
debugging.

## Environments vs Packages

- Activate environments.
- Develop (dev) packages into environments.
- Avoid activating packages directly.

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
using Revise
Pkg.activate("./dev")
Pkg.develop(path="./MyPackage.jl")
using MyPackage

# Make changes to src/MyPackage.jl
# Changes are automatically reloaded!
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
JULIA_DEBUG=MyPackage julia -tauto --project=.
```

## Reference

- **[Pkg Commands](references/pkg-commands.md)** - Pkg command reference
- **[Debugging](references/debugging.md)** - Infiltrator.jl, Debugger.jl, code exploration

## Related Skills

- `julia-tests-run` - Running tests
- `julia-tests-write` - Writing tests
- `julia-multipackage` - Multi-package workflows
