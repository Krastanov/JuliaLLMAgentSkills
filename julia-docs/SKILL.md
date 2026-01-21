# Julia Documentation

Build documentation for Julia packages using Documenter.jl.

For writing docstrings, see the `julia-docstrings` skill.
For writing doctests, see the `julia-doctests` skill.
For citations and bibliographies, see the `julia-doccitations` skill.

## Philosophy

- **Document at the highest level possible**: Document interfaces and abstract types rather than
  every method/subtype. All instances should refer to higher-level documentation.
- **Tutorials before reference**: Users need to understand the "90% use case" before diving into
  API details.
- **Opinionated tutorials**: Show a complete workflow. Pick specific tools (plotting packages,
  etc.) and demonstrate them. Don't leave users guessing.
- **Variable names matter**: If you use `u0`, everyone will copy it. Show the right naming.
- **Summarize before details**: Every page should summarize its contents before diving into
  specifics.

## Project Structure

```
MyPackage.jl/
├── Project.toml              # Must include [workspace] entry
├── docs/
│   ├── Project.toml          # Documentation dependencies
│   ├── make.jl               # Build script
│   └── src/
│       ├── index.md          # Landing page
│       ├── manual.md         # Getting started tutorial
│       ├── tutorial/         # Additional tutorials
│       ├── howto/            # How-to guides
│       └── API.md            # API reference
├── src/
│   └── MyPackage.jl
└── ext/                      # Package extensions
```

## Workspace Configuration

### Base Project.toml

Add a workspace entry to your package's `Project.toml`:

```toml
[workspace]
projects = ["docs"]
```

If you have other subprojects (benchmarks, etc.):

```toml
[workspace]
projects = ["docs", "benchmark"]
```

### docs/Project.toml

List documentation dependencies:

```toml
[deps]
Documenter = "e30172f5-a6a5-5a46-863b-614d45cd2de4"

[compat]
Documenter = "1"
```

For packages with extensions, add their trigger packages:

```toml
[deps]
Documenter = "e30172f5-a6a5-5a46-863b-614d45cd2de4"
SomeDependency = "uuid-here"
AnotherDep = "uuid-here"

[compat]
Documenter = "1"
```

## Building Documentation

Use the provided script or run manually:

```bash
# Install dependencies and build
julia --project=docs -e '
    using Pkg
    Pkg.develop(PackageSpec(path=pwd()))
    Pkg.instantiate()'
julia --project=docs docs/make.jl

# View locally
xdg-open docs/build/index.html  # Linux
open docs/build/index.html      # macOS
```

## docs/make.jl Template

### Simple Package

```julia
using Documenter
using MyPackage

DocMeta.setdocmeta!(MyPackage, :DocTestSetup, :(using MyPackage); recursive=true)

makedocs(
    sitename = "MyPackage.jl",
    modules = [MyPackage],
    authors = "Your Name",
    format = Documenter.HTML(),
    doctest = false,           # Run doctests separately in test suite
    clean = true,
    warnonly = [:missing_docs, :linkcheck],
    pages = [
        "MyPackage.jl" => "index.md",
        "Manual" => "manual.md",
        "API" => "API.md",
    ]
)

deploydocs(
    repo = "github.com/YourOrg/MyPackage.jl.git"
)
```

