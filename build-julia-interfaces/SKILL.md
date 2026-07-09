---
name: build-julia-interfaces
description: "Build and repair Julia user interfaces: simple scripts and installable command-line apps, Comonicon-based command trees in compatible existing projects, styled terminal output and Term.jl live widgets, and custom Makie 0.24 plot recipes. Use for CLI entry points, options and subcommands, terminal reports or TUIs, package plotting extensions, and focused interface tests; use the workload skill instead for subprocess, pipeline, task, or thread mechanics."
---

# Build Julia Interfaces

Start with the smallest interface that meets the user-facing contract. Keep domain logic in
ordinary functions and make each interface a thin adapter.

## Route the Task

- Choose between a script, Base `@main`, experimental Pkg apps, and Comonicon: read
  [references/cli.md](references/cli.md).
- Add styled terminal output, progress, or a Term live application: read
  [references/term.md](references/term.md).
- Extend Makie with a type conversion or full plot recipe: read
  [references/makie-recipes.md](references/makie-recipes.md).
- Test argument handling, rendered output, live layouts, or recipes: read
  [references/testing.md](references/testing.md).

Open only the references required by the task.

## Apply These Defaults

1. For one small command, use a plain Julia function plus Base `@main` on Julia 1.11+.
2. Use a Pkg app only on Julia 1.12+ when package installation is part of the requirement
   and the project accepts that Pkg app support is currently experimental.
3. Add a CLI framework only for meaningful parsing, help, completion, or subcommand needs.
   Keep Comonicon for compatible existing projects; do not make it the default.
4. Use plain text first, Term renderables second, and a Term live app only when keyboard
   interaction or continuously updated layout is required.
5. Use PrettyTables, via `handle-julia-data`, for ordinary tabular reports. Use
   `Term.Tables.Table` only inside a Term composition.
6. Target Makie 0.24's ComputeGraph for new reactive recipes. Do not copy pre-0.24
   Observable mutation patterns into new code.
7. Test pure interface logic with explicit argument vectors and `IOBuffer`s. Avoid elaborate
   mocks; add a small end-to-end smoke test only where the installed command contract matters.

For `Cmd`, environment, pipeline, process-I/O, deadlock, task, or thread details, use
`orchestrate-julia-workloads`, especially its `references/commands-and-processes.md` file.
