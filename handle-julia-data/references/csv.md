# CSV.jl

## Choose the Read API

| Need | API | Important constraint |
|---|---|---|
| Materialized `DataFrame` | `CSV.read(source, DataFrame; kwargs...)` | Avoids unnecessary column copies for this sink. |
| Reusable Tables.jl source | `CSV.File(source; kwargs...)` | Materializes parsed columns. |
| Minimal-memory row iteration | `CSV.Rows(source; kwargs...)` | Does no type inference unless `type`/`types` is supplied. |
| File partitions | `CSV.Chunks(source; kwargs...)` | Experimental; each chunk infers types independently unless types are fixed. |

Start with `CSV.read` or `CSV.File`. Select `CSV.Rows` only for a genuinely streaming,
single-pass algorithm. Select `CSV.Chunks` only when the consumer benefits from partitions
and can honor a stable schema.

```julia
using CSV, DataFrames, Dates

df = CSV.read(
    "input.csv",
    DataFrame;
    types=Dict(:id => Int, :date => Date, :value => Float64),
    dateformat="yyyy-mm-dd",
    missingstring=["", "NA"],
    strict=true,
)
```

Use `IOBuffer(text)` for CSV data already held in a `String`. Sources may also be paths,
byte vectors, `IO` objects, commands, or vectors of matching inputs. Only gzip input is
automatically decompressed; `buffer_in_memory=true` trades temporary-file use for memory.

## Stream Rows Safely

```julia
rows = CSV.Rows("large.csv"; types=Dict(:id => Int), reusebuffer=true)
for row in rows
    consume(row.id, row.payload)
end
```

With `reusebuffer=true`, the current row becomes invalid after iteration advances. Never
store those row objects or call `collect(rows)`. Without explicit types, cells are
essentially `Union{String,Missing}`.

## Use Chunks Deliberately

```julia
for chunk in CSV.Chunks("large.csv"; types=Dict(:id => Int, :value => Float64))
    consume_partition(chunk)
end
```

Each chunk is a `CSV.File`. Fix types when partitions feed the same downstream operation;
otherwise later values can cause different inferred column types. `ntasks` controls parser
tasks for `CSV.File` and the number of `CSV.Chunks` partitions, but does not apply to
`CSV.Rows`. For an exact `limit` on a large file, also use `ntasks=1`.

`ignorerepeated=true` handles repeated delimiter padding, such as whitespace-aligned
fields. It is not a general parser for arbitrary fixed character ranges.

## Write Tables

```julia
CSV.write("output.csv", table; writeheader=true)

for line in CSV.RowWriter(table; delim='\t')
    consume(line)
end
```

For `CSV.write`, use `append`, `compress`, or `partition` only when the output contract
requires them. When appending, column names are omitted by default; set `writeheader`
explicitly if needed. `CSV.RowWriter` is an iterator of formatted row strings and does not
support file-level options such as append, compression, or partitioning.

## Sources

- [CSV.jl reading reference](https://csv.juliadata.org/stable/reading.html)
- [CSV.jl writing reference](https://csv.juliadata.org/stable/writing.html)
- [CSV.jl examples](https://csv.juliadata.org/stable/examples.html)
