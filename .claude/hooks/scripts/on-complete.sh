#!/bin/bash
# on-complete.sh
# Runs when Claude Code session completes

LOG_DIR="${HOME}/.claude/logs"
SESSION_LOG="${LOG_DIR}/session-$(date +%Y%m%d).log"

# Create log directory if needed
mkdir -p "$LOG_DIR"

# Log session completion
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "[$TIMESTAMP] Session completed" >> "$SESSION_LOG"

# Optional: Run cleanup tasks
# - Clear temporary files
# - Rotate old logs
# - Send summary notification

# Rotate logs older than 30 days
find "$LOG_DIR" -name "*.log" -mtime +30 -delete 2>/dev/null

# Optional: Play completion sound (macOS)
# afplay /System/Library/Sounds/Glass.aiff 2>/dev/null

exit 0
