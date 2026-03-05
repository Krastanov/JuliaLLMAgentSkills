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

## Filter Escaping in Docstrings

Three escaping pitfalls to avoid in doctest filters inside docstrings:

1. **`raw"""` does NOT work**: `raw"""..."""` strings do not attach to functions
   as documentation. The docstring is silently lost.

2. **Backslash escapes**: Use character classes instead of backslash escapes:
   `[(]` for `\(`, `[)]` for `\)`, `[0-9]` for `\d`, `[[:space:]]` for `\s`.

3. **`$` must be escaped as `\$`**: In a `"""..."""` docstring, bare `$` triggers
   string interpolation. Write `\$` in the source to get a literal `$` in the
   compiled docstring (e.g., for the regex end-of-string anchor).

## Filters Must Match Both Outputs

**Critical**: Documenter.jl only applies a filter when the regex matches
**both** the expected and evaluated output (see `filter_doctests` in
Documenter's source: `if all(occursin.((r,), strings))`). If a filter only
matches one side, it is silently skipped.

This means a filter like `r" [(]empty range[)]"` to strip text that only
appears on some Julia versions will **not work** — it matches the evaluated
output `3:2 (empty range)` but not the expected output `3:2`.

**Solution**: Make the match optional so it matches both strings:

````julia
"""
```jldoctest; filter = r"( [(]empty range[)])?\$"
julia> myfunction(3)
3:2
```
"""
````

Note: `\$` in the docstring source becomes `$` (end-of-string anchor) in the
compiled regex. The optional group `(...)?` with `$` anchor matches both:
- `"3:2"` → matches empty optional group at end of string → unchanged
- `"3:2 (empty range)"` → matches ` (empty range)` at end → stripped to `"3:2"`

**Rules for version-dependent output filters**:
- The filter regex **must** match both expected and evaluated output
- Use optional groups `(...)?` when the extra text only appears on some versions
- Always anchor with `$` (written as `\$` in docstring source) to avoid
  unintended matches elsewhere in the output
- Test with `all(occursin.((filter,), (expected, evaluated)))` to verify

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
