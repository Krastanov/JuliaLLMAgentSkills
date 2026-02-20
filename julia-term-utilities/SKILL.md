---
name: julia-term-utilities
description: Use Term.jl utilities including progress bars, styled logging, custom repr, and introspection tools. Use for progress tracking, log formatting, or displaying Julia objects.
---

# Term.jl Utilities

Progress bars, styled logging, custom repr, introspection, and markdown rendering.

## Progress Bars

### Quick: @track

Simplest way to add a progress bar to a loop:

```julia
using Term.Progress

@track for i in 1:100
    sleep(0.01)
end
```

### Standard: with() Block

Safe pattern that handles start/stop automatically:

```julia
using Term.Progress

pbar = ProgressBar()
job = addjob!(pbar; N=100)

with(pbar) do
    for i in 1:100
        update!(job)
        sleep(0.01)
    end
end
```

### Multiple Jobs

```julia
pbar = ProgressBar()
job1 = addjob!(pbar; N=50, description="Download")
job2 = addjob!(pbar; N=100, description="Process")

with(pbar) do
    for i in 1:100
        i <= 50 && update!(job1)
        update!(job2)
        sleep(0.01)
    end
end
```

### foreachprogress

Wrap an iterable with progress tracking:

```julia
using Term.Progress

pbar = ProgressBar()
foreachprogress(1:100, pbar, description="Outer") do i
    foreachprogress(1:5, pbar, description="  Inner") do j
        sleep(rand() / 5)
    end
end
```

### Manual start!/stop! (not recommended)

```julia
pbar = ProgressBar()
job = addjob!(pbar; N=5)
start!(pbar)
for i in 1:5
    update!(job)
    render(pbar)
    sleep(0.1)
end
stop!(pbar)
```

### Column Presets

Control what information is shown:

```julia
ProgressBar(; columns=:minimal)    # description + progress bar
ProgressBar(; columns=:default)    # + percentage + counts
ProgressBar(; columns=:detailed)   # + elapsed + ETA + speed
ProgressBar(; columns=:spinner)    # spinner (for unknown-length jobs)
```

### ProgressBar Options

| Kwarg | Type | Default | Description |
|-------|------|---------|-------------|
| `columns` | `Symbol`/`Vector` | `:default` | Column preset or custom list |
| `columns_kwargs` | `Dict` | `Dict()` | Per-column kwargs |
| `width` | `Int` | auto | Progress bar display width |
| `expand` | `Bool` | `false` | Fill available terminal width |
| `transient` | `Bool` | `false` | Erase bars when finished |
| `colors` | `String` | theme | Progress bar color |

### addjob! Options

| Kwarg | Type | Default | Description |
|-------|------|---------|-------------|
| `N` | `Int` | none | Expected steps (omit for unknown length) |
| `description` | `String` | `""` | Job label (supports markup) |
| `columns_kwargs` | `Dict` | `Dict()` | Per-job column style overrides |

### Custom Column Style

```julia
pbar = ProgressBar(;
    columns=:detailed,
    columns_kwargs=Dict(
        :ProgressColumn => Dict(:completed_char => '█', :remaining_char => '░'),
        :DescriptionColumn => Dict(:style => "bold red"),
    )
)
```

See `references/progress-columns.md` for custom column interface.

### Extra Info Display

```julia
using Term.Progress

extra_info = Dict("Speed" => "0 it/s", "Loss" => 0.0)
pbar = ProgressBar(; extra_info)
job = addjob!(pbar; N=100)

with(pbar) do
    for i in 1:100
        pbar.extra_info["Loss"] = 1.0 / i
        pbar.extra_info["Speed"] = "$i it/s"
        update!(job)
        sleep(0.01)
    end
end
```

### Threading Note

Progress bar display runs on a separate thread. With single-threaded Julia, add
`sleep(0.001)` or `yield()` in your loop to allow display updates.

## Logging

Replace Julia's default logger with styled output:

```julia
using Term: install_term_logger, uninstall_term_logger

install_term_logger()    # install globally

@info "Message" x=1 y="hello"    # styled output with types, timestamps
@warn "Careful!" value=42
@error "Failed!" err=ErrorException("oops")

uninstall_term_logger()  # revert to default
```

### TermLogger Directly

```julia
using Term: TermLogger, TERM_THEME
import Logging: with_logger

with_logger(TermLogger(stderr, TERM_THEME[])) do
    @info "Scoped logging" x=42
end
```

### ProgressLogging Integration

```julia
using ProgressLogging
using Term: install_term_logger
install_term_logger()

@progress "Processing..." for i in 1:100
    sleep(0.01)
end
```

## Error Handling

Styled stack traces with abbreviated frames:

```julia
using Term: install_term_stacktrace

install_term_stacktrace()  # install globally

# Options
install_term_stacktrace(;
    reverse_backtrace=true,   # show most-relevant frame first
    max_n_frames=30,
    hide_frames=false,        # hide Base/Pkg frames
)

# Runtime configuration
using Term: STACKTRACE_HIDDEN_MODULES, STACKTRACE_HIDE_FRAMES
STACKTRACE_HIDDEN_MODULES[] = ["REPL", "OhMyREPL"]
STACKTRACE_HIDE_FRAMES[] = true
```

## Repr

### @with_repr -- Styled Type Display

Auto-generate a rich REPL display for your types:

```julia
using Term.Repr

@with_repr struct Config
    name::String
    debug::Bool
    level::Int
end

Config("myapp", true, 3)  # shows styled Panel in REPL
```

### termshow -- Display Any Object

```julia
using Term: termshow

termshow(Dict(:x => 1, :y => 2))    # styled dict
termshow(zeros(3, 3))                # styled matrix
termshow(Panel)                      # type info + methods + docstring
termshow(termshow)                   # function methods + docstring
```

### install_term_repr

Make all REPL display go through `termshow`:

```julia
using Term: install_term_repr
install_term_repr()

Panel  # now shows styled output in REPL
```

### @showme -- Method Source Code

Show which method is called and its source:

```julia
using Term.Repr: @showme

@showme tprint(stdout, "hello")   # shows exact method + source code
@showme tprint("hello")           # different method

# Show all methods too
@showme tprint("hello") show_all_methods=true
```

## Introspection

### inspect -- Type Details

```julia
using Term: inspect

inspect(Panel)                      # all info
inspect(Panel; documentation=true)  # include docstring
```

Shows: docstring, definition, constructors, methods, supertype methods.

### typestree -- Type Hierarchy

```julia
using Term: typestree

typestree(AbstractFloat)   # shows Float16, Float32, Float64, BigFloat
typestree(Number)          # full numeric hierarchy
```

### expressiontree -- Expression Structure

```julia
using Term: expressiontree

expressiontree(:(2x + sqrt(x)^y))
```

## Markdown

Term renders Julia `Markdown` objects with styled output:

```julia
using Term: tprint
using Markdown

tprint(md"""
# Header

Paragraph with **bold** and `code`.

* list item 1
* list item 2

> blockquote

!!! tip "Pro tip"
    Admonitions are supported!
""")
```

### parse_md

```julia
using Term.TermMarkdown: parse_md
using Markdown

mymd = md"# Title\nParagraph"
rendered = parse_md(mymd)
tprintln(rendered)
```

## Related Skills

- `julia-term-style` -- markup syntax used for styling progress bars, logs, etc.
- `julia-term` -- hub overview
