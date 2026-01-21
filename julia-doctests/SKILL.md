---
name: julia-doctests
description: Configure and write doctests for Julia packages using Documenter.jl. Use this skill when adding testable code examples to docstrings or setting up doctest infrastructure.
---

# Julia Doctests

Write and test doctests - executable code examples embedded in docstrings that are
automatically verified for correctness.

## Purpose

Doctests serve as **pedagogical examples** that are automatically tested:

- They teach users how to use your API with real, working code
- They catch documentation rot when APIs change
- They are **NOT** replacements for unit tests - keep them simple and illustrative

## Two Doctest Formats

### REPL Examples

Simulate an interactive Julia session with `julia>` prompts:

```julia
"""
    double(x)

Return twice the value of `x`.

# Examples
```jldoctest
julia> double(2)
4

julia> double(3.5)
7.0
```
"""
double(x) = 2x
```

- Lines starting with `julia>` are executed
- Following lines (until next `julia>` or end) are expected output
- Use `;` at end of line to suppress output (like in REPL)
- Continuation lines use `       ` (7 spaces) for alignment

### Script Examples

Use `# output` to separate code from expected output:

````julia
"""
    sum_and_product(a, b)

# Examples
```jldoctest
a, b = 2, 3
println("Sum: ", a + b)
println("Product: ", a * b)
# output
Sum: 5
Product: 6
```
"""
````

## Named Doctests (Shared State)

Label doctests to share state across multiple blocks:

````julia
"""
```jldoctest myexample
julia> x = [1, 2, 3]
3-element Vector{Int64}:
 1
 2
 3
```

Some explanatory text here...

```jldoctest myexample
julia> sum(x)  # x is still defined from above
6
```
"""
````

All blocks with the same label share a module scope.

## Setup and Teardown

### Module-Level Setup (Recommended)

Apply setup to all docstrings in a module using `DocMeta`:

```julia
using Documenter

DocMeta.setdocmeta!(
    MyPackage,
    :DocTestSetup,
    :(using MyPackage; using MyPackage.SubModule);
    recursive=true
)

doctest(MyPackage)
```

### Block-Level Setup

For specific blocks in markdown documentation:

````markdown
```@meta
DocTestSetup = quote
    using MyPackage
    x = [1, 2, 3]
end
```

```jldoctest
julia> sum(x)
6
```

```@meta
DocTestTeardown = quote
    # cleanup code
end
```
````

### Inline Setup

For individual doctest blocks:

````julia
```jldoctest; setup = :(using MyPackage)
julia> myfunction(1)
42
```
````

**Important**: Setup code re-runs for each doctest block. State is not shared unless
using named doctests.

## Handling Randomness with StableRNGs.jl

Never use `rand()` directly - output varies across Julia versions. Use StableRNGs.jl:

```julia
"""
    random_sample(n)

# Examples
```jldoctest
julia> using StableRNGs

julia> rng = StableRNG(42);

julia> random_sample(rng, 3)
3-element Vector{Float64}:
 0.5557510873245796
 0.43710797460962514
 0.12174322140083723
```
"""
function random_sample(rng, n)
    rand(rng, n)
end
```

StableRNGs guarantees identical output across:
- Julia versions
- 32-bit and 64-bit architectures
- Different operating systems

## Filters for Non-Deterministic Output

Use regex filters to normalize variable output (memory addresses, timings, etc.):

### Global Filters

```julia
doctestfilters = [
    r"Ptr{0x[0-9a-f]+}",           # memory addresses
    r"\d+\.\d+ seconds",            # timing
    r"(MyPackage\.|)"               # optional module prefix
]

doctest(MyPackage; doctestfilters)
```

### Replacement Filters

```julia
doctestfilters = [
    r"[0-9]+ bytes" => s"N bytes"
]
```

### Block-Level Filters

````julia
```jldoctest; filter = r"[0-9\.]+ seconds"
julia> @elapsed sleep(0.1)
0.104 seconds
```
````

## Testing Exceptions

Test that code throws expected errors:

