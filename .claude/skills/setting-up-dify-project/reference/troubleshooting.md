# Setup Troubleshooting

Common setup issues and solutions.

## Contents
- Credential issues
- Docker and environment issues
- Connection problems
- File permission issues
- Platform-specific issues

---

## Credential issues

### "Invalid credentials" or "Authentication failed"

**Symptoms:**
```
Error: Invalid email or password
Error: Unauthorized
```

**Root causes and solutions:**

1. **Wrong email format**:
   - Verify you're using your **account email**, not API key
   - Check for typos and extra spaces
   - Confirm email is associated with your Dify account

2. **Incorrect password**:
   - Try logging in via web UI first (https://cloud.dify.ai)
   - Verify password works there
   - Check if recently changed

3. **Wrong Dify instance**:
   - Cloud users: ensure `https://cloud.dify.ai`
   - Self-hosted: use correct URL and port
   - Example: `http://localhost:5001` or `https://dify.company.com`

**Fix procedure:**

```bash
# 1. Verify credentials in Dify web UI first
# Go to https://cloud.dify.ai and log in manually

# 2. Update .env with correct values
nano .env
# Correct:
# DIFY_EMAIL=your-actual-email@example.com
# DIFY_PASSWORD=your-actual-password
# DIFY_BASE_URL=https://cloud.dify.ai

# 3. Test login again
docker compose run --rm dify-creator login
```

---

### "Account locked" or "Too many login attempts"

**Symptoms:**
```
Error: Account locked. Too many failed attempts.
```

**Solution:**

1. **Wait 15-30 minutes** before retrying
2. **Verify credentials are correct**
3. **Reset password** if possible via Dify web UI
4. **Contact Dify support** if locked for extended time

---

## Docker and environment issues

### "Docker is not installed" or "docker command not found"

**Symptoms:**
```
Command 'docker' not found
```

**Solution:**

1. **Install Docker**:
   - Mac: https://docs.docker.com/desktop/install/mac-install/
   - Windows: https://docs.docker.com/desktop/install/windows-install/
   - Linux: https://docs.docker.com/engine/install/

2. **Verify installation**:
   ```bash
   docker --version
   # Should output: Docker version 20.x or higher
   ```

3. **Start Docker daemon** (if installed but not running):
   - **Mac**: Docker Desktop app
   - **Windows**: Docker Desktop app
   - **Linux**: `sudo systemctl start docker`

---

### "Docker daemon is not running"

**Symptoms:**
```
Error: Cannot connect to Docker daemon at unix:///var/run/docker.sock
```

**Solution:**

1. **On Mac/Windows**: Open Docker Desktop application
2. **On Linux**:
   ```bash
   sudo systemctl start docker
   # Or:
   sudo service docker start
   ```

3. **Verify it's running**:
   ```bash
   docker ps
   # Should list running containers (may be empty)
   ```

---

### "Docker build fails"

**Symptoms:**
```
Error during build: ...
Failed to build image
```

**Solutions:**

1. **Clean rebuild** (removes cache):
   ```bash
   docker compose build --no-cache
   ```

2. **Check disk space**:
   ```bash
   df -h /
   # Need at least 5GB free
   # If low: delete unused Docker images/containers
   ```

3. **Check internet connection**:
   - Build downloads dependencies from internet
   - Verify connection is stable

4. **Retry with verbose output**:
   ```bash
   docker compose build --verbose
   # Shows more details about what failed
   ```

---

### ".env file not found" or "Cannot find .env"

**Symptoms:**
```
Error: .env file not found
Error: Cannot read .env
```

**Solution:**

```bash
# Check if .env exists
ls -la .env

# If not found, create it:
cp .env.example .env

# Verify it was created
cat .env

# Edit with your credentials
nano .env  # or your preferred editor
```

---

### ".env is empty or invalid"

**Symptoms:**
```
Configuration empty
Variables not loaded
```

**Solution:**

```bash
# Check file size
wc -l .env
# Should show 4+ lines

# If empty or corrupted, restore from template
cat .env.example > .env

# Edit with your values
nano .env
```

---

## Connection problems

### "Could not connect to Dify"

**Symptoms:**
```
Error: Connection refused
Error: Failed to connect to https://cloud.dify.ai
```

**Solutions:**

1. **Check internet connection**:
   ```bash
   ping google.com
   # Should get responses
   ```

2. **Test connection to Dify**:
   ```bash
   # For cloud:
   ping cloud.dify.ai

   # For self-hosted:
   ping your-server-ip
   ```

3. **Verify URL in .env**:
   ```bash
   grep DIFY_BASE_URL .env
   # Should show: DIFY_BASE_URL=https://cloud.dify.ai
   # (or your self-hosted URL)
   ```

4. **Check DNS resolution**:
   ```bash
   nslookup cloud.dify.ai
   # Should show IP addresses
   ```

---

### "Connection timeout"

**Symptoms:**
```
Error: Connection timed out
Error: Timed out connecting to server
```

**Solutions:**

1. **Increase timeout** in `.env`:
   ```bash
   # Add or modify
   CONNECTION_TIMEOUT=30
   REQUEST_TIMEOUT=60
   ```

2. **Check for firewall**:
   - May be blocking port 443 (HTTPS)
   - For self-hosted: check port 5001

3. **Check network/proxy**:
   - Corporate firewall?
   - Proxy required?
   - Try connecting from different network

4. **Verify server is running**:
   - For self-hosted: Is Dify running?
   - Check: `curl http://your-server:5001`

---

### "SSL certificate error"

**Symptoms:**
```
Error: Certificate verification failed
Error: SSL: CERTIFICATE_VERIFY_FAILED
```

**Solutions:**

1. **For self-signed certificates** (development only):
   ```bash
   # Edit .env
   DIFY_VERIFY_SSL=false
   ```

2. **For real certificates**:
   - Verify certificate is valid and not expired
   - Check certificate chains
   - Update system certificates

3. **Test connection ignoring SSL**:
   ```bash
   # For debugging only
   curl -k https://your-server:5001
   # -k ignores SSL errors
   ```

---

### "Proxy or firewall blocking"

**Symptoms:**
```
Error: Cannot reach Dify
Works on different network
```

**Solutions:**

1. **Configure proxy** in `.env`:
   ```bash
   HTTP_PROXY=http://proxy-server:8080
   HTTPS_PROXY=http://proxy-server:8080
   NO_PROXY=localhost,127.0.0.1
   ```

2. **Test with proxy settings**:
   ```bash
   docker compose run --rm dify-creator login
   # Should now connect through proxy
   ```

3. **Check with network admin**:
   - May need to whitelist Dify domain
   - May require VPN
   - May need corporate proxy certificate

---

## File and permission issues

### "Permission denied" or "Cannot write .env"

**Symptoms:**
```
Error: Permission denied while trying to open '.env'
```

**Solution:**

```bash
# Check current permissions
ls -la .env

# Make it readable/writable
chmod 600 .env

# Verify
ls -la .env
# Should show: -rw------- (or similar with write permissions)
```

---

### "Cannot execute docker compose"

**Symptoms:**
```
Error: docker-compose: command not found
Or: docker: 'compose' is not a command
```

**Solution:**

1. **Check Docker Compose is installed**:
   ```bash
   docker compose version
   # Modern: should work
   # Old: try `docker-compose` instead
   ```

2. **Install Docker Compose** (if needed):
   - Usually comes with Docker Desktop
   - For Linux: https://docs.docker.com/compose/install/

---

### "Cannot read docker-compose.yml"

**Symptoms:**
```
Error: Cannot locate docker-compose.yml
```

**Solution:**

```bash
# Verify you're in the correct directory
pwd
# Should show: /path/to/Dify-Creator

# Check file exists
ls docker-compose.yml
# Should exist in current directory
```

---

## Platform-specific issues

### macOS issues

**Docker Desktop not starting**:
```bash
# Try restarting
pkill Docker
open /Applications/Docker.app

# Check logs
cat ~/Library/Containers/com.docker.docker/data/log/vm/docker.log
```

**Permission issues**:
```bash
# May need sudo
sudo docker compose run --rm dify-creator login

# Or fix permissions
sudo chown -R $(whoami) .
```

---

### Windows issues

**Docker Desktop won't start**:
1. Check if Hyper-V is enabled
2. Check if WSL 2 is installed
3. Restart Docker Desktop from Settings

**Path issues**:
- Use forward slashes in paths: `C:/Users/Name/project`
- Not backslashes: `C:\Users\Name\project`

**Terminal issues**:
- Use PowerShell, not Command Prompt
- Or use Windows Terminal (preferred)

---

### Linux issues

**Docker daemon permissions**:
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply group changes
newgrp docker

# Verify
docker ps
# Should work without sudo now
```

**Firewall issues**:
```bash
# Allow Docker
sudo ufw allow 5001
# (if using ufw)
```

---

## Verification checklist

Before declaring setup complete, verify:

```
✅ Docker is installed and running
   docker --version

✅ Docker Compose is available
   docker compose version

✅ .env file exists and has credentials
   cat .env | grep DIFY

✅ Connection test passes
   docker compose run --rm dify-creator login

✅ Sample template validates
   docker compose run --rm dify-creator validate --dsl examples/templates/1_simple_chatbot.dsl.yml

✅ .env is not in git
   git status | grep .env
   (should show nothing)
```

---

## Getting help

If you're still stuck:

1. **Collect diagnostic information**:
   ```bash
   # System info
   uname -a                    # Mac/Linux
   systeminfo                  # Windows

   # Docker info
   docker --version
   docker compose version
   docker ps

   # Setup info
   cat .env | grep -v PASSWORD
   docker compose run --rm dify-creator login
   ```

2. **Save the output**:
   ```bash
   # Redirect to file for easier sharing
   docker compose run --rm dify-creator login 2>&1 | tee setup-error.log
   cat setup-error.log
   ```

3. **Share with Claude**:
   - Describe what you're trying to do
   - Include the error message
   - Include system information
   - Include setup steps you took

---

## Quick fix checklist

**"It's not working, what do I do?"**

Try these in order:

1. ✅ **Restart Docker**: Close Docker Desktop / `sudo systemctl restart docker`
2. ✅ **Update .env**: Verify credentials are correct
3. ✅ **Clean rebuild**: `docker compose build --no-cache`
4. ✅ **Check connection**: `ping cloud.dify.ai` (or your server)
5. ✅ **Check disk space**: `df -h /` (need 5GB free)
6. ✅ **Remove old containers**: `docker compose down` then `docker compose up`

If still stuck → collect diagnostics and ask Claude for help.
