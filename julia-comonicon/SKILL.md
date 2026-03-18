---
name: julia-comonicon
description: Build Julia command-line interfaces with Comonicon.jl using @main, @cast, docstring-driven help text, options/flags parsing, command trees, and package install/build workflows. Use this skill when creating or refactoring Julia CLI scripts/packages, adding subcommands, configuring Comonicon.toml, or troubleshooting Comonicon CLI behavior.
---

# Julia Comonicon

Use Comonicon to turn Julia functions/modules into CLI commands.

## Quick Start: Single Command Script

Use `@main` on a function for one-command CLIs:

```julia
using Comonicon

"""
Example CLI.

# Arguments
- `input`: input value.

# Options
- `-o, --output <path>`: output path.

# Flags
- `-f, --force`: overwrite existing files.
"""
@main function mycmd(input; output="out.txt", force::Bool=false)
    println("input=", input, " output=", output, " force=", force)
end
```

Run with:

```bash
julia myscript.jl -h
```

If creating an executable script, add a Julia shebang and `chmod +x`.

## Build a Multi-Command CLI Package

Use `@cast` to register leaf commands and modules, then `@main` for the entry:

```julia
module Demo
using Comonicon

@cast greet(name; loud::Bool=false) = loud ? println(uppercase(name)) : println(name)
@cast version() = println("Demo CLI")

module Admin
using Comonicon
@cast prune(days::Int=30) = println("pruning older than ", days, " days")
end

@cast Admin
@main

end # module
```

Prefer package-style CLIs for serious use. This gives install/build workflows and better startup optimization options.

## Use the Built-In Entry/Install Functions

After `@main`, Comonicon generates module helpers, including:
- `command_main` for CLI entry.
- `comonicon_install` and `comonicon_install_path` for install flows.
- `julia_main` for standalone application builds.
- `CASTED_COMMANDS` registry for generated command AST/metadata.

Use a `deps/build.jl` install entry like:

```julia
using Demo
Demo.comonicon_install()
```

## Follow Comonicon Naming and Help Conventions

- Map positional arguments to CLI arguments.
- Map keyword arguments to options/flags.
- Use `Bool=false` kwargs for flags.
- Expect `_` in kwarg names to become `-` in CLI long options.
- Use docstring sections `# Arguments`, `# Options`, and `# Flags` for rich help.
- Remember `-h/--help` and `--version` are always generated.

For exact syntax patterns, open `references/conventions.md`.

## Configure Build and Advanced Behavior

Use `Comonicon.toml` (or `JuliaComonicon.toml`) in project root for behavior like plugin enablement and system-image/application builds.

For concrete templates and installation/build flow, open `references/project-workflow.md`.

## Related Skills

- `julia-package-init` - creating Julia packages with infrastructure
- `julia-tests` - running package tests while developing CLI code
- `julia-package-dev` - also covers lightweight Pkg-native apps when Comonicon is not needed
