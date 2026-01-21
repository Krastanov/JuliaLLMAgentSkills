# Julia CI with GitHub Actions

Configure continuous integration for Julia packages using GitHub Actions.

## Core Workflows

A complete CI setup includes:

| Workflow | Purpose |
|----------|---------|
| `ci.yml` | Main tests across OS/Julia versions |
| `ci-julia-nightly.yml` | Test against Julia nightly/alpha |
| `downgrade.yml` | Test with minimum dependency versions |
| `benchmark.yml` | Performance tracking on PRs |
| `spelling.yml` | Spell checking with typos |
| `changelog-enforcer.yml` | Require CHANGELOG updates |
| `TagBot.yml` | Automatic tagging after registry merge |

## Main CI Workflow

### .github/workflows/ci.yml

```yaml
name: CI
on:
  push:
    branches: [master, main]
    tags: ["*"]
  pull_request:

concurrency:
  # Limit concurrent builds; allow multiple on main branch
  group: ${{ github.workflow }}-${{ github.ref }}-${{ (github.ref != 'refs/heads/master' && github.ref != 'refs/heads/main') || github.run_number }}
  cancel-in-progress: ${{ startsWith(github.ref, 'refs/pull/') }}

env:
  PYTHON: ~  # Disable Python/PyCall auto-detection

jobs:
  test:
    name: Julia ${{ matrix.version }} - t=${{ matrix.threads }} - ${{ matrix.os }} - ${{ matrix.arch }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        version:
          - '1'          # Latest stable
          - '1.10'       # LTS or specific version
        os:
          - ubuntu-latest
        threads:
          - '2'
        arch:
          - x64
        include:
          # macOS ARM
          - arch: aarch64
            os: macos-latest
            version: '1'
            threads: '1'
          # Windows
          - arch: x64
            os: windows-latest
            version: '1'
            threads: '1'
    steps:
      - uses: actions/checkout@v6
      - uses: julia-actions/setup-julia@v2
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
      - uses: julia-actions/setup-julia@v2
        with:
          version: '1'
      - uses: julia-actions/cache@v2
      - uses: julia-actions/julia-buildpkg@v1
      - uses: julia-actions/julia-docdeploy@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          DOCUMENTER_KEY: ${{ secrets.DOCUMENTER_KEY }}
```

## Nightly/Alpha Testing

### .github/workflows/ci-julia-nightly.yml

```yaml
name: CI-nightly
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
    name: Julia ${{ matrix.version }} - jet=${{ matrix.jet }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        include:
          # Julia nightly/alpha
          - os: ubuntu-latest
            arch: x64
            version: alpha
            threads: 2
            jet: 'false'
          # JET static analysis (on stable)
          - os: ubuntu-latest
            arch: x64
            version: '1'
            threads: 2
            jet: 'true'
    steps:
      - uses: actions/checkout@v6
      - uses: julia-actions/install-juliaup@v2
        with:
          channel: ${{ matrix.version }}~${{ matrix.arch }}
      - uses: julia-actions/cache@v2
      - uses: julia-actions/julia-buildpkg@v1
      - uses: julia-actions/julia-runtest@v1
        env:
          JULIA_NUM_THREADS: ${{ matrix.threads }}
          JET_TEST: ${{ matrix.jet }}
      - uses: julia-actions/julia-processcoverage@v1
      - uses: codecov/codecov-action@v5
        with:
          files: lcov.info
          token: ${{ secrets.CODECOV_TOKEN }}
```

## Downgrade Testing

Tests with minimum supported dependency versions.

### .github/workflows/downgrade.yml

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
      - uses: julia-actions/setup-julia@v2
        with:
          version: ${{ matrix.version }}
      - uses: julia-actions/julia-downgrade-compat@v2
        with:
          skip: Pkg,TOML,InteractiveUtils,Random,LinearAlgebra
      - uses: julia-actions/cache@v2
      - uses: julia-actions/julia-buildpkg@v1
      - uses: julia-actions/julia-runtest@v1
```

## TagBot

Automatic tagging after Julia registry merge.

### .github/workflows/TagBot.yml

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

## Spell Checking

### .github/workflows/spelling.yml

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

### .typos.toml

```toml
[default.extend-words]
# Add domain-specific words that aren't typos
ket = "ket"
bra = "bra"
```

## Changelog Enforcer

### .github/workflows/changelog-enforcer.yml

```yaml
name: "Changelog Enforcer"
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review, labeled, unlabeled]

jobs:
  changelog:
    runs-on: ubuntu-latest
    steps:
      - uses: dangoslen/changelog-enforcer@v3
```

## Dependabot

### .github/dependabot.yml

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

## Documentation with Graphics

For packages requiring a display (Makie, Plots):

```yaml
docs:
  name: Documentation
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v6
    - name: Install binary dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y xorg-dev mesa-utils xvfb libgl1 freeglut3-dev \
          libxrandr-dev libxinerama-dev libxcursor-dev libxi-dev libxext-dev
    - uses: julia-actions/setup-julia@v2
      with:
        version: '1'
    - uses: julia-actions/cache@v2
    - uses: julia-actions/julia-buildpkg@v1
    - uses: julia-actions/julia-docdeploy@v1
      with:
        prefix: xvfb-run
      env:
        GKSwstype: nul
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        DOCUMENTER_KEY: ${{ secrets.DOCUMENTER_KEY }}
```

## Testing Sublibraries

For monorepos with multiple packages:

```yaml
- uses: julia-actions/julia-buildpkg@v1
  with:
    project: 'lib/SubPackage'
- uses: julia-actions/julia-runtest@v1
  with:
    project: 'lib/SubPackage'
  env:
    JULIA_NUM_THREADS: ${{ matrix.threads }}
```

## Coverage for Extensions

```yaml
- uses: julia-actions/julia-processcoverage@v1
  with:
    directories: './src,./ext,./lib/SubPkg/src'
```

## Required Secrets

| Secret | Purpose | How to Generate |
|--------|---------|-----------------|
| `CODECOV_TOKEN` | Code coverage upload | From codecov.io dashboard |
| `DOCUMENTER_KEY` | Documentation deployment | `DocumenterTools.genkeys()` |
| `GITHUB_TOKEN` | Auto-provided | Built-in |

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `PYTHON: ~` | Disable PyCall auto-detection |
| `PYCALL_DEBUG_BUILD: yes` | Debug PyCall issues |
| `GKSwstype: nul` | Fix Plots/GR on headless |
| `JULIA_NUM_THREADS` | Set thread count |

## Related Skills

- `julia-ci-buildkite` - Buildkite CI configuration
- `julia-tests` - Test setup and patterns
- `julia-benchmarks` - Benchmark configuration
- `julia-docs` - Documentation setup
