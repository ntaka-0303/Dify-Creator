# Dify App Templates

This guide helps you choose and understand the 5 available DSL templates for different app types.

## Contents
- Template overview and selection guide
- When to use each template
- Template structure and key sections
- Customization guidance
- Real-world use cases

---

## Quick selection guide

| Template | App Type | Use Cases | Best for |
|----------|----------|-----------|----------|
| **1_simple_chatbot** | Q&A Chat | Support bot, FAQ answering, conversational AI | Beginners, simple interactions |
| **2_echo_workflow** | Workflow | Text echo, simple pass-through | Learning, minimal processing |
| **3_llm_workflow** | Workflow + LLM | Text analysis, summarization, transformation | Standard multi-step operations |
| **4_conditional_workflow** | Branching logic | Routing, decision trees, conditional outputs | Complex decision-making |
| **5_http_api_workflow** | API integration | External data fetching, service calls | Third-party integrations |

---

## Template 1: Simple Chatbot (`1_simple_chatbot.dsl.yml`)

### What it does
A straightforward Q&A chatbot powered by Claude. Users ask questions, the AI responds conversationally.

### Best for
- Customer support chatbots
- FAQ answering services
- General knowledge Q&A
- First-time Dify users

### Key characteristics
- **Mode:** `chat` (conversational)
- **Model:** Claude (latest version)
- **Input:** User message
- **Output:** AI response
- **Complexity:** ⭐ Low
- **Number of steps:** 1 (single LLM call)

### Structure overview

```yaml
version: "0.5.0"
kind: app
metadata:
  name: "Your App Name"
  description: "Your description"
app:
  mode: "chat"
  name: "Your App Name"
model_config:
  opening_statement: "Initial greeting message"
  system_prompt: "Instructions for the AI (tone, behavior, constraints)"
  model:
    provider: "anthropic"
    name: "claude-3-5-sonnet-20241022"
    temperature: 0.7
    max_tokens: 2048
```

### Customization tips

**To change the tone:**
```yaml
system_prompt: |
  You are a professional customer support agent.
  Be formal, concise, and solution-focused.
  Always offer next steps.
```

**To add context or knowledge:**
```yaml
system_prompt: |
  You are a support agent for an e-commerce platform.
  Our policies: [list key policies]
  Common issues and solutions: [document issues]
```

**To set response limits:**
```yaml
model:
  max_tokens: 512  # Shorter responses
  temperature: 0.3 # More deterministic
```

### Variables (if needed)

For dynamic behavior, add prompt variables:
```yaml
prompt_variables:
  - variable_name: "customer_tier"
    type: "string"
  - variable_name: "language_preference"
    type: "string"
```

Then reference in system_prompt: `{customer_tier}`, `{language_preference}`

---

## Template 2: Echo Workflow (`2_echo_workflow.dsl.yml`)

### What it does
A minimal workflow that echoes input text back. Useful for understanding workflow structure.

### Best for
- Learning Dify workflow basics
- Testing the connection
- Template for very simple pass-through operations
- Sanity checks

### Key characteristics
- **Mode:** `workflow` (process-based)
- **Steps:** 1 (echo/passthrough)
- **Input:** Text
- **Output:** Same text (echoed)
- **Complexity:** ⭐ Very Low
- **Use case:** Not recommended for production use; primarily educational

### Structure overview

```yaml
version: "0.5.0"
kind: app
app:
  mode: "workflow"
  name: "Echo Workflow"
workflow:
  nodes:
    - id: "echo_node"
      type: "echo"
      input: "${start.input_text}"
      output:
        result: "${echo_node.output}"
```

### When to use in practice
- Verify Dify connection is working
- Test app deployment mechanism
- Baseline for more complex workflows

---

## Template 3: LLM Workflow (`3_llm_workflow.dsl.yml`)

### What it does
A multi-step workflow combining data input, processing, and LLM analysis. The standard choice for most applications.

### Best for
- Text summarization
- Content analysis and classification
- Data transformation and enrichment
- Most production applications

### Key characteristics
- **Mode:** `workflow` (process-based)
- **Steps:** 2-4 (typically: input → process → LLM → output)
- **Flexibility:** High—easy to add/remove steps
- **Complexity:** ⭐⭐ Medium
- **LLM integration:** Full control

### Structure overview

