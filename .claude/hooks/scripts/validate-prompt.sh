#!/bin/bash
# validate-prompt.sh
# Validates user prompts before processing

PROMPT="$1"

# Patterns that might indicate prompt injection attempts
SUSPICIOUS_PATTERNS=(
    "ignore previous instructions"
    "ignore all previous"
    "disregard previous"
    "forget everything"
    "you are now"
    "pretend you are"
    "act as if"
    "new persona"
    "jailbreak"
    "DAN mode"
)

# Check for suspicious patterns (case-insensitive)
PROMPT_LOWER=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]')

for pattern in "${SUSPICIOUS_PATTERNS[@]}"; do
    pattern_lower=$(echo "$pattern" | tr '[:upper:]' '[:lower:]')
    if [[ "$PROMPT_LOWER" == *"$pattern_lower"* ]]; then
        echo "WARNING: Suspicious prompt pattern detected: '$pattern'"
        # Note: We warn but don't block - let the user decide
    fi
done

# Check for extremely long prompts that might be attacks
PROMPT_LENGTH=${#PROMPT}
MAX_LENGTH=100000

if [ $PROMPT_LENGTH -gt $MAX_LENGTH ]; then
    echo "WARNING: Prompt is unusually long ($PROMPT_LENGTH characters)"
fi

# Check for encoded content that might hide instructions
if echo "$PROMPT" | grep -qE "base64|\\\\x[0-9a-fA-F]{2}|%[0-9a-fA-F]{2}"; then
    echo "NOTE: Prompt contains encoded content"
fi

exit 0
