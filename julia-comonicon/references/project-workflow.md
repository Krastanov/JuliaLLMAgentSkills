# Comonicon Project Workflow
## Minimal Package Layout
Start with a standard Julia package:

```text
Demo
├── Project.toml
├── Manifest.toml
├── src/Demo.jl
└── test/runtests.jl
```

## Build a Multi-Command CLI
Use `@cast` for command definitions and `@main` for entry registration.

```julia
module Demo
using Comonicon

@cast build(input; release::Bool=false) = println(input, " release=", release)

module Admin
using Comonicon
@cast clean(; all::Bool=false) = println("clean all=", all)
end

@cast Admin
@main
end
```

## Install Command on Package Build

Create `deps/build.jl`:

```julia
using Demo
Demo.comonicon_install()
```

Then build package:

```julia
] build
```

This installs into `~/.julia/bin` by default. Ensure this path is in shell `PATH`.

## Build and Install Tuning

Comonicon supports:

- script mode with cache enable/disable
- package install to `~/.julia/bin`
- `compile = :min` in install flow for faster compilation when runtime speed is less critical
- `sysimg = true` in install flow when startup and runtime performance matter

## Configure via Comonicon.toml

Define project configuration in `Comonicon.toml` or `JuliaComonicon.toml`.

Example enabling system image build:

```toml
name = "demo"

[install]
completion = true
quiet = false
optimize = 2

[sysimg]
incremental = false
filter_stdlibs = true

[sysimg.precompile]
execution_file = ["deps/precompile.jl"]
```

Alternative precompile input:

```toml
[sysimg.precompile]
statements_file = ["deps/statements.jl"]
```

## Build Standalone Application

Configure application build:

```toml
[application]
incremental = true
filter_stdlibs = false

[application.precompile]
statements_file = ["deps/statements.jl"]
```

`@main` also generates `julia_main` for standalone application entry usage.
