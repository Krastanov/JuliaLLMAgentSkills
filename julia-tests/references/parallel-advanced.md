# Advanced ParallelTestRunner Configuration

## Custom Test Suite

Instead of auto-discovery, define tests manually:

```julia
testsuite = find_tests(pwd())

# Conditional filtering
args = parse_args(ARGS)
if filter_tests!(testsuite, args)
    if !Sys.iswindows()
        delete!(testsuite, "windows_only")
    end
    if get(ENV, "JET_TEST", "") != "true"
        delete!(testsuite, "jet")
    end
end

runtests(MyPackage, args; testsuite)
```

`filter_tests!` returns `true` if no positional args were given (allowing
programmatic filtering), `false` if the user specified tests on the CLI.

## init_code (Per-Test Setup)

Evaluated in each test file's isolated module sandbox:

```julia
const init_code = quote
    function test_helper(x)
        return x * 2
    end
end

runtests(MyPackage, ARGS; init_code)
```

## init_worker_code (Per-Worker Setup)

For expensive initialization (e.g., GPU setup ~3s), run once per worker:

```julia
const init_worker_code = quote
    function complex_common_test_helper(x)
        return x * 2
    end
end

const init_code = quote
    import ..complex_common_test_helper
end

runtests(MyPackage, ARGS; init_worker_code, init_code)
```

**Key**: `init_worker_code` runs once per worker. Tests must `import ..name`
via `init_code` to access definitions (module isolation).

## Custom Workers

Assign specific tests to workers with custom settings:

```julia
function test_worker(name)
    if name == "needs_env_var"
        return addworker(; env=["SPECIAL_ENV_VAR" => "42"])
    elseif name == "needs_threads"
        return addworker(; exeflags=["--threads=4"])
    end
    return nothing  # default worker pool
end

runtests(MyPackage, ARGS; test_worker)
```

## Custom CLI Flags

```julia
args = parse_args(ARGS; custom=["myflag", "another-flag"])

if args.custom["myflag"] !== nothing
    println("Custom flag was set!")
end

runtests(MyPackage, args)
```

Values are `nothing` (unset) or `Some(value)` (set).

## Performance Tips

1. Balance test file execution times across files
2. Use `init_worker_code` for shared expensive setup, not `init_code`
3. Minimize custom workers — only when genuinely needed
