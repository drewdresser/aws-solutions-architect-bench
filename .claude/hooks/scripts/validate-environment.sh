#!/bin/bash
# validate-environment.sh
# Validates the development environment on session start

ERRORS=0
WARNINGS=0

echo "Validating development environment..."

# Check for required tools
check_tool() {
    local tool="$1"
    local required="$2"

    if command -v "$tool" &> /dev/null; then
        version=$($tool --version 2>/dev/null | head -n1)
        echo "✓ $tool: $version"
    else
        if [ "$required" = "required" ]; then
            echo "✗ $tool: NOT FOUND (required)"
            ((ERRORS++))
        else
            echo "⚠ $tool: not found (optional)"
            ((WARNINGS++))
        fi
    fi
}

# Required tools
check_tool "git" "required"

# Python ecosystem (optional based on project)
check_tool "python" "optional"
check_tool "uv" "optional"
check_tool "ruff" "optional"

# Node ecosystem (optional based on project)
check_tool "node" "optional"
check_tool "pnpm" "optional"

# Check git configuration
if [ -d ".git" ]; then
    echo ""
    echo "Git repository detected:"
    echo "  Branch: $(git branch --show-current 2>/dev/null)"
    echo "  Status: $(git status --porcelain 2>/dev/null | wc -l | tr -d ' ') uncommitted changes"

    # Check for uncommitted sensitive files
    if git status --porcelain 2>/dev/null | grep -qE "\.env|credentials|secrets"; then
        echo "⚠ WARNING: Sensitive files detected in uncommitted changes"
        ((WARNINGS++))
    fi
fi

# Check for .env file
if [ -f ".env" ]; then
    echo ""
    echo "✓ Environment file (.env) found"
elif [ -f ".env.example" ]; then
    echo ""
    echo "⚠ No .env file found, but .env.example exists"
    echo "  Consider copying: cp .env.example .env"
    ((WARNINGS++))
fi

# Summary
echo ""
echo "Environment validation complete:"
echo "  Errors: $ERRORS"
echo "  Warnings: $WARNINGS"

if [ $ERRORS -gt 0 ]; then
    echo ""
    echo "Environment has errors. Some features may not work correctly."
    exit 1
fi

exit 0
