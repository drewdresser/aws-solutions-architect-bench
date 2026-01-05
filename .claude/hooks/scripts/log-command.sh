#!/bin/bash
# log-command.sh
# Logs all bash commands for audit purposes

TOOL_INPUT="$1"
LOG_DIR="${HOME}/.claude/logs"
LOG_FILE="${LOG_DIR}/command-history.log"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Extract command from tool input
COMMAND=$(echo "$TOOL_INPUT" | grep -oP '"command"\s*:\s*"\K[^"]+' || echo "$TOOL_INPUT")

# Log with timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "[$TIMESTAMP] $COMMAND" >> "$LOG_FILE"

# Dangerous command patterns to warn about
DANGEROUS_PATTERNS=(
    "rm -rf /"
    "rm -rf ~"
    "rm -rf \$HOME"
    "> /dev/sda"
    "mkfs"
    "dd if="
    ":(){:|:&};:"
    "chmod -R 777 /"
    "curl.*|.*sh"
    "wget.*|.*sh"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if [[ "$COMMAND" == *"$pattern"* ]]; then
        echo "BLOCKED: Dangerous command pattern detected: $pattern"
        exit 1
    fi
done

exit 0
