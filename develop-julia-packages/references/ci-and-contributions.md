# Julia CI and Contribution Workflow

Follow repository instructions first. Keep CI edits scoped to the requested package change and preserve required checks, release automation, and platform support.

## Prepare a Contribution

1. Read `CONTRIBUTING.md`, issue/PR templates, `Project.toml` compat, and all Julia workflows.
2. Reproduce the issue under a supported Julia version and the repository's package environment.
3. Change source, tests, docs, and compat together when the public behavior requires it.
4. Run focused tests, then the full package test entry point.
5. Run docs and configured quality jobs when affected.
6. Review the diff for unrelated formatting, manifest churn, generated docs, coverage files, or runtime data.

Do not tag releases, edit registries, publish docs, push branches, or alter repository secrets unless explicitly requested. Preserve project-specific changelog and release-note policy.

## Build a Minimal Julia Test Job

Use current official Julia Actions and quote version values:

```yaml
name: CI

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        julia-version: ['min', '1']
        os: [ubuntu-latest]
    runs-on: ${{ matrix.os }}
    env:
      JULIA_NUM_THREADS: auto
      JULIA_PKG_SERVER_REGISTRY_PREFERENCE: conservative
    steps:
      - uses: actions/checkout@v6
      - uses: julia-actions/setup-julia@v3
        with:
          version: ${{ matrix.julia-version }}
      - uses: julia-actions/cache@v3
        with:
          delete-old-caches: false
      - uses: julia-actions/julia-runtest@v1
```

Adapt the matrix to `[compat]` and repository policy. `'min'` selects the minimum compatible Julia minor using the project; use an explicit version when exact patch behavior matters. Add Windows/macOS only when the package claims or needs that coverage. Put prerelease/nightly jobs in `continue-on-error` only if repository policy treats them as advisory.

`julia-runtest` invokes the package test interface and enables coverage. It currently sets the eager registry flavor unless already configured, so the example explicitly retains conservative behavior. The read-only example also disables cache deletion; a trusted workflow may grant `actions: write` instead when old-cache cleanup is desired. A direct `Pkg.test()` command is also valid and may be clearer when custom arguments are needed.

For ParallelTestRunner, pass filters or `--jobs` through the action's `test_args` input or `Pkg.test(test_args=...)`. Do not conditionally install test dependencies inside `runtests.jl`.

## Split Jobs by Compatibility

- Run behavioral tests on the supported Julia matrix.
- Run JET on a Julia version supported by the pinned JET release.
- Run docs on the version selected by the repository, normally a current stable Julia.
- Run Aqua in the test matrix or one quality job according to runtime and compatibility.
- Process coverage once, not in every matrix leg, unless merging is intentional.

Use `julia-actions/julia-processcoverage@v1` to create `lcov.info` when the repository uploads coverage. Preserve the existing upload provider and credentials model.

## Keep Pull Requests Unprivileged

Use `pull_request` for workflows that check out and execute contributor code. Avoid `pull_request_target` for such jobs because it runs with base-repository privileges and can expose write tokens or secrets. If a trusted metadata-only workflow needs elevated permissions, keep it separate and never execute untrusted checkout content.

Pin third-party actions according to the repository's security policy. Workflows with secrets should use reviewed commit SHAs, and dependency automation should keep those pins current.

## Handle Compatibility Deliberately

- Add a Julia compat bump when new syntax or APIs require it.
- Gate Julia 1.12 workspaces and app features; do not leave an older compat claim.
- Keep extensions behind Julia 1.9+ or preserve the existing older-version mechanism.
- Test the minimum supported version before claiming it remains supported.
- Do not use a nightly-only tool failure as evidence that package code is broken.

Report the exact jobs or local equivalents run and call out checks that require hosted credentials or unavailable platforms.

## Sources

- [setup-julia v3 and version selectors](https://github.com/julia-actions/setup-julia)
- [julia-actions/cache v3](https://github.com/julia-actions/cache)
- [julia-runtest and test arguments](https://github.com/julia-actions/julia-runtest)
- [julia-processcoverage](https://github.com/julia-actions/julia-processcoverage)
- [Pkg compatibility](https://pkgdocs.julialang.org/v1/compatibility/)
- [GitHub guidance for `pull_request_target`](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request_target)
- [GitHub Actions security hardening](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
