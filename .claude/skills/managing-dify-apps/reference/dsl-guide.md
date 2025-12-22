# DSL 設定ガイド

Dify DSL（ドメイン固有言語）設定構造の簡単なリファレンスです。

## 概要

DifyアプリはYAML形式で定義されます（DSLバージョン 0.5.0）。各アプリは以下を必要とします：
- **基本メタデータ**: name、description、icon
- **モード選択**: chat、workflow、またはagent
- **設定**: モデル設定（chat）またはワークフローノード（workflow）

詳細な技術仕様については、[DSL_SPECIFICATION.md](../../docs/DSL_SPECIFICATION.md)を参照してください。

---

## 基本構造

すべてのDifyアプリは次の構造に従います：

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

## モード選択

### チャットモード
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

**用途：** Q&A、対話型インタラクション

### ワークフローモード
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

**用途：** マルチステップ処理、複雑なロジック、API統合

### エージェントモード
```yaml
app:
  mode: "agent"
model_config:
  # Similar to chat, but with agent-specific configuration
```

**用途：** ツール使用を伴う自律エージェント

---

## 一般的な設定パターン

### 変数付きチャットアプリ

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

### 複数ステップを含むワークフロー

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

### 条件分岐を含むワークフロー

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

## キーセクションリファレンス

### `metadata` セクション
```yaml
metadata:
  name: "Display Name"
  description: "Human-readable description"
  icon: "emoji or URL"
  icon_background: "#hexcolor"
```

### `model_config` セクション（チャット/エージェントモード）
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

### `workflow` セクション（ワークフローモード）
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

### ワークフロー内のノードタイプ

| タイプ | 目的 | キーフィールド |
|------|---------|-----------|
| `start` | ワークフロー入口 | `data: [入力定義]` |
| `llm` | 言語モデルの呼び出し | `system_prompt`、`model`、`input_mapping` |
| `if` | 条件分岐 | `condition`、branches |
| `http_request` | 外部API呼び出し | `method`、`url`、`headers`、`body` |
| `text_processing` | テキスト操作 | `operation`、`input_mapping` |
| `code` | コード実行 | `language`、`code`、`input_mapping` |
| `end` | ワークフロー出力 | `output_mapping` |

---

## モデル設定の詳細

### 温度設定

```yaml
model:
  temperature: 0.7
```

| 値 | 動作 | 適している用途 |
|-------|----------|----------|
| 0.0 | 決定的、一貫性あり | Q&A、事実ベースの回答 |
| 0.3-0.5 | 焦点化されて多少の多様性 | カスタマーサポート、構造化出力 |
| 0.7 | バランス型（デフォルト） | 一般的な対話的使用 |
| 0.9-1.0 | 創造的、多様性あり | クリエイティブライティング、ブレーンストーミング |

### 最大トークン

```yaml
model:
  max_tokens: 2048
```

**ガイドライン：**
- カスタマーサポート：512-1024
- 分析/要約：1024-2048
- クリエイティブコンテンツ：2048-4096

### プロンプト変数

```yaml
prompt_variables:
  - variable_name: "customer_tier"
    type: "string"
  - variable_name: "request_count"
    type: "number"
```

プロンプト内での使用：
```yaml
system_prompt: |
  Customer tier: {customer_tier}
  Requests handled: {request_count}
  Adjust service level accordingly.
```

---

## 入出力スキーマ

### 入力を定義（チャットモード）

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

### 入力を定義（ワークフローモード）

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

## 検証チェックリスト

デプロイ前に確認：

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

検証を実行：
```bash
docker compose run --rm dify-creator validate --dsl app.dsl.yml
```

---

## よくあるエラーと修正

### エラー：必須フィールドが見つかりません

```
Error: Required field 'workflow' not found
```

**修正：** `app.mode`を確認してください。「workflow」の場合は、`workflow`セクションが必須です。

### エラー：無効なモード

```
Error: 'app.mode' must be one of: workflow, chat, agent
```

**修正：** スペルを確認してください。モード値は小文字のみです。

### エラー：ノードが見つかりません

```
Error: Reference to undefined node 'process_step'
```

**修正：** リファレンス内のノードID表記を確認してください。大文字小文字を区別します。

### エラー：YAMLの構文エラー

```
Error: Unexpected indent at line 42
```

**修正：** YAMLインデントは一貫している必要があります（通常2スペース）。配置を確認してください。

---

## 詳細情報

- [完全なDSL仕様](../../docs/DSL_SPECIFICATION.md)
- [テンプレート例](templates.md)
- [ワークフローガイド](workflows.md)
- [Dify公式ドキュメント](https://docs.dify.ai/)

ほとんどのユーザーにとって、[templates.md](templates.md)のテンプレートは必要なすべての構造を提供しています。テンプレートをコピーしてカスタマイズします。最初から構築する必要はありません。
