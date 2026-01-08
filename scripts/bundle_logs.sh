#!/bin/bash
# Bundle evaluation logs for static hosting
#
# Usage:
#   ./scripts/bundle_logs.sh
#   LOG_DIR=logs/custom OUTPUT_DIR=docs/logs ./scripts/bundle_logs.sh
#
# This script:
# 1. Runs `inspect view bundle` to create a static log viewer
# 2. Generates a manifest.json mapping models to their logs
# 3. Places output in docs/logs/ for GitHub Pages deployment

set -e

# Configuration
LOG_DIR="${LOG_DIR:-logs}"
OUTPUT_DIR="${OUTPUT_DIR:-docs/logs}"

echo "=== Log Bundling Script ==="
echo "Log directory: $LOG_DIR"
echo "Output directory: $OUTPUT_DIR"

# Check if logs directory exists and has files
if [ ! -d "$LOG_DIR" ]; then
    echo "Warning: Log directory '$LOG_DIR' does not exist"
    echo "No logs to bundle. Exiting gracefully."
    exit 0
fi

# Find log files (recursively, looking for .eval files)
LOG_COUNT=$(find "$LOG_DIR" -name "*.eval" 2>/dev/null | wc -l | tr -d ' ')

if [ "$LOG_COUNT" -eq 0 ]; then
    echo "Warning: No .eval log files found in '$LOG_DIR'"
    echo "No logs to bundle. Exiting gracefully."
    exit 0
fi

echo "Found $LOG_COUNT log file(s)"

# Create output directory if needed
mkdir -p "$OUTPUT_DIR"

# Run inspect view bundle
echo "Running inspect view bundle..."
uv run inspect view bundle \
    --log-dir "$LOG_DIR" \
    --output-dir "$OUTPUT_DIR" \
    --overwrite

echo "Bundle created at $OUTPUT_DIR"

# Generate manifest.json from listing.json for leaderboard integration
LISTING_FILE="$OUTPUT_DIR/logs/listing.json"
MANIFEST_FILE="$OUTPUT_DIR/manifest.json"

if [ -f "$LISTING_FILE" ]; then
    echo "Generating manifest.json for leaderboard integration..."

    # Use Python to transform listing.json into a model-centric manifest
    uv run python3 << 'PYTHON_SCRIPT'
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

output_dir = sys.argv[1] if len(sys.argv) > 1 else "docs/logs"
listing_path = Path(output_dir) / "logs" / "listing.json"
manifest_path = Path(output_dir) / "manifest.json"

if not listing_path.exists():
    print(f"Warning: {listing_path} not found")
    sys.exit(0)

with open(listing_path) as f:
    listing = json.load(f)

# Build model-centric manifest
models = {}
for log_file, meta in listing.items():
    model = meta.get("model", "unknown")

    # Normalize model name (remove openrouter/ prefix for display)
    display_model = model
    if model.startswith("openrouter/"):
        display_model = model.replace("openrouter/", "")

    if display_model not in models:
        models[display_model] = {
            "logs": [],
            "latest_run": None
        }

    log_entry = {
        "file": f"logs/{log_file}",
        "task": meta.get("task", "unknown"),
        "status": meta.get("status", "unknown"),
        "score": meta.get("primary_metric", {}).get("value"),
        "started_at": meta.get("started_at"),
        "completed_at": meta.get("completed_at")
    }
    models[display_model]["logs"].append(log_entry)

    # Track latest run
    if meta.get("completed_at"):
        current_latest = models[display_model]["latest_run"]
        if current_latest is None or meta["completed_at"] > current_latest:
            models[display_model]["latest_run"] = meta["completed_at"]

manifest = {
    "_generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "_log_count": len(listing),
    "models": models
}

with open(manifest_path, "w") as f:
    json.dump(manifest, f, indent=2)

print(f"Manifest written to {manifest_path}")
print(f"  - {len(models)} models")
print(f"  - {len(listing)} total logs")
PYTHON_SCRIPT

else
    echo "Warning: listing.json not found, skipping manifest generation"
fi

echo ""
echo "=== Bundle Complete ==="
echo "Output: $OUTPUT_DIR"
echo ""
echo "To view locally:"
echo "  python -m http.server 8000 --directory $OUTPUT_DIR"
echo "  open http://localhost:8000"
