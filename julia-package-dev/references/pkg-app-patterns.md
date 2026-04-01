# Pkg App Patterns

## Project Scaffolding

Minimal app project structure:

```
MyApp/
├── Project.toml
├── src/
│   └── MyApp.jl
└── test/
    └── runtests.jl
```

Create or modify package dependencies and compat through `Pkg`, not by
hand-editing `Project.toml`. The example below is the resulting shape of a
package app project file, not a recommendation to edit the file directly.

Illustrative `Project.toml` shape:

```toml
name = "MyApp"
uuid = "..."
authors = ["Your Name <your@email.com>"]
version = "0.1.0"

[deps]
# Add your dependencies here

[compat]
julia = "1.11"

[apps]
myapp = {}
```

Generate UUID with:

```julia
using UUIDs; uuid4()
```

## Argument Parsing Patterns

The `@main` function receives `ARGS` as a `Vector{String}`. Parse manually or use ArgParse.jl:

### Manual Parsing

```julia
function (@main)(ARGS)
    if isempty(ARGS) || "--help" in ARGS
        println("Usage: myapp <input> [--output <path>] [--verbose]")
        return
    end

    verbose = "--verbose" in ARGS
    args = filter(a -> !startswith(a, "--"), ARGS)

    output_idx = findfirst(==("--output"), ARGS)
    output = output_idx !== nothing ? ARGS[output_idx + 1] : "out.txt"

    input = first(args)
    # ... process
end
```

### With ArgParse.jl

```julia
module MyApp

using ArgParse

function parse_args(args)
    s = ArgParseSettings(; prog="myapp", description="My application")
    @add_arg_table! s begin
        "input"
            help = "input file"
            required = true
        "--output", "-o"
            help = "output file"
            default = "out.txt"
        "--verbose", "-v"
            help = "enable verbose output"
            action = :store_true
    end
    return ArgParse.parse_args(args, s)
end

function (@main)(ARGS)
    parsed = parse_args(ARGS)
    # parsed["input"], parsed["output"], parsed["verbose"]
end

end
```

Remember to add ArgParse to the package dependencies.

## Exit Codes

Return an integer from `@main` to set the process exit code:

```julia
function (@main)(ARGS)
    try
        run_app(ARGS)
        return 0
    catch e
        println(stderr, "Error: ", e)
        return 1
    end
end
```

Returning nothing or omitting a return value results in exit code 0.

## Testing App Logic

Separate business logic from the entry point for testability:

```julia
# src/MyApp.jl
module MyApp

function process(input::String; verbose=false)
    verbose && @info "Processing $input"
    return reverse(input)
end

function (@main)(ARGS)
    isempty(ARGS) && (println(stderr, "Usage: myapp <input>"); return 1)
    result = process(ARGS[1])
    println(result)
    return 0
end

end
```

```julia
# test/runtests.jl
using Test
using MyApp

@testset "MyApp" begin
    @test MyApp.process("hello") == "olleh"
    @test MyApp.process("hello"; verbose=true) == "olleh"
end
```

## Multiple Apps with Shared Logic

```julia
# src/MyTools.jl
module MyTools

# Shared utilities
function common_setup(args)
    verbose = "--verbose" in args
    filtered = filter(a -> a != "--verbose", args)
    return (; verbose, args=filtered)
end

include("Format.jl")
include("Lint.jl")

function (@main)(ARGS)
    println("MyTools: use 'format' or 'lint' subcommands")
    return 1
end

end
```

```julia
# src/Format.jl
module Format
using ..MyTools: common_setup

function (@main)(ARGS)
    cfg = common_setup(ARGS)
    cfg.verbose && @info "Formatting..."
    # format logic
    return 0
end

end
```

```toml
[apps]
mytools = {}
format = { submodule = "Format" }
lint = { submodule = "Lint" }
```

## Known Limitations

- Pkg app support is **experimental** - APIs may change
- `~/.julia/bin` must be added to PATH manually
- Apps are tied to the Julia executable that installed them; switching Julia versions requires reinstallation
- No built-in help generation, argument parsing, or shell completions (use ArgParse.jl or Comonicon.jl for those)