````julia
```jldoctest
julia> div(1, 0)
ERROR: DivideError: integer division error
[...]
```
````

- `[...]` indicates truncated output (stacktrace omitted)
- Error matching uses prefix comparison

## Running Doctests

### In Test Suite

```julia
@testitem "Doctests" begin
    using Documenter
    using MyPackage

    DocMeta.setdocmeta!(MyPackage, :DocTestSetup, :(using MyPackage); recursive=true)
    doctest(MyPackage; manual=false)
end
```

### Standalone

```julia
using Documenter
using MyPackage

doctest(MyPackage)
```

### During Documentation Build

```julia
makedocs(
    modules = [MyPackage],
    doctest = true,  # default, set false to skip
    # ...
)
```

## Testing Package Extensions

Package extensions have docstrings too! Load the extension and include it in the modules
list:

```julia
@testitem "Doctests" begin
    using Documenter
    using MyPackage

    # Collect extensions to test
    extensions = []

    # Load extension by importing its trigger package
    import SomeDependency
    const MyPackageSomeDependencyExt = Base.get_extension(MyPackage, :MyPackageSomeDependencyExt)
    push!(extensions, MyPackageSomeDependencyExt)

    # Conditional extensions (platform/version specific)
    @static if VERSION >= v"1.11"
        import AnotherDep
        const MyPackageAnotherDepExt = Base.get_extension(MyPackage, :MyPackageAnotherDepExt)
        push!(extensions, MyPackageAnotherDepExt)
    end

    # Set display size for consistent output
    ENV["LINES"] = 80
    ENV["COLUMNS"] = 80

    DocMeta.setdocmeta!(MyPackage, :DocTestSetup, :(using MyPackage); recursive=true)

    # Test main package AND all extensions
    modules = [MyPackage, MyPackage.SubModule, extensions...]
    doctest(nothing, modules)
end
```

Key points:
- Use `Base.get_extension(Package, :ExtensionName)` to get extension module
- Import the trigger package first to load the extension
- Use `@static if` for conditional extensions
- Set `ENV["LINES"]` and `ENV["COLUMNS"]` for consistent display output

## Fix Mode

Automatically update outdated doctest output:

```julia
# Standalone
doctest(MyPackage; fix=true)

# During build
makedocs(..., doctest = :fix)
```

**Requirements:**
- Files must use LF line endings (not CRLF)
- Review changes carefully before committing

## Output Suppression

Hide output section in rendered docs while still testing:

````julia
```jldoctest; output = false
result = complex_calculation()
result == expected_value
# output
true
```
````

## Common Pitfalls

### Whitespace Sensitivity

Output matching is exact. Watch for:
- Trailing spaces
- Number of blank lines
- Indentation in multi-line output

### Module Prefixes

Output may include module names inconsistently:

```julia
# Filter to handle both "MyType" and "MyPackage.MyType"
doctestfilters = [r"(MyPackage\.|)"]
```

### Display Size

Array printing depends on terminal size. Set explicitly:

```julia
ENV["LINES"] = 80
ENV["COLUMNS"] = 80
```

### REPL vs Script Mode

- REPL mode: each `julia>` line evaluated separately
- Script mode: entire block evaluated, then output compared
- Named doctests share state only within same label

## Quick Reference

| Feature | Syntax |
|---------|--------|
| REPL example | ` ```jldoctest ` with `julia>` prompts |
| Script example | ` ```jldoctest ` with `# output` separator |
| Named/shared | ` ```jldoctest mylabel ` |
| Setup | `DocMeta.setdocmeta!(Mod, :DocTestSetup, expr)` |
| Teardown | `DocMeta.setdocmeta!(Mod, :DocTestTeardown, expr)` |
| Filter | `doctest(...; doctestfilters=[r"pattern"])` |
| Fix output | `doctest(...; fix=true)` |
| Skip in build | `makedocs(..., doctest=false)` |
| Truncated output | `[...]` |
| Suppress output | `; output = false` |
| Stable randomness | `StableRNG(seed)` from StableRNGs.jl |
| Get extension | `Base.get_extension(Pkg, :ExtName)` |
