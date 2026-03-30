---
name: whitespace
description: "Fix trailing whitespace, clean up line endings, and ensure files end with exactly one newline. Use this skill when preparing code for commit, running pre-commit cleanup, or when whitespace or EOL formatting issues are detected in source files."
---

# Whitespace

Fix whitespace issues in source code: trailing whitespace and missing final newlines.

## Workflow

1. **Check** — dry-run to see what would change:
   ```bash
   <skills>/whitespace/scripts/whitespace-check.sh [directory] [extensions]
   ```
2. **Fix** — apply corrections:
   ```bash
   <skills>/whitespace/scripts/whitespace-fix.sh [directory] [extensions]
   ```
3. **Verify** — review changes before committing:
   ```bash
   git diff
   ```

Default extensions: `jl,py,js,ts,tsx,rs,go,md,json,yaml,yml,toml,sh`

Default directory: current working directory (`.`)

## What Gets Fixed

1. **Trailing whitespace** - spaces/tabs at end of lines
2. **Final newline** - ensures files end with exactly one newline

## Notes

- Scripts require GNU sed (Linux default, install via `brew install gnu-sed` on macOS)
- Binary files and `.git` directory are excluded
