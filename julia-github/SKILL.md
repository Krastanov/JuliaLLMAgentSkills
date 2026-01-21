---
name: julia-github
description: Use Git and the GitHub CLI for version control and pull request workflows in Julia package development. Use this skill when working with Git remotes, branches, and PRs.
---

# Julia GitHub Workflow

Use Git and the GitHub CLI (`gh`) for version control and pull request workflows
in Julia package development.

## Repository Setup

### Configure Remotes

Keep two remotes: `upstream` (source of truth) and `origin` (your fork):

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/PackageName.jl.git
cd PackageName.jl

# Add upstream remote
git remote add upstream https://github.com/OriginalOrg/PackageName.jl.git

# Verify remotes
git remote -v
```

### Standard Remote Layout

```
origin    https://github.com/YOUR_USERNAME/PackageName.jl.git (fetch)
origin    https://github.com/YOUR_USERNAME/PackageName.jl.git (push)
upstream  https://github.com/OriginalOrg/PackageName.jl.git (fetch)
upstream  https://github.com/OriginalOrg/PackageName.jl.git (push)
```

## Daily Workflow

### Before Starting Work

**Always** pull the latest changes:

```bash
# Update main/master from upstream
git checkout master
git pull upstream master

# If working on existing branch, pull that too
git checkout my-branch
git pull origin my-branch
```

### Creating a Feature Branch

```bash
# Ensure you're on latest master
git checkout master
git pull upstream master

# Create feature branch
git checkout -b descriptive-branch-name
```

### Making Changes

```bash
# Make changes to files...

# Stage changes
git add file1.jl file2.jl

# Or stage all changes
git add .

# Commit with descriptive message
git commit -m "Add feature X that does Y"

# Push to your fork
git push -u origin descriptive-branch-name
```

## Creating Pull Requests

### Using GitHub CLI

```bash
# Create PR targeting upstream
gh pr create \
    --title "Your PR Title" \
    --body "Description of changes" \
    --repo OriginalOrg/PackageName.jl

# Create PR with full body
gh pr create --title "Add feature X" --body "$(cat <<'EOF'
## Summary
- Added feature X
- Fixed bug Y

## Test plan
- [ ] Run tests locally
- [ ] Verify feature works

🤖 Generated with Claude Code
EOF
)"
```

### PR Best Practices

1. **Keep PRs focused**: One self-contained change per PR
2. **Don't mix concerns**: Separate feature work from formatting fixes
3. **Run tests first**: `julia --project=. -e 'using Pkg; Pkg.test()'`
4. **Update CHANGELOG**: If the project uses one

## Working with PRs

### View PR Information

```bash
# List open PRs
gh pr list

# View specific PR
gh pr view 123

# View PR diff
gh pr diff 123

# Check PR status/checks
gh pr checks 123
```

### Review and Comment

```bash
# View PR comments
gh api repos/Org/Repo.jl/pulls/123/comments

# Add comment to PR
gh pr comment 123 --body "Looks good! One minor suggestion..."

# Approve PR
gh pr review 123 --approve

# Request changes
gh pr review 123 --request-changes --body "Please fix X"
```

### Update Your PR

```bash
# Make additional changes
git add .
git commit -m "Address review feedback"
git push origin my-branch
```

### Sync with Upstream

If master has changed since you branched:

```bash
# Update master
git checkout master
git pull upstream master

# Rebase your branch
git checkout my-branch
git rebase master

# Force push (only for your own PR branches!)
git push origin my-branch --force-with-lease
```

## Issue Management

```bash
# List issues
gh issue list

# View issue
gh issue view 123

# Create issue
gh issue create --title "Bug: X doesn't work" --body "Description..."

# Close issue
gh issue close 123
```

## Git Best Practices

### Commit Messages

```bash
# Good: Descriptive, starts with verb
git commit -m "Add support for feature X"
git commit -m "Fix bug in function Y"
git commit -m "Update dependency Z to v2.0"

# Bad: Vague or non-descriptive
git commit -m "Fix"
git commit -m "Updates"
git commit -m "WIP"
```

### Atomic Commits

Make each commit a single logical change:

```bash
# Good: Separate commits for separate changes
git add src/feature.jl
git commit -m "Add new feature function"

git add test/test_feature.jl
git commit -m "Add tests for new feature"

# Bad: Everything in one commit
git add .
git commit -m "Add feature and tests and fix other stuff"
```

### Branch Naming

Use descriptive, lowercase, hyphenated names:

```bash
# Good
git checkout -b add-serialization-support
git checkout -b fix-memory-leak-in-parser
git checkout -b update-docs-for-v2

# Bad
git checkout -b fix
git checkout -b myBranch
git checkout -b Feature_X
```

## Common Git Operations

### Undo Last Commit (Keep Changes)

```bash
git reset --soft HEAD~1
```

### Discard Local Changes

```bash
# Discard changes to specific file
git checkout -- file.jl

# Discard all local changes
git checkout -- .
```

### Stash Changes

```bash
# Save changes temporarily
git stash

# Apply stashed changes
git stash pop

# List stashes
git stash list
```

### View History

```bash
# View commit log
git log --oneline -10

# View changes in commit
git show abc123

# View file at specific commit
git show abc123:path/to/file.jl
```

## GitHub CLI Quick Reference

| Task | Command |
|------|---------|
| Create PR | `gh pr create --title "..." --body "..."` |
| List PRs | `gh pr list` |
| View PR | `gh pr view 123` |
| Checkout PR | `gh pr checkout 123` |
| Merge PR | `gh pr merge 123` |
| Close PR | `gh pr close 123` |
| List issues | `gh issue list` |
| View issue | `gh issue view 123` |
| Create issue | `gh issue create` |
| View repo | `gh repo view` |

## Git Quick Reference

| Task | Command |
|------|---------|
| Clone | `git clone URL` |
| Pull | `git pull origin branch` |
| Push | `git push origin branch` |
| Branch | `git checkout -b name` |
| Status | `git status` |
| Diff | `git diff` |
| Add | `git add file` |
| Commit | `git commit -m "msg"` |
| Log | `git log --oneline` |
| Stash | `git stash` / `git stash pop` |

## Related Skills

- `julia-multipackage` - Multi-package development workflows
- `julia-package-dev` - Package development basics
- `julia-ci-github` - GitHub Actions CI
