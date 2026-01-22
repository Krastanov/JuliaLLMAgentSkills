# @-Block Reference

## Table of Contents

- [Docstring Blocks](#docstring-blocks)
- [Cross-References](#cross-references)
- [Code Examples](#code-examples)
- [Metadata and Setup](#metadata-and-setup)
- [Admonitions](#admonitions)
- [Math (LaTeX)](#math-latex)
- [Raw HTML/LaTeX](#raw-htmllatex)

## Docstring Blocks

### Individual docstrings

```markdown
```@docs
function_name
TypeName
```
```

### All public docstrings from modules

```markdown
```@autodocs
Modules = [MyPackage]
Private = false
```
```

### All private docstrings

```markdown
```@autodocs
Modules = [MyPackage]
Private = true
Public = false
```
```

### Filtered by type

```markdown
```@autodocs
Modules = [MyPackage]
Order = [:type, :function]
```
```

## Cross-References

```markdown
See [`function_name`](@ref) for details.

See the [Manual](@ref manual-section-id) section.

Link to [custom text](@ref MyPackage.specific_function).
```

## Code Examples

### Evaluated code block (shows input and output)

```markdown
```@example myexample
x = 1 + 1
```
```

### REPL-style (shows julia> prompts)

```markdown
```@repl myexample
x + 1
```
```

### Hidden setup code

```markdown
```@setup myexample
using MyPackage
data = load_test_data()
```
```

### Continue from previous block

```markdown
```@example myexample; continued = true
y = x + 1
```
```

### Hide specific lines

```markdown
```@example
visible_code()
hidden_code() # hide
```
```

## Metadata and Setup

### Meta block

```markdown
```@meta
CurrentModule = MyPackage
DocTestSetup = quote
    using MyPackage
end
```
```

### Table of contents

```markdown
```@contents
Pages = ["page1.md", "page2.md"]
Depth = 2
```
```

### Index

```markdown
```@index
Pages = ["API.md"]
```
```

## Admonitions

```markdown
!!! note "Optional Title"
    Note content here.

!!! tip
    Helpful tip.

!!! warning
    Warning message.

!!! danger
    Critical warning.

!!! compat "Julia 1.9"
    This feature requires Julia 1.9 or later.

!!! details "Click to expand"
    Collapsible content.
```

## Math (LaTeX)

Inline math: ``` ``E = mc^2`` ```

Display math:

```markdown
```math
\frac{\partial u}{\partial t} = \nabla^2 u
```
```

## Raw HTML/LaTeX

```markdown
```@raw html
<div class="custom-element">
  Custom HTML content
</div>
```
```
