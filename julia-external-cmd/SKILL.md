---
name: julia-external-cmd
description: Run and orchestrate external programs from Julia using Cmd objects, backtick command literals, interpolation, quoting, pipelines, and IO redirection. Use this skill when replacing shell scripts with Julia, building subprocess pipelines, setting command environments, or troubleshooting subprocess deadlocks and quoting issues.
---

# Julia External Cmd

Use Julia backtick command literals and `Cmd` APIs to run subprocesses without shell ambiguity.

## Core Command Model

Backticks produce `Cmd`, they do not execute immediately:

```julia
cmd = `echo hello`
run(cmd)
text = readchomp(cmd)
```

Remember: Julia executes commands directly (no implicit shell), so quoting/interpolation follows Julia command rules, not shell expansion.

## Interpolation and Quoting

- Use `$value` to pass one argument safely, including paths with spaces.
- Interpolate arrays/iterables to expand into multiple arguments.
- Inside one shell word, array interpolation performs shell-like brace/cartesian expansion.
- Quote shell metacharacters inside backticks when meant literally.

## Build Pipelines Explicitly

Use `pipeline` instead of shell metacharacters in command literals:

```julia
run(pipeline(`cut -d: -f3 /etc/passwd`, `sort -n`, `tail -n5`))
```

Use `&` to run producers in parallel and merge output into downstream stages.

## Avoid Pipeline Deadlocks

When both writing and reading, actively consume output:
- Prefer `read(out, String)` over waiting on process completion alone.
- Split reader/writer into separate tasks when needed.

## Configure Command Environment

Use `Cmd(...)` keywords and env helpers:
- `Cmd(cmd; dir=..., env=..., detach=..., ignorestatus=...)`
- `setenv(cmd, pairs...)`
- `addenv(cmd, pairs...)`

Use `open(cmd, mode, ...)` for stream-style interaction.

## Platform Note

Many shell built-ins on Windows are not external executables; invoke `cmd /C ...` when necessary.

## Reference

- `references/cmd-pipeline-patterns.md` - command composition and subprocess IO patterns

## Related Skills

- `julia-async` - task-based orchestration around process IO
- `julia-comonicon` - Julia CLI development once command patterns are stable
