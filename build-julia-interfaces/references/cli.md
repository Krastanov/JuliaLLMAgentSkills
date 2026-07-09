# Julia Command-Line Interfaces

Keep parsing and process exit at the edge. Put behavior in a function that accepts an
argument vector and explicit output streams.

## Choose the Smallest Entry Point

| Requirement | Default |
|---|---|
| Local script or a few positional arguments | Base `ARGS`, optionally Base `@main` |
| Installable command provided by a package on Julia 1.12+ | Pkg app, after accepting its experimental status |
| Existing compatible project with typed options, help, completion, or subcommands | Comonicon |

Do not add Comonicon merely to read one or two positional arguments.

## Base `@main` on Julia 1.11+

```julia
function run_cli(args; out::IO=stdout, err::IO=stderr)::Int
    if length(args) != 1
        println(err, "usage: greet NAME")
        return 2
    end
    println(out, "Hello, ", only(args))
    return 0
end

(@main)(args) = run_cli(args)
```

Julia invokes `Main.main(ARGS)` at the end of a script only when the definition opted in
through `@main`. For packages, the documented form `function (@main)(ARGS) ... end` also
works. If the package supports Julia before 1.11, use an explicit script tail such as
`exit(run_cli(ARGS))` rather than assuming `@main` exists.

## Pkg Apps

On Julia 1.12+, an app package defines an `@main` entry point and an `[apps]` table:

```toml
[apps]
greet = {}
```

Install it with `Pkg.Apps.add` or `pkg> app add`. Pkg apps require Julia 1.12+ and are
currently experimental; do not select them for a package whose supported Julia range starts
earlier. Keep the app entry thin so library users can call the same tested implementation
without installing a command.

## Comonicon for Compatible Existing Projects

On Julia 1.11+, Base and Comonicon both export `@main`. Qualify Comonicon macros:

```julia
import Comonicon

Comonicon.@main function greet(name; loud::Bool=false)
    println(loud ? uppercase(name) : name)
end
```

Use positional arguments for command arguments, keyword arguments with defaults for
options, and `Bool=false` keyword arguments for flags. Use `Comonicon.@cast` plus
`Comonicon.@main` only when subcommands are needed. Document short names under the
`# Arguments`, `# Options`, and `# Flags` docstring sections.

Do not introduce the released Comonicon 1.0.8 into a Julia 1.12 script without a compatibility
check: its released script-mode entry can hit Julia 1.12's stricter world-age handling.
Upstream `main` contains a subsequent `invokelatest` fix, but do not depend on an unregistered
branch unless the project explicitly chooses that risk. Prefer Base `@main` meanwhile.

When maintaining a compatible Comonicon package, its generated helpers include
`command_main`, `comonicon_install`, `comonicon_install_path`, and `julia_main`. Keep build
configuration in `Comonicon.toml`; current `install.compile` is a string such as `"min"`,
not the symbol `:min`.

## Sources

- [Julia command-line interface and Base `@main`](https://docs.julialang.org/en/v1/manual/command-line-interface/)
- [Pkg apps](https://pkgdocs.julialang.org/v1/apps/)
- [Comonicon syntax and conventions](https://comonicon.org/stable/conventions/)
- [Comonicon project workflow](https://comonicon.org/stable/project/)
- [Comonicon 1.0.8 configuration types](https://github.com/comonicon/Comonicon.jl/blob/v1.0.8/src/configs.jl)
- [Comonicon current repository, including Julia 1.12 entry fixes](https://github.com/comonicon/Comonicon.jl)
