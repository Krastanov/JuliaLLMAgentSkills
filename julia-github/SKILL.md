---
name: julia-github
description: "Create branches, push commits, open and review pull requests, manage remotes, and resolve merge conflicts using Git and the GitHub CLI (gh) in Julia package development. Use this skill when committing changes, pushing to remotes, creating or merging PRs, syncing forks, cloning repos, or resolving conflicts in .jl packages."
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

## Verify After Push

After pushing, confirm CI passes and the PR is ready:

```bash
gh pr checks          # watch CI status
gh pr view --web      # open in browser to review
```

If push fails due to upstream changes:

```bash
git fetch upstream
git rebase upstream/master  # or main
git push --force-with-lease origin descriptive-branch-name
```

## Reference

- **[Best Practices](references/best-practices.md)** - Commit messages, branch naming, atomic commits
- **[Common Operations](references/common-ops.md)** - Undo, sync, stash, conflict resolution

## Related Skills

- `julia-package-dev` - Package development basics, including multi-package workflows
