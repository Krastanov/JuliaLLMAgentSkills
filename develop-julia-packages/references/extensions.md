# Package Extensions

Use an extension when optional functionality needs both the package and another package. Keep ordinary required functionality in `src/`.

## Declare the Extension

Package extensions require Julia 1.9+. Check `[compat]` before introducing them.

```toml
[weakdeps]
OptionalDep = "00000000-0000-0000-0000-000000000000"

[extensions]
PackageOptionalDepExt = "OptionalDep"

[compat]
julia = "1.9"
OptionalDep = "1"
```

Use the real registered UUID and a tested compat range. For an extension that requires every package in a set, use an array of trigger names in `[extensions]`.

Create `ext/PackageOptionalDepExt.jl`:

```julia
module PackageOptionalDepExt

using PackageName
using OptionalDep

# Add narrowly-scoped integration methods here.

end
```

The extension name, file name, and `[extensions]` key must agree.

## Keep Boundaries Clear

- Keep optional imports out of the parent module.
- Extend functions owned by the parent or optional dependency only for argument types the package owns or is explicitly responsible for.
- Avoid type piracy and broad fallback methods.
- Do not reach into an extension module as a stable public API. When the parent must retrieve extension-owned state, use `Base.get_extension` and gate that code on supported Julia versions.
- Do not copy backend-specific internals into a generic extension guide. Follow the optional dependency's public API.

Use multiple trigger dependencies only when the integration truly requires all of them; otherwise split independent integrations.

## Test Loading and Behavior

Declare the trigger package as a test dependency through the repository's supported test environment. Never install it from `runtests.jl`.

Cover:

1. the parent package loads without the optional dependency;
2. loading the optional dependency activates the extension;
3. representative integration methods return correct results;
4. errors and unsupported inputs remain clear;
5. precompilation succeeds in a fresh Julia process.

Run no-extension and extension cases in explicitly separate processes when load order or global package state matters. ParallelTestRunner gives each file a fresh sandbox module, but worker processes can be reused, so module isolation does not unload packages. Each file must still import every dependency it uses.

If docs include extension docstrings, load the trigger dependency in the docs environment and include the extension's module in Documenter's `modules` only when those docstrings are meant to be checked.

For a package supporting Julia below 1.9, preserve its existing compatibility mechanism rather than adding an extension that cannot load on supported versions.

## Sources

- [Pkg: weak dependencies and extensions](https://pkgdocs.julialang.org/v1/creating-packages/#Conditional-loading-of-code-in-packages-(Extensions))
- [Julia: package extensions and loading](https://docs.julialang.org/en/v1/manual/code-loading/#man-extensions)
- [Julia: style guide and type piracy](https://docs.julialang.org/en/v1/manual/style-guide/)
