#!/usr/bin/env bash
set -euo pipefail

DIR="${1:-.}"
EXTS="${2:-jl,py,js,ts,tsx,rs,go,md,json,yaml,yml,toml,sh}"

# Build find pattern
PATTERN=$(echo "$EXTS" | sed 's/,/" -o -name "*./g' | sed 's/^/-name "*./' | sed 's/$/"/')

echo "Checking for whitespace issues in $DIR..."

ISSUES=0

# Check trailing whitespace
echo "=== Trailing whitespace ==="
while IFS= read -r -d '' file; do
    if grep -qE '[[:space:]]$' "$file" 2>/dev/null; then
        echo "  $file"
        ISSUES=$((ISSUES + 1))
    fi
done < <(eval "find \"$DIR\" -type f \( $PATTERN \) -not -path '*/.git/*' -print0")

# Check missing final newlines
echo "=== Missing final newline ==="
while IFS= read -r -d '' file; do
    if [ -s "$file" ] && [ "$(tail -c1 "$file" | wc -l)" -eq 0 ]; then
        echo "  $file"
        ISSUES=$((ISSUES + 1))
    fi
done < <(eval "find \"$DIR\" -type f \( $PATTERN \) -not -path '*/.git/*' -print0")

if [ "$ISSUES" -eq 0 ]; then
    echo "No whitespace issues found."
else
    echo "Found $ISSUES file(s) with issues."
    exit 1
fi
