---
name: julia-ci-buildkite
description: Configure Buildkite CI for Julia packages, especially for GPU testing and specialized hardware. Use this skill when setting up Buildkite pipelines.
---

# Julia CI with Buildkite

Configure continuous integration for Julia packages using Buildkite.

Buildkite is useful for:
- GPU testing (CUDA, ROCm, OpenCL)
- Specialized hardware queues
- Long-running tests that exceed GitHub Actions limits
- Private/on-premise runners

## Basic Pipeline

### .buildkite/pipeline.yml

```yaml
env:
  CODECOV_TOKEN: your-codecov-token
  JULIA_NUM_THREADS: auto,auto
  PYTHON: ""

steps:
  - label: "MyPackage Tests"
    plugins:
      - JuliaCI/julia#v1:
          version: "1"
      - JuliaCI/julia-test#v1: ~
      - JuliaCI/julia-coverage#v1:
          codecov: true
          dirs: './src,./ext'
```

## Matrix Builds

### Simple Matrix

```yaml
steps:
  - label: "Tests - {{matrix.LABEL}}"
    plugins:
      - JuliaCI/julia#v1:
          version: "1"
      - JuliaCI/julia-test#v1: ~
      - JuliaCI/julia-coverage#v1:
          codecov: true
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

### GPU Testing Matrix

```yaml
steps:
  - label: "Tests - {{matrix.LABEL}}"
    plugins:
      - JuliaCI/julia#v1:
          version: "1"
          compiled_size_limit: 10737418240  # 10GiB
      - JuliaCI/julia-test#v1: ~
      - JuliaCI/julia-coverage#v1:
          codecov: true
          dirs: './src,./ext'
    env:
      JET_TEST: "{{matrix.JET_TEST}}"
      GPU_TEST: "{{matrix.GPU_TEST}}"
    agents:
      queue: "{{matrix.QUEUE}}"
    matrix:
      setup:
        LABEL: ["base tests"]
        QUEUE: ["default"]
        JET_TEST: ["false"]
        GPU_TEST: ["false"]
      adjustments:
        - with:
            LABEL: "JET"
            QUEUE: default
            JET_TEST: true
            GPU_TEST: false
        - with:
            LABEL: "GPU - CUDA"
            QUEUE: cuda
            JET_TEST: false
            GPU_TEST: "cuda"
        - with:
            LABEL: "GPU - ROCm"
            QUEUE: rocm
            JET_TEST: false
            GPU_TEST: "rocm"
        - with:
            LABEL: "GPU - OpenCL"
            QUEUE: default
            JET_TEST: false
            GPU_TEST: "opencl"
```

## Test Categories

Split tests into categories for parallel execution:

```yaml
matrix:
  setup:
    LABEL: ["base tests"]
    QUEUE: ["default"]
    TEST_CATEGORY: ["false"]
  adjustments:
    - with:
        LABEL: "ECC Base"
        QUEUE: default
        TEST_CATEGORY: "base"
    - with:
        LABEL: "ECC Encoding"
        QUEUE: default
        TEST_CATEGORY: "encoding"
    - with:
        LABEL: "ECC Decoding"
        QUEUE: default
        TEST_CATEGORY: "decoding"
```

## Graphics/Display Tests

Use xvfb plugin for headless display:

```yaml
steps:
  - label: "Plotting Tests"
    plugins:
      - JuliaCI/julia#v1:
          version: "1"
      - QuantumSavory/julia-xvfb#v1: ~
      - JuliaCI/julia-test#v1: ~
      - JuliaCI/julia-coverage#v1:
          codecov: true
    env:
      MYPACKAGE_PLOT_TEST: true
```

## Downstream Testing

Test packages that depend on yours:

```yaml
steps:
  - label: "Downstream Tests - {{matrix.PACKAGE}}"
    plugins:
      - JuliaCI/julia#v1:
          version: "1"
    command:
      - julia --project=$(mktemp -d) -e '
        using Pkg;
        pkg"dev .";
        Pkg.add("{{matrix.PACKAGE}}");
        Pkg.build("{{matrix.PACKAGE}}");
        Pkg.test("{{matrix.PACKAGE}}");'
    matrix:
      setup:
        PACKAGE: ["DependentPkg1", "DependentPkg2", "DependentPkg3"]
