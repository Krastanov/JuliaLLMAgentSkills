---
name: julia-package-init
description: Create new Julia packages with modern infrastructure including tests, documentation, and CI. Use this skill when starting a new Julia package from scratch.
---

# Julia Package Initialization

Create a new Julia package with modern infrastructure: tests, documentation, CI, and more.

## Package Structure

```
MyPackage.jl/
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       ├── ci.yml
│       ├── downgrade.yml
│       └── TagBot.yml
├── docs/
│   ├── Project.toml
│   ├── make.jl
│   └── src/
├── src/
│   └── MyPackage.jl
├── test/
│   ├── Project.toml
│   └── runtests.jl
├── .gitignore
├── LICENSE
└── Project.toml
```

## Quick Start

### Using PkgTemplates.jl (Recommended)

```julia
using PkgTemplates

t = Template(;
    user = "YourGitHubUsername",
    authors = "Your Name <your@email.com>",
    plugins = [
        Git(; manifest=false),
        GitHubActions(; extra_versions=["1.10", "nightly"]),
        Codecov(),
        Documenter{GitHubActions}(),
        License(; name="MIT"),
    ],
)

t("MyPackage")
```

### Manual Creation

```bash
mkdir -p MyPackage.jl/{src,test,docs/src,.github/workflows}
```

## Core Files

### Project.toml

```toml
name = "MyPackage"
uuid = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"  # Generate with `using UUIDs; uuid4()`
version = "0.1.0"
authors = ["Your Name <your@email.com>"]

[workspace]
projects = ["docs", "benchmark"]

[deps]
# Direct dependencies here

[compat]
julia = "1.10"
```

### src/MyPackage.jl

```julia
module MyPackage

export main_function, MainType

include("types.jl")
include("functions.jl")

end # module
```

### .gitignore

```gitignore
Manifest.toml
LocalPreferences.toml
*.cov
.vscode
scratch/
```

## Secrets Setup

| Secret | Purpose | How to Generate |
|--------|---------|-----------------|
| `CODECOV_TOKEN` | Coverage upload | From codecov.io dashboard |
| `DOCUMENTER_KEY` | Doc deployment | `DocumenterTools.genkeys()` |

## Initialization Checklist

- [ ] `Project.toml` with UUID, version, compat
- [ ] `[workspace]` entry for subprojects
- [ ] `src/MyPackage.jl` with module structure
- [ ] `test/` setup (see `julia-tests-run` skill)
- [ ] `docs/` setup (see `julia-docs` skill)
- [ ] `.gitignore` and `LICENSE`
- [ ] `.github/workflows/ci.yml`
- [ ] Secrets added to GitHub

## Reference

- **[CI Workflows](references/workflows.md)** - Complete GitHub Actions workflow templates

## Related Skills

- `julia-tests-run` - Test runner setup
- `julia-tests-write` - Writing tests
- `julia-docs` - Documentation setup
- `julia-ci-github` - CI configuration details
