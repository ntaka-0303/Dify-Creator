# Setup Workflow Guide

Complete step-by-step guide for setting up Dify-Creator.

## Contents
- Pre-setup checklist
- Setup steps
- Verification
- Troubleshooting
- Advanced configuration

---

## Pre-setup checklist

Before starting setup, ensure you have:

```
Setup Requirements:
- [ ] Dify account created (cloud.dify.ai or self-hosted)
- [ ] Dify login email and password
- [ ] Docker installed (docker --version shows version)
- [ ] Git repository cloned locally
- [ ] Terminal/CLI access
- [ ] Stable internet connection
```

### Quick verification

```bash
# Check Docker is installed
docker --version
# Should output: Docker version 20.x.x or higher

# Check Git
git --version
# Should output: git version 2.x.x or higher
```

---

## Setup process

### Step 1: Gather your information

**Dify Cloud (recommended)**:
```
URL: https://cloud.dify.ai
Email: your-email@example.com
Password: your-dify-password
SSL verification: Yes (leave default)
```

**Self-hosted Dify**:
```
URL: http://your-server-ip:5001
Email: your-email@example.com
Password: your-password
SSL verification: Depends on certificate
```

### Step 2: Run setup

```bash
# Ask Claude to set up the project:
/setting-up-dify-project
```

Or manually:

```bash
# Create .env from template (if it doesn't exist)
test -f .env || cp .env.example .env

# Edit .env with your credentials
# (see values below)
```

### Step 3: Provide configuration

Claude will ask for:

1. **Dify URL**
   - Cloud: `https://cloud.dify.ai` (default)
   - Self-hosted: `http://your-server:5001`

2. **Email**
   - Your Dify account email
   - Example: `user@example.com`

3. **Password**
   - Your Dify account password
   - Keep it secure in `.env`

4. **SSL Verification** (for self-hosted)
   - `true` for valid SSL certificates (recommended)
   - `false` for self-signed certificates

### Step 4: Automatic configuration

Claude sets up:

```bash
# 1. Create/update .env file
DIFY_BASE_URL=https://cloud.dify.ai
DIFY_EMAIL=your-email@example.com
DIFY_PASSWORD=your-password
DIFY_VERIFY_SSL=true

# 2. Build Docker image
docker compose build

# 3. Test connection
docker compose run --rm dify-creator login

# 4. Show success message
# Setup complete! You're ready to create apps.
```

### Step 5: Verify setup

Success looks like:

```
✅ Configuration created
✅ Docker image built
✅ Connection test passed
✅ Ready to create apps
```

---

## After successful setup

### Test that everything works

```bash
# Test login (should succeed silently)
docker compose run --rm dify-creator login

# If successful, no error message shown
# If failed, you'll see an error—report it
```

### What's been created

```
.env                          # Your credentials (DO NOT COMMIT TO GIT)
(docker image)                # Built and ready to use
.docker/               # Docker files (created if needed)
```

### Ready to use

You can now:
- Create new Dify apps: `/managing-dify-apps`
- Edit existing apps: `/managing-dify-apps`
- Manage your project

---

## Detailed configuration options

### `.env` file

The setup creates `.env` with these variables:

| Variable | Meaning | Example |
|----------|---------|---------|
| `DIFY_BASE_URL` | Dify server address | `https://cloud.dify.ai` |
| `DIFY_EMAIL` | Your Dify account email | `user@example.com` |
| `DIFY_PASSWORD` | Your Dify password | `your-secure-password` |
| `DIFY_VERIFY_SSL` | Verify SSL certificates | `true` or `false` |

### For Dify Cloud

```env
DIFY_BASE_URL=https://cloud.dify.ai
DIFY_EMAIL=your-email@example.com
DIFY_PASSWORD=your-password
DIFY_VERIFY_SSL=true
```

### For self-hosted with valid SSL

```env
DIFY_BASE_URL=https://your-domain.com:5001
DIFY_EMAIL=your-email@example.com
DIFY_PASSWORD=your-password
DIFY_VERIFY_SSL=true
```

### For self-hosted with self-signed certificate

```env
DIFY_BASE_URL=https://your-domain.com:5001
DIFY_EMAIL=your-email@example.com
DIFY_PASSWORD=your-password
DIFY_VERIFY_SSL=false
```

### For local development

```env
DIFY_BASE_URL=http://localhost:5001
DIFY_EMAIL=your-email@example.com
DIFY_PASSWORD=your-password
DIFY_VERIFY_SSL=false
```

---

## Verification steps

### Step 1: Check .env exists

```bash
# File should exist and not be empty
test -f .env && wc -l .env
# Output: 4 .env (or similar)
```

### Step 2: Verify connection

```bash
# This should succeed without errors
docker compose run --rm dify-creator login

# Success: No output or "Login successful"
# Failure: Error message about credentials or connection
```

### Step 3: Check Docker image

```bash
# Docker image should be available
docker images | grep dify-creator
# Should show the image listed
```

### Step 4: Run a test

After completing other setup steps:

```bash
# This validates the entire setup
docker compose run --rm dify-creator validate --dsl examples/templates/1_simple_chatbot.dsl.yml
# Should output: ✅ Validation successful
```

---

## Troubleshooting setup

### "Could not find .env" or ".env is empty"

**Problem**: Configuration file is missing.

