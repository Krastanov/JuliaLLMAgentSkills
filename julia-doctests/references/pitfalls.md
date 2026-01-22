# Common Pitfalls

## Whitespace Sensitivity

Output matching is exact. Watch for:
- Trailing spaces
- Number of blank lines
- Indentation in multi-line output

## Module Prefixes

Output may include module names inconsistently:

```julia
# Filter to handle both "MyType" and "MyPackage.MyType"
doctestfilters = [r"(MyPackage\.|)"]
```

## Display Size

Array printing depends on terminal size. Set explicitly:

```julia
ENV["LINES"] = 80
ENV["COLUMNS"] = 80
```

## REPL vs Script Mode

- REPL mode: each `julia>` line evaluated separately
- Script mode: entire block evaluated, then output compared
- Named doctests share state only within same label

## Continuation Lines

For multi-line input in REPL mode, use 7 spaces for alignment:

```julia
julia> function foo(x)
       return x + 1
       end
```

## Suppressing Output

End a line with `;` to suppress output (like in REPL):

```julia
julia> x = 42;

julia> x
42
```
