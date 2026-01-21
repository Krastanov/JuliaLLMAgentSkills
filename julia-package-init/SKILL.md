# Julia Package Initialization

Create a new Julia package with modern infrastructure: tests, documentation, CI, and more.

## Package Structure

A complete modern Julia package:

```
MyPackage.jl/
├── .buildkite/
│   └── pipeline.yml
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       ├── ci.yml
│       ├── ci-julia-nightly.yml
│       ├── downgrade.yml
│       ├── benchmark.yml
│       ├── spelling.yml
│       ├── changelog-enforcer.yml
│       └── TagBot.yml
├── benchmark/
│   ├── Project.toml
│   └── benchmarks.jl
├── docs/
│   ├── Project.toml
│   ├── make.jl
│   └── src/
│       ├── index.md
│       └── API.md
├── ext/
│   └── MyPackageSomeDepExt.jl
├── src/
│   └── MyPackage.jl
├── test/
│   ├── Project.toml
│   └── runtests.jl
├── .gitattributes
├── .gitignore
├── .typos.toml
├── CHANGELOG.md
├── LICENSE
├── Project.toml
└── README.md
```

## Creating a New Package

### Using PkgTemplates.jl (Recommended)

```julia
using PkgTemplates

t = Template(;
    user = "YourGitHubUsername",
    authors = "Your Name <your@email.com>",
    plugins = [
        Git(; manifest=false),
        GitHubActions(; extra_versions=["1.10", "nightly"]),
        Codecov(),
        Documenter{GitHubActions}(),
        License(; name="MIT"),
    ],
)

t("MyPackage")
```

### Manual Creation

```bash
mkdir -p MyPackage.jl/{src,test,docs/src,ext,.github/workflows,.buildkite,benchmark}
cd MyPackage.jl
```

## Core Files

### Project.toml

```toml
name = "MyPackage"
uuid = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"  # Generate with `using UUIDs; uuid4()`
version = "0.1.0"
authors = ["Your Name <your@email.com>"]

[workspace]
projects = ["docs", "benchmark"]

[deps]
# Direct dependencies here

[weakdeps]
# Optional dependencies that trigger extensions
Makie = "ee78f7c6-11fb-53f2-987a-cfe4a2b5a57a"

[extensions]
MyPackageMakieExt = "Makie"

[compat]
julia = "1.10"
# Add compat entries for all deps
```

### src/MyPackage.jl

```julia
module MyPackage

export main_function, MainType

include("types.jl")
include("functions.jl")

end # module
```

### .gitignore

```gitignore
*.ipynb_checkpoints
Manifest.toml
LocalPreferences.toml
*/.*.swp
scratch/
*.cov
.history
.vscode
```

### .gitattributes

```
*.jl diff=julia
```

### LICENSE

Use MIT, BSD, or Apache 2.0. Generate at https://choosealicense.com/

## Test Setup

### test/Project.toml

```toml
[deps]
Aqua = "4c88cf16-eb10-579e-8560-4a9242c79595"
Documenter = "e30172f5-a6a5-5a46-863b-614d45cd2de4"
JET = "c3a54625-cd67-489e-a8e7-0a5a0ff4e31b"
MyPackage = "your-package-uuid"
Test = "8dfed614-e22c-5e08-85e1-65c5234f0b40"
TestItemRunner = "f8b46487-2199-4994-9208-9a1283c18c0a"
```

### test/runtests.jl

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

See the `julia-tests` skill for detailed test patterns.

## GitHub Actions CI

### .github/workflows/ci.yml

```yaml
name: CI
on:
  push:
    branches: [master, main]
    tags: ["*"]
  pull_request:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}-${{ (github.ref != 'refs/heads/master' && github.ref != 'refs/heads/main') || github.run_number }}
  cancel-in-progress: ${{ startsWith(github.ref, 'refs/pull/') }}

env:
  PYTHON: ~

jobs:
  test:
    name: Julia ${{ matrix.version }} - t=${{ matrix.threads }} - ${{ matrix.os }} - ${{ matrix.arch }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        version:
          - '1'
          - '1.10'
        os:
          - ubuntu-latest
        threads:
          - '2'
        arch:
          - x64
        include:
          - arch: aarch64
            os: macos-latest
            version: '1'
            threads: '1'
          - arch: x64
            os: windows-latest
            version: '1'
            threads: '1'
    steps:
      - uses: actions/checkout@v6
      - uses: julia-actions/setup-julia@v1
        with:
          version: ${{ matrix.version }}
          arch: ${{ matrix.arch }}
      - uses: julia-actions/cache@v2
      - uses: julia-actions/julia-buildpkg@v1
      - uses: julia-actions/julia-runtest@v1
        env:
          JULIA_NUM_THREADS: ${{ matrix.threads }}
      - uses: julia-actions/julia-processcoverage@v1
      - uses: codecov/codecov-action@v5
        with:
          files: lcov.info
          token: ${{ secrets.CODECOV_TOKEN }}

  docs:
    name: Documentation
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: julia-actions/setup-julia@v1
        with:
          version: '1'
      - uses: julia-actions/cache@v2
      - uses: julia-actions/julia-buildpkg@v1
      - uses: julia-actions/julia-docdeploy@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          DOCUMENTER_KEY: ${{ secrets.DOCUMENTER_KEY }}
```

