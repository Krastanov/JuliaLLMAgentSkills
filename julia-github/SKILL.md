---
name: julia-github
description: Use Git and the GitHub CLI for version control and pull request workflows in Julia package development. Use this skill when working with Git remotes, branches, and PRs.
---

# Julia GitHub Workflow

Use Git and the GitHub CLI (`gh`) for version control and pull request workflows
in Julia package development.

## Repository Setup

Keep two remotes: `upstream` (source of truth) and `origin` (your fork):

```bash
git clone https://github.com/YOUR_USERNAME/PackageName.jl.git
cd PackageName.jl
git remote add upstream https://github.com/OriginalOrg/PackageName.jl.git
```

## Daily Workflow

### Before Starting Work

```bash
git checkout master
git pull upstream master
```

### Creating a Feature Branch

```bash
git checkout master
git pull upstream master
git checkout -b descriptive-branch-name
```

### Making Changes

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

## GitHub CLI Quick Reference

| Task | Command |
|------|---------|
| Create PR | `gh pr create --title "..." --body "..."` |
| List PRs | `gh pr list` |
| View PR | `gh pr view 123` |
| Checkout PR | `gh pr checkout 123` |
| Merge PR | `gh pr merge 123` |
| List issues | `gh issue list` |
| View issue | `gh issue view 123` |

## Git Quick Reference

| Task | Command |
|------|---------|
| Clone | `git clone URL` |
| Pull | `git pull origin branch` |
| Push | `git push origin branch` |
| Branch | `git checkout -b name` |
| Status | `git status` |
| Diff | `git diff` |
| Log | `git log --oneline` |
| Stash | `git stash` / `git stash pop` |

## Reference

- **[Best Practices](references/best-practices.md)** - Commit messages, branch naming, atomic commits
- **[Common Operations](references/common-ops.md)** - Undo, sync, stash

## Related Skills

- `julia-multipackage` - Multi-package development workflows
- `julia-package-dev` - Package development basics
