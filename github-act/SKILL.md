---
name: github-act
description: Run and debug GitHub Actions locally with gh act. Use this skill when validating CI workflows, reproducing failures, or iterating on workflow YAML without pushing commits.
---

# Run GitHub Actions Locally with gh act

Use `gh act` to run `.github/workflows` jobs locally before pushing.
This is useful for fast CI iteration in any repository.

## Setup

Install the extension once:

```bash
gh extension install https://github.com/nektos/gh-act
```

Check available options:

```bash
gh act --help
```

`gh act` requires a running container runtime (typically Docker).

## Quick Commands

```bash
# List discovered workflows/jobs
gh act -l

# Run the default event (usually push)
gh act

# Run a specific event
gh act push
gh act pull_request
gh act workflow_dispatch

# Run one job by job id
gh act pull_request -j test

# Restrict to one workflow file
gh act pull_request -W .github/workflows/ci.yml
```

## CI Workflow Loop

```bash
# 1) Validate workflow syntax without creating containers
gh act -n --validate

# 2) Run only the failing job with verbose logs
gh act pull_request -j test -v

# 3) Re-run quickly while preserving container state
gh act pull_request -j test --reuse
```

Use `--matrix` to target one matrix entry while debugging:

```bash
gh act pull_request -j test --matrix os:ubuntu-latest --matrix shard:1
```

## Inputs, Secrets, Vars, and Env

Pass values directly:

```bash
gh act workflow_dispatch \
  --input target=staging \
  --secret GITHUB_TOKEN="$(gh auth token)" \
  --var DEPLOY_REGION=us-east-1 \
  --env CI=true
```

Or load from files (defaults shown):

- `.input` via `--input-file`
- `.secrets` via `--secret-file`
- `.vars` via `--var-file`
- `.env` via `--env-file`

## High-Value Flags

- `-n, --dryrun`: validate workflow/job planning without running containers
- `--validate`: strict workflow validation
- `-v, --verbose`: detailed logs
- `--json`: machine-readable logs
- `-g, --graph`: show workflow graph
- `-w, --watch`: rerun on file changes
- `-C, --directory`: run against another repository path
- `-W, --workflows`: choose workflow file(s) or directories
- `-P, --platform`: override runner image mapping
- `--pull`, `--action-offline-mode`: control image/action refresh behavior

## Troubleshooting

- If `ubuntu-latest` image resolution fails, provide explicit mapping with `-P`.
- If secrets are missing, pass with `--secret` or provide `.secrets`.
- If a workflow depends on GitHub-hosted services, local runs may need mocks or conditional steps.
- Use `gh act -l` first to confirm job ids before `-j <job-id>`.
