---
name: julia-github
description: Use Git and the GitHub CLI for version control and pull request workflows in Julia package development. Use this skill when working with Git remotes, branches, and PRs.
---

# Julia GitHub Workflow

Use Git and the GitHub CLI (`gh`) for version control and pull request workflows
in Julia package development.

## Start Clean

- Keep `upstream` as source of truth and `origin` as your fork.
- Start from the current upstream default branch (`master` or `main`), not an
  old feature branch.
- Pull upstream first, then create a new branch from that tip.

```bash
git checkout master  # or main
git pull upstream master  # or main
git checkout -b descriptive-branch-name
```

## Basic Flow

```bash
git add file1.jl file2.jl
git commit -m "Add feature X that does Y"
git push -u origin descriptive-branch-name
```

## Creating Pull Requests

```bash
gh pr create \
    --title "Your PR Title" \
    --body "Description of changes" \
    --repo OriginalOrg/PackageName.jl
```

## Reference

- **[Best Practices](references/best-practices.md)** - Commit messages, branch naming, atomic commits
- **[Common Operations](references/common-ops.md)** - Undo, sync, stash

## Related Skills

- `julia-package-dev` - Package development basics, including multi-package workflows
