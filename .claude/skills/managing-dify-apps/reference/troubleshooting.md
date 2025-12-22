# Troubleshooting Guide

Common issues and solutions when using the Dify app management tools.

## Contents
- Connection and authentication issues
- Validation errors
- Test execution problems
- Workflow errors
- Model configuration issues
- Best practices to prevent problems

---

## Connection and authentication issues

### "Connection refused" or "Could not connect to Dify"

**Symptoms:**
```
Error: Could not connect to https://cloud.dify.ai
Connection refused
```

**Solutions:**

1. **Check internet connection**
   ```bash
   ping cloud.dify.ai
   ```

2. **Verify Dify credentials** in `.env`:
   ```bash
   cat .env | grep DIFY
   ```

3. **Test login manually** (for local Dify instances):
   ```bash
   docker compose run --rm dify-creator login
   ```

4. **Check URL format**:
   - Cloud: `https://cloud.dify.ai` ✅
   - Local: `http://localhost:5001` (no HTTPS) ✅
   - Custom: Ensure URL is complete and accessible

5. **For self-hosted Dify with SSL issues**:
   - If using self-signed certificates, update `.env`:
     ```
     DIFY_VERIFY_SSL=false
     ```

---

### "Invalid credentials" or "Authentication failed"

**Symptoms:**
```
Error: Invalid email or password
```

**Solutions:**

1. **Verify credentials are correct**:
   - Are you using the Dify account email? (not API key)
   - Is the password correct?
   - Has the password been changed recently?

2. **Update `.env` with correct credentials**:
   ```bash
   # Edit .env
   DIFY_EMAIL=your-actual-email@example.com
   DIFY_PASSWORD=your-actual-password
   ```

3. **Re-run setup**:
   ```bash
   /dify-setup
   ```

4. **Test connection**:
   ```bash
   docker compose run --rm dify-creator login
   ```

---

## Validation errors

### "Validation failed: Required field not found"

**Symptoms:**
```
❌ Validation failed (2 errors):
  - Required field 'workflow' not found
  - 'app.mode' is invalid
```

**Cause:** YAML structure is incomplete or has wrong mode.

**Solutions:**

1. **Check app.mode matches your configuration**:
   ```yaml
   app:
     mode: "chat"      # or "workflow" or "agent"
   ```

2. **Ensure required sections exist**:
   - For `mode: chat` → need `model_config` section
   - For `mode: workflow` → need `workflow` section
   - For `mode: agent` → need `model_config` section

3. **Use a template as reference**: See [templates.md](templates.md)

---

### "Invalid field value" or "Type mismatch"

**Symptoms:**
```
Error: 'temperature' must be a number between 0.0 and 1.0
Error: 'max_tokens' must be a positive integer
```

**Solutions:**

1. **Check field types**:
   ```yaml
   # ✅ Correct
   temperature: 0.7          # number
   max_tokens: 2048          # integer
   system_prompt: "text"     # string

   # ❌ Wrong
   temperature: "0.7"        # string (should be number)
   max_tokens: "2048"        # string (should be integer)
   ```

2. **For temperature**: must be between 0.0 and 1.0
3. **For max_tokens**: must be positive integer (typical: 512-4096)

---

### "YAML syntax error"

**Symptoms:**
```
Error: Failed to parse YAML at line 25: unexpected indent
```

**Solutions:**

1. **Check indentation** (YAML is strict):
   ```yaml
   # ✅ Correct - consistent 2-space indentation
   model:
     provider: "anthropic"
     name: "claude-3-5-sonnet-20241022"

   # ❌ Wrong - inconsistent indentation
   model:
    provider: "anthropic"
     name: "claude-3-5-sonnet-20241022"
   ```

2. **No tabs** - use spaces only:
   ```bash
   # Check for tabs
   grep -P '\t' app.dsl.yml
   # (should return nothing)
   ```

