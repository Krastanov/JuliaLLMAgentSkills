# Julia Development Skills for Claude Code

A collection of Claude Code skills for Julia package development, following modern best practices and conventions.

## Skills Overview

### Package Development

| Skill | Description |
|-------|-------------|
| [julia-package-dev](julia-package-dev/) | Develop Julia packages, multi-package workspaces, extensions, and Pkg apps |

### Documentation

| Skill | Description |
|-------|-------------|
| [julia-docs](julia-docs/) | Build documentation with Documenter.jl, docstrings, doctests, and citations |

### Testing & Quality

| Skill | Description |
|-------|-------------|
| [julia-tests](julia-tests/) | Run and write tests with Test.jl, TestItemRunner.jl, and ParallelTestRunner.jl |

### Static Analysis

| Skill | Description |
|-------|-------------|
| [julia-jet](julia-jet/) | JET.jl overview, error analysis, optimization analysis, and configuration |

### Performance

| Skill | Description |
|-------|-------------|
| [julia-perf](julia-perf/) | Optimize Julia code for performance |
| [julia-bench](julia-bench/) | Quick benchmarks, benchmark suites, result comparison, and benchmark CI |

### Concurrency

| Skill | Description |
|-------|-------------|
| [julia-async](julia-async/) | Asynchronous programming with Julia tasks/channels |
| [julia-threads](julia-threads/) | Multithreading patterns and thread safety in Julia |

### Data Serialization

| Skill | Description |
|-------|-------------|
| [julia-toml](julia-toml/) | Parse and write TOML files with Julia TOML stdlib |
| [julia-yaml](julia-yaml/) | Parse and write YAML files with YAML.jl |

### Tabular Data

| Skill | Description |
|-------|-------------|
| [julia-csv](julia-csv/) | Parse and write CSV files with CSV.jl |
| [julia-prettytables](julia-prettytables/) | Render text/markdown/HTML tables with PrettyTables.jl |

### Version Control

| Skill | Description |
|-------|-------------|
| [julia-github](julia-github/) | Git and GitHub CLI workflows |
| [github-act](github-act/) | Run and debug GitHub Actions locally with `gh act` |

### CLI Development

| Skill | Description |
|-------|-------------|
| [julia-comonicon](julia-comonicon/) | Build Julia CLI interfaces with Comonicon.jl |

### Data Storage

| Skill | Description |
|-------|-------------|
| [julia-scratch](julia-scratch/) | Manage mutable scratch spaces with Scratch.jl |

### System Integration

| Skill | Description |
|-------|-------------|
| [julia-external-cmd](julia-external-cmd/) | Run external programs safely from Julia |

### Visualization

| Skill | Description |
|-------|-------------|
| [julia-makie-recipes](julia-makie-recipes/) | Create custom Makie plot recipes |

### Terminal UI

| Skill | Description |
|-------|-------------|
| [julia-term](julia-term/) | Terminal output, layouts, renderables, progress bars, and TUI apps with Term.jl |

### Utilities

| Skill | Description |
|-------|-------------|
| [whitespace](whitespace/) | Fix trailing whitespace and newlines |

## Usage

These skills are automatically available when working in projects that include
this `.agents/skills/` directory. The agent will use the appropriate skill
based on the task context.

### Skill Header Format

Each skill uses YAML frontmatter for metadata:

```yaml
---
name: skill-name
description: Brief description of when to use this skill.
---
```

## Skill Dependencies

Many skills reference each other. Key relationships:

```
julia-package-dev
├── julia-tests (for package test setup and execution)
├── julia-docs (for package docs and doctests)
├── julia-comonicon (full CLI framework)
└── julia-makie-recipes (extension use case)

julia-docs
└── julia-tests (for running doctests in the test suite)

julia-bench
└── julia-perf (performance diagnosis before or after benchmarking)

julia-comonicon
├── julia-package-dev (for package workflows)
└── julia-toml (for Project.toml configuration)

julia-threads
└── julia-async (for task-level coordination)

julia-external-cmd
└── julia-async (for subprocess IO with tasks)

julia-toml
└── julia-package-dev (for Project.toml and config workflows)

julia-yaml
└── julia-package-dev (for YAML config workflows)

julia-prettytables
└── julia-csv (common ingestion source in table workflows)

julia-jet
├── julia-perf (performance optimization)
└── julia-tests (JET test templates)

julia-tests
├── julia-docs (doctest authoring and Documenter setup)
├── julia-perf (performance workflow)
└── julia-jet (static analysis in test suites)

julia-scratch
├── julia-package-dev (for package development workflows)
└── julia-toml (for version-specific scratch key patterns)
```

## Contributing

When adding or modifying skills:

1. Include YAML frontmatter with `name` and `description`
2. Add a "Related Skills" section linking to relevant skills
3. Include practical examples and code snippets
4. Keep content focused and actionable
5. Update this README when adding new skills
