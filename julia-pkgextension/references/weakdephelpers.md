# WeakDepHelpers for User-Friendly Errors

Provide helpful error messages when users call functions without loading the extension.

## Setup in Main Package

```julia
# src/MyPackage.jl
module MyPackage

using WeakDepHelpers: WeakDepCache, method_error_hint_callback,
    @declare_struct_is_in_extension, @declare_method_is_in_extension

export LPCode, special_algorithm  # Export names even though defined in extension

const WEAKDEP_METHOD_ERROR_HINTS = WeakDepCache()

function __init__()
    if isdefined(Base.Experimental, :register_error_hint)
        Base.Experimental.register_error_hint(MethodError) do io, exc, argtypes, kwargs
            method_error_hint_callback(WEAKDEP_METHOD_ERROR_HINTS, io, exc, argtypes, kwargs)
        end
    end
end

end
```

## Declare Extension Types and Methods

```julia
# src/extension_stubs.jl (included in main module)
using WeakDepHelpers: @declare_struct_is_in_extension, @declare_method_is_in_extension

const hecke_docstring = "Implemented in extension requiring Hecke.jl."

# Declare types implemented in extensions
@declare_struct_is_in_extension MyPackage LPCode :MyPackageHeckeExt (:Hecke,) hecke_docstring
@declare_struct_is_in_extension MyPackage GeneralizedBicycle :MyPackageHeckeExt (:Hecke,) hecke_docstring

# Declare functions implemented in extensions
@declare_method_is_in_extension MyPackage.WEAKDEP_METHOD_ERROR_HINTS special_algorithm (:Hecke,) hecke_docstring
```

## User Experience

Without Hecke loaded:
```julia
julia> using MyPackage
julia> LPCode(args...)
[...] # an informative error hint telling the user to import Hecke (the weak dep)
```

After loading Hecke:
```julia
julia> import Hecke
julia> LPCode(args...)  # Works!
```
