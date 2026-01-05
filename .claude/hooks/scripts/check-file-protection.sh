#!/bin/bash
# check-file-protection.sh
# Prevents modification of protected files and directories

TOOL_INPUT="$1"

# Extract file path from tool input
FILE_PATH=$(echo "$TOOL_INPUT" | grep -oP '"file_path"\s*:\s*"\K[^"]+' || echo "")

if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Protected patterns
PROTECTED_PATTERNS=(
    ".env"
    ".env.*"
    "*.pem"
    "*.key"
    "*credentials*"
    "*secrets*"
    ".git/config"
    ".ssh/*"
    "node_modules/*"
    ".venv/*"
    "__pycache__/*"
)

# Check if file matches protected patterns
for pattern in "${PROTECTED_PATTERNS[@]}"; do
    if [[ "$FILE_PATH" == $pattern ]]; then
        echo "BLOCKED: Cannot modify protected file: $FILE_PATH"
        exit 1
    fi
done

# Check for sensitive content patterns in the file
if [ -f "$FILE_PATH" ]; then
    if grep -qE "(password|secret|api_key|private_key)\s*=" "$FILE_PATH" 2>/dev/null; then
        echo "WARNING: File contains sensitive patterns. Proceeding with caution."
    fi
fi

exit 0
