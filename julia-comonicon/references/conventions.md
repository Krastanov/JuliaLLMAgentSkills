# Comonicon Conventions Reference

## Function-to-CLI Mapping

- Treat function positional arguments as CLI arguments.
- Treat function keyword arguments as CLI options/flags.
- Require default values for keyword arguments.
- Treat `Bool=false` keyword arguments as flags.
- Convert values automatically when argument/keyword types are annotated.

## Option and Flag Naming

- Convert underscore `_` in Julia kwarg names to dash `-` in CLI names.
- Write docs using dashed names to match generated CLI options.
- Support short forms through docstrings (for example `-o, --output <path>`).

## Always-Available Flags

- `-h` and `--help` are generated automatically.
- `--version` is generated automatically.
- Version is read from package `Project.toml`, else defaults to `0.0.0`.

## Docstring Sections

Use these sections for CLI help pages:

- `# Arguments` (or `# Args`)
- `# Options`
- `# Flags`
- `# Intro` (or `# Introduction`) for long description text

Comonicon uses first paragraph as brief description.

### Arguments Format

```md
# Arguments
- `input`: input path.
```

### Options Format

```md
# Options
- `-o, --output <path>`: output file path.
- `--threads=<n>`: number of threads.
```

### Flags Format

```md
# Flags
- `-f, --force`: overwrite output.
```

## Command Structure Terms

- Leaf command: terminal command that accepts arguments/options/flags.
- Node command: command containing subcommands.

Example:

```text
git remote show origin
```

`remote` is a node command; `show` is a leaf command.

## Useful Runtime Patterns

### Dash Separator

Use `--` to separate arguments for nested scripts:

```bash
run --flag -- script.jl a b c
```

### Configurations.jl Option Types

When option types are defined with `@option`, Comonicon supports both field overrides and file loading:

```bash
command --config.c=1 --config.option.a=1 --config.option.b=1
command --config=config.toml
command -c config.toml --config.option.b=2
```

### Plugin Commands

Enable plugin discovery in `Comonicon.toml`:

```toml
[command]
plugin = true
```

This enables `<main-command>-<plugin>` executables to be called as subcommands.