### Package with Extensions

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
        "How-To Guides" => [
            "howto.md",
            "Common Task" => "howto/common_task.md",
        ],
        "Explanations" => [
            "explanations.md",
            "Architecture" => "architecture.md",
        ],
        "References" => [
            "references.md",
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

## Key makedocs Options

### Quality Assurance

**`warnonly`** controls whether issues fail the build or just warn:

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

**`linkcheck`** verifies external URLs (uses `curl`):

```julia
makedocs(
    linkcheck = true,
    linkcheck_ignore = [r"localhost", "http://example.com"],
    linkcheck_timeout = 10,  # seconds
    warnonly = [:linkcheck],  # Don't fail on link errors
)
```

**`checkdocs`** controls docstring coverage checking:

```julia
checkdocs = :exports  # Only check exported names (default: :all)
# Options: :all, :exports, :public, :none
```

**`modules`** specifies which modules to check for documentation coverage:

```julia
modules = [MyPackage, MyPackage.SubModule]
```

Any docstring from these modules not included in the docs triggers a warning.

### Doctests

**`doctest`** controls doctest execution:

```julia
doctest = true   # Run doctests (default)
doctest = false  # Skip doctests (run separately in test suite)
doctest = :only  # Only run doctests, skip full build
```

**`meta`** sets default `@meta` values for all pages:

```julia
meta = Dict(:DocTestSetup => :(using MyPackage))
```

### Output Control

**`draft`** skips slow steps for faster iteration:

```julia
draft = true  # Skip @example blocks, faster builds
```

**`pagesonly`** ignores markdown files not in `pages`:

```julia
pagesonly = true  # Only process pages listed in `pages`
```

### HTML Format Options

```julia
format = Documenter.HTML(
    size_threshold_ignore = ["API.md"],  # Skip size warnings for large pages
    assets = ["assets/custom.css"],       # Custom CSS/JS
)
```

## Page Structure

### Landing Page (index.md)

```markdown
# MyPackage.jl

```@meta
DocTestSetup = quote
    using MyPackage
end
```

Brief description of what the package does and why users should care.

## Key Features

- Feature 1 with [`relevant_function`](@ref)
- Feature 2 with [`AnotherType`](@ref)

## Quick Start

```julia
using MyPackage

# Show the most common use case
result = do_something(input)
```

## Components

Describe the main components/modules of the package, linking to detailed pages.

## Support

Information about maintainers, funding, how to contribute.
```

### Tutorial Pages

```markdown
# Getting Started

This tutorial covers the most common use case for MyPackage.jl.

## Prerequisites

What users need to know/install before starting.

## Step 1: Setup

```julia
using MyPackage
using Plots  # Be opinionated - pick a specific plotting package

# Use good variable names that users will copy
initial_state = create_state(10)
```

## Step 2: Main Workflow

Show the complete workflow with explanations.

## Step 3: Visualization

Always show how to visualize results.

```julia
plot(result)
```

## Next Steps

Link to more advanced tutorials and the API reference.
```

### API Reference Page

```markdown
# [Full API](@id Full-API)

Brief summary of the API organization.

## States

Explanation of state-related types and when to use each.

```@docs
State1
State2
```

## Autogenerated API List

```@autodocs
Modules = [MyPackage, MyPackage.SubModule]
Private = false
```

## Private API

!!! danger "Private Implementation Details"
    These functions are used internally and may change without warning.

```@autodocs
Modules = [MyPackage]
Private = true
Public = false
```

### Extension API Page

Document extension APIs separately:

```markdown
# Extension API

## Core Module

```@autodocs
Modules = [MyPackage.SubModule]
Private = false
```
```

## SomeDependency Extension

Requires `SomeDependency.jl` to be loaded.

```@autodocs
Modules = [MyPackageSomeDependencyExt]
Private = false
```

## AnotherDep Extension

Requires `AnotherDep.jl` to be loaded.

```@autodocs
Modules = [MyPackageAnotherDepExt]
Private = false
```

## @-Block Reference

### Docstring Blocks

```markdown
# Individual docstrings
```@docs
function_name
TypeName
```

# All public docstrings from modules
```@autodocs
Modules = [MyPackage]
Private = false
```

# All private docstrings
```@autodocs
Modules = [MyPackage]
Private = true
Public = false
```

# Filtered by type
```@autodocs
Modules = [MyPackage]
Order = [:type, :function]
```
```

### Cross-References

```markdown
See [`function_name`](@ref) for details.

See the [Manual](@ref manual-section-id) section.

Link to [custom text](@ref MyPackage.specific_function).
```

### Code Examples

```markdown
# Evaluated code block (shows input and output)
```@example myexample
x = 1 + 1
```

# REPL-style (shows julia> prompts)
```@repl myexample
x + 1
```

# Hidden setup code
```@setup myexample
using MyPackage
data = load_test_data()
```

# Continue from previous block
```@example myexample; continued = true
y = x + 1
```

# Hide specific lines
```@example
visible_code()
hidden_code() # hide
```

### Metadata and Setup

```markdown
```@meta
CurrentModule = MyPackage
DocTestSetup = quote
    using MyPackage
end
```

```@contents
Pages = ["page1.md", "page2.md"]
Depth = 2
```

```@index
Pages = ["API.md"]
```
```

### Admonitions

```markdown
!!! note "Optional Title"
    Note content here.

!!! tip
    Helpful tip.

!!! warning
    Warning message.

!!! danger
    Critical warning.

!!! compat "Julia 1.9"
    This feature requires Julia 1.9 or later.

!!! details "Click to expand"
    Collapsible content.
```

### Math (LaTeX)

```markdown
Inline math: ``E = mc^2``

Display math:
```math
\frac{\partial u}{\partial t} = \nabla^2 u
```
```

### Raw HTML/LaTeX

```markdown
```@raw html
<div class="custom-element">
  Custom HTML content
</div>
```
```

## Page Organization Guidelines

Follow the Diátaxis framework:

| Type | Purpose | Content |
|------|---------|---------|
| **Tutorials** | Learning-oriented | Step-by-step lessons for beginners |
| **How-To Guides** | Task-oriented | Solutions to specific problems |
| **Explanations** | Understanding-oriented | Background and context |
| **Reference** | Information-oriented | Technical descriptions (API docs) |

Order in navigation: Tutorials → How-To → Explanations → Reference

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

## Checklist

- [ ] `Project.toml` has `[workspace]` entry including `"docs"`
- [ ] `docs/Project.toml` includes all dependencies (including extension triggers)
- [ ] `docs/make.jl` includes all modules (including extensions!)
- [ ] `DocMeta.setdocmeta!` configured for doctests
- [ ] `warnonly = [:missing_docs, :linkcheck]` set appropriately
- [ ] Landing page has quick start example
- [ ] Tutorial covers the "90% use case"
- [ ] API pages organized by concept, not alphabetically
- [ ] Extensions documented in separate API sections
- [ ] Cross-references use `@ref` links
- [ ] `deploydocs` configured for CI
