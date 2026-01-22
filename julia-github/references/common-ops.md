# Common Git Operations

## Undo Last Commit (Keep Changes)

```bash
git reset --soft HEAD~1
```

## Discard Local Changes

```bash
# Specific file
git checkout -- file.jl

# All changes
git checkout -- .
```

## Stash Changes

```bash
git stash           # Save temporarily
git stash pop       # Apply stashed changes
git stash list      # List stashes
```

## Sync with Upstream

```bash
git checkout master
git pull upstream master

git checkout my-branch
git rebase master

# Force push (only for your own PR branches!)
git push origin my-branch --force-with-lease
```

## View History

```bash
git log --oneline -10
git show abc123
git show abc123:path/to/file.jl
```

## Working with PRs

```bash
gh pr view 123
gh pr diff 123
gh pr checks 123
gh pr comment 123 --body "Looks good!"
gh pr review 123 --approve
```

## Issue Management

```bash
gh issue list
gh issue view 123
gh issue create --title "Bug: X" --body "Description..."
gh issue close 123
```
