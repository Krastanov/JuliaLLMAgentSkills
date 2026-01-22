# makedocs Options

## Table of Contents

- [Packages with Extensions](#packages-with-extensions)
- [Quality Assurance](#quality-assurance)
- [Doctests](#doctests)
- [Output Control](#output-control)
- [HTML Format Options](#html-format-options)
- [Common Patterns](#common-patterns)

## Packages with Extensions

Extensions must be explicitly loaded and included in the modules list:

```julia
using Documenter
using MyPackage
using MyPackage.SubModule

# Load extensions by importing their trigger packages
import SomeDependency
const MyPackageSomeDependencyExt = Base.get_extension(MyPackage, :MyPackageSomeDependencyExt)

import AnotherDep
const MyPackageAnotherDepExt = Base.get_extension(MyPackage, :MyPackageAnotherDepExt)

# Set display size for consistent output in doctests/examples
ENV["LINES"] = 80
ENV["COLUMNS"] = 80

# All modules to document (including extensions!)
doc_modules = [
    MyPackage,
    MyPackage.SubModule,
    MyPackageSomeDependencyExt,
    MyPackageAnotherDepExt,
]

DocMeta.setdocmeta!(MyPackage, :DocTestSetup, :(using MyPackage); recursive=true)

makedocs(
    sitename = "MyPackage.jl",
    modules = doc_modules,
    authors = "Your Name",
    format = Documenter.HTML(
        size_threshold_ignore = ["API.md"],  # Large API pages
    ),
    doctest = false,
    clean = true,
    warnonly = [:missing_docs, :linkcheck],
    linkcheck = true,
    pages = [
        "MyPackage.jl" => "index.md",
        "Getting Started" => "manual.md",
        "Tutorials" => [
            "tutorial.md",
            "Basic Usage" => "tutorial/basic.md",
            "Advanced Features" => "tutorial/advanced.md",
        ],
        "References" => [
            "API" => "API.md",
            "SubModule API" => "API_SubModule.md",
        ],
    ]
)

deploydocs(
    repo = "github.com/YourOrg/MyPackage.jl.git",
    push_preview = false
)
```

## Quality Assurance

### warnonly

Controls whether issues fail the build or just warn:

```julia
# Recommended: warn for these, error for everything else
warnonly = [:missing_docs, :linkcheck]
```

| Error Class | Why warnonly? |
|-------------|---------------|
| `:missing_docs` | Private/internal symbols don't need docs |
| `:linkcheck` | External servers may rate-limit or be temporarily down |

Other error classes (set to error by default):
- `:autodocs_block` - errors in `@autodocs` blocks
- `:cross_references` - broken `@ref` links
- `:docs_block` - errors in `@docs` blocks
- `:doctest` - failing doctests
- `:eval_block` - errors in `@example`/`@repl` blocks
- `:example_block` - errors in `@example` blocks
- `:footnote` - footnote issues
- `:meta_block` - errors in `@meta` blocks
- `:parse_error` - markdown parsing errors
- `:setup_block` - errors in `@setup` blocks

### linkcheck

Verifies external URLs (uses `curl`):

```julia
makedocs(
    linkcheck = true,
    linkcheck_ignore = [r"localhost", "http://example.com"],
    linkcheck_timeout = 10,  # seconds
    warnonly = [:linkcheck],  # Don't fail on link errors
)
```

### checkdocs

Controls docstring coverage checking:

```julia
checkdocs = :exports  # Only check exported names (default: :all)
# Options: :all, :exports, :public, :none
```

### modules

Specifies which modules to check for documentation coverage:

```julia
modules = [MyPackage, MyPackage.SubModule]
```

Any docstring from these modules not included in the docs triggers a warning.

## Doctests

### doctest option

```julia
doctest = true   # Run doctests (default)
doctest = false  # Skip doctests (run separately in test suite)
doctest = :only  # Only run doctests, skip full build
```

### meta option

Sets default `@meta` values for all pages:

```julia
meta = Dict(:DocTestSetup => :(using MyPackage))
```

## Output Control

### draft

Skips slow steps for faster iteration:

```julia
draft = true  # Skip @example blocks, faster builds
```

### pagesonly

Ignores markdown files not in `pages`:

```julia
pagesonly = true  # Only process pages listed in `pages`
```

## HTML Format Options

```julia
format = Documenter.HTML(
    size_threshold_ignore = ["API.md"],  # Skip size warnings for large pages
    assets = ["assets/custom.css"],       # Custom CSS/JS
)
```

## Common Patterns

### Suppress Large Page Warnings

```julia
format = Documenter.HTML(
    size_threshold_ignore = ["API.md", "ECC_API.md"],
)
```

### Custom CSS

```julia
format = Documenter.HTML(
    assets = ["assets/custom.css"]
)
```

### Compact API Tables

Add to a markdown page:

```markdown
```@raw html
<style>
    .content table td {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
</style>
```
```
