# DSL Configuration Guide

Quick reference for Dify DSL (Domain Specific Language) configuration structure.

## Overview

Dify apps are defined in YAML format (DSL version 0.5.0). Each app requires:
- **Basic metadata**: name, description, icon
- **Mode selection**: chat, workflow, or agent
- **Configuration**: model settings (chat) or workflow nodes (workflow)

For complete technical details, see [DSL_SPECIFICATION.md](../../docs/DSL_SPECIFICATION.md).

---

## Basic structure

Every Dify app follows this structure:

```yaml
version: "0.5.0"
kind: app

metadata:
  name: "Your App Name"
  description: "What it does"
  icon: "🤖"
  icon_background: "#f0f0f0"

app:
  name: "Your App Name"
  mode: "chat"  # or "workflow" or "agent"
  description: "What it does"
  icon: "🤖"
  icon_background: "#f0f0f0"

# Then either model_config (for chat) OR workflow (for workflow)
model_config:
  # Chat mode configuration...
  opening_statement: "Hi, how can I help?"
  system_prompt: "You are helpful..."

# OR

workflow:
  # Workflow mode configuration...
  nodes:
    - id: "node_id"
      type: "llm"
      # ...
```

---

## Mode selection

### Chat mode
```yaml
app:
  mode: "chat"
model_config:
  opening_statement: "Initial greeting"
  system_prompt: "Instructions for Claude"
  model:
    provider: "anthropic"
    name: "claude-3-5-sonnet-20241022"
    temperature: 0.7
    max_tokens: 2048
```

**Use for:** Q&A, conversational interaction

### Workflow mode
```yaml
app:
  mode: "workflow"
workflow:
  nodes:
    - id: "start"
      type: "start"
    - id: "llm_step"
      type: "llm"
      # ...
    - id: "end"
      type: "end"
```

**Use for:** Multi-step processes, complex logic, API integration

### Agent mode
```yaml
app:
  mode: "agent"
model_config:
  # Similar to chat, but with agent-specific configuration
```

**Use for:** Autonomous agents with tool use

---

## Common configuration patterns

### Chat app with variables

```yaml
model_config:
  system_prompt: |
    You are a support agent for {company_name}.
    Current user tier: {user_tier}
    Respond appropriately for their tier.

  prompt_variables:
    - variable_name: "company_name"
      type: "string"
    - variable_name: "user_tier"
      type: "string"

  model:
    provider: "anthropic"
    name: "claude-3-5-sonnet-20241022"
    temperature: 0.7
```

### Workflow with multiple steps

```yaml
workflow:
  variable_pool:
    - variable_name: "input_text"
      type: "string"
      description: "User input"

  nodes:
    - id: "start"
      type: "start"
      data:
        - key: "input_text"
          type: "string"

    - id: "analyze"
      type: "llm"
      data:
        system_prompt: "Analyze this text..."
        input_mapping:
          text: "${start.input_text}"

    - id: "output"
      type: "end"
      output_mapping:
        result: "${analyze.output}"
```

### Workflow with conditional branching

```yaml
nodes:
  - id: "classifier"
    type: "llm"
    data:
      system_prompt: "Classify: complaint or question?"

  - id: "branch"
    type: "if"
    data:
      condition: "${classifier.output.contains('complaint')}"

  - id: "complaint_handler"
    type: "llm"
    parent_node: "branch"
    data:
      system_prompt: "Handle complaint..."

  - id: "output"
    type: "end"
```

---

## Key sections reference

### `metadata` section
```yaml
metadata:
  name: "Display Name"
  description: "Human-readable description"
  icon: "emoji or URL"
  icon_background: "#hexcolor"
```

### `model_config` section (Chat/Agent modes)
```yaml
model_config:
  opening_statement: "Initial greeting message"
  system_prompt: "Instructions for the model"

  model:
    provider: "anthropic"
    name: "claude-3-5-sonnet-20241022"
    temperature: 0.7          # 0.0 = deterministic, 1.0 = creative
    max_tokens: 2048          # Max output length

  prompt_variables: []        # Variables for dynamic prompts
  tools: []                   # Tools/plugins (if any)
  knowledge_bases: []         # Knowledge bases (if any)
```

