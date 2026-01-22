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
| [julia-tests-run](julia-tests-run/) | Run tests with filtering and conditional loading |
| [julia-tests-write](julia-tests-write/) | Write tests with TestItemRunner.jl patterns |
| [julia-benchmarks](julia-benchmarks/) | Performance benchmarking with BenchmarkTools.jl |

### Continuous Integration

| Skill | Description |
|-------|-------------|
| [julia-ci-github](julia-ci-github/) | Configure GitHub Actions CI |
| [julia-ci-buildkite](julia-ci-buildkite/) | Configure Buildkite CI (GPU testing) |

### Version Control

| Skill | Description |
|-------|-------------|
| [julia-github](julia-github/) | Git and GitHub CLI workflows |

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
├── julia-tests-write
├── julia-ci-github
└── julia-ci-buildkite

julia-pkgextension
├── julia-docs (for documenting extensions)
├── julia-tests-run (for running extension tests)
├── julia-tests-write (for writing extension tests)
└── julia-makie-recipes (example use case)

julia-docs
├── julia-docstrings
├── julia-doctests
└── julia-doccitations
```

## Contributing

When adding or modifying skills:

1. Include YAML frontmatter with `name` and `description`
2. Add a "Related Skills" section linking to relevant skills
3. Include practical examples and code snippets
4. Keep content focused and actionable
5. Update this README when adding new skills
