---
name: setting-up-dify-project
description: Set up and configure a Dify-Creator project for the first time. Use during initial setup when configuring Dify credentials, environment variables, and Docker. Handles credential configuration, connection testing, and build setup.
---

# Setting up a Dify project

Complete initial setup for the Dify-Creator project. This Skill guides you through credential configuration, environment setup, and verification.

## What this Skill does

- **Configures credentials**: Collects Dify account information
- **Sets up environment**: Creates `.env` file with your settings
- **Builds Docker image**: Prepares the container environment
- **Tests connection**: Verifies access to Dify
- **Validates setup**: Confirms everything is ready to use

## When to use

Use this Skill:
- **First time** setting up the project
- **When environment variables change** (new password, different Dify URL)
- **After moving to a new machine**
- **When connection tests fail**

## Quick start

### Step-by-step setup

1. **Run setup**: Ask me to set up your Dify project
2. **Provide information**:
   - Dify URL (cloud or self-hosted)
   - Email address
   - Password
   - SSL verification (if self-hosted)
3. **I'll handle the rest**:
   - Create `.env` configuration
   - Build Docker image
   - Test the connection
   - Confirm setup is complete

### Information needed

Have this ready before starting:

- **Dify account email**: Your login email (not API key)
- **Dify password**: Your account password
- **Dify URL**: Cloud (https://cloud.dify.ai) or self-hosted URL
- **SSL certificate** (for self-hosted): Whether to verify SSL

## Setup workflow

See [reference/setup-workflow.md](reference/setup-workflow.md) for:
- Detailed step-by-step instructions
- Troubleshooting common setup issues
- Configuration options
- Verifying successful setup

## Automation scripts

This Skill uses the following script to verify your setup:

**Setup verification**:
```bash
bash scripts/verify-setup.sh
```
- Tests connection to Dify server
- Validates credentials
- Confirms Docker environment is ready
- Implementation details: [scripts/verify-setup.sh](scripts/verify-setup.sh)

The Skill runs this automatically during setup - no need to run it manually.

## After setup

Once setup is complete, you can use the `managing-dify-apps` Skill to:
- Create new Dify apps
- Edit existing apps
- Test configurations
- Deploy and iterate

## Prerequisites

- Git repository (you're reading this, so ✅)
- Docker installed (`docker --version` should work)
- Dify account credentials
- Terminal access

## Troubleshooting setup

**If setup fails:**
- See [reference/troubleshooting.md](reference/troubleshooting.md) for common issues
- Most issues are related to credentials or Docker
- Follow the diagnostic steps to identify the problem

## Environment variables

Setup creates a `.env` file with:
```
DIFY_BASE_URL=https://cloud.dify.ai
DIFY_EMAIL=your-email@example.com
DIFY_PASSWORD=your-password
DIFY_VERIFY_SSL=true
```

**Note**: Keep `.env` secure—it contains your credentials.

## What's installed

After setup:
- ✅ `.env` configuration file
- ✅ Docker image built and ready
- ✅ Connection verified
- ✅ Project ready for app development

## Next steps

1. Setup completes → see success message
2. Use `managing-dify-apps` Skill to create/edit apps
3. Develop your Dify applications