```yaml
version: "0.5.0"
kind: app
app:
  mode: "workflow"
  name: "LLM Workflow"
workflow:
  nodes:
    - id: "start"
      type: "start"
      data:
        - key: "input_text"
          type: "string"

    - id: "llm_node"
      type: "llm"
      model:
        provider: "anthropic"
        name: "claude-3-5-sonnet-20241022"
        system_prompt: "Your instructions"
      input:
        text: "${start.input_text}"

    - id: "output"
      type: "end"
      output:
        result: "${llm_node.output}"
```

### Customization examples

**Example 1: Text Summarizer**
```yaml
llm_node:
  system_prompt: |
    You are a text summarizer.
    Summarize the provided text in 3-5 bullet points.
    Focus on key insights and actionable points.
  input:
    text: "${start.article_text}"
```

**Example 2: Sentiment Analyzer**
```yaml
llm_node:
  system_prompt: |
    Analyze the sentiment of the provided customer feedback.
    Respond with: sentiment (positive/negative/neutral) and 2 supporting details.
  input:
    feedback: "${start.customer_feedback}"
```

**Example 3: Code Reviewer**
```yaml
llm_node:
  system_prompt: |
    You are a code reviewer. Review the provided code for:
    - Correctness and logic errors
    - Performance issues
    - Security vulnerabilities
    - Best practices
  input:
    code: "${start.code_snippet}"
```

### Adding multiple steps

Extend the workflow by chaining LLM nodes:

```yaml
workflow:
  nodes:
    - id: "step1_analyze"
      type: "llm"
      # First analysis...

    - id: "step2_refine"
      type: "llm"
      input:
        previous_result: "${step1_analyze.output}"
      # Refine based on first result...

    - id: "output"
      type: "end"
      output:
        final_result: "${step2_refine.output}"
```

---

## Template 4: Conditional Workflow (`4_conditional_workflow.dsl.yml`)

### What it does
A workflow with branching logic. Sends data down different paths based on conditions.

### Best for
- Routing to different handlers based on content
- Decision trees and categorization
- Complex multi-path processes
- Dynamic response selection

### Key characteristics
- **Mode:** `workflow` (process-based)
- **Steps:** 3+ (includes conditional branching)
- **Branching:** Yes—different paths for different conditions
- **Complexity:** ⭐⭐⭐ Higher
- **Typical structure:** Input → Classify → Branch → Process → Output

### Structure overview

```yaml
workflow:
  nodes:
    - id: "start"
      type: "start"
      data:
        - key: "customer_message"
          type: "string"

    - id: "classifier"
      type: "llm"
      system_prompt: |
        Classify the message into one category:
        - COMPLAINT (refund request, product issue)
        - QUESTION (how to use, feature info)
        - COMPLIMENT (positive feedback)
        Return only the category name.

    - id: "router"
      type: "if"
      condition: "${classifier.output} == 'COMPLAINT'"
      branches:
        - id: "complaint_handler"
          type: "llm"
          system_prompt: "Handle complaints with empathy and solutions"
        - id: "other_handler"
          type: "llm"
          system_prompt: "Handle questions and feedback professionally"

    - id: "output"
      type: "end"
```

### Use case examples

**Example 1: Customer support routing**
```yaml
# Classify → Route to different teams
# COMPLAINT → apology + solution
# QUESTION → helpful answer
# COMPLIMENT → thank you + engagement
```

**Example 2: Content moderation**
```yaml
# Classify → Route based on risk level
# HIGH_RISK → human review
# MEDIUM_RISK → filter + allow
# LOW_RISK → approve immediately
```

**Example 3: Dynamic response selection**
```yaml
# Analyze input → Select response template
# FORMAL_TONE → professional response
# CASUAL_TONE → friendly response
# URGENT → expedited handling
```

### Conditional node syntax

```yaml
- id: "router"
  type: "if"
  condition: "${classifier.output.contains('urgent')}"
  branches:
    - id: "urgent_path"
      # nodes for urgent handling...
    - id: "standard_path"
      # nodes for normal handling...
```

---

## Template 5: HTTP API Workflow (`5_http_api_workflow.dsl.yml`)

### What it does
A workflow that fetches data from external APIs and processes it.

### Best for
- Real-time data fetching (weather, news, prices)
- Third-party service integration
- Database queries via API
- External enrichment

### Key characteristics
- **Mode:** `workflow` (process-based)
- **Steps:** 3+ (includes API call)
- **External calls:** Yes—HTTP requests to external services
- **Complexity:** ⭐⭐⭐ Higher
- **Typical structure:** Input → Prepare request → API call → Process → Output

