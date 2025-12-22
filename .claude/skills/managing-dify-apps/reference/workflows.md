# Detailed Workflows

## Contents
- Creating new apps
- Editing existing apps
- Validation and testing
- Iteration loops
- Troubleshooting patterns

---

## Creating a new Dify app

Use this workflow when you want to create a brand new application.

### Step-by-step workflow

**Copy and track your progress:**

```
Creating New App:
- [ ] Step 1: Gather app requirements
- [ ] Step 2: Choose app type
- [ ] Step 3: Select appropriate template
- [ ] Step 4: Generate initial YAML
- [ ] Step 5: Validate configuration
- [ ] Step 6: Register with Dify
- [ ] Step 7: Run test execution
- [ ] Step 8: Review results
- [ ] Step 9: Iterate or finalize
```

### Step 1: Gather app requirements

Provide a detailed description of what you want to build:

**Good examples:**
- "A customer support chatbot that answers frequently asked questions from our knowledge base with a helpful tone"
- "A workflow that analyzes customer sentiment from text and routes responses based on emotion (positive, neutral, negative)"
- "An API connector that fetches weather data and summarizes it for end users"

**Important details to include:**
- What is the main purpose?
- What will users input?
- What should the output look like?
- Are there any special requirements? (tone, format, integrations)

### Step 2: Choose app type

Select one based on your requirements. See [templates.md](templates.md) for detailed examples.

| Type | Best for | Complexity |
|------|----------|-----------|
| **Q&A Chatbot** | Simple question-answer pairs, customer support | ⭐ Low |
| **Workflow** | Multi-step processing, data transformation | ⭐⭐ Medium |
| **Conditional Logic** | Decision trees, dynamic routing | ⭐⭐⭐ Higher |
| **API Integration** | External service calls, data fetching | ⭐⭐⭐ Higher |

### Step 3: Select appropriate template

Claude will help choose from 5 templates:
- `1_simple_chatbot.dsl.yml` → Q&A
- `2_echo_workflow.dsl.yml` → Simple workflow
- `3_llm_workflow.dsl.yml` → Standard workflow
- `4_conditional_workflow.dsl.yml` → Complex logic
- `5_http_api_workflow.dsl.yml` → API integration

See [templates.md](templates.md) for full details.

### Step 4: Generate initial YAML

Claude generates a customized `app.dsl.yml` based on your requirements:
- Sets app name and description
- Configures input/output schemas
- Creates prompts and instructions
- Defines workflow steps (if applicable)

### Step 5: Validate configuration

Run validation to catch errors early:

```bash
docker compose run --rm dify-creator validate --dsl app.dsl.yml
```

**Expected output on success:**
```
✅ Validation successful: DSL is structurally valid
```

**On errors:**
- Fix the reported issues
- Revalidate until successful

See [troubleshooting.md](troubleshooting.md) for common errors.

### Step 6: Register with Dify

Upload the validated configuration to create the app:

```bash
docker compose run --rm dify-creator import --dsl app.dsl.yml
```

This returns an `app_id` that you'll use for future edits. **Save this ID.**

### Step 7: Run test execution

Execute the app with sample inputs to verify it works:

```bash
docker compose run --rm dify-creator sync \
  --dsl app.dsl.yml \
  --app-id <returned_app_id> \
  --inputs-json examples/inputs.json
```

Results are saved to `artifacts/run_result.json`.

### Step 8: Review results

Examine the test output:
- Did it produce the expected format?
- Are responses appropriate for your use case?
- Are there any errors or unexpected behavior?

### Step 9: Iterate or finalize

**If results are good:** ✅ App is ready to use or publish via Dify web UI

**If results need improvement:** → Use the "Editing" workflow below

---

## Editing an existing Dify app

Use this workflow when you need to modify a running app.

### Step-by-step workflow

**Copy and track your progress:**

```
Editing Existing App:
- [ ] Step 1: Get app ID from Dify
- [ ] Step 2: Describe desired changes
- [ ] Step 3: Download current configuration
- [ ] Step 4: Apply modifications
- [ ] Step 5: Preview changes (for approval)
- [ ] Step 6: Validate configuration
- [ ] Step 7: Upload to Dify
- [ ] Step 8: Execute tests
- [ ] Step 9: Review and iterate
```

### Step 1: Get app ID

From Dify web UI, find your app's ID in the URL:

```
https://cloud.dify.ai/app/abc123def456/overview
                         ^^^^^^^^^^^^^^
                          This is your app_id
```

### Step 2: Describe changes

Provide clear descriptions of what to modify. Examples:

**Good descriptions:**
- "Make the prompt more professional and formal"
- "Add a new workflow step to summarize the response"
- "Change the input field name from 'question' to 'customer_query'"
- "Add conditional branching for different user types"

**Vague descriptions (avoid):**
- "Make it better"
- "Fix it"
- "Change the prompt"

### Step 3: Download current configuration

Claude downloads the app's current configuration from Dify:

```bash
docker compose run --rm dify-creator export \
  --app-id <your_app_id> \
  --out app.dsl.yml
```

