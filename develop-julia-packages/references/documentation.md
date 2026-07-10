# Documentation and Doctests

Use Julia docstrings for API help and Documenter.jl for a package manual. Preserve an existing docs layout and deployment setup.

## Write Attached Docstrings

Place a normal string literal immediately before the binding it documents, with no blank line or comment between them. Start with the callable signature, state behavior and important contracts, and give a small executable example when useful.

Use explicit `@doc raw"""...""" definition` syntax when a raw string is needed for LaTeX, backslashes, or dollar signs. Do not assume a bare raw string literal attaches like an ordinary docstring.

DocStringExtensions placeholders such as `$TYPEDEF` and `$TYPEDFIELDS` are interpolation expressions. Import `DocStringExtensions` in the scope where the docstring is evaluated before using them; otherwise use a plain docstring. Do not add the dependency for a trivial template.

Exporting a name affects its public status; it is not required for Documenter to find a name listed in `@docs` or a module selected by `@autodocs`.

## Keep the Documenter Setup Small

A typical `docs/make.jl` is:

```julia
using Documenter
using PackageName

makedocs(
    modules = [PackageName],
    sitename = "PackageName.jl",
    pages = ["Home" => "index.md"],
)
```

Declare Documenter, the parent package, and example dependencies in the docs environment. Instantiate that environment before building:

```sh
julia --project=docs -e 'using Pkg; Pkg.instantiate()'
julia --project=docs docs/make.jl
```

Use `@docs` for curated APIs and `@autodocs` when broad automatic listing is intentional. Set `modules` so Documenter can check included package docstrings. Do not suppress `checkdocs` or use broad `warnonly` merely to make a failing build green.

## Make Examples Executable

Use `jldoctest` for stable REPL or script examples. Set module-level setup before `makedocs` or `doctest`:

```julia
using Documenter
using PackageName

DocMeta.setdocmeta!(
    PackageName,
    :DocTestSetup,
    :(using PackageName);
    recursive = true,
)
```

Documenter runs doctests by default during `makedocs`. Keep that default unless the same doctests run in a dedicated test step. For a test entry:

```julia
using Documenter
using PackageName

doctest(PackageName)
```

Declare Documenter as a test dependency before using this. With ParallelTestRunner, put doctests in their own discovered test file so they can run independently.

Use narrow filters only for genuinely nondeterministic text. Prefer deterministic examples over filtering times, addresses, random values, or unordered output after the fact.

`doctest(...; fix=true)` rewrites source and Markdown. Run it only on a clean, developed checkout, then inspect every change.

## Build Before Deploying

Validate the local build and links required by repository policy before changing deployment. Keep deployment tokens and release-only logic out of pull-request builds. Preserve existing DocumenterCitations or plugin setup, and consult that plugin's current docs rather than embedding a generic bibliography tutorial.

## Sources

- [Julia documentation manual, including `@doc raw`](https://docs.julialang.org/en/v1/manual/documentation/)
- [Documenter package guide](https://documenter.juliadocs.org/stable/man/guide/)
- [Documenter doctests](https://documenter.juliadocs.org/stable/man/doctests/)
- [Documenter syntax](https://documenter.juliadocs.org/stable/man/syntax/)
- [Documenter public API](https://documenter.juliadocs.org/stable/lib/public/)
