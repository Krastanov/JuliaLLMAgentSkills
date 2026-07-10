# Julia Agent Skills

Five task-oriented skills for Julia work. Each `SKILL.md` is a small router;
details and examples live in references that are loaded only for the current
task.

| Skill | Scope |
| --- | --- |
| [`develop-julia-packages`](develop-julia-packages/) | Environments, package structure, extensions, tests, documentation, quality checks, runtime data, and Julia CI |
| [`optimize-julia-code`](optimize-julia-code/) | Benchmarking, profiling, inference, allocations, data layout, and evidence-driven optimization |
| [`orchestrate-julia-workloads`](orchestrate-julia-workloads/) | Tasks, channels, threads, synchronization, native-library thread control, and subprocesses |
| [`handle-julia-data`](handle-julia-data/) | DataFrames/Tables workflows, delimited data, TOML/YAML configuration, and table reports |
| [`build-julia-interfaces`](build-julia-interfaces/) | Scripts, Pkg apps, Comonicon CLIs, Term output/TUIs, and Makie recipes |

## Design

- Trigger on a user task, not on a single package name.
- Keep the core workflow in `SKILL.md`; open only the directly linked reference
  needed for the task.
- Prefer Julia's standard library and an existing project's conventions before
  adding dependencies or migrating frameworks.
- Treat version-sensitive package APIs as such and follow the authoritative
  sources linked from each reference.
- Preserve existing test runners. For a new file-oriented parallel suite,
  prefer `ParallelTestRunner.jl`; use `TestItemRunner.jl` mainly when the project
  already uses `@testitem`.
- Keep tests straightforward. Favor pure functions, explicit inputs, temporary
  directories, and small fixtures over elaborate mocking.

Each skill also includes `agents/openai.yaml` metadata for skill pickers and
explicit invocation.
