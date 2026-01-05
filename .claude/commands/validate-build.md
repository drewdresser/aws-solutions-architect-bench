---
name: validate-build
description: Ensure the project builds successfully.
allowed-tools:
  - Bash
  - Read
---

# Validate Build Command

Verify that the project builds successfully and all artifacts are generated correctly.

## Process

### 1. Clean Previous Build
```bash
# Python
rm -rf dist/ build/ *.egg-info/

# Node/React
rm -rf dist/ build/ .next/ node_modules/.cache/
```

### 2. Install Dependencies
```bash
# Python
uv sync

# Node
pnpm install
```

### 3. Run Build
```bash
# Python package
uv build

# Frontend
pnpm build
```

### 4. Verify Artifacts
- Check expected output files exist
- Verify file sizes are reasonable
- Check for build warnings

## Output Format

```markdown
## Build Validation Report

### Environment
- Python: 3.12.x
- Node: 20.x
- Platform: darwin-arm64

### Build Steps

| Step | Status | Duration |
|------|--------|----------|
| Clean | ✓ | 0.5s |
| Install | ✓ | 12.3s |
| Build | ✓ | 8.7s |
| Verify | ✓ | 0.2s |

### Artifacts
| File | Size |
|------|------|
| dist/app.js | 142 KB |
| dist/app.css | 28 KB |

### Warnings
[Any build warnings]

### Result
✓ Build successful
```

## Common Issues

### Node Memory
```bash
# Increase memory if needed
NODE_OPTIONS=--max_old_space_size=4096 pnpm build
```

### Missing Dependencies
```bash
# Ensure all deps installed
pnpm install --frozen-lockfile
```

### Type Errors
```bash
# Check types first
pnpm typecheck
```
