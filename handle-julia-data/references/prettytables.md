# PrettyTables.jl

Use PrettyTables for presentation, not as a storage format. Keep CSV or another machine
format as the data interchange output.

## Render the Same Table to Common Backends

```julia
using PrettyTables

report = (
    metric=["accuracy", "loss"],
    value=[0.9312, 0.0847],
)

formatter = (v, i, j) -> v isa AbstractFloat ? round(v; digits=3) : v

pretty_table(report; formatters=[formatter])
markdown = pretty_table(String, report; backend=:markdown, formatters=[formatter])
html = pretty_table(String, report; backend=:html, stand_alone=true,
                    formatters=[formatter])
```

Use `pretty_table(String, ...)` when embedding output in a log or generated document. The
default output backend is text for ordinary terminal IO. Current PrettyTables 3 also has
LaTeX, Typst, and Excel backends; open their backend documentation only when requested.

## Add Only the Sections the Report Needs

Useful cross-backend keywords include:

- `title`, `subtitle`, `column_labels`, and `row_labels`
- `summary_rows` and matching `summary_row_labels`
- `footnotes` and `source_notes`
- `maximum_number_of_rows`, `maximum_number_of_columns`, and `vertical_crop_mode`
- `alignment`, `formatters`, and backend-specific `highlighters`

A formatter has signature `(value, row, column) -> formatted_value`; formatters run in
vector order. Ensure each formatter accepts the output type of the previous one.

Highlighters are backend-specific: `TextHighlighter`, `MarkdownHighlighter`, and
`HtmlHighlighter` do not share decoration types. Select the backend first, then open its
documentation instead of guessing constructor arguments.

Keep `allow_markdown_in_cells=false` and `allow_html_in_cells=false` for untrusted cell
content. Enable raw markup only for data the application controls.

Use `Term.Tables.Table` instead only when cells or surrounding layout are Term renderables.

## Sources

- [PrettyTables 3 usage](https://ronisbr.github.io/PrettyTables.jl/stable/man/usage/)
- [Text backend](https://ronisbr.github.io/PrettyTables.jl/stable/man/text/text_backend/)
- [Markdown backend](https://ronisbr.github.io/PrettyTables.jl/stable/man/markdown/markdown_backend/)
- [HTML backend](https://ronisbr.github.io/PrettyTables.jl/stable/man/html/html_backend/)
- [PrettyTables library reference](https://ronisbr.github.io/PrettyTables.jl/stable/lib/library/)
