# Advanced CI Configurations

## Table of Contents

- [Documentation with Graphics](#documentation-with-graphics)
- [Testing Sublibraries](#testing-sublibraries)
- [Coverage for Extensions](#coverage-for-extensions)

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
