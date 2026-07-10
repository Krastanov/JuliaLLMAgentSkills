# Commands and Processes

## Build commands without a shell

Backticks construct a `Cmd`; they do not execute it. Interpolate values as arguments:

```julia
input = "path with spaces.txt"
cmd = `tool --input $input`
run(cmd)
output = read(cmd, String)
```

Julia launches the program directly, so shell quoting, globbing, variables, redirection, and pipes are not implicit. Interpolating a string produces one argument; interpolating a collection expands it into arguments.

Invoke a shell explicitly only when shell syntax is genuinely required. Do not concatenate untrusted text into `sh -c`, `cmd /C`, or another shell program.

## Compose pipelines and environments

```julia
cmd = pipeline(`producer`, `consumer --mode stable`)
text = read(cmd, String)

configured = addenv(
    Cmd(`tool --input $input`; dir=workdir),
    "MODE" => "safe",
)
run(configured)
```

Use `pipeline` keywords or arguments for `stdin`, `stdout`, and `stderr`. Use `setenv` to replace the environment and `addenv` to overlay variables.

By default, `run` waits and throws `ProcessFailedException` for an unsuccessful command. Use `run(cmd; wait=false)` only when the caller retains the returned process, later waits for it, and checks success. Use `ignorestatus` only when nonzero exit codes are part of the program's documented protocol.

## Prevent pipe deadlocks

Consume output while the child can still write it. Prefer `read(process_or_cmd, String)` to waiting first when collecting all output. For bidirectional protocols, put reading and writing in separate owned tasks and wait for both.

Do not let both sides wait while kernel pipe buffers fill. Bound input and output when a child can produce unlimited data, and decide whether logs are streamed, captured, or redirected.

## Preserve process boundaries

- Pass argument vectors rather than recreating shell parsing.
- Set `dir` on `Cmd` instead of changing the parent process's working directory.
- Pass secrets through the narrowest supported channel and avoid printing the constructed environment.
- Handle platform-specific executable names explicitly; shell built-ins require a platform shell.
- Propagate interrupts and clean up children that the caller started.
- Test spaces, Unicode, empty arguments, nonzero exits, large output, and a missing executable.

## Sources

- [Julia manual: running external programs](https://docs.julialang.org/en/v1/manual/running-external-programs/)
- [Julia `Cmd` and process reference](https://docs.julialang.org/en/v1/base/base/#Base.Cmd)
