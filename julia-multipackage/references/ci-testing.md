# CI Downstream Testing

## Buildkite Downstream Testing

```yaml
# .buildkite/pipeline.yml
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
        PACKAGE: ["QuantumSavory", "BPGates", "QuantumSymbolics"]
```

## Environment Script Example

```bash
#!/bin/bash
# setup-quantum-dev.sh

mkdir -p workspace && cd workspace

# Clone all packages
git clone https://github.com/QuantumSavory/QuantumInterface.jl.git
git clone https://github.com/QuantumSavory/QuantumClifford.jl.git
git clone https://github.com/QuantumSavory/QuantumSavory.jl.git

# Set up development environment
julia -e '
    using Pkg
    Pkg.activate("quantum-dev")
    Pkg.develop(path="./QuantumInterface.jl")
    Pkg.develop(path="./QuantumClifford.jl")
    Pkg.develop(path="./QuantumSavory.jl")
    Pkg.instantiate()
    println("Environment ready! Activate with: julia --project=quantum-dev")
'
```

## Common Patterns

### Check Which Version is Active

```julia
using Pkg
Pkg.status()  # Shows all packages and whether they're dev'd
```

### Free a Package from Dev Mode

```julia
Pkg.free("PackageName")  # Returns to registered version
```

### Update to Latest Registered Version

```julia
Pkg.free("PackageName")
Pkg.update("PackageName")
```
