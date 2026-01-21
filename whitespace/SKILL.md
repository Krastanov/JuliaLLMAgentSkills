---
name: whitespace
description: Fix trailing whitespace and ensure files end with newlines. Use this skill when preparing code for commit or when whitespace issues are detected.
---

# Whitespace

Fix whitespace issues in source code: trailing whitespace and missing final newlines.

## When to Use

- Before committing code
- When user asks to clean up or format files
- When preparing a PR
- When whitespace issues are flagged by linters or CI

## Actions

### Check for issues (dry-run)
```bash
./.claude/skills/whitespace/scripts/whitespace-check.sh [directory] [extensions]
```

### Fix issues
```bash
./.claude/skills/whitespace/scripts/whitespace-fix.sh [directory] [extensions]
```

Default extensions: `jl,py,js,ts,tsx,rs,go,md,json,yaml,yml,toml,sh`

Default directory: current working directory (`.`)

## What Gets Fixed

1. **Trailing whitespace** - spaces/tabs at end of lines
2. **Final newline** - ensures files end with exactly one newline

## Notes

- Scripts require GNU sed (Linux default, install via `brew install gnu-sed` on macOS)
- Binary files and `.git` directory are excluded
- Always review changes with `git diff` after running
