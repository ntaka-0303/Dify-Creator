#!/bin/bash
# Test connection to Dify

# Usage:
#   bash scripts/test-connection.sh
#
# This script verifies that the Dify connection is working
# and credentials are properly configured.

echo "Testing Dify connection..."
docker compose run --rm dify-creator login

# Check exit status
if [ $? -eq 0 ]; then
    echo "✅ Connection successful!"
    exit 0
else
    echo "❌ Connection failed. Check .env configuration:"
    echo "   - DIFY_BASE_URL"
    echo "   - DIFY_EMAIL"
    echo "   - DIFY_PASSWORD"
    exit 1
fi