3. **Use a YAML validator**:
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('app.dsl.yml'))"
   ```

4. **Common YAML issues**:
   - Missing colons after keys
   - Quotes not properly closed
   - Lists starting with `-` not properly indented

---

## Test execution problems

### "Test returned unexpected format"

**Symptoms:**
```
Test ran successfully but output format is wrong
```

**Solutions:**

1. **Check system_prompt** specifies output format:
   ```yaml
   system_prompt: |
     Return responses in JSON format:
     {
       "answer": "...",
       "confidence": "high|medium|low"
     }
   ```

2. **Test with simple inputs** first:
   - Before complex cases, test with basic input
   - Verify the app understands basic requests

3. **Check prompt_variables** are passed correctly:
   ```yaml
   prompt_variables:
     - variable_name: "output_format"
       type: "string"
   ```

---

### "No output from test" or "Empty response"

**Symptoms:**
```
Test execution completed but result is empty
```

**Solutions:**

1. **Check if API key is valid**:
   ```bash
   docker compose run --rm dify-creator login
   ```

2. **Verify model is available**:
   - Check model name: `claude-3-5-sonnet-20241022` or latest
   - Confirm your account has access to this model

3. **Check input parameters** in `examples/inputs.json`:
   ```json
   {
     "input_text": "your test input here"
   }
   ```

4. **Look at full error log**:
   ```bash
   cat artifacts/run_result.json
   ```

---

### "App timed out during test"

**Symptoms:**
```
Error: Test execution timed out after 30 seconds
```

**Solutions:**

1. **Reduce max_tokens**:
   ```yaml
   model:
     max_tokens: 1024  # reduce from 2048
   ```

2. **Simplify the prompt**:
   - Remove unnecessary instructions
   - Make system_prompt more concise

3. **Check for infinite loops** in workflows:
   - Verify conditional branches have exit conditions
   - No circular node references

4. **For slow API integrations**:
   - Increase timeout in configuration (if available)
   - Test with faster endpoints

---

## Workflow-specific issues

### "Node not found" error

**Symptoms:**
```
Error: Reference to undefined node 'process_step'
```

**Solutions:**

1. **Check node ID spelling** (case-sensitive):
   ```yaml
   nodes:
     - id: "process_step"    # Define first
       type: "llm"

     - id: "next_step"
       input:
         data: "${process_step.output}"  # Correct reference
   ```

2. **Verify all node IDs are unique**:
   ```bash
   grep "id:" app.dsl.yml | sort | uniq -d
   # (should return nothing if all unique)
   ```

---

### "Variable reference is invalid"

**Symptoms:**
```
Error: Undefined variable reference: ${unknown_var.output}
```

**Solutions:**

1. **Check variable pool** defines variables:
   ```yaml
   workflow:
     variable_pool:
       - variable_name: "user_input"
         type: "string"
   ```

2. **Verify node output variables**:
   ```yaml
   nodes:
     - id: "my_step"
       type: "llm"
       # Has output...

   # Later reference:
   input: "${my_step.output}"  # Correct
   ```

3. **Common mistakes**:
   ```yaml
   # ❌ Wrong - undefined node
   value: "${undefined_node.output}"

   # ❌ Wrong - node exists but typo in output
   value: "${my_node.result}"  # Should be .output

   # ✅ Correct
   value: "${my_node.output}"
   ```

---

## Model configuration issues

### "Model not available" or "Quota exceeded"

**Symptoms:**
```
Error: Model claude-3-5-sonnet-20241022 not available
Error: Rate limit exceeded
```

**Solutions:**

1. **Check available models**:
   - Visit Dify console to see which models your account has access to
   - Update `model.name` to an available model

2. **For quota exceeded**:
   - Wait before retrying
   - Reduce `max_tokens` to use fewer resources
   - Check account usage limits

---

### "Responses are inconsistent" or "Quality varies"

**Solutions:**

1. **Lower temperature** for consistency:
   ```yaml
   model:
     temperature: 0.3  # More consistent than 0.7
   ```

2. **Add specific constraints** in system_prompt:
   ```yaml
   system_prompt: |
     Always follow these rules:
     1. Provide exact format: [A], [B], [C]
     2. No extra explanation
     3. If unsure, say "Unknown"
   ```

3. **Use prompt_variables** for dynamic content:
   ```yaml
   prompt_variables:
     - variable_name: "tone"
       type: "string"

   system_prompt: "Respond with {tone} tone: ..."
   ```

---

## Upload issues

### "Upload failed: app_id not found"

**Symptoms:**
```
Error: App with ID 'abc123' not found
```

**Solutions:**

1. **Verify app_id**:
   - From Dify web: `https://cloud.dify.ai/app/YOUR_APP_ID/...`
   - Is it correct?

2. **Check app still exists**:
   - Log into Dify web console
   - Look for the app in your apps list
   - May have been deleted accidentally

3. **Use correct format**:
   - app_id should be alphanumeric
   - No extra spaces or characters

---

### "Upload failed: permission denied"

**Symptoms:**
```
Error: Permission denied. You don't have access to this app.
```

**Solutions:**

1. **Verify you own the app**:
   - Logged in as the correct user?
   - Check Dify console to confirm you own the app

2. **Check account status**:
   - Is your Dify account active?
   - Have you been locked out?

3. **Verify credentials** in `.env` match the account that owns the app

---

## General troubleshooting checklist

**Before reporting issues, verify:**

```
Connection & Auth:
- [ ] Internet connection is working
- [ ] .env has correct credentials
- [ ] Login test passes: docker compose run --rm dify-creator login
- [ ] Using cloud.dify.ai or correct URL for self-hosted

Configuration:
- [ ] YAML validates: docker compose run --rm dify-creator validate --dsl app.dsl.yml
- [ ] Required fields present (version, kind, app, mode)
- [ ] No indentation/syntax errors in YAML
- [ ] All node IDs are unique
- [ ] All variable references exist

Execution:
- [ ] Test inputs in examples/inputs.json are valid
- [ ] Model is available in your account
- [ ] API key/credentials haven't expired
- [ ] No timeout issues (check max_tokens and prompt)
```

---

## Getting more help

**If issues persist:**

1. **Collect diagnostic information**:
   ```bash
   # Show validation errors
   docker compose run --rm dify-creator validate --dsl app.dsl.yml

   # Show test result details
   cat artifacts/run_result.json | python3 -m json.tool
   ```

2. **Review recent changes**:
   - What was changed since last successful run?
   - Can you revert to a working version?

3. **Try a minimal example**:
   - Start with simplest template (Template 1 or 2)
   - Does it work?
   - Gradually add complexity

4. **Ask Claude for help**:
   - Share the error message and relevant YAML section
   - Describe what you're trying to do
   - Include steps to reproduce

---

## Prevention tips

✅ **DO:**
- Validate after every change
- Test with simple inputs first
- Keep prompts concise and clear
- Use templates as starting points
- Commit working versions to git
- Test locally before updating live app

❌ **DON'T:**
- Make multiple changes without validating between them
- Skip validation before uploading
- Copy-paste YAML without checking syntax
- Use inconsistent indentation
- Test only with edge cases first
- Upload without testing locally
