# Testing and Documenting Extensions

## Testing Extensions

### In Test Suite

```julia
# test/test_hecke_extension.jl
using Hecke
using MyPackage
using Test

# Get extension module for testing internals
const HeckeExt = Base.get_extension(MyPackage, :MyPackageHeckeExt)

@testset "Hecke extension" begin
    @test LPCode(args...) isa MyPackage.AbstractCode
    @test HeckeExt.internal_function() == expected
end
```

### Conditional Loading in runtests.jl

```julia
if get(ENV, "HECKE_TEST", "") == "true"
    include("test_hecke_extension.jl")
end
```

## Documenting Extensions

### Load Extensions Before Building Docs

```julia
# docs/make.jl
using Documenter
using MyPackage

# Load extension triggers
import Hecke
const MyPackageHeckeExt = Base.get_extension(MyPackage, :MyPackageHeckeExt)

import Makie
const MyPackageMakieExt = Base.get_extension(MyPackage, :MyPackageMakieExt)

# Include all modules
makedocs(
    modules = [MyPackage, MyPackageHeckeExt, MyPackageMakieExt],
    # ...
)
```

### Document Extension API Separately

```markdown
# Extension API

## Hecke Extension

Requires `Hecke.jl` to be loaded.

```@autodocs
Modules = [MyPackageHeckeExt]
Private = false
```
```

### Extension with Exports (for Documentation)

When you need Documenter.jl to find types defined in extensions:

```julia
# ext/MyPackageHeckeExt/MyPackageHeckeExt.jl
module MyPackageHeckeExt

using Hecke
using MyPackage
using DocStringExtensions

# Export types so Documenter can find them
export SpecialCode, AnotherCode

include("codes.jl")
include("algorithms.jl")

end # module
```