**Solution**:
```bash
# Create from template
cp .env.example .env

# Edit with your credentials
nano .env  # (or your preferred editor)

# Verify
cat .env
```

### "Docker is not installed"

**Problem**: Docker command not found.

**Solution**:
1. Install Docker Desktop or Docker Engine
   - Mac: https://docs.docker.com/desktop/install/mac-install/
   - Windows: https://docs.docker.com/desktop/install/windows-install/
   - Linux: https://docs.docker.com/engine/install/

2. Verify installation:
   ```bash
   docker --version
   ```

### "Authentication failed" or "Login error"

**Problem**: Credentials are incorrect or account doesn't exist.

**Solutions**:

1. **Verify credentials**:
   - Is the email correct? (should be your account login email)
   - Is the password correct? (check caps lock, special characters)
   - Has password been changed recently?

2. **Test credentials manually**:
   - Log into Dify web UI (https://cloud.dify.ai)
   - Confirm email/password work there

3. **Update .env**:
   ```bash
   nano .env
   # Fix DIFY_EMAIL and DIFY_PASSWORD
   ```

4. **Retry login**:
   ```bash
   docker compose run --rm dify-creator login
   ```

### "Connection timeout" or "Cannot reach server"

**Problem**: Cannot connect to Dify server.

**Solutions**:

1. **Check internet connection**:
   ```bash
   ping cloud.dify.ai  # For cloud version
   # Should return responses
   ```

2. **Verify URL in .env**:
   ```bash
   grep DIFY_BASE_URL .env
   # Should show correct URL
   ```

3. **For self-hosted Dify**:
   - Is the server running?
   - Is the URL correct and accessible?
   - Test in browser: `http://your-server:5001`

4. **Firewall/proxy issues**:
   - Check if firewall blocks the connection
   - Check if corporate proxy needs configuration

### "Docker build failed"

**Problem**: Docker image build encountered an error.

**Solutions**:

1. **Check Docker daemon**:
   ```bash
   docker ps
   # If error, Docker daemon isn't running
   ```

2. **Retry build**:
   ```bash
   docker compose build --no-cache
   ```

3. **Check disk space**:
   ```bash
   df -h /
   # Need at least 5GB free
   ```

### "Port already in use"

**Problem**: Docker can't bind to required port.

**Solutions**:

1. **Find process using port**:
   ```bash
   # On Mac/Linux:
   lsof -i :5001

   # On Windows:
   netstat -ano | findstr :5001
   ```

2. **Change port** in `docker-compose.yml`:
   ```yaml
   services:
     dify-creator:
       ports:
         - "5002:5001"  # Changed from 5001 to 5002
   ```

---

## Advanced configuration

### Multiple environments

If you need to manage multiple Dify instances:

```bash
# Create separate .env files
.env.cloud          # Cloud instance
.env.local          # Local development
.env.staging        # Staging server

# Load specific environment
DIFY_ENV_FILE=.env.staging docker compose run --rm dify-creator login
```

### Using environment variables instead of .env

```bash
# Set variables directly (takes precedence over .env)
export DIFY_BASE_URL=https://cloud.dify.ai
export DIFY_EMAIL=user@example.com
export DIFY_PASSWORD=password

docker compose run --rm dify-creator login
```

### Proxy configuration

If behind a corporate proxy:

```bash
# Add to .env
HTTP_PROXY=http://proxy-server:port
HTTPS_PROXY=http://proxy-server:port
NO_PROXY=localhost,127.0.0.1
```

---

## Security best practices

✅ **DO:**
- Keep `.env` file secure (never commit to Git)
- Use strong passwords
- Rotate passwords periodically
- Add `.env` to `.gitignore` (should already be done)
- Use HTTPS for Dify URL when possible
- Verify SSL certificates

❌ **DON'T:**
- Share `.env` file with others
- Commit `.env` to version control
- Use easily guessable passwords
- Leave default credentials in production
- Disable SSL verification unless necessary (self-signed certs only)

---

## Verifying security

```bash
# Verify .env is in .gitignore
grep .env .gitignore
# Should output: .env

# Verify .env won't be committed
git status
# Should NOT show .env in changes
```

---

## Resetting setup

If you need to start over:

```bash
# Option 1: Update credentials
nano .env
# Edit DIFY_EMAIL and DIFY_PASSWORD

# Option 2: Rebuild Docker image
docker compose down
docker compose build --no-cache

# Option 3: Start completely fresh
rm .env
rm -rf .docker
# Then run setup again
```

---

## Getting help

If setup still fails:

1. **Collect error messages**:
   ```bash
   docker compose run --rm dify-creator login 2>&1 | tee setup-error.log
   ```

2. **Check logs**:
   ```bash
   cat setup-error.log
   ```

3. **Share the error** with Claude along with:
   - Your error message
   - What you were trying to do
   - Your system (Mac/Windows/Linux)
   - Dify version (if self-hosted)

---

## Next steps after setup

Once setup is complete:

1. **Create your first app**:
   - Use `/managing-dify-apps`
   - Choose a template
   - Create and test your app

2. **Verify connection works** by creating a test app

3. **Learn about templates**:
   - See [../managing-dify-apps/reference/templates.md](../managing-dify-apps/reference/templates.md)

4. **Explore workflows**:
   - See [../managing-dify-apps/reference/workflows.md](../managing-dify-apps/reference/workflows.md)
