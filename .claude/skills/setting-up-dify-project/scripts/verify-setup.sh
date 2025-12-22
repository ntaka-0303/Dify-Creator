#!/bin/bash
# Verify Dify project setup

# Usage:
#   bash scripts/verify-setup.sh
#
# This script checks if all required setup steps have been completed

echo "Verifying Dify project setup..."
echo ""

# Check for .env file
echo "1. Checking .env configuration..."
if [ -f ".env" ]; then
    echo "   ✅ .env file exists"

    # Check for required variables
    if grep -q "DIFY_BASE_URL" .env && \
       grep -q "DIFY_EMAIL" .env && \
       grep -q "DIFY_PASSWORD" .env; then
        echo "   ✅ Required environment variables configured"
    else
        echo "   ❌ Missing required environment variables"
        exit 1
    fi
else
    echo "   ❌ .env file not found. Run setup first."
    exit 1
fi

echo ""
echo "2. Checking Docker setup..."
if docker --version > /dev/null 2>&1; then
    echo "   ✅ Docker is installed"
else
    echo "   ❌ Docker is not installed"
    exit 1
fi

# Check for docker-compose
if docker compose version > /dev/null 2>&1; then
    echo "   ✅ Docker Compose is available"
else
    echo "   ❌ Docker Compose is not available"
    exit 1
fi

echo ""
echo "3. Testing Dify connection..."
docker compose run --rm dify-creator login > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "   ✅ Successfully connected to Dify"
else
    echo "   ❌ Failed to connect to Dify"
    echo "   Check your .env configuration and verify your credentials"
    exit 1
fi

echo ""
echo "✅ All setup verification checks passed!"
echo ""
echo "You're ready to use Dify-Creator. Try:"
echo "  - Creating a new app: dify-new-app"
echo "  - Editing an app: dify-edit-app"
echo "  - Managing apps: managing-dify-apps"
