---
name: julia-pkg-app
description: Create standalone Julia applications using Pkg's built-in app support with @main entry points, [apps] Project.toml configuration, julia_flags, and Pkg.Apps.add installation. Use this skill when building distributable command-line applications with Julia's native Pkg app system (not Comonicon).
---

# Julia Pkg Apps

Build standalone Julia CLI applications using Pkg's native app support (experimental as of Julia 1.12+).

## When to Use Pkg Apps vs Comonicon

- **Pkg apps**: Lightweight, zero-dependency CLI apps using Julia's built-in `@main` macro and `Pkg.Apps`. Best for simple tools that don't need argument parsing, option/flag handling, or help generation.
- **Comonicon.jl**: Full-featured CLI framework with docstring-driven help, option/flag parsing, subcommand trees. Use when you need rich CLI ergonomics.

## Requirements

A Julia app needs two things:

1. A `@main` entry point in the package module
2. An `[apps]` section in `Project.toml` listing executable names

## Minimal App

```julia
# src/MyReverseApp.jl
module MyReverseApp

function (@main)(ARGS)
    for arg in ARGS
        print(stdout, reverse(arg), " ")
    end
    return
end

end # module
```

```toml
# Project.toml
name = "MyReverseApp"
uuid = "..."
version = "0.1.0"

[apps]
reverse = {}
```

After installation, `$ reverse some input string` outputs `emos tupni gnirts`.

On Julia 1.12+, the parentheses around `@main` are optional:

```julia
function @main(ARGS)
    # ...
end
```

## Multiple Apps per Package

Use submodules with separate `@main` entry points:

```julia
# src/MyMultiApp.jl
module MyMultiApp

function (@main)(ARGS)
    println("Main app: ", join(ARGS, " "))
end

include("CLI.jl")

end # module
```

```julia
# src/CLI.jl
module CLI

function (@main)(ARGS)
    println("CLI submodule: ", join(ARGS, " "))
end

end # module CLI
```

```toml
# Project.toml
[apps]
main-app = {}
cli-app = { submodule = "CLI" }
```

- `main-app` executes `julia -m MyMultiApp`
- `cli-app` executes `julia -m MyMultiApp.CLI`

## Julia Flags

Set default Julia runtime flags per app in Project.toml:

```toml
[apps]
myapp = { julia_flags = ["--threads=4", "--optimize=2"] }
performance-app = { julia_flags = ["--threads=auto", "--startup-file=yes", "--depwarn=no"] }
debug-app = { submodule = "Debug", julia_flags = ["--check-bounds=yes", "--optimize=0"] }
```

Override flags at runtime using `--` as separator:

```bash
# Uses default flags
myapp input.txt output.txt

# Override thread count (flags before --, app args after --)
myapp --threads=8 -- input.txt output.txt
```

Flag composition order: fixed flags -> Project.toml `julia_flags` -> runtime flags -> app args.

## Installation

Install apps with `Pkg.Apps.add` or the Pkg REPL `app add` mode:

```julia
using Pkg
Pkg.Apps.add("PackageName")
```

```julia
# From Pkg REPL
pkg> app add PackageName
```

Use `Pkg.Apps.develop` for local development:

```julia
Pkg.Apps.develop(path="./MyApp")
```

Installed apps go to `~/.julia/bin/`. Ensure this is on your PATH.

## Override Julia Executable

Use the `JULIA_APPS_JULIA_CMD` environment variable:

```bash
export JULIA_APPS_JULIA_CMD=/path/to/different/julia
myapp input.txt
```

## Reference

- **[references/app-patterns.md](references/app-patterns.md)** - Project scaffolding, argument parsing patterns, and testing strategies

## Related Skills

- `julia-comonicon` - Full-featured CLI framework with argument parsing and help generation
- `julia-package-init` - Creating Julia packages with infrastructure
- `julia-package-dev` - Julia package development workflow
- `julia-toml` - Working with Project.toml configuration
- `julia-external-cmd` - Running external commands from Julia
