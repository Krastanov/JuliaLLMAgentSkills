---
name: julia-term-style
description: Style terminal text with Term.jl markup, color macros, themes, and tprint. Use when adding colors, bold/italic, or custom themes to terminal output.
---

# Term.jl Styled Text

Style terminal output with markup syntax, color macros, themes, and `tprint`.

## Markup Syntax

Wrap text in `{style}...{/style}` tags. Opening and closing tags must match exactly
(same word order and spacing).

```julia
using Term: tprint

# Basic color
tprint("{red}error{/red} and {green}success{/green}")

# Multiple styles -- space-separated in one tag
tprint("{bold blue underline}styled text{/bold blue underline}")

# Background color -- prefix with on_
tprint("{white on_red}alert{/white on_red}")

# RGB color -- (r, g, b) tuple
tprint("{(255, 100, 50)}warm{/(255, 100, 50)}")

# Hex color
tprint("{#42A5F5}sky blue{/#42A5F5}")

# Nesting
tprint("{bold}{red}bold red{/red} just bold{/bold}")

# Unclosed tags auto-close at end of string
tprint("{red}all red")
```

Use double braces `{{like this}}` to print literal `{` and `}`.

## Style Macros

Return styled strings (no `tprint` needed for concatenation):

```julia
using Term

# Color macros: @black @red @green @yellow @blue @magenta @cyan @white @default
println(@green("ok") * " " * @red("fail"))

# Mode macros: @bold @dim @italic @underline
println(@bold "important")

# Multi-style with @style
println(@style "fancy" bold blue underline)

# Interpolation
name = "world"
println("Hello $(@green(name))!")
```

## tprint / tprintln

`tprint` applies markup and auto-highlights numbers, types, symbols, and code:

```julia
using Term: tprint, tprintln

# Markup + auto-highlight
tprint("{bold}Result:{/bold} value is 42 of ::Int64")

# Multiple args -- space-separated automatically
tprint("count:", 42, "type:", Int64)

# Disable highlighting
tprint("no colors on 42"; highlight=false)

# tprintln adds newline
tprintln("line 1")
tprintln("line 2")

# Print renderables
tprint(Panel(width=20), Panel(width=20))  # stacked vertically
```

## Color Types

Three color representations (used automatically based on markup):

| Type | Markup example | Notes |
|------|---------------|-------|
| `NamedColor` | `{red}` | 9 basic: black red green yellow blue magenta cyan white default |
| `BitColor` | `{gold3}` | ~160 named 256-colors (see `references/color-names.md`) |
| `RGBColor` | `{(255,100,50)}` or `{#FF6432}` | Hex converted to RGB internally |

Background variants: prefix any color with `on_` (e.g. `{on_red}`, `{on_#FF6432}`).

## Highlighting

```julia
using Term: highlight, highlight_syntax, load_code_and_highlight

# Auto-highlight numbers, types, symbols, strings, operators
tprint(highlight("value 42 of ::Int64 and :sym"))

# Highlight text as a specific type
tprint(highlight("everything here", :number))  # colored as number

# Julia syntax highlighting
code = """
function foo(x::Int)
    x^2
end
"""
tprint(highlight_syntax(code))

# Load and highlight a source file (shows lines around lineno)
load_code_and_highlight("src/myfile.jl", 50; delta=5) |> tprint
```

## Theme

The `Theme` struct controls colors for highlighting, trees, tables, logging, progress
bars, and more. See `references/theme-fields.md` for all fields.

```julia
using Term: Theme, set_theme, TERM_THEME

# View current theme
current = TERM_THEME[]

# Create custom theme (only override what you need)
mytheme = Theme(string="red", code="black on_white", box=:HEAVY)
set_theme(mytheme)

# Pre-built themes
set_theme(Theme())        # default (dark terminal)
using Term: LightTheme
set_theme(LightTheme)     # light terminal

# Preview theme colors
using Term: demo_theme
demo_theme(mytheme)
```

## Console

Simulate a different terminal width:

```julia
using Term.Consoles: Console, enable, disable

con = Console(60)   # 60 columns wide
con |> enable       # activate -- tprint and renderables respect this width

tprintln("long text gets wrapped to 60 cols"^5)
Panel()  # panel also resized

con |> disable      # restore normal width
```

## Configuration

```julia
using Term

TERM_THEME[]                    # current Theme (Ref{Theme})
Term.DEFAULT_CONSOLE_WIDTH[]    # default max width (default: 88)
Term.NOCOLOR[]                  # set to true to strip all ANSI codes
```

## Related Skills

- `julia-term` -- hub overview and setup
- `julia-term-renderables` -- Panel, Table, Tree use markup styles
