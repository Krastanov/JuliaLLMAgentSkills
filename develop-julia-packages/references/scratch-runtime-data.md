# Scratch Spaces and Runtime Data

Package source trees may be read-only and shared by environments. Do not write caches, downloads, generated configuration, or mutable state under `src/`, `deps/`, or the installed package directory.

## Choose the Storage Mechanism

- Put small immutable source data under version control when it is genuinely part of the package.
- Use Pkg artifacts for immutable, content-addressed data or binaries that should be reproducible.
- Use Scratch.jl for mutable caches, downloaded indexes, compiled runtime data, and other regenerable package state.
- Use a caller-supplied path for user-owned outputs.
- Use Preferences.jl, not a scratch file, for persistent package preferences when that dependency and workflow are intentional.

Do not use Scratch for secrets or as the only copy of irreplaceable user data. Scratch spaces may be garbage-collected after the environments that use them are removed.

## Create a Namespaced Scratch Space

Declare Scratch as a dependency and create a named space from package code:

```julia
module PackageName

using Scratch

runtime_cache() = @get_scratch!("runtime-cache")

end
```

The macro associates the path with the calling package's UUID. Keep the key stable unless a deliberate cache migration is required.

Create files lazily. Validate downloaded or decoded content before exposing it, and use a temporary file plus an atomic rename when readers could observe a partial write. Coordinate concurrent writers with the smallest appropriate lock or file-level protocol.

Cache keys should include the upstream version, format version, or options needed to decide whether content is reusable. A cache hit must not silently change program correctness.

## Test Without Polluting the User Depot

Pass runtime paths into lower-level functions where practical. Test those functions with `mktempdir`.

Scratch also provides `with_scratch_directory` to redirect scratch operations during a test:

```julia
using Scratch

mktempdir() do dir
    Scratch.with_scratch_directory(dir) do
        # Exercise code that calls @get_scratch!.
    end
end
```

Do not delete a real user's scratch space as test cleanup. Do not mock Scratch internals or replace its methods globally.

## Build and Initialization Rules

Pkg warns against build steps modifying the package directory. Prefer artifacts or Scratch for generated build/runtime data. Keep `__init__` fast: establish paths or lightweight state there, but defer network access and expensive generation until the feature is requested.

Return clear errors when an offline user requests missing remote data. Do not make package import depend on network availability.

## Sources

- [Scratch.jl stable API and lifecycle](https://juliapackaging.github.io/Scratch.jl/stable/)
- [Pkg artifacts](https://pkgdocs.julialang.org/v1/artifacts/)
- [Pkg package-creation guidance on runtime writes](https://pkgdocs.julialang.org/v1/creating-packages/)
- [Preferences.jl](https://juliapackaging.github.io/Preferences.jl/stable/)
