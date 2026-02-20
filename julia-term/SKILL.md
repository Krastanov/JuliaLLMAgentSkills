---
name: julia-term
description: Work with Term.jl for styled terminal output and TUI apps in Julia. Use when building terminal interfaces, styled output, or interactive applications with Term.jl.
---

# Term.jl Development

Term.jl is a Julia library for styled terminal output and TUI applications, inspired
by Python's `rich`.

## Quick Start

```julia
using Pkg
Pkg.add("Term")

using Term

# Styled text with markup
tprint("{bold green}Hello{/bold green}, {red}world{/red}!")

# Panel
print(Panel("content"; title="My Panel", style="blue"))

# Stacking
Panel(width=20) * Panel(width=20)  # side by side
Panel(width=20) / Panel(width=20)  # stacked vertically
```

## Module Architecture

| Module | Import | Purpose |
|--------|--------|---------|
| `Term` | `using Term` | Core: tprint, Panel, markup, themes |
| `Term.Tables` | `using Term.Tables` | Table renderable |
| `Term.Trees` | `using Term.Trees` | Tree renderable |
| `Term.Dendograms` | `using Term.Dendograms` | Dendogram renderable |
| `Term.Annotations` | `using Term.Annotations` | Annotation renderable |
| `Term.Layout` | `using Term.Layout` | hstack, vstack, Spacer, hLine, vLine |
| `Term.Grid` | `using Term.Grid` | grid() layout |
| `Term.Compositors` | `using Term.Compositors` | Compositor layout |
| `Term.Progress` | `using Term.Progress` | Progress bars |
| `Term.LiveWidgets` | `using Term.LiveWidgets` | App, widgets, keyboard |
| `Term.Repr` | `using Term.Repr` | @with_repr, termshow, @showme |
| `Term.Consoles` | `using Term.Consoles` | Console width simulation |
| `Term.TermMarkdown` | `using Term.TermMarkdown` | Markdown rendering |

## Key Configuration

```julia
using Term

# Theme -- controls all styling (colors, box types, etc.)
TERM_THEME[]                     # current theme (Ref{Theme})
set_theme(Theme(box=:HEAVY))     # change theme

# Console width
Term.DEFAULT_CONSOLE_WIDTH[]     # default max width (88)

# Disable color output
Term.NOCOLOR[] = true            # strip all ANSI codes
```

## Sub-Skills

| Skill | Use for |
|-------|---------|
| `julia-term-style` | Markup syntax, color macros, themes, tprint |
| `julia-term-renderables` | Panel, Table, Tree, Dendogram, Annotation |
| `julia-term-layout` | Stacking, alignment, grid, Compositor |
| `julia-term-utilities` | Progress bars, logging, repr, introspection |
| `julia-term-apps` | Interactive TUI: App, widgets, keyboard input |

## Related Skills

- `julia-package-dev` -- Julia package development workflow
- `julia-tests-write` -- testing patterns for Julia packages
