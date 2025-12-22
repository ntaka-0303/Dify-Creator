#!/bin/bash
# Validate DSL configuration

# Usage:
#   bash scripts/run-validation.sh <path-to-dsl>
#
# Example:
#   bash scripts/run-validation.sh app.dsl.yml

DSL_FILE="${1:-app.dsl.yml}"

if [ ! -f "$DSL_FILE" ]; then
    echo "❌ Error: DSL file not found: $DSL_FILE"
    exit 1
fi

echo "Validating DSL: $DSL_FILE"
docker compose run --rm dify-creator validate --dsl "$DSL_FILE"