### `workflow` section (Workflow mode)
```yaml
workflow:
  variable_pool:              # Global variables
    - variable_name: "name"
      type: "string"

  nodes:                      # Workflow steps
    - id: "unique_id"
      type: "llm|if|http_request|etc"
      title: "Step Name"
      data:
        # Type-specific configuration
```

### Node types in workflows

| Type | Purpose | Key fields |
|------|---------|-----------|
| `start` | Workflow entry point | `data: [input definitions]` |
| `llm` | Call language model | `system_prompt`, `model`, `input_mapping` |
| `if` | Conditional branching | `condition`, branches |
| `http_request` | Call external API | `method`, `url`, `headers`, `body` |
| `text_processing` | Manipulate text | `operation`, `input_mapping` |
| `code` | Execute code | `language`, `code`, `input_mapping` |
| `end` | Workflow output | `output_mapping` |

---

## Model configuration details

### Temperature settings

```yaml
model:
  temperature: 0.7
```

| Value | Behavior | Best for |
|-------|----------|----------|
| 0.0 | Deterministic, consistent | Q&A, fact-based responses |
| 0.3-0.5 | Focused with some variety | Customer support, structured output |
| 0.7 | Balanced (default) | General conversational use |
| 0.9-1.0 | Creative, diverse | Creative writing, brainstorming |

### Max tokens

```yaml
model:
  max_tokens: 2048
```

**Guidelines:**
- Customer support: 512-1024
- Analysis/Summary: 1024-2048
- Creative content: 2048-4096

### Prompt variables

```yaml
prompt_variables:
  - variable_name: "customer_tier"
    type: "string"
  - variable_name: "request_count"
    type: "number"
```

Usage in prompts:
```yaml
system_prompt: |
  Customer tier: {customer_tier}
  Requests handled: {request_count}
  Adjust service level accordingly.
```

---

## Input/Output schemas

### Define inputs (Chat mode)

```yaml
model_config:
  input_variables:
    - variable_name: "question"
      type: "string"
      description: "Customer question"

  output:
    - variable_name: "response"
      type: "string"
      description: "AI response"
```

### Define inputs (Workflow mode)

```yaml
workflow:
  variable_pool:
    - variable_name: "document_text"
      type: "string"
      description: "Document to analyze"

  nodes:
    - id: "start"
      data:
        - key: "document_text"
          type: "string"
```

---

## Validation checklist

Before deploying, verify:

```
✅ version is "0.5.0"
✅ kind is "app"
✅ metadata.name is set
✅ app.mode is valid (chat/workflow/agent)
✅ app.name matches metadata.name
✅ model_config exists (for chat/agent mode)
✅ workflow exists (for workflow mode)
✅ All node IDs are unique
✅ All variable references are valid
✅ system_prompt is clear and specific
✅ YAML syntax is valid (no indentation errors)
```

Run validation:
```bash
docker compose run --rm dify-creator validate --dsl app.dsl.yml
```

---

## Common errors and fixes

### Error: Required field missing

```
Error: Required field 'workflow' not found
```

**Fix:** Check your `app.mode`. If it's "workflow", you must have a `workflow` section.

### Error: Invalid mode

```
Error: 'app.mode' must be one of: workflow, chat, agent
```

**Fix:** Check spelling—mode values are lowercase only.

### Error: Node not found

```
Error: Reference to undefined node 'process_step'
```

**Fix:** Check node ID spelling in references. They're case-sensitive.

### Error: Syntax error in YAML

```
Error: Unexpected indent at line 42
```

**Fix:** YAML indentation must be consistent (usually 2 spaces). Check alignment.

---

## For more information

- [Full DSL Specification](../../docs/DSL_SPECIFICATION.md)
- [Template Examples](templates.md)
- [Workflow Guide](workflows.md)
- [Dify Official Documentation](https://docs.dify.ai/)

For most users, the templates in [templates.md](templates.md) provide all necessary structure. Copy a template and customize—no need to build from scratch.
