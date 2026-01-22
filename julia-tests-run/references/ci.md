# Test CI Integration

## GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        julia-version: ['1.10', '1', 'nightly']
    steps:
      - uses: actions/checkout@v4
      - uses: julia-actions/setup-julia@v2
        with:
          version: ${{ matrix.julia-version }}
      - uses: julia-actions/cache@v2
      - uses: julia-actions/julia-buildpkg@v1
      - uses: julia-actions/julia-runtest@v1
        with:
          test_args: '--threads=auto'
      - uses: julia-actions/julia-processcoverage@v1
      - uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
```

## Buildkite Pipeline

```yaml
# .buildkite/pipeline.yml
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

## Running Specific Test Groups

```bash
# Run only JET tests
JET_TEST=true julia --project=. -e 'using Pkg; Pkg.test()'

# Run GPU tests
GPU_TEST=cuda julia --project=. -e 'using Pkg; Pkg.test()'

# Run base test category
TEST_CATEGORY=base julia --project=. -e 'using Pkg; Pkg.test()'
```
