#!/bin/bash
# Run app with test inputs

# Usage:
#   bash scripts/run-test-inputs.sh <app-id> [inputs-file] [output-dir]
#
# Examples:
#   bash scripts/run-test-inputs.sh abc123def456
#   bash scripts/run-test-inputs.sh abc123def456 examples/inputs.json artifacts
#
# If inputs-file or output-dir are not provided, defaults are used:
#   - inputs-file: examples/inputs.json
#   - output-dir: artifacts

APP_ID="${1:-}"
INPUTS_FILE="${2:-examples/inputs.json}"
OUTPUT_DIR="${3:-artifacts}"

# Validate inputs
if [ -z "$APP_ID" ]; then
    echo "❌ Error: App ID is required"
    echo ""
    echo "Usage: bash scripts/run-test-inputs.sh <app-id> [inputs-file] [output-dir]"
    echo ""
    echo "Example:"
    echo "  bash scripts/run-test-inputs.sh abc123def456"
    echo "  bash scripts/run-test-inputs.sh abc123def456 examples/inputs.json artifacts"
    exit 1
fi

if [ ! -f "$INPUTS_FILE" ]; then
    echo "❌ Error: Inputs file not found: $INPUTS_FILE"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "Running app $APP_ID with test inputs from $INPUTS_FILE"
docker compose run --rm dify-creator sync \
  --app-id "$APP_ID" \
  --dsl app.dsl.yml \
  --inputs-json "$INPUTS_FILE" \
  --out-dir "$OUTPUT_DIR"

# Check exit status
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Test execution complete"
    echo "Results saved to: $OUTPUT_DIR/run_result.json"

    if [ -f "$OUTPUT_DIR/run_result.json" ]; then
        echo ""
        echo "Preview of results:"
        head -n 20 "$OUTPUT_DIR/run_result.json"
    fi
    exit 0
else
    echo "❌ Test execution failed"
    exit 1
fi
