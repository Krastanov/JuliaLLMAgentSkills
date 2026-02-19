# Cmd and Pipeline Patterns

## Backticks and Execution

- Backticks create `Cmd` objects; they do not execute.
- Execute with `run(cmd)`.
- Capture output with `read(cmd, String)` or `readchomp(cmd)`.
- Default command output goes to Julia `stdout`.

## Interpolation Rules

- `$x` injects one argument safely.
- `$xs` where `xs` is iterable expands to multiple arguments.
- In composite words, iterable interpolation expands like shell brace/cartesian patterns.
- Julia displays quotes for readability; values are not interpreted by an intermediate shell.

## Quoting and Metacharacters

- Literal shell metacharacters (`|`, `&`, `>`) inside command literals must be quoted/escaped.
- For real piping/parallel composition, use Julia APIs (`pipeline`, `&`) outside command literals.

## Pipeline Construction

```julia
run(pipeline(`echo hello`, `sort`))
run(pipeline(`echo world` & `echo hello`, `sort`))
```

Redirection:

```julia
pipeline(`do_work`, stdout=pipeline(`sort`, "out.txt"), stderr="errs.txt")
```

## Avoid Deadlocks

- Avoid `wait(process)` as the only consumer if process output is large.
- Prefer active reads (`read(out, String)`).
- Separate write/read work into tasks when both ends are used:

```julia
writer = Threads.@spawn write(process, "data")
reader = Threads.@spawn read(process, String)
wait(writer)
fetch(reader)
```

## Working with Cmd Objects

Use `Cmd` keyword arguments to control execution context:

```julia
run(Cmd(`pwd`, dir="/"))
run(Cmd(`sh -c "echo \$HOWLONG"`, env=("HOWLONG" => "ever!",)))
run(Cmd(Cmd(["pwd"]), detach=true, ignorestatus=true))
```

Environment helpers:

```julia
run(setenv(`sh -c "echo \$HOWLONG"`, ("HOWLONG" => "ever!",)))
run(addenv(`sh -c "echo \$HOWLONG"`, "HOWLONG" => "ever!"))
```

## Portability Note

The manual examples assume POSIX shells/tools. On Windows, commands like `echo` may be shell built-ins rather than standalone executables; use `cmd /C ...` where needed.
