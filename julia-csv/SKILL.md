---
name: julia-csv
description: Parse and write delimited text data with CSV.jl, including CSV.File/CSV.read/CSV.Rows/CSV.Chunks for ingestion and CSV.write/CSV.RowWriter for output, with control over schema, delimiters, missing values, quoting, dates, pooling, and multithreading. Use this skill when handling CSV/TSV/fixed-width style files in Julia.
---

# Julia Csv

Use CSV.jl for high-performance reading/writing of delimited data with explicit control over parsing behavior.

## Choose the Read Mode

- `CSV.File(input; kw...)`: full-column parse, table-like object, best default.
- `CSV.read(input, sink; kw...)`: parse and hand columns directly to sink (e.g. `DataFrame`) without intermediate copies.
- `CSV.Rows(input; kw...)`: row-streaming with lower memory footprint; supports `reusebuffer=true`.
- `CSV.Chunks(input; ntasks=...)`: chunked parsing for very large files.

```julia
using CSV, DataFrames

f = CSV.File("data.csv")
df = CSV.read("data.csv", DataFrame)
```

## Parse Schema and Layout Explicitly

Common schema/layout controls:
- `header`, `normalizenames`, `skipto`, `footerskip`
- `select` / `drop`, `limit`
- `types`, `typemap`, `stringtype`, `pool`, `downcast`
- `strict`, `silencewarnings`, `maxwarnings`

Delimiter and cell interpretation:
- `delim`, `ignorerepeated` (fixed-width style data)
- `missingstring`
- `quoted`, `quotechar` / `openquotechar` / `closequotechar`, `escapechar`
- `dateformat`, `decimal`, `groupmark`, `truestrings`, `falsestrings`

Threading and chunking:
- `ntasks`, `rows_to_check`

## Support Multiple Input Forms

CSV.jl supports:
- filename/filepath
- `IO` / `Cmd`
- `Vector{UInt8}`
- vector of inputs for vertical concatenation (matching schema)

Gzip (`.gz`) input is handled automatically; use `buffer_in_memory=true` if needed.

## Write CSV Output

```julia
CSV.write("out.csv", table)
rows = CSV.RowWriter(table)
```

Useful write controls:
- `delim`, `quotechar`, `openquotechar`, `closequotechar`, `escapechar`
- `missingstring`, `dateformat`, `decimal`
- `append`, `header`, `newline`, `quotestrings`
- `transform`, `bom`, `compress`, `partition`, `bufsize`

## Reference

- `references/csv-patterns.md` - read/write mode selection and option patterns

## Related Skills

- `julia-prettytables` - rendering parsed tabular data
