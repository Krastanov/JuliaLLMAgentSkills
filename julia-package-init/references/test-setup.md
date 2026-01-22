# Test Setup

## test/Project.toml

```toml
[deps]
Aqua = "4c88cf16-eb10-579e-8560-4a9242c79595"
Documenter = "e30172f5-a6a5-5a46-863b-614d45cd2de4"
JET = "c3a54625-cd67-489e-a8e7-0a5a0ff4e31b"
MyPackage = "your-package-uuid"
Test = "8dfed614-e22c-5e08-85e1-65c5234f0b40"
TestItemRunner = "f8b46487-2199-4994-9208-9a1283c18c0a"
```

## test/runtests.jl

```julia
using MyPackage
using TestItemRunner

testfilter = ti -> begin
    exclude = Symbol[]
    if get(ENV, "JET_TEST", "") != "true"
        push!(exclude, :jet)
    end
    if !(VERSION >= v"1.10")
        push!(exclude, :doctests)
        push!(exclude, :aqua)
    end
    return all(!in(exclude), ti.tags)
end

println("Starting tests with $(Threads.nthreads()) threads out of `Sys.CPU_THREADS = $(Sys.CPU_THREADS)`...")

@run_package_tests filter=testfilter
```

## Buildkite Pipeline

### .buildkite/pipeline.yml

```yaml
env:
  CODECOV_TOKEN: your-codecov-token
  JULIA_NUM_THREADS: auto,auto
  PYTHON: ""

steps:
  - label: "MyPackage Tests - {{matrix.LABEL}}"
    plugins:
      - JuliaCI/julia#v1:
          version: "1"
      - JuliaCI/julia-test#v1:
      - JuliaCI/julia-coverage#v1:
          codecov: true
          dirs: './src,./ext'
    env:
      JET_TEST: "{{matrix.JET_TEST}}"
    agents:
      queue: "{{matrix.QUEUE}}"
    matrix:
      setup:
        LABEL: ["base tests"]
        QUEUE: ["default"]
        JET_TEST: ["false"]
      adjustments:
        - with:
            LABEL: "JET"
            QUEUE: default
            JET_TEST: true
```

## Documenter Key Setup

```bash
julia -e '
    using DocumenterTools
    DocumenterTools.genkeys(user="YourOrg", repo="MyPackage.jl")
'
```

Add the public key as a deploy key (with write access) in your GitHub repo settings.
Add the private key as `DOCUMENTER_KEY` in GitHub secrets.
