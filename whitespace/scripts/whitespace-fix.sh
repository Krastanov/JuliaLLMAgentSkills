#!/usr/bin/env bash
set -euo pipefail

DIR="${1:-.}"
EXTS="${2:-jl,py,js,ts,tsx,rs,go,md,json,yaml,yml,toml,sh}"

# Build find pattern
PATTERN=$(echo "$EXTS" | sed 's/,/" -o -name "*./g' | sed 's/^/-name "*./' | sed 's/$/"/')

echo "Fixing whitespace issues in $DIR..."

# Fix trailing whitespace and missing final newlines
eval "find \"$DIR\" -type f \( $PATTERN \) -not -path '*/.git/*' -print0" | while IFS= read -r -d '' file; do
    # Remove trailing whitespace
    sed -i 's/[[:space:]]*$//' "$file"
    # Add final newline if missing
    if [ -s "$file" ] && [ "$(tail -c1 "$file" | wc -l)" -eq 0 ]; then
        echo "" >> "$file"
    fi
done

echo "Done. Review changes with: git diff"
