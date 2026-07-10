# Debugging Julia Packages

Diagnose the failing environment and entry point before changing code.

## Reproduce the Real Invocation

Record:

- `VERSION` and `Base.active_project()`;
- `Pkg.status()` and relevant `Pkg.why(...)` output;
- command, working directory, arguments, environment variables, and thread count;
- whether the failure occurs in a fresh Julia process with `--startup-file=no`;
- the narrowest test file or public call that reproduces it.

Use `Pkg.instantiate()` for the intended project. Do not delete the manifest, switch to a global environment, or run `Pkg.add` in a test to make the symptom disappear.

For a PTR suite, list or filter tests through runner arguments and reproduce with `--jobs=1` only to distinguish resource/order coupling from functional failure.

## Read the Exception and Load State

Capture the original backtrace:

```julia
try
    failing_call()
catch err
    showerror(stderr, err, catch_backtrace())
    println(stderr)
    rethrow()
end
```

Use `@error ... exception=(err, catch_backtrace())` when the failure belongs in structured logs. Do not discard the original exception behind a generic message.

For loading or extension failures, inspect:

- active `LOAD_PATH` and `DEPOT_PATH`;
- dependency/weak-dependency names and UUIDs;
- extension key and file-name agreement;
- whether all trigger packages were loaded;
- a fresh process, because loaded modules cannot be unloaded reliably.

## Inspect Dispatch and Inference

Load `InteractiveUtils` and start with the concrete call:

- `@which f(args...)` identifies the selected method;
- `methods(f)` shows candidate definitions;
- `@code_warntype f(args...)` exposes inference issues;
- `@code_typed` or `code_typed` gives deeper compiler output when needed;
- `@less f(args...)` opens source when source locations are available.

Do not "fix" a dispatch issue by narrowing every public argument to concrete container types. First identify the ambiguous, missing, or unintended method.

Use `@show`, `@info`, and `@debug` for small probes. Julia logging macros avoid evaluating disabled messages; keep expensive diagnostics inside logging expressions rather than constructing them unconditionally.

## Separate Common Failure Classes

- **Environment/resolution:** inspect projects, compat, and manifests.
- **World age/redefinition:** reproduce in a fresh process; use Revise only for the interactive edit loop.
- **Precompilation:** remove runtime side effects at module top level and keep `__init__` bounded.
- **Extension loading:** verify declaration, trigger imports, and supported Julia version.
- **Filesystem/runtime data:** use writable temporary or scratch paths, not package source.
- **Nondeterminism:** use an explicit RNG, unique resources, bounded synchronization, and repeated focused runs.
- **Concurrency:** reproduce at one worker/thread, then restore parallelism and fix the shared-state or lifecycle defect.

Optional interactive debuggers are useful after a minimal reproduction exists. Do not add them as package runtime dependencies.

## Sources

- [Julia stack traces](https://docs.julialang.org/en/v1/manual/stacktraces/)
- [Julia control flow and exception handling](https://docs.julialang.org/en/v1/manual/control-flow/#Exception-Handling)
- [Julia logging](https://docs.julialang.org/en/v1/stdlib/Logging/)
- [InteractiveUtils](https://docs.julialang.org/en/v1/stdlib/InteractiveUtils/)
- [Pkg API](https://pkgdocs.julialang.org/v1/api/)
- [Julia code loading and extensions](https://docs.julialang.org/en/v1/manual/code-loading/)
