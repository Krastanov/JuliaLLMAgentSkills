# Tables.jl and DataFrames.jl

Use Tables.jl as the common input/output contract. Use DataFrames.jl when the task needs
named-column manipulation, grouping, joins, or row filtering.

## Consume a Generic Table

```julia
using Tables

rows = Tables.rows(table)
schema = Tables.schema(rows)  # may be nothing

for row in rows
    names = Tables.columnnames(row)
    values = map(name -> Tables.getcolumn(row, name), names)
    # process this row
end
```

Use `Tables.columns(table)` for column-oriented work. Do not assume
`Tables.schema(...)` is known; fall back to `Tables.columnnames` on the first row or on the
columns object. Use `Tables.rowtable` or `Tables.columntable` only when that materialized
shape is actually useful.

Wrap a matrix before passing it to a Tables.jl sink:

```julia
tbl = Tables.table(matrix; header=[:x, :y])
```

## Use a Minimal DataFrame Workflow

```julia
using CSV, DataFrames, Statistics

df = CSV.read(
    "measurements.csv",
    DataFrame;
    types=Dict(:sample_id => Int, :value => Float64),
    missingstring=["", "NA"],
)

@assert allunique(df.sample_id)
@assert all(x -> ismissing(x) || isfinite(x), df.value)

clean = subset(df, :value => ByRow(!ismissing))
scaled = transform(clean, :value => (x -> x ./ maximum(x)) => :scaled_value)
summary = combine(groupby(scaled, :group), :value => mean => :mean_value)
```

Choose operations by row-shape behavior:

- `select` chooses or derives columns and preserves row count.
- `transform` retains existing columns, adds derived columns, and preserves row count.
- `subset` filters rows.
- `groupby` plus `combine` produces group summaries and may change row count.
- Bang variants mutate; use them only when ownership is clear and mutation is intentional.

DataFrames copies selected columns by default. Use `copycols=false` only when aliasing the
source columns is deliberate. Transformation functions may run in tasks when threading is
enabled; keep them free of shared mutable state or pass `threads=false` for a genuinely
serial requirement.

## Keep the Boundary Clear

- Do not convert every Tables.jl source to a `DataFrame` merely to iterate rows.
- Do not use a `Matrix` for heterogeneous columns; conversion promotes element types and
  discards column names.
- Keep parsing, validation, transformation, and presentation as separate functions so each
  can be tested with small in-memory tables.

## Sources

- [Tables.jl: Using the Interface](https://tables.juliadata.org/stable/using-the-interface/)
- [DataFrames.jl: First Steps](https://dataframes.juliadata.org/stable/man/basics/)
- [DataFrames.jl: Working with DataFrames](https://dataframes.juliadata.org/stable/man/working_with_dataframes/)
- [DataFrames.jl function reference and threading behavior](https://dataframes.juliadata.org/stable/lib/functions/index.html)
