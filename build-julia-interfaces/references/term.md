# Term.jl

Use Term renderables for styled output and composable terminal layout. Use live widgets only
when the interface needs focus, keys, navigation, or continuous refresh.

## Static Output First

```julia
using Term

tprintln("{bold green}ready{/bold green}")
panel = Panel("content"; title="Status", width=40)
println(panel)

layout = Panel("left"; width=20) * Panel("right"; width=20)
println(layout)
```

Use `Term.Tables.Table` only when table cells or surrounding content are Term renderables.
Use PrettyTables for an ordinary standalone terminal, Markdown, or HTML table.

## Restore Progress State Reliably

```julia
using Term.Progress

pbar = ProgressBar()
job = addjob!(pbar; N=10, description="Work")

with(pbar) do
    for _ in 1:10
        do_work()
        update!(job)
        yield()
    end
end
```

Prefer `with(pbar) do ... end`; it restores terminal state on errors. Term progress display
runs in the background, so single-threaded compute loops must yield occasionally. The 2.0.8
presets are `:minimal`, `:default`, `:detailed`, and `:spinner`. Its spinner keys are
`:dot`, `:circle`, `:toggle`, `:toggle2`, `:bar`, and `:greek`; inspect `SPINNERS` rather
than inventing names. Term 2.0.8 has no `SpeedColumn`.

## Add a Live App Only When Needed

```julia
using Term.LiveWidgets

app = App(TextWidget("Hello"; as_panel=true))
preview = frame(app)
play(app)
```

For multiple widgets, use an expression such as `:(left(12, 0.5) * right(12, 0.5))`
and pass a `widgets` dictionary with matching symbols. Literal fractional widths work; they
do not need interpolation. Preview with `frame(app)` before entering `play`.

In Term 2.0.8, assign a built-in button callback after construction; the callback receives
the button, not both a widget and key:

```julia
button = Button("Save")
button.callback = button -> save_current_state()
```

Avoid custom widget and custom progress-column types unless built-ins cannot express the
requirement. If one is necessary, copy the current 2.0.8 interface from source rather than
relying on old field lists. `Term.Tables.Table` uses `vertical_justify=:center` by default.

## Sources

- [Term.jl basics and renderables](https://fedeclaudi.github.io/Term.jl/stable/basics/renderables/)
- [Term.jl progress bars](https://fedeclaudi.github.io/Term.jl/stable/adv/progressbars/)
- [Term.jl live apps](https://fedeclaudi.github.io/Term.jl/stable/live/app_intro/)
- [Term.jl widgets](https://fedeclaudi.github.io/Term.jl/stable/live/widgets/)
- [Term 2.0.8 progress source](https://github.com/FedeClaudi/Term.jl/blob/v2.0.8/src/_progress.jl)
- [Term 2.0.8 button source](https://github.com/FedeClaudi/Term.jl/blob/v2.0.8/src/Live/buttons.jl)
- [Term 2.0.8 table source](https://github.com/FedeClaudi/Term.jl/blob/v2.0.8/src/tables.jl)
