# Environments and Package Layout

Use this reference when changing dependencies, compatibility, manifests, subprojects, workspaces, apps, or package structure.

## Inspect Before Editing

Read:

- root `Project.toml`, especially `name`, `uuid`, `version`, `[deps]`, `[weakdeps]`, `[extensions]`, `[compat]`, `[extras]`, `[targets]`, `[sources]`, and `[workspace]`;
- committed `Manifest.toml` files and the repository's manifest policy;
- `src/PackageName.jl`, `ext/`, `test/`, `docs/`, `benchmark/`, and `.github/workflows/`;
- the minimum Julia version in `[compat]`.

Preserve a nonstandard layout when it is intentional and working. Do not reorganize a package as collateral work.

## Keep Environment Changes Reproducible

Activate the intended project before invoking Pkg:

```julia
using Pkg
Pkg.activate(".")
Pkg.status()
```

Use Pkg operations for dependency graph changes:

- `Pkg.add` adds or changes a dependency.
- `Pkg.rm` removes a dependency.
- `Pkg.compat` updates a compat entry.
- `Pkg.develop` tracks a local path or repository checkout.
- `Pkg.free` stops path/repository tracking and returns to a registered version; it does not remove the dependency.
- `Pkg.resolve` reconciles project and manifest after an intentional project edit.
- `Pkg.instantiate` installs the environment represented by the project and, when present, its manifest.
- `Pkg.why` explains why a package is present.

Edit structural tables such as `[workspace]`, `[extensions]`, `[apps]`, and `[sources]` deliberately. Let Pkg update manifest content; do not hand-edit it.

## Preserve Manifests and Registry Defaults

A manifest records exact resolved versions. If it is committed, preserve it and review changes. If it is intentionally untracked for a library, do not introduce one without reason.

Do not delete a manifest as a routine fix. First identify the conflict with `Pkg.status`, `Pkg.why`, compat inspection, and `Pkg.resolve`. Re-resolve without the manifest only when intentionally changing the repository's resolution baseline, and explain the reproducibility impact.

Pkg's registry preference is `conservative` by default. Do not set `JULIA_PKG_SERVER_REGISTRY_PREFERENCE=eager` globally or by habit. Use `eager` only for a diagnosed need to see a just-published registry entry and account for environments that cannot fetch resources outside a Pkg server.

## Choose a Test-Dependency Layout by Julia Compatibility

Preserve the repository's current supported arrangement unless migration is part of the task:

- For Julia 1.12+, a root workspace may list `test`, `docs`, or benchmark projects:

  ```toml
  [workspace]
  projects = ["test", "docs"]
  ```

  Each subproject declares its own dependencies, including the parent package where required. The workspace resolves them together into the root manifest.

- For earlier Julia versions, use the repository's legacy `test/Project.toml` arrangement or root `[extras]` plus `[targets]`. Do not add `[workspace]` while claiming support below Julia 1.12.

Never compensate for an undeclared test dependency by running `Pkg.add` inside tests.

## Keep the Package Entry Point Simple

For a library:

```text
Project.toml
src/PackageName.jl
test/runtests.jl
ext/                    # only for declared extensions
docs/                   # when the package builds a manual
```

The file `src/PackageName.jl` defines `module PackageName ... end`, imports required dependencies, includes internal files, and exposes the intended API. Avoid loading optional dependencies from the core module.

## Gate Pkg Apps

Pkg app support is experimental and belongs to the Julia 1.12-era app workflow. Only adopt `[apps]` and a `@main` entry point when the package's Julia compat and CI include the required version. Follow current Pkg app schema instead of copying a hand-written argument parser. Keep parsing small or use the repository's established parser.

Do not turn a library into an installed app unless the task calls for that product boundary.

## Sources

- [Pkg: creating packages, tests, and Julia 1.12+ workspaces](https://pkgdocs.julialang.org/v1/creating-packages/)
- [Pkg: Project.toml and Manifest.toml](https://pkgdocs.julialang.org/v1/toml-files/)
- [Pkg API](https://pkgdocs.julialang.org/v1/api/)
- [Pkg apps](https://pkgdocs.julialang.org/v1/apps/)
- [Julia environment variables and registry flavors](https://docs.julialang.org/en/v1/manual/environment-variables/)
