---
name: julia-prettytables
description: Render Julia tables with PrettyTables.jl in text, markdown, and HTML backends, including table sections (titles, labels, summary rows, footnotes), formatters, highlighters, and backend-specific styling/format options. Use this skill when displaying matrix/table data for terminal output, markdown reports, or HTML pages.
---

# Julia PrettyTables

Use `PrettyTables.jl` to render tabular data consistently across text, markdown, and HTML outputs.

## Core Rendering Flow

```julia
using PrettyTables

pretty_table(data)  # default text backend
md = pretty_table(String, data; backend=:markdown)
html = pretty_table(String, data; backend=:html, stand_alone=true)
```

Use `String` output when the table must be embedded in logs, markdown files, or generated HTML.

## Configure Table Sections

Use section-related keywords for report-style output:
- `title`, `subtitle`
- `column_labels`, `row_labels`, `show_row_number_column`, `row_group_labels`
- `summary_rows`, `summary_row_labels`
- `footnotes`, `source_notes`
- `merge_column_label_cells`

For alignment and display behavior:
- `alignment`, `column_label_alignment`, other section-specific alignment options
- `maximum_number_of_rows`, `maximum_number_of_columns`, `vertical_crop_mode`
- `renderer`, `compact_printing`, `limit_printing`

## Format and Highlight Data

- Use `formatters` to transform displayed cell text.
- Use backend-specific highlighters:
  - `TextHighlighter`
  - `MarkdownHighlighter`
  - `HtmlHighlighter`

Apply formatter logic first in design, then add highlighters for visual emphasis.

## Backend-Specific Controls

- Text (`backend=:text`): `table_format::TextTableFormat`, `style::TextTableStyle`, line wrapping/cropping controls.
- Markdown (`backend=:markdown`): `allow_markdown_in_cells`, `line_breaks`, `table_format::MarkdownTableFormat`.
- HTML (`backend=:html`): `allow_html_in_cells`, `stand_alone`, `minify`, `wrap_table_in_div`, `table_format::HtmlTableFormat`, `style::HtmlTableStyle`.

Prefer markdown backend for docs/README and HTML backend for web/report export.

## Reference

- `references/prettytables-patterns.md` - sections, backends, and styling examples

## Related Skills

- `julia-csv` - CSV data ingestion before tabular rendering