```

## Testing Subpackages

For monorepos:

```yaml
steps:
  - label: "SubPackage Tests"
    plugins:
      - JuliaCI/julia#v1:
          version: "1"
      - JuliaCI/julia-test#v1:
          package: "SubPackage"
      - JuliaCI/julia-coverage#v1:
          codecov: true
          dirs: './src,./ext,./lib/SubPackage/src'
```

## Environment Variables

```yaml
env:
  # Codecov upload token
  CODECOV_TOKEN: your-token

  # Thread configuration (auto = number of CPUs)
  JULIA_NUM_THREADS: auto,auto

  # Disable Python auto-detection
  PYTHON: ""
  PYCALL_DEBUG_BUILD: yes
```

## Commands Block

Run arbitrary commands:

```yaml
steps:
  - label: "Tests"
    plugins:
      - JuliaCI/julia#v1:
          version: "1"
      - JuliaCI/julia-test#v1: ~
    commands:
      - echo "Julia depot path $${JULIA_DEPOT_PATH}"
      - echo "Environment: PYTHON=$${PYTHON}"
```

## Resource Limits

Set compiled cache size limit:

```yaml
plugins:
  - JuliaCI/julia#v1:
      version: "1"
      compiled_size_limit: 10737418240  # 10GiB
```

## Agent Queues

Route jobs to specific hardware:

```yaml
agents:
  queue: "{{matrix.QUEUE}}"  # default, cuda, rocm, etc.
```

Common queues:
- `default` - Standard x86_64 runners
- `cuda` - NVIDIA GPU runners
- `rocm` - AMD GPU runners
- `arm64` - ARM runners

## Complete Example

```yaml
env:
  CODECOV_TOKEN: your-codecov-token
  JULIA_NUM_THREADS: auto,auto
  PYTHON: ""
  PYCALL_DEBUG_BUILD: yes

steps:
  - label: "MyPackage Tests - {{matrix.LABEL}}"
    plugins:
      - JuliaCI/julia#v1:
          version: "1"
          compiled_size_limit: 10737418240
      - JuliaCI/julia-test#v1: ~
      - JuliaCI/julia-coverage#v1:
          codecov: true
          dirs: './src,./ext'
    commands:
      - echo "Julia depot path $${JULIA_DEPOT_PATH}"
    env:
      JET_TEST: "{{matrix.JET_TEST}}"
      GPU_TEST: "{{matrix.GPU_TEST}}"
    agents:
      queue: "{{matrix.QUEUE}}"
    matrix:
      setup:
        LABEL: ["base tests"]
        QUEUE: ["default"]
        JET_TEST: ["false"]
        GPU_TEST: ["false"]
      adjustments:
        - with:
            LABEL: "JET"
            QUEUE: default
            JET_TEST: true
            GPU_TEST: false
        - with:
            LABEL: "GPU - CUDA"
            QUEUE: cuda
            JET_TEST: false
            GPU_TEST: "cuda"
        - with:
            LABEL: "GPU - ROCm"
            QUEUE: rocm
            JET_TEST: false
            GPU_TEST: "rocm"

  - label: "Downstream - {{matrix.PACKAGE}}"
    plugins:
      - JuliaCI/julia#v1:
          version: "1"
    command:
      - julia --project=$(mktemp -d) -e '
        using Pkg;
        pkg"dev .";
        Pkg.add("{{matrix.PACKAGE}}");
        Pkg.test("{{matrix.PACKAGE}}");'
    matrix:
      setup:
        PACKAGE: ["DownstreamPkg1", "DownstreamPkg2"]
```

## Available Plugins

| Plugin | Purpose |
|--------|---------|
| `JuliaCI/julia#v1` | Install Julia |
| `JuliaCI/julia-test#v1` | Run package tests |
| `JuliaCI/julia-coverage#v1` | Generate/upload coverage |
| `QuantumSavory/julia-xvfb#v1` | Virtual framebuffer for graphics |

## Related Skills

- `julia-ci-github` - GitHub Actions CI configuration
- `julia-tests` - Test setup and patterns
- `julia-benchmarks` - Benchmark configuration
