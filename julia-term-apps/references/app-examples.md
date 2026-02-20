# App Examples

Complete annotated examples of Term.jl interactive applications.

## Example 1: Two-Panel Text Viewer

```julia
using Term
using Term.LiveWidgets

layout = :(a(25, 0.5) * b(25, 0.5))

widgets = Dict(
    :a => TextWidget("""
    This is the left panel with some content.
    It shows information about the application.
    """; as_panel=true),
    :b => TextWidget("""
    This is the right panel.
    Navigate between panels with arrow keys.
    Press q or Esc to quit.
    """; as_panel=true),
)

app = App(layout; widgets=widgets)
play(app)  # interactive session
```

## Example 2: Menu Application

```julia
using Term.LiveWidgets

layout = :(title(3, 1.0) / menu(20, 1.0))

widgets = Dict(
    :title => TextWidget("Select an option:"; as_panel=true),
    :menu  => SimpleMenu(["New File", "Open File", "Save", "Quit"]),
)

app = App(layout; widgets=widgets)
selected = play(app)  # returns selected index
println("You chose option: $selected")
```

## Example 3: Complex Layout with Manual Transitions

```julia
using Term.LiveWidgets

# Layout: sidebar | (top / bottom)
layout = :(sidebar(20, 0.25) * (main(10, 0.75) / details(10, 0.75)))

widgets = Dict(
    :sidebar => SimpleMenu(["Dashboard", "Settings", "Help"]),
    :main    => TextWidget("Main content area"; as_panel=true),
    :details => TextWidget("Details panel"; as_panel=true),
)

# Manual transition rules for non-trivial layout
transition_rules = Dict(
    ArrowRight() => Dict(:sidebar => :main),
    ArrowLeft()  => Dict(:main => :sidebar, :details => :sidebar),
    ArrowDown()  => Dict(:main => :details),
    ArrowUp()    => Dict(:details => :main),
)

app = App(layout; widgets=widgets, transition_rules=transition_rules)
play(app)
```

## Example 4: Pager with Line Numbers

```julia
using Term.LiveWidgets

# Load source code
code = read("src/myfile.jl", String)

app = App(Pager(code; line_numbers=true, height=30, width=80))
play(app)
```

## Example 5: Gallery of Widgets

```julia
using Term.LiveWidgets

pages = [
    TextWidget("Page 1: Introduction\n\nWelcome to the app!"),
    TextWidget("Page 2: Details\n\nHere are the details..."),
    TextWidget("Page 3: Summary\n\nIn conclusion..."),
]

gallery = Gallery(pages; height=20, width=60, title="Documentation")
app = App(gallery)
play(app)  # arrows to switch pages
```

## Example 6: Input Form

```julia
using Term.LiveWidgets

layout = :(
    (label1(3, 0.3) * input1(3, 0.7)) /
    (label2(3, 0.3) * input2(3, 0.7)) /
    submit(3, 1.0)
)

widgets = Dict(
    :label1 => TextWidget("Name:"; as_panel=true),
    :input1 => InputBox(),
    :label2 => TextWidget("Email:"; as_panel=true),
    :input2 => InputBox(),
    :submit => Button("Submit"; callback=(w, k) -> println("Submitted!")),
)

transition_rules = Dict(
    ArrowDown()  => Dict(:input1 => :input2, :input2 => :submit),
    ArrowUp()    => Dict(:input2 => :input1, :submit => :input2),
    ArrowRight() => Dict(:label1 => :input1, :label2 => :input2),
    ArrowLeft()  => Dict(:input1 => :label1, :input2 => :label2),
)

app = App(layout; widgets=widgets, transition_rules=transition_rules)
play(app)
```

## Tips

- Always include quit controls (`Esc()` or `'q'`) in at least one widget
- Use `frame(app)` during development to preview layout without interaction
- Use `Float64` widths (0.0-1.0) for responsive layouts
- Active widget appears brighter; inactive widgets appear dimmed
- Press `h` during `play()` for a help tooltip
