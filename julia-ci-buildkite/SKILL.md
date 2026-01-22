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

```yaml
steps:
  - label: "Tests - {{matrix.LABEL}}"
    plugins:
      - JuliaCI/julia#v1:
          version: "1"
      - JuliaCI/julia-test#v1: ~
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

## Agent Queues

Route jobs to specific hardware:

| Queue | Purpose |
|-------|---------|
| `default` | Standard x86_64 runners |
| `cuda` | NVIDIA GPU runners |
| `rocm` | AMD GPU runners |
| `arm64` | ARM runners |

```yaml
agents:
  queue: "{{matrix.QUEUE}}"
```

## Available Plugins

| Plugin | Purpose |
|--------|---------|
| `JuliaCI/julia#v1` | Install Julia |
| `JuliaCI/julia-test#v1` | Run package tests |
| `JuliaCI/julia-coverage#v1` | Generate/upload coverage |
| `QuantumSavory/julia-xvfb#v1` | Virtual framebuffer for graphics |

## Reference

- **[Pipeline Templates](references/pipelines.md)** - Complete pipeline examples for various scenarios

## Related Skills

- `julia-ci-github` - GitHub Actions CI configuration
- `julia-tests-run` - Running tests