### Structure overview

```yaml
workflow:
  nodes:
    - id: "start"
      type: "start"
      data:
        - key: "search_query"
          type: "string"

    - id: "api_call"
      type: "http_request"
      method: "GET"
      url: "https://api.example.com/search"
      params:
        q: "${start.search_query}"
        limit: "10"
      headers:
        Authorization: "Bearer YOUR_API_KEY"

    - id: "process_results"
      type: "llm"
      system_prompt: "Summarize and format the API results"
      input:
        api_data: "${api_call.output}"

    - id: "output"
      type: "end"
      output:
        result: "${process_results.output}"
```

### Use case examples

**Example 1: Weather Bot**
```yaml
# Get city from user → Call weather API → Format result
# Input: city_name
# API: weather service
# Output: "Today in [city]: [temp], [condition]"
```

**Example 2: Stock Price Checker**
```yaml
# Get symbol from user → Call financial API → Analyze trend
# Input: stock_symbol
# API: financial data provider
# Output: "Current price, change, 1-year performance"
```

**Example 3: Documentation Lookup**
```yaml
# Get question from user → Search docs API → Answer using search results
# Input: technical_question
# API: documentation search service
# Output: relevant docs + Claude's explanation
```

### API configuration

```yaml
- id: "api_call"
  type: "http_request"
  method: "POST"
  url: "https://api.example.com/endpoint"
  headers:
    Content-Type: "application/json"
    Authorization: "Bearer ${env.API_KEY}"
  body:
    query: "${start.user_input}"
    filters:
      limit: 20
      sort: "relevance"
```

### Error handling patterns

```yaml
- id: "api_call"
  type: "http_request"
  # ... api configuration ...
  on_error:
    - id: "error_handler"
      type: "llm"
      system_prompt: "Politely explain that data fetch failed, offer alternatives"
```

---

## Template selection decision tree

```
START: "I want to build a Dify app"
  │
  ├─ "Is it just Q&A conversation?"
  │  └─ YES → Use Template 1: Simple Chatbot
  │
  ├─ "Does it involve multiple processing steps?"
  │  ├─ YES (with branching?)
  │  │  ├─ YES → Use Template 4: Conditional Workflow
  │  │  └─ NO → Use Template 3: LLM Workflow
  │  └─ NO (testing/learning?)
  │     └─ Use Template 2: Echo Workflow
  │
  └─ "Does it call external APIs or services?"
     └─ YES → Use Template 5: HTTP API Workflow
```

---

## Customization workflow

### General process for all templates

1. **Copy the base template** to your project as `app.dsl.yml`
2. **Update metadata** (name, description, icon)
3. **Customize model configuration** (system_prompt, temperature, max_tokens)
4. **Define input/output schemas** (what users provide, what they get back)
5. **Add prompt variables** if your app needs dynamic behavior
6. **Validate** with `docker compose run --rm dify-creator validate --dsl app.dsl.yml`
7. **Test** with representative inputs
8. **Iterate** based on results

### Common customization patterns

**Pattern 1: Change the system prompt**
```yaml
system_prompt: |
  Your custom instructions here.
  Define the AI's role, constraints, and output format.
```

**Pattern 2: Add input variables**
```yaml
prompt_variables:
  - variable_name: "user_tier"
  - variable_name: "language"
```

Then use in prompts: `"Respond in {language} for {user_tier} users"`

**Pattern 3: Chain multiple LLM calls**
```yaml
nodes:
  - id: "step1"
    type: "llm"
    # First operation...
  - id: "step2"
    type: "llm"
    input:
      context: "${step1.output}"
    # Refine based on step1...
```

---

## Best practices for templates

✅ **DO:**
- Start with the closest matching template
- Keep prompts clear and specific
- Test with diverse inputs
- Document what each step does
- Validate after every change
- Use meaningful node IDs

❌ **DON'T:**
- Try to bend a template beyond its design (start over with a better template)
- Leave generic prompts unchanged
- Add unnecessary complexity upfront
- Assume template will work without testing
- Ignore validation errors
- Make multiple unrelated changes at once

---

## Next steps

1. **Choose your template** from the guide above
2. **View the template file** at `examples/templates/`
3. **Customize** for your specific needs
4. **Validate** the configuration
5. **Test** with real inputs
6. **Deploy** and iterate based on results

See [workflows.md](workflows.md) for the complete app creation and iteration workflows.
