# Workflow Templates

## Table of Contents

- [Full CI Workflow](#full-ci-workflow)
- [Nightly/Alpha Testing](#nightlyalpha-testing)
- [Downgrade Testing](#downgrade-testing)
- [TagBot](#tagbot)
- [Spell Checking](#spell-checking)
- [Changelog Enforcer](#changelog-enforcer)
- [Dependabot](#dependabot)

## Full CI Workflow

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
  pull_request:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ startsWith(github.ref, 'refs/pull/') }}

env:
  PYTHON: ~

jobs:
  test:
    name: Julia ${{ matrix.version }} - jet=${{ matrix.jet }}
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        include:
          - version: alpha
            jet: 'false'
          - version: '1'
            jet: 'true'
    steps:
      - uses: actions/checkout@v6
      - uses: julia-actions/install-juliaup@v2
        with:
          channel: ${{ matrix.version }}~x64
      - uses: julia-actions/cache@v2
      - uses: julia-actions/julia-buildpkg@v1
      - uses: julia-actions/julia-runtest@v1
        env:
          JET_TEST: ${{ matrix.jet }}
```

## Downgrade Testing

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
    steps:
      - uses: actions/checkout@v6
      - uses: julia-actions/setup-julia@v2
        with:
          version: '1'
      - uses: julia-actions/julia-downgrade-compat@v2
        with:
          skip: Pkg,TOML,InteractiveUtils,Random,LinearAlgebra
      - uses: julia-actions/cache@v2
      - uses: julia-actions/julia-buildpkg@v1
      - uses: julia-actions/julia-runtest@v1
```

## TagBot

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
