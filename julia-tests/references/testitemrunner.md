# TestItemRunner.jl

Use this reference when the package uses `@testitem` tests.

## CLI Commands

```bash
julia -tauto --project=test -e 'using TestItemRunner; TestItemRunner.run_tests("test")'
julia -tauto --project=test -e 'using TestItemRunner; TestItemRunner.run_tests("test"; filter=ti->(:core in ti.tags))'
julia -tauto --project=test -e 'using TestItemRunner; TestItemRunner.run_tests("test"; filter=ti->occursin(r"fft.*edge", ti.name))'
```

## `runtests.jl` Pattern

```julia
using MyPackage
using TestItemRunner

testfilter = ti -> begin
    exclude = Symbol[]
    if get(ENV, "JET_TEST", "") == "true"
        return :jet in ti.tags
    else
        push!(exclude, :jet)
    end
    if VERSION < v"1.10"
        push!(exclude, :doctests, :aqua)
    end
    return all(!in(exclude), ti.tags)
end

@run_package_tests filter=testfilter
```

## Filtering Rules

1. Tags are `Symbol`s.
2. `ti.filename` is a full path, so use `endswith` or regex.
3. Keep filter functions simple and pure.

## When To Open More

- For writing filter-friendly `@testitem`s:
  `references/testitem.md`

