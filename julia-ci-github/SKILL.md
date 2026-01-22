---
name: julia-ci-github
description: Configure GitHub Actions CI for Julia packages including testing, documentation, and benchmarks. Use this skill when setting up or modifying CI workflows.
---

# Julia CI with GitHub Actions

Configure continuous integration for Julia packages using GitHub Actions.

## Core Workflows

| Workflow | Purpose |
|----------|---------|
| `ci.yml` | Main tests across OS/Julia versions |
| `ci-julia-nightly.yml` | Test against Julia nightly/alpha |
| `downgrade.yml` | Test with minimum dependency versions |
| `benchmark.yml` | Performance tracking on PRs |
| `TagBot.yml` | Automatic tagging after registry merge |

## Main CI Workflow

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
    name: Julia ${{ matrix.version }} - ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        version: ['1', '1.10']
        os: [ubuntu-latest]
    steps:
      - uses: actions/checkout@v6
      - uses: julia-actions/setup-julia@v2
        with:
          version: ${{ matrix.version }}
      - uses: julia-actions/cache@v2
      - uses: julia-actions/julia-buildpkg@v1
      - uses: julia-actions/julia-runtest@v1
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

## Required Secrets

| Secret | Purpose | How to Generate |
|--------|---------|-----------------|
| `CODECOV_TOKEN` | Coverage upload | From codecov.io dashboard |
| `DOCUMENTER_KEY` | Doc deployment | `DocumenterTools.genkeys()` |
| `GITHUB_TOKEN` | Auto-provided | Built-in |

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `PYTHON: ~` | Disable PyCall auto-detection |
| `GKSwstype: nul` | Fix Plots/GR on headless |
| `JULIA_NUM_THREADS` | Set thread count |

## Reference

- **[Workflow Templates](references/workflows.md)** - Complete workflow files for all scenarios
- **[Advanced Configurations](references/advanced.md)** - Graphics, sublibraries, coverage for extensions

## Related Skills

- `julia-ci-buildkite` - Buildkite CI configuration
- `julia-tests` - Test setup and patterns
