# CSV.jl Patterns

## Basic Read APIs

```julia
using CSV

f = CSV.File("data.csv")
```

Direct to sink:

```julia
using DataFrames
df = CSV.read("data.csv", DataFrame)
```

Streaming rows:

```julia
rows = CSV.Rows("data.csv"; reusebuffer=true)
for row in rows
    # process row
end
```

Chunked parsing:

```julia
chunks = CSV.Chunks("big.csv"; ntasks=8)
for chunk in chunks
    # chunk is CSV.File
end
```

## Common Parsing Controls

Layout/header:
- `header`
- `normalizenames`
- `skipto`
- `footerskip`
- `comment`
- `ignoreemptyrows`

Column selection and limits:
- `select` / `drop`
- `limit`
- `ntasks`
- `rows_to_check`

Missing/quoting/delimiters:
- `missingstring`
- `delim`
- `ignorerepeated`
- `quoted`
- `quotechar` / `openquotechar` / `closequotechar`
- `escapechar`

Type behavior:
- `dateformat`
- `decimal`
- `groupmark`
- `truestrings` / `falsestrings`
- `types`
- `typemap`
- `pool`
- `downcast`
- `stringtype`
- `strict`
- `silencewarnings`
- `maxwarnings`

## Input Types

CSV.jl accepts:
- file paths
- `IO` / `Cmd`
- `Vector{UInt8}`
- vectors of inputs for vertical concatenation

For gzip (`.gz`) input, CSV.jl supports automatic decompression.

## Writing APIs

```julia
CSV.write("out.csv", table)
```

Row-by-row formatted output:

```julia
for line in CSV.RowWriter(table)
    # each line is one CSV row string
end
```

Common write options:
- `bufsize`
- `delim`
- `quotechar` / `openquotechar` / `closequotechar`
- `escapechar`
- `missingstring`
- `dateformat`
- `append`
- `header`
- `newline`
- `quotestrings`
- `decimal`
- `transform`
- `bom`
- `partition`
- `compress`

## Source

- CSV docs: `https://csv.juliadata.org/latest/`
