# Julia Development Skills for Claude Code

A collection of Claude Code skills for Julia package development, following modern best practices and conventions.

## Skills Overview

### Package Development

| Skill | Description |
|-------|-------------|
| [julia-package-init](julia-package-init/) | Create new Julia packages with modern infrastructure |
| [julia-package-dev](julia-package-dev/) | Work with packages in development mode |
| [julia-multipackage](julia-multipackage/) | Develop multiple inter-related packages together |
| [julia-pkgextension](julia-pkgextension/) | Build package extensions (weak dependencies) |

### Documentation

| Skill | Description |
|-------|-------------|
| [julia-docs](julia-docs/) | Build documentation with Documenter.jl |
| [julia-docstrings](julia-docstrings/) | Write docstrings using DocStringExtensions.jl |
| [julia-doctests](julia-doctests/) | Configure and write doctests |
| [julia-doccitations](julia-doccitations/) | Add citations with DocumenterCitations.jl |

### Testing & Quality

| Skill | Description |
|-------|-------------|
| [julia-tests-run](julia-tests-run/) | Run tests with the standard library Test and conditional loading |
| [julia-tests-write](julia-tests-write/) | Write tests with the standard library Test |
| [julia-retestitems-run](julia-retestitems-run/) | Run `@testitem` suites with ReTestItems.jl (parallel + filtering) |
| [julia-testitem-run](julia-testitem-run/) | Legacy TestItemRunner.jl `@testitem` runner |
| [julia-testitem-write](julia-testitem-write/) | Write `@testitem` tests for reliable filtering |

### Static Analysis

| Skill | Description |
|-------|-------------|
| [julia-jet](julia-jet/) | JET.jl overview, setup, and configuration |
| [julia-jet-errors](julia-jet-errors/) | Error analysis with `@report_call` and `report_package` |
| [julia-jet-opt](julia-jet-opt/) | Optimization analysis with `@report_opt` |

### Benchmarking

| Skill | Description |
|-------|-------------|
| [julia-bench-quick](julia-bench-quick/) | Quick impromptu benchmarks with @btime/@b |
| [julia-bench-write](julia-bench-write/) | Write benchmark suites with BenchmarkTools.jl |
| [julia-bench-run](julia-bench-run/) | Run benchmark suites and CI performance tracking |

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
| [julia-pkg-app](julia-pkg-app/) | Build standalone apps with Pkg's native app support |

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

### Utilities

| Skill | Description |
|-------|-------------|
| [whitespace](whitespace/) | Fix trailing whitespace and newlines |

## Usage

These skills are automatically available to Claude Code when working in projects that include this `.claude/skills/` directory. Claude will use the appropriate skill based on the task context.

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
julia-package-init
├── julia-docs
├── julia-tests-run
└── julia-tests-write

julia-pkgextension
├── julia-docs (for documenting extensions)
├── julia-tests-run (for running extension tests)
├── julia-tests-write (for writing extension tests)
└── julia-makie-recipes (example use case)

julia-tests-run
└── julia-retestitems-run (optional, if the repo uses `@testitem`)

julia-tests-write
└── julia-testitem-write (optional, if the repo uses `@testitem`)

julia-retestitems-run
└── julia-testitem-write (for filter-friendly test design)

julia-testitem-run
└── julia-testitem-write (legacy runner)

julia-docs
├── julia-docstrings
├── julia-doctests
└── julia-doccitations

julia-bench-write
├── julia-bench-quick (for patterns)
└── julia-bench-run (for execution)

julia-comonicon
├── julia-package-dev (for package workflows)
├── julia-package-init (for project bootstrapping)
└── julia-pkg-app (lightweight alternative without arg parsing)

julia-pkg-app
├── julia-comonicon (full-featured CLI alternative)
├── julia-package-init (for project bootstrapping)
├── julia-package-dev (for development workflow)
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
├── julia-jet-errors (error analysis details)
├── julia-jet-opt (optimization analysis details)
├── julia-perf (performance optimization)
└── julia-tests-write (JET test templates)

julia-jet-errors
├── julia-jet (overview)
├── julia-jet-opt (optimization analysis)
└── julia-perf (type stability fixes)

julia-jet-opt
├── julia-jet (overview)
├── julia-jet-errors (error analysis)
├── julia-perf (performance workflow)
└── julia-bench-quick (verify dispatch fixes)

julia-scratch
├── julia-package-dev (for package development workflows)
├── julia-package-init (for adding Scratch.jl as a dependency)
└── julia-toml (for version-specific scratch key patterns)
```

## Contributing

When adding or modifying skills:

1. Include YAML frontmatter with `name` and `description`
2. Add a "Related Skills" section linking to relevant skills
3. Include practical examples and code snippets
4. Keep content focused and actionable
5. Update this README when adding new skills
