---
name: handle-julia-data
description: Build and repair focused Julia data workflows that consume Tables.jl sources, transform tabular data with DataFrames.jl, read or write delimited files with CSV.jl, handle TOML or YAML configuration, and render ordinary reports with PrettyTables.jl. Use for CSV/TSV ingestion, table transformations, configuration serialization, schema validation, and terminal/Markdown/HTML table output; do not use as a general statistics, database, plotting, or machine-learning guide.
---

# Handle Julia Data

Choose the narrowest workflow that fits. Inspect the active project and existing package
choices before adding dependencies.

## Route the Task

- Consume an arbitrary table or transform a `DataFrame`: read
  [references/tables-dataframes.md](references/tables-dataframes.md).
- Read or write CSV, TSV, padded-delimiter, streaming-row, or partitioned data: read
  [references/csv.md](references/csv.md).
- Parse or emit configuration in TOML or YAML: read
  [references/toml-yaml.md](references/toml-yaml.md).
- Format an ordinary table for a terminal, Markdown, or HTML report: read
  [references/prettytables.md](references/prettytables.md).

Open only the references required by the task.

## Apply These Defaults

1. Treat Tables.jl as the interchange boundary; materialize a `DataFrame` only when its
   transformations or indexing are useful.
2. For a `DataFrame`, prefer `CSV.read(source, DataFrame)` over constructing a temporary
   `CSV.File` and copying it into a frame.
3. Validate names, types, missing-value policy, and key invariants immediately after input.
   Supply types and date formats when inference would be risky.
4. Prefer TOML for Julia-owned configuration. Use YAML only when an external format or
   existing file requires it.
5. Use Pkg operations for dependency and compatibility changes. Do not rewrite a
   `Manifest.toml` with `TOML.print`.
6. Use PrettyTables for ordinary reports. Use Term tables only when the table must compose
   with a Term renderable or live terminal application.
7. Test round trips semantically, not by requiring emitted text to preserve whitespace,
   comments, quoting, or key order.

Keep format-specific option inventories in the references rather than repeating them here.
