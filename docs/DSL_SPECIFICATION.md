# Dify DSL 仕様書

このドキュメントは、ClaudeCodeを使ってDifyアプリケーションをDSL（Domain Specific Language）で作成・編集するための仕様書です。

## 概要

Dify DSLはYAML形式の言語定義ファイルで、Difyアプリケーション（Workflow、ChatBot、Agent）の完全な構成を記述します。

**参考資料：**
- [Dify App Management](https://docs.dify.ai/en/guides/management/app-management)
- [Dify Workflow Guide](https://docs.dify.ai/guides/workflow)

## DSLバージョン

```
バージョン: 0.5.0
形式: YAML
対応: Dify v0.6 以上
```

## DSLの基本構造

```yaml
version: "0.5.0"
kind: app
metadata:
  name: "アプリケーション名"
  description: "説明"
  icon: "emoji or url"
  icon_background: "#ffffff"

app:
  name: "アプリケーション名"
  mode: "workflow" # or "chat" or "agent"
  icon: "emoji or url"
  icon_background: "#ffffff"

workflow:
  # または model_config（Chat/Agentモードの場合）
  # Workflowノードとコネクション定義
```

## トップレベルフィールド

| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| `version` | string | ✅ | DSLバージョン（現在 0.5.0） |
| `kind` | string | ✅ | アプリケーション種別。常に "app" |
| `metadata` | object | ❌ | アプリケーションメタデータ |
| `app` | object | ✅ | アプリケーション設定 |
| `workflow` | object | ⚠️ | Workflowモード時に必須 |
| `model_config` | object | ⚠️ | ChatBotモード時に必須 |
| `dependencies` | object | ❌ | プラグイン依存関係 |

## `app` セクション

```yaml
app:
  name: "My Workflow App"
  mode: "workflow"  # "workflow" | "chat" | "agent"
  description: "Brief description of the app"
  icon: "🤖"
  icon_background: "#ffffff"
  created_at: 1234567890
  updated_at: 1234567890
```

| フィールド | 値 | 説明 |
|-----------|-----|------|
| `name` | string | アプリケーション名 |
| `mode` | "workflow" \| "chat" \| "agent" | アプリケーションモード |
| `description` | string | 説明（オプション） |
| `icon` | string | アイコン（絵文字またはURL） |
| `icon_background` | string | アイコン背景色（16進数） |

## `workflow` セクション（Workflowモード）

### 基本構造

```yaml
workflow:
  # グローバル変数
  variable_pool:
    - variable_name: "input_text"
      type: "string"
      description: "入力テキスト"
      value: ""

  # ノード定義
  nodes:
    - id: "node-1"
      title: "LLMノード"
      type: "llm"
      position:
        x: 100
        y: 100
      data: {...}

    - id: "node-2"
      title: "テキスト処理"
      type: "text_generation"
      position:
        x: 300
        y: 100
      data: {...}

  # ノード間の接続
  connections:
    - source:
        node_id: "node-1"
        output: "text"
      target:
        node_id: "node-2"
        input_from: "context"
```

### ノード種別

| ノードタイプ | 説明 |
|-----------|------|
| `start` | 開始ノード（必須） |
| `end` | 終了ノード（必須） |
| `llm` | LLM呼び出し（OpenAI、Claude等） |
| `http_request` | HTTP/REST API呼び出し |
| `code_executor` | Python/JavaScriptコード実行 |
| `tool` | 外部ツール呼び出し |
| `knowledge_retrieval` | 知識ベース検索 |
| `if_else` | 条件分岐 |
| `iteration` | ループ処理 |
| `variable_assignment` | 変数設定 |
| `question_answering` | Q&A処理 |

### LLMノードの例

```yaml
nodes:
  - id: "llm-node-1"
    title: "Claude API呼び出し"
    type: "llm"
    position:
      x: 200
      y: 150
    data:
      provider_name: "anthropic"  # "openai" | "anthropic" | ...
      model_name: "claude-3-opus-20250604"
      temperature: 0.7
      max_tokens: 2000
      prompt_template: |
        You are a helpful assistant.

        Context: {{context}}

        User Query: {{user_input}}

        Please provide a helpful response.
      variables:
        - name: "context"
          type: "string"
          required: true
        - name: "user_input"
          type: "string"
          required: true
      outputs:
        - name: "text"
          type: "string"
        - name: "usage"
          type: "object"
```

### 条件分岐（If/Else）の例

```yaml
nodes:
  - id: "if-node-1"
    title: "感情判定"
    type: "if_else"
    position:
      x: 300
      y: 300
    data:
      conditions:
        - variable: "sentiment"
          operator: "is"
          value: "positive"
          logic: "and"
      output_name: "condition_result"
```

### HTTPリクエストノードの例

```yaml
nodes:
  - id: "http-node-1"
    title: "API呼び出し"
    type: "http_request"
    position:
      x: 400
      y: 200
    data:
      method: "POST"  # "GET" | "POST" | "PUT" | "DELETE"
      url: "https://api.example.com/endpoint"
      headers:
        "Content-Type": "application/json"
        "Authorization": "Bearer {{api_key}}"
      body:
        type: "application/json"
        data:
          query: "{{search_query}}"
      timeout: 30
```

## `model_config` セクション（Chat/Agentモード）

```yaml
model_config:
  mode: "chat"
  opening_statement: |
    こんにちは。何かお手伝いできることはありますか？

  model:
    provider: "anthropic"
    name: "claude-3-opus-20250604"
    temperature: 0.7
    top_p: 0.95
    max_tokens: 2000

  system_prompt: |
    You are a helpful customer support assistant.
    Always be polite and professional.

  prompt_variables:
    - variable_name: "company_name"
      type: "string"
      description: "会社名"

  tools: []

  knowledge_bases: []
```

## `dependencies` セクション

```yaml
dependencies:
  providers:
    - name: "openai"
      version: "1.0.0"
    - name: "anthropic"
      version: "1.0.0"

  tools: []

  integrations: []
```

## 変数とテンプレート

### 変数参照の方法

Dify DSLでは、`{{variable_name}}` 形式で変数を参照します。

```yaml
prompt_template: |
  Context: {{context}}
  User input: {{user_input}}
  Previous response: {{prev_response}}
```

### 変数の種別

| 型 | 説明 | 例 |
|----|------|-----|
| `string` | テキスト | "Hello" |
| `number` | 数値 | 42 |
| `boolean` | 真偽値 | true |
| `object` | JSON オブジェクト | `{"key": "value"}` |
| `array` | 配列 | `["item1", "item2"]` |

## Difyアプリケーション開発フロー

### フロー1：新規作成（ClaudeCodeから）

```
1. DSL テンプレートファイルを ClaudeCode で作成
   └─ app.dsl.yml として保存

2. ローカルで DSL を編集
   ├─ ノード定義
   ├─ プロンプト
   ├─ 接続関係

3. Dify にインポート（新規作成）
   $ dify_creator import --dsl app.dsl.yml

4. 出力された app_id を控える

5. テスト入力で実行
   $ dify_creator run --app-id <app_id> --inputs-json examples/inputs.json

6. 結果を確認して繰り返し
```

### フロー2：既存アプリを編集（Export → 編集 → Import）

```
1. Dify から既存アプリを エクスポート
   $ dify_creator export --app-id <app_id> --out current.dsl.yml

2. ClaudeCode で current.dsl.yml を編集

3. 上書きインポート
   $ dify_creator import --dsl current.dsl.yml --app-id <app_id>

4. テスト実行
   $ dify_creator sync --dsl current.dsl.yml --app-id <app_id>
```

### フロー3：開発ループ（最速）

```
# 最初の 1 回だけ export して app.dsl.yml を用意
$ dify_creator export --app-id <app_id> --out app.dsl.yml

# その後は、app.dsl.yml を編集して sync するだけ
$ dify_creator sync --dsl app.dsl.yml --app-id <app_id>
```

## ClaudeCode での推奨ワークフロー

### ステップ1：プロジェクト初期化

```bash
# .env を設定
export DIFY_BASE_URL="https://your-dify.example.com"
export DIFY_EMAIL="your-email@example.com"
export DIFY_PASSWORD="your-password"

# ログイン確認
docker compose run --rm dify-creator login
```

### ステップ2：既存アプリからエクスポート、またはテンプレートから新規作成

**既存アプリを使う場合：**
```bash
docker compose run --rm dify-creator export \
  --app-id "existing_app_uuid" \
  --out app.dsl.yml
```

**新規作成の場合：**
- このドキュメント内の「テンプレート例」を参照
- `examples/templates/` からテンプレートをコピー

### ステップ3：ClaudeCode で DSL を編集

1. `app.dsl.yml` をエディタで開く
2. ノード、プロンプト、変数を編集
3. 保存

### ステップ4：テスト実行（ファイル更新のたびに）

```bash
docker compose run --rm dify-creator sync \
  --dsl app.dsl.yml \
  --app-id "<app_uuid>" \
  --inputs-json examples/inputs.json
```

### ステップ5：結果確認

`artifacts/run_result.json` を確認して、期待通りかチェック。

修正が必要なら、ステップ3-5を繰り返す。

## トラブルシューティング

### インポートが pending 状態で止まる

**原因**: 依存関係の確認待ち（モデルの認証設定など）

**解決策**:
```bash
# 既存の pending をクリアして再試行
dify_creator import --dsl app.dsl.yml --app-id <app_id>

# 自動的に confirm が実行されます
```

### ノードが接続できない

**確認項目**:
- `connections` の `node_id` が正確か
- `output` / `input_from` のフィールド名が一致しているか
- ノード間のデータ型が互換性あるか

### 環境変数が設定されていないエラー

```bash
# .env が正しく読まれているか確認
cat .env

# Docker compose 実行時に指定
docker compose --env-file .env run --rm dify-creator sync ...
```

## 参考：完全な最小サンプル DSL

```yaml
version: "0.5.0"
kind: app
metadata:
  name: "Simple Echo App"
  description: "ユーザー入力をそのまま返す"
  icon: "🎯"

app:
  name: "Simple Echo App"
  mode: "workflow"
  description: "ユーザー入力をそのまま返す"

workflow:
  variable_pool:
    - variable_name: "user_input"
      type: "string"
      description: "ユーザーからの入力"
      value: ""

  nodes:
    - id: "start"
      title: "開始"
      type: "start"
      position:
        x: 100
        y: 100
      data: {}

    - id: "end"
      title: "終了"
      type: "end"
      position:
        x: 300
        y: 100
      data:
        outputs:
          - variable: "user_input"

  connections:
    - source:
        node_id: "start"
        output: "output"
      target:
        node_id: "end"
        input_from: "input"
```

## 次のステップ

- `examples/templates/` で複数のテンプレート例を参照
- Dify公式ドキュメントでワークフロー構築のベストプラクティスを学習
- ClaudeCodeでテンプレートを修正してカスタムアプリを作成
