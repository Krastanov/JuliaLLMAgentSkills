---
name: julia-term
description: Work with Term.jl for styled terminal output, renderables, layouts, progress bars, repr helpers, and interactive TUI apps. Use when building terminal interfaces or rich terminal output in Julia.
---

# Term.jl

Use this skill for all Term.jl work. Keep the entry point small and load only
the reference file that matches the task.

## Quick Start

```julia
using Term

tprint("{bold green}Hello{/bold green}")
print(Panel("content"; title="Example", width=40))
print(Panel(width=20) * Panel(width=20))
```

## Core Modules

```julia
using Term
using Term.Layout
using Term.Progress
using Term.LiveWidgets
```

- `Term` covers markup, `tprint`, `Panel`, themes, repr, and markdown rendering.
- `Term.Layout` covers stacking, alignment, grids, spacers, and compositors.
- `Term.Progress` covers progress bars and custom progress columns.
- `Term.LiveWidgets` covers `App`, widgets, keyboard handling, and navigation.

## Common Patterns

### Styling

```julia
tprint("{bold blue}status{/bold blue}")
set_theme(Theme(box=:HEAVY))
```

Open these only when needed:

- `references/color-names.md`
- `references/theme-fields.md`

### Renderables

```julia
panel = Panel("body"; title="Title", width=50)
```

Open these only when needed:

- `references/box-types.md`
- `references/table-api.md`

### Layout

```julia
layout = Panel(width=20) * Panel(width=20)
```

For the expression DSL and `Compositor`, open:

- `references/compositor-dsl.md`

### Utilities

```julia
using Term.Progress

pbar = ProgressBar(; columns=:default)
job = addjob!(pbar; N=10, description="Work")
```

For column presets and custom columns, open:

- `references/progress-columns.md`

### Interactive Apps

```julia
using Term.LiveWidgets

app = App(TextWidget("Hello"; as_panel=true))
play(app)
```

Open these only when needed:

- `references/app-examples.md`
- `references/widget-api.md`

## Notes

- Use `frame(app)` to preview a widget layout without entering the interactive loop.
- Keep `SKILL.md` small. Read the topic-specific reference file instead of loading
  everything at once.
- For package workflows and tests around Term.jl code, see `julia-package-dev`
  and `julia-tests`.

