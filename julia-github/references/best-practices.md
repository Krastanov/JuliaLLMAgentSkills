# Git Best Practices

## Commit Messages

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

## Atomic Commits

Make each commit a single logical change:

```bash
# Good: Separate commits
git add src/feature.jl
git commit -m "Add new feature function"

git add test/test_feature.jl
git commit -m "Add tests for new feature"

# Bad: Everything in one commit
git add .
git commit -m "Add feature and tests and fix other stuff"
```

## Branch Naming

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

## PR Best Practices

1. **Keep PRs focused**: One self-contained change per PR
2. **Don't mix concerns**: Separate feature work from formatting fixes
3. **Run tests first**: `julia -tauto --project=. -e 'using Pkg; Pkg.test()'`
4. **Update CHANGELOG**: If the project uses one
