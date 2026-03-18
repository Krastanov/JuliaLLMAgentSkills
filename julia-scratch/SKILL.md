---
name: julia-scratch
description: Use Scratch.jl for package-specific mutable data containers (caches, compiled objects, host-specific data). Use this skill when storing or managing scratch spaces in Julia packages.
---

# Julia Scratch Spaces

Use Scratch.jl to create and manage mutable, package-specific data directories for
caches, compiled objects, and machine-specific data.

## When to Use Scratch Spaces vs Artifacts

- **Scratch spaces**: mutable, write-many/read-many, machine-specific data (caches,
  compiled objects, host introspection results, user-specific data).
- **Artifacts**: immutable, write-once/read-many, distributable across machines.

Scratch spaces are **not user-facing** -- don't use them for files users access via file
browsers. For user-facing output, write to a user-specified path instead.

## Basic Usage

Always initialize scratch paths in `__init__()` for relocatability:

```julia
module MyPackage
using Scratch

download_cache = ""

function __init__()
    global download_cache = @get_scratch!("downloaded_files")
end

function download_dataset(url)
    fname = joinpath(download_cache, basename(url))
    if !isfile(fname)
        download(url, fname)
    end
    return fname
end

end # module
```

The `@get_scratch!` macro automatically detects the calling module's UUID. The verbose
equivalent uses `get_scratch!`:

```julia
function __init__()
    global download_cache = get_scratch!(@__MODULE__, "downloaded_files")
end
```

## Regenerate Data on Empty Directory

Check contents after `get_scratch!` to handle users who called `clear_scratchspaces!()`:

```julia
function get_dataset_dir()
    dataset_dir = @get_scratch!("dataset")
    if isempty(readdir(dataset_dir))
        perform_expensive_dataset_generation(dataset_dir)
    end
    return dataset_dir
end
```

## Version-Specific Scratch Spaces

Incorporate package version into the key to isolate data across versions:

```julia
module VersionSpecificExample
using Pkg.TOML, Scratch

function get_version()
    return VersionNumber(TOML.parsefile(joinpath(dirname(@__DIR__), "Project.toml"))["version"])
end
const pkg_version = get_version()

const version_specific_scratch = Ref{String}()

function __init__()
    scratch_name = "data_for_version-$(pkg_version.major).$(pkg_version.minor)"
    global version_specific_scratch[] = @get_scratch!(scratch_name)
end

end # module
```

## Cleanup

- **Automatic**: `Pkg.gc()` removes scratch spaces for uninstalled packages (Julia 1.6+).
- **Manual per-package**: `clear_scratchspaces!(pkg)`.
- **Manual full wipe**: `clear_scratchspaces!()`.
- **Single space**: `delete_scratch!(key; pkg_uuid)`.

## Converting Scratch Space to Artifact

When data is mature and ready to share, export it as an immutable Artifact:

```julia
using Pkg, Scratch, Pkg.Artifacts

function export_scratch(scratch_name::String)
    scratch_dir = @get_scratch!(scratch_name)

    hash = create_artifact() do artifact_dir
        rm(artifact_dir)
        cp(scratch_dir, artifact_dir)
    end

    mktempdir() do upload_dir
        tarball_path = joinpath(upload_dir, "$(scratch_name).tar.gz")
        tarball_hash = archive_artifact(hash, tarball_path)
        tarball_url = upload_tarball(tarball_path)  # user-defined upload function

        bind_artifact!(
            joinpath(@__DIR__, "Artifacts.toml"),
            scratch_name,
            hash;
            download_info=[(tarball_url, tarball_hash)],
            force=true,
        )
    end
end
```

## Disable Access Logging

Set `JULIA_SCRATCH_TRACK_ACCESS=0` to disable logging to `logs/scratch_usage.toml`.

## Reference

- **[Scratch.jl API](references/scratch-api.md)** - Full API reference and patterns

## Related Skills

- `julia-package-dev` - Package development workflows
- `julia-package-dev` - Package bootstrapping (add Scratch.jl as a dependency)
- `julia-toml` - TOML parsing (used for version-specific scratch keys)
