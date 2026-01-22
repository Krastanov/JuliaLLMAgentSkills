# Debugging

## Infiltrator.jl (Lightweight)

Minimal performance impact, sets breakpoints in your code:

```julia
using Infiltrator

function myfunction(n)
    @infiltrate  # Breakpoint here
    # ...
end
```

In the infiltrate REPL:
- `@exfiltrate x y` - Save variables to global `safehouse`
- `@continue` - Resume execution

## Debugger.jl (Full Stepping)

Step through any code, including external functions:

```julia
using Debugger
@enter myfunction(args)
```

Debugger commands:
- `n` - Next step
- `` ` `` - Enter evaluation mode to inspect variables
- `c` - Continue

## Code Exploration

```julia
using InteractiveUtils

@which exp(1)              # Find method definition location
supertypes(Int64)          # Show type hierarchy
methodswith(MyType)        # Find methods for a type
versioninfo()              # System info
```

## Running Tests

```bash
# Run all tests
julia --project=. -e 'using Pkg; Pkg.test("PackageName")'

# With threads
julia -tauto --project=. -e 'using Pkg; Pkg.test()'

# Specific categories
MYPACKAGE_PLOT_TEST=true julia --project=. -e 'using Pkg; Pkg.test()'
```