This creates a local copy of what's currently running.

### Step 4: Apply modifications

Claude modifies the configuration based on your description:
- Edits prompts and instructions
- Adds or removes workflow steps
- Changes variables and schemas
- Updates conditional logic
- Modifies API endpoints (if applicable)

### Step 5: Preview changes (for approval)

**Claude shows you a summary:**
- What specifically is changing?
- Lines added/removed?
- Variable modifications?

**Review and approve** before proceeding.

### Step 6: Validate configuration

Verify the modified YAML is syntactically correct:

```bash
docker compose run --rm dify-creator validate --dsl app.dsl.yml
```

If validation fails, Claude automatically fixes the issues and re-validates.

### Step 7: Upload to Dify

Apply the modifications to your live app:

```bash
docker compose run --rm dify-creator import \
  --dsl app.dsl.yml \
  --app-id <your_app_id>
```

Changes are now in "draft" state (not publicly visible until you publish).

### Step 8: Execute tests

Test the modified app with sample inputs:

```bash
docker compose run --rm dify-creator sync \
  --dsl app.dsl.yml \
  --app-id <your_app_id> \
  --inputs-json examples/inputs.json
```

### Step 9: Review and iterate

**Results look good?** ✅
- Modifications are complete
- Publish via Dify web UI when ready

**Need more adjustments?** 🔄
- Describe what's different or missing
- Claude automatically iterates: modify → validate → test
- Repeat until satisfied

The validation feedback loop ensures each iteration is error-free and properly tested.

---

## Validation workflow

Use this workflow to validate your configuration at any time.

```
Validation Checklist:
- [ ] YAML syntax is correct
- [ ] Required fields present
- [ ] App mode is valid (workflow/chat/agent)
- [ ] Node definitions are properly structured
- [ ] Variable names are consistent
- [ ] Prompts are clear and actionable
```

**Run validation:**

```bash
docker compose run --rm dify-creator validate --dsl app.dsl.yml
```

**If errors occur:**
1. Read the error message carefully (it points to the specific problem)
2. Fix the issue in `app.dsl.yml`
3. Revalidate immediately
4. Only proceed when validation passes

---

## Test execution workflow

```
Testing Workflow:
- [ ] Step 1: Prepare test inputs
- [ ] Step 2: Run test execution
- [ ] Step 3: Check artifacts/run_result.json
- [ ] Step 4: Compare against expectations
- [ ] Step 5: Iterate or finalize
```

**Run tests:**

```bash
docker compose run --rm dify-creator sync \
  --dsl app.dsl.yml \
  --app-id <app_id> \
  --inputs-json examples/inputs.json \
  --out-dir artifacts
```

**Examine results:**
- `artifacts/run_result.json` contains the app's output
- Compare against what you expected
- If output format or content doesn't match, iterate via editing workflow

---

## Iteration patterns

### Pattern 1: Quick iterations (modify → test → review)

```
1. Make a small focused change (e.g., adjust prompt tone)
2. Validate and test immediately
3. Review results quickly
4. Keep iterating until satisfied
```

**Recommended for:** Prompt tuning, variable changes, small fixes

### Pattern 2: Structured iterations (gather → plan → implement → test)

```
1. Collect all desired changes
2. Plan the approach (which template? which steps?)
3. Implement in batches
4. Test thoroughly at each milestone
```

**Recommended for:** Major restructuring, complex workflows, architecture changes

### Pattern 3: Validation-driven development (validate early and often)

```
1. Make a change
2. IMMEDIATELY validate (don't wait)
3. Fix any issues before proceeding
4. Test only after validation passes
```

**Best practice:** This catches errors early and saves debugging time.

---

## Common iteration scenarios

### Scenario: "The output format is wrong"

**What to do:**
1. Describe the issue: "Responses should be in bullet-point format, not paragraphs"
2. Claude modifies the prompt to enforce the format
3. Test again with same inputs
4. Verify output matches expected format

### Scenario: "The app is too slow"

**What to do:**
1. Check if workflow has unnecessary steps
2. Simplify the process if possible
3. Consider if API calls are needed
4. Test performance with typical inputs

### Scenario: "Some inputs cause errors"

**What to do:**
1. Test with problematic inputs
2. Add error handling in the workflow (if applicable)
3. Improve input validation rules
4. Test with edge cases

### Scenario: "I need to add a new feature"

**What to do:**
1. Start with the current app (use editing workflow)
2. Add the new feature as a workflow step
3. Validate the new structure
4. Test the combined functionality
5. Iterate until it works smoothly

---

## Best practices

✅ **DO:**
- Test after every meaningful change
- Read error messages carefully—they're usually clear
- Validate before uploading to Dify
- Use checklists to track progress
- Ask for clarification if instructions are unclear
- Break complex changes into smaller iterations

❌ **DON'T:**
- Skip validation even if you're confident
- Make multiple unrelated changes at once (makes debugging harder)
- Upload to Dify without testing first
- Ignore error messages—fix the root cause
- Try to fix everything in one iteration
- Assume the app works without testing edge cases
