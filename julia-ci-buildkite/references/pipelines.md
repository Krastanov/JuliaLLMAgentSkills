# Pipeline Templates

## Table of Contents

- [GPU Testing Matrix](#gpu-testing-matrix)
- [Test Categories](#test-categories)
- [Graphics/Display Tests](#graphicsdisplay-tests)
- [Downstream Testing](#downstream-testing)
- [Testing Subpackages](#testing-subpackages)
- [Complete Example](#complete-example)

## GPU Testing Matrix

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