### .github/workflows/downgrade.yml

Tests with minimum supported dependency versions:

```yaml
name: Downgrade
on:
  pull_request:
    branches: [master, main]
    paths-ignore:
      - 'docs/**'
  push:
    branches: [master, main]
    paths-ignore:
      - 'docs/**'

env:
  PYTHON: ~

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        version: ['1']
    steps:
      - uses: actions/checkout@v6
      - uses: julia-actions/setup-julia@v1
        with:
          version: ${{ matrix.version }}
      - uses: julia-actions/julia-downgrade-compat@v2
        with:
          skip: Pkg,TOML,InteractiveUtils,Random,LinearAlgebra
      - uses: julia-actions/cache@v2
      - uses: julia-actions/julia-buildpkg@v1
      - uses: julia-actions/julia-runtest@v1
```

### .github/workflows/TagBot.yml

Automatic tag creation after Julia registry merge:

```yaml
name: TagBot
on:
  issue_comment:
    types:
      - created
  workflow_dispatch:

jobs:
  TagBot:
    if: github.event_name == 'workflow_dispatch' || github.actor == 'JuliaTagBot'
    runs-on: ubuntu-latest
    steps:
      - uses: JuliaRegistries/TagBot@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          ssh: ${{ secrets.DOCUMENTER_KEY }}
```

### .github/workflows/benchmark.yml

PR benchmark comparison with AirspeedVelocity:

```yaml
name: Benchmarks
on:
  pull_request_target:
    branches: [master, main]

permissions:
  pull-requests: write

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: MilesCranmer/AirspeedVelocity.jl@action-v1
        with:
          julia-version: '1'
          tune: 'false'
```

### .github/workflows/spelling.yml

Spell checking with typos:

```yaml
name: Spell Check
on: [pull_request]

jobs:
  typos-check:
    name: Spell Check with Typos
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: crate-ci/typos@master
        with:
          config: .typos.toml
```

### .github/dependabot.yml

Automatic dependency updates:

```yaml
version: 2
enable-beta-ecosystems: true
updates:
  - package-ecosystem: "julia"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## Buildkite CI

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

## Spell Checking

### .typos.toml

```toml
[default.extend-words]
# Add domain-specific words that aren't typos
ket = "ket"
bra = "bra"
```

## Codecov Setup

1. Sign up at https://codecov.io with GitHub
2. Add repository
3. Copy the `CODECOV_TOKEN` to GitHub repository secrets

## Documenter Key Setup

For automatic documentation deployment:

```bash
# Generate deploy key
julia -e '
    using DocumenterTools
    DocumenterTools.genkeys(user="YourOrg", repo="MyPackage.jl")
'
```

Add the public key as a deploy key (with write access) in your GitHub repo settings.
Add the private key as `DOCUMENTER_KEY` in GitHub secrets.

## Registering the Package

### JuliaHub

1. Create account at https://juliahub.com
2. Use web interface to register

### Local Registration

```julia
using LocalRegistry
register("MyPackage")
```

### General Registry

Use [Registrator.jl](https://github.com/JuliaRegistries/Registrator.jl) or the GitHub
app by commenting `@JuliaRegistrator register` on a commit.

## Initialization Checklist

- [ ] `Project.toml` with UUID, version, compat
- [ ] `[workspace]` entry for subprojects
- [ ] `src/MyPackage.jl` with module structure
- [ ] `test/Project.toml` and `test/runtests.jl`
- [ ] `docs/` setup (see `julia-docs` skill)
- [ ] `.gitignore` and `.gitattributes`
- [ ] `LICENSE` file
- [ ] `README.md` with badges
- [ ] `.github/workflows/ci.yml`
- [ ] `.github/workflows/TagBot.yml`
- [ ] `.github/workflows/downgrade.yml`
- [ ] `.github/dependabot.yml`
- [ ] `CODECOV_TOKEN` secret added
- [ ] `DOCUMENTER_KEY` secret added

## Related Skills

- `julia-docs` - Documentation setup
- `julia-doctests` - Doctest configuration
- `julia-doccitations` - Bibliography setup
- `julia-tests` - Test patterns and setup (coming soon)
- `julia-ci` - CI configuration details (coming soon)
- `julia-benchmarks` - Benchmark setup (coming soon)
