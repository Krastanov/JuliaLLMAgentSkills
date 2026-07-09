---
name: develop-julia-packages
description: Develop and maintain Julia packages, including Project.toml and package layout changes, dependencies and compatibility, extensions, ParallelTestRunner-first tests, existing TestItemRunner suites, Documenter docs and doctests, JET/Aqua/coverage checks, Scratch runtime data, debugging, CI, and contribution workflows. Use for Julia package repositories and files such as Project.toml, Manifest.toml, src/*.jl, ext/*.jl, test/runtests.jl, docs/make.jl, and Julia GitHub Actions.
---

# Develop Julia Packages

Make the smallest coherent package change, preserve the repository's supported Julia versions and established conventions, and validate through the package environment.

## Start With Repository Evidence

1. Read `Project.toml`, the package entry module, tests, docs setup, CI, and contribution instructions.
2. Check `[compat]` before choosing Julia, Pkg, stdlib, or package APIs.
3. Inspect the current test runner and environment layout before changing either.
4. Check `git status` and preserve unrelated work.
5. Reproduce a failure with the same project and entry point used by CI.

Do not infer policy from a generated `Manifest.toml` alone. Treat a committed manifest, test project, docs project, and CI matrix as deliberate until repository evidence says otherwise.

## Implement Conservatively

- Keep library code in the package module under `src/`. Keep optional integrations in `ext/`.
- Declare dependencies and compat bounds; never install packages from package source or test code.
- Preserve the manifest policy. Do not delete or hand-edit a manifest to solve an ordinary resolution problem.
- Keep Pkg's conservative registry flavor unless a diagnosed publication-latency problem justifies `eager`.
- Gate workspaces and app entry points on the package's minimum Julia version.
- Prefer clear public seams and small fakes over method patching or a mocking framework.
- Keep runtime-generated or mutable data out of the package source tree.

Read [environments and package layout](references/environments-and-layout.md) before changing dependencies, projects, manifests, workspaces, apps, or directory structure.

## Test Through the Package

Use `Test` assertions and make `ParallelTestRunner.jl` the default runner for a new file-split package suite. Preserve an established runner unless migration is requested or necessary. Preserve `TestItemRunner.jl` only when the repository already uses `@testitem`; do not introduce it into a conventional file suite just to standardize runners. A tiny or intentionally ordered suite may remain sequential.

Run focused tests first, then the package's full entry point. Never call `Pkg.add`, `Pkg.develop`, `Pkg.instantiate`, or registry operations from `test/runtests.jl` or discovered test files.

Read [testing](references/testing.md) for runner selection, isolated files, deterministic fixtures, and simple test doubles.

## Route to the Needed Reference

- [Environments and package layout](references/environments-and-layout.md): `Project.toml`, manifests, dependencies, workspaces, apps, and standard layout.
- [Extensions](references/extensions.md): weak dependencies, extension modules, load behavior, and extension tests.
- [Testing](references/testing.md): ParallelTestRunner-first setup, `Test`, existing `@testitem` suites, RNGs, fixtures, and test doubles.
- [Documentation](references/documentation.md): docstrings, Documenter, doctests, and local docs builds.
- [Quality checks](references/quality.md): Aqua, JET, coverage, and a proportional validation sequence.
- [Scratch and runtime data](references/scratch-runtime-data.md): mutable caches, downloads, artifacts, and test isolation.
- [Debugging](references/debugging.md): environment, loading, dispatch, exceptions, precompilation, and nondeterminism.
- [CI and contributions](references/ci-and-contributions.md): Julia Actions, version matrices, security boundaries, and handoff discipline.

Load only the references needed for the current change.

## Validate and Report

Choose checks in proportion to the change:

1. Run the narrowest affected test or PTR file filter.
2. Run `Pkg.test()` through the package environment.
3. Run docs, Aqua, JET, or coverage only when affected or required by the repository.
4. Test the minimum supported Julia version when using a version-sensitive feature.
5. Review the diff for accidental manifest, generated-file, source-tree data, or CI changes.

Report changed behavior, commands run, versions used, and any checks not run. Do not claim compatibility with Julia versions you did not preserve structurally or validate.
