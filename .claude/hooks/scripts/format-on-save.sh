#!/bin/bash
# format-on-save.sh
# Automatically formats files after editing

TOOL_INPUT="$1"

# Extract file path from tool input
FILE_PATH=$(echo "$TOOL_INPUT" | grep -oP '"file_path"\s*:\s*"\K[^"]+' || echo "")

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# Get file extension
EXTENSION="${FILE_PATH##*.}"

# Format based on file type
case "$EXTENSION" in
    py)
        # Python formatting with ruff if available
        if command -v ruff &> /dev/null; then
            ruff format "$FILE_PATH" --quiet 2>/dev/null
        elif command -v black &> /dev/null; then
            black "$FILE_PATH" --quiet 2>/dev/null
        fi
        ;;
    js|jsx|ts|tsx|json|css|scss|md|yaml|yml)
        # JavaScript/TypeScript/JSON formatting with prettier if available
        if command -v prettier &> /dev/null; then
            prettier --write "$FILE_PATH" --log-level error 2>/dev/null
        fi
        ;;
    go)
        # Go formatting
        if command -v gofmt &> /dev/null; then
            gofmt -w "$FILE_PATH" 2>/dev/null
        fi
        ;;
    rs)
        # Rust formatting
        if command -v rustfmt &> /dev/null; then
            rustfmt "$FILE_PATH" 2>/dev/null
        fi
        ;;
esac

exit 0
