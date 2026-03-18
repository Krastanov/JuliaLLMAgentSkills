# Progress Columns Reference

## Built-in Column Types

Import from `Term.Progress`:

| Column | Description | Key kwargs |
|--------|-------------|------------|
| `DescriptionColumn` | Job description text | `style` |
| `ProgressColumn` | Visual progress bar | `completed_char`, `remaining_char`, `style` |
| `CompletedColumn` | "N/Total" count | `style` |
| `SeparatorColumn` | Visual separator | `style` |
| `PercentageColumn` | Percentage complete | `style` |
| `ElapsedColumn` | Time elapsed | `style` |
| `ETAColumn` | Estimated time remaining | `style` |
| `SpeedColumn` | Iterations per second | `style` |
| `SpinnerColumn` | Animated spinner | `spinnertype`, `style` |

## Presets

| Preset | Columns included |
|--------|-----------------|
| `:minimal` | Description, ProgressBar |
| `:default` | Description, ProgressBar, Percentage, Completed |
| `:detailed` | Description, ProgressBar, Percentage, Completed, Elapsed, ETA, Speed |
| `:spinner` | Description, Spinner, Completed |

## Custom Column Selection

```julia
using Term.Progress

mycols = [DescriptionColumn, CompletedColumn, SeparatorColumn, ProgressColumn]
cols_kwargs = Dict(
    :DescriptionColumn => Dict(:style => "red bold"),
    :ProgressColumn => Dict(:completed_char => '█', :remaining_char => '░'),
)

pbar = ProgressBar(; columns=mycols, columns_kwargs=cols_kwargs, width=100)
```

## Per-Job Column Overrides

```julia
job = addjob!(pbar; N=10, description="Custom",
    columns_kwargs=Dict(
        :ProgressColumn => Dict(:completed_char => 'x', :remaining_char => '_'),
    )
)
```

## Custom Column Interface

Create a custom column by subtyping `AbstractColumn`:

```julia
using Term.Progress
import Term.Progress: AbstractColumn, update!
import Term.Segments: Segment
import Term.Measures: Measure

struct MyColumn <: AbstractColumn
    job::ProgressJob
    segments::Vector{Segment}
    measure::Measure
    style::String

    function MyColumn(job::ProgressJob; style="blue")
        txt = Segment("init", style)
        return new(job, [txt], txt.measure, style)
    end
end

function Progress.update!(col::MyColumn, color::String, args...)::String
    # Return styled text for this column
    value = "step $(col.job.i)"
    return Segment(value, col.style).text
end
```

### Required fields
- `job::ProgressJob` -- the associated job
- `segments::Vector{Segment}` -- current display segments
- `measure::Measure` -- current size
- `style::String` -- default style

### Required constructor
```julia
MyColumn(job::ProgressJob; kwargs...)
```
Accepts the job and any kwargs from `columns_kwargs`.

### Required method
```julia
Progress.update!(col::MyColumn, color::String, args...)::String
```
Called each render cycle. Return the text to display for this column.

## Spinner Types

```julia
using Term.Progress: SPINNERS

# Available spinners (keys of SPINNERS dict):
# :dots, :line, :braille, :toggle, :arrow, etc.

columns_kwargs = Dict(
    :SpinnerColumn => Dict(:spinnertype => :dots, :style => "bold green"),
)
```
