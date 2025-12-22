---
name: managing-dify-apps
description: Create, edit, validate, and deploy Dify AI applications. Use when creating new Dify apps, modifying existing apps, testing configurations, or syncing changes. Handles app creation workflows, YAML configuration edits, validation, and test execution.
---

# Managing Dify Apps

Create and manage Dify AI applications efficiently without opening the Dify Studio UI. This Skill handles the complete app lifecycle: creation, modification, validation, and deployment.

## What this Skill does

- **Create new apps**: Generate Dify apps from natural language descriptions
- **Edit existing apps**: Modify prompts, workflows, variables, and logic
- **Validate configurations**: Check DSL syntax and structure before deployment
- **Test and deploy**: Execute test runs and sync changes to Dify
- **Manage iterations**: Support iterative refinement with validation feedback loops

## Quick start

### Creating a new app

1. Describe what you want: "I need a chatbot that answers customer questions"
2. Specify the app type: Q&A chatbot, workflow, conditional logic, or API integration
3. Claude handles the rest: generates YAML → validates → uploads → tests

### Editing an existing app

1. Provide the app ID and describe changes: "Make the prompt more polite"
2. Claude: downloads current config → modifies → validates → tests
3. Review results and iterate until satisfied

### Testing and validation

Run validation at any time to catch configuration errors before deployment.

## Core workflows

See [reference/workflows.md](reference/workflows.md) for detailed step-by-step workflows including:
- Creating new apps with different types
- Editing and iterating on existing apps
- Validation and error handling
- Troubleshooting common issues

## Key resources

**For templates and examples**:
See [reference/templates.md](reference/templates.md) for:
- All 5 available DSL templates
- When to use each template
- Template structure and customization

**For DSL configuration**:
See [reference/dsl-guide.md](reference/dsl-guide.md) for:
- DSL YAML structure overview
- Required fields and sections
- Common configuration patterns

**For troubleshooting**:
See [reference/troubleshooting.md](reference/troubleshooting.md) for:
- Common errors and solutions
- Connection issues
- Validation failures
- Test execution problems

## Validation and feedback loops

This Skill uses validation feedback loops to ensure quality:

1. **Create or modify** your app configuration
2. **Validate** the YAML syntax and structure
3. **Preview** proposed changes before applying
4. **Test** the app with sample inputs
5. **Iterate** if results don't match expectations

Error messages point to specific problems, making it easy to fix issues.

## Supported app types

- **Q&A Chatbot**: Simple question-answer interactions
- **Workflow**: Multi-step process flows
- **Conditional Logic**: Decision trees and branching logic
- **API Integration**: Connect to external services

See [reference/templates.md](reference/templates.md) for detailed examples of each type.

## Prerequisites

- Dify account and credentials (email/password)
- Dify project already set up (see `setting-up-dify-project` Skill)
- Basic understanding of your app's purpose and inputs/outputs

For initial setup, use the `setting-up-dify-project` Skill first.
