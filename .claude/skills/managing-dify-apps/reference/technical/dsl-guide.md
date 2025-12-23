# Dify DSL 設定ガイド

Dify DSL（ドメイン固有言語）設定構造の包括的なリファレンスです。

## 目次
- 基本構造
- アプリケーションモード
- ワークフローノード詳細
- 変数とデータフロー
- ベストプラクティス

---

## 概要

DifyアプリはYAML形式で定義されます（DSLバージョン 0.5.0）。各アプリは以下を必要とします：
- **基本メタデータ**: name、description、icon
- **モード選択**: chat、workflow、advanced-chat、またはagent-chat
- **設定**: モデル設定またはワークフローノード

---

## 基本構造

すべてのDifyアプリは次の構造に従います：

```yaml
version: "0.5.0"
kind: app

app:
  name: "アプリ名"
  description: "アプリの説明"
  icon: "🤖"
  icon_background: "#FFEAD5"
  mode: "workflow"  # chat/workflow/advanced-chat/agent-chat

# モードに応じた設定
model_config:  # chat/agent-chatモードの場合
  # チャット設定...

workflow:  # workflow/advanced-chatモードの場合
  # ワークフロー設定...
```

---

## アプリケーションモード

### 1. Chat（チャット）
シンプルな対話型アプリ

```yaml
app:
  mode: "chat"

model_config:
  opening_statement: "こんにちは！"
  system_prompt: "あなたは親切なアシスタントです"
  model:
    provider: "openai"
    name: "gpt-4o"
    mode: chat
    completion_params:
      temperature: 0.7
```

**用途：** Q&A、カスタマーサポート、シンプルな対話

### 2. Workflow（ワークフロー）
複数ステップの処理フロー

```yaml
app:
  mode: "workflow"

workflow:
  graph:
    edges: []
    nodes: []
```

**用途：** データ処理、API統合、複雑なロジック

### 3. Advanced Chat（高度なチャット）
ワークフローとチャットの組み合わせ

```yaml
app:
  mode: "advanced-chat"

workflow:
  conversation_variables: []
  graph:
    edges: []
    nodes: []
```

**用途：** 知識検索、質問分類、複雑な対話フロー

### 4. Agent Chat（エージェントチャット）
ツール使用を伴う自律エージェント

```yaml
app:
  mode: "agent-chat"

model_config:
  agent_mode:
    enabled: true
    max_iteration: 5
    strategy: function_call
    tools: []
```

**用途：** API呼び出し、外部ツール統合、複雑なタスク実行

---

## ワークフローノード詳細

### Start（開始）ノード

ワークフローの入口点

```yaml
- id: "1731228343114"
  data:
    type: start
    title: 開始
    variables:
      - type: text-input
        variable: user_query
        label: ユーザーの質問
        required: true
        max_length: 500
```

**変数タイプ：**
- `text-input`: 短文テキスト
- `paragraph`: 長文テキスト
- `number`: 数値
- `file`: ファイルアップロード
- `select`: 選択肢

### LLM（言語モデル）ノード

テキスト生成と分析

```yaml
- id: "1731229438627"
  data:
    type: llm
    title: LLM処理
    model:
      provider: openai
      name: gpt-4o
      mode: chat
      completion_params:
        temperature: 0.7
    prompt_template:
      - id: "prompt1"
        role: system
        text: 'あなたは専門家です。{{#1731228343114.user_query#}}に答えてください。'
    context:
      enabled: true
      variable_selector:
        - "1731228343114"
        - "user_query"
    vision:
      enabled: false
```

**重要ポイント：**
- 変数参照: `{{#ノードID.変数名#}}`
- temperature: 0.0（決定的） ～ 1.0（創造的）
- プロンプトはシングルクォートで括る

### End（終了）ノード

ワークフローの出力

```yaml
- id: "1731228345560"
  data:
    type: end
    title: 終了
    outputs:
      - value_selector:
          - "1731229438627"
          - "text"
        variable: result
```

### Question Classifier（質問分類器）ノード

質問を自動分類

```yaml
- id: "1731230000000"
  data:
    type: question-classifier
    title: 質問分類器
    model:
      provider: openai
      name: gpt-4o
      mode: chat
      completion_params:
        temperature: 0.7
    query_variable_selector:
      - "1731228343114"
      - "user_query"
    classes:
      - id: '1'
        name: 技術的な質問
      - id: '2'
        name: 請求に関する質問
```

**エッジ接続：**
```yaml
edges:
  - source: "1731230000000"
    sourceHandle: '1'  # クラスID
    target: "技術サポートノードID"
    targetHandle: target
    data:
      sourceType: question-classifier
      targetType: llm
```

### Knowledge Retrieval（知識取得）ノード

ナレッジベースから情報検索

```yaml
- id: "1731231000000"
  data:
    type: knowledge-retrieval
    title: 知識取得
    dataset_ids:
      - "データセットID"
    retrieval_mode: multiple
    multiple_retrieval_config:
      reranking_enable: true
      reranking_mode: weighted_score
      top_k: 4
      weights:
        vector_setting:
          embedding_model_name: text-embedding-3-large
          embedding_provider_name: openai
          vector_weight: 1
        keyword_setting:
          keyword_weight: 0
    query_variable_selector:
      - "1731228343114"
      - "user_query"
```

### IF/ELSE（条件分岐）ノード

条件に基づく分岐

```yaml
- id: "1731232000000"
  data:
    type: if-else
    title: 条件分岐
    cases:
      - case_id: 'true'
        logical_operator: and
        conditions:
          - id: "cond1"
            varType: string
            variable_selector:
              - "1731228343114"
              - "user_query"
            comparison_operator: 'contains'
            value: '緊急'
```

**比較演算子：**
- `contains`: 含む
- `not contains`: 含まない
- `start with`: 始まる
- `end with`: 終わる
- `is`: 完全一致
- `is not`: 完全不一致
- `=`, `≠`, `>`, `<`, `≥`, `≤`: 数値比較

**エッジ接続：**
```yaml
edges:
  - source: "1731232000000"
    sourceHandle: 'true'
    target: "緊急処理ノードID"
    data:
      sourceType: if-else
      targetType: llm
  - source: "1731232000000"
    sourceHandle: 'false'
    target: "通常処理ノードID"
    data:
      sourceType: if-else
      targetType: llm
```

### HTTP Request（HTTPリクエスト）ノード

外部API呼び出し

```yaml
- id: "1731233000000"
  data:
    type: http-request
    title: HTTPリクエスト
    authorization:
      type: no-auth  # no-auth/basic/bearer
      config: null
    method: post  # get/post/put/delete
    url: "https://api.example.com/endpoint"
    headers: "Content-Type:application/json"
    body:
      type: json
      data:
        - id: "key1"
          key: ''
          type: text
          value: |
            {
              "query": "{{#1731228343114.user_query#}}"
            }
    timeout:
      max_connect_timeout: 30
      max_read_timeout: 60
      max_write_timeout: 60
```

### Tool（ツール）ノード

#### JinaReader（Webスクレイピング）

```yaml
- id: "1731234000000"
  data:
    type: tool
    title: JinaReader
    provider_id: jina
    provider_name: jina
    provider_type: builtin
    tool_label: JinaReader
    tool_name: jina_reader
    tool_configurations:
      gather_all_images_at_the_end: 0
      gather_all_links_at_the_end: 0
      image_caption: 0
      no_cache: 0
      proxy_server: null
      summary: 0
      target_selector: null
      wait_for_selector: null
    tool_parameters:
      url:
        type: mixed
        value: '{{#1731228343114.url#}}'
```

#### TavilySearch（Web検索）

```yaml
- id: "1731235000000"
  data:
    type: tool
    title: TavilySearch
    provider_id: tavily
    provider_name: tavily
    provider_type: builtin
    tool_label: TavilySearch
    tool_name: tavily_search
    tool_configurations:
      exclude_domains: null
      include_domains: null
      include_answer: null
      include_images: null
      include_raw_content: null
      max_results: 3
      search_depth: basic  # basic/advanced
    tool_parameters:
      query:
        type: mixed
        value: '{{#1731228343114.search_query#}}'
```

### Code（コード実行）ノード

Pythonコードの実行

```yaml
- id: "1731236000000"
  data:
    type: code
    title: Pythonコード実行
    code_language: python3
    code: "def main(input_text: str) -> dict:\n    result = input_text.upper()\n    return {\n        \"output\": result\n    }"
    outputs:
      output:
        type: string
        children: null
    variables:
      - value_selector:
          - "1731228343114"
          - "user_query"
        variable: input_text
```

**利用可能なライブラリ：**
- datetime, math, random, re, string
- json, base64, hashlib
- その他多数（詳細はworkflow_generator_prompt.ymlを参照）

**出力型：**
- string, number, object, array
- array[string], array[number], array[object]

### Parameter Extractor（パラメータ抽出）ノード

テキストから構造化データを抽出

```yaml
- id: "1731237000000"
  data:
    type: parameter-extractor
    title: パラメータ抽出
    query:
      - "1731228343114"
      - "user_query"
    model:
      provider: openai
      name: gpt-4o
      mode: chat
      completion_params:
        temperature: 0.0
    reasoning_mode: function_call  # prompt/function_call
    parameters:
      - name: product_name
        type: string
        description: 製品名
        required: true
      - name: quantity
        type: number
        description: 数量
        required: true
    instruction: |
      ユーザーの入力から製品名と数量を抽出してください。
```

**出力変数：**
- 定義した各パラメータ
- `__is_success`: 抽出成功フラグ（0/1）
- `__reason`: エラー理由

### Answer（応答）ノード

チャットモードでの応答出力

```yaml
- id: "1731238000000"
  data:
    type: answer
    title: 応答出力
    answer: |
      検索結果：{{#1731229438627.text#}}
    variables: []
```

### Template Transform（テンプレート変換）ノード

Jinja2テンプレートによる文字列生成

```yaml
- id: "1731239000000"
  data:
    type: template-transform
    title: テンプレート変換
    template: |
      こんにちは、{{ user_name }}さん！
      {% if score >= 80 %}
      合格です！
      {% else %}
      不合格です。
      {% endif %}
    variables:
      - value_selector:
          - "1731228343114"
          - "user_name"
        variable: user_name
      - value_selector:
          - "1731228343114"
          - "score"
        variable: score
```

### Variable Aggregator（変数集約）ノード

複数の変数を統合

```yaml
- id: "1731240000000"
  data:
    type: variable-aggregator
    title: 変数集約器
    output_type: string
    variables:
      - - "1731237000000"  # IF分岐からの出力1
        - "result"
      - - "1731238000000"  # IF分岐からの出力2
        - "result"
```

---

## エッジ（接続）の定義

ノード間の接続を定義

```yaml
graph:
  edges:
    # 基本接続
    - source: "開始ノードID"
      target: "LLMノードID"
      data:
        sourceType: start
        targetType: llm
      sourceHandle: source
      targetHandle: target

    # 質問分類器からの分岐
    - source: "質問分類器ノードID"
      sourceHandle: '1'  # クラスID
      target: "ターゲットノードID"
      targetHandle: target
      data:
        sourceType: question-classifier
        targetType: llm

    # IF/ELSE分岐
    - source: "IF/ELSEノードID"
      sourceHandle: 'true'
      target: "TRUE分岐ノードID"
      data:
        sourceType: if-else
        targetType: llm
    - source: "IF/ELSEノードID"
      sourceHandle: 'false'
      target: "FALSE分岐ノードID"
      data:
        sourceType: if-else
        targetType: llm
```

---

## 変数とデータフロー

### 変数参照

ワークフロー内で変数を参照：

```
{{#ノードID.変数名#}}
```

**例：**
- `{{#1731228343114.user_query#}}` - 開始ノードの入力
- `{{#1731229438627.text#}}` - LLMノードの出力
- `{{#1731233000000.body#}}` - HTTPリクエストの応答

### 会話変数（Advanced Chatモード）

```yaml
workflow:
  conversation_variables:
    - id: "unique_id"
      name: topics
      description: "調査トピックのリスト"
      value: []
      value_type: array[string]
      selector:
        - conversation
        - topics
```

**用途：** チャットセッション間でデータを保持

---

## ベストプラクティス

### 1. ノードIDの管理

```
✅ 良い例: 17000000000000 から 17999999999999 の範囲
❌ 悪い例: 任意の数字、重複ID
```

### 2. プロンプトの書き方

```yaml
# ✅ 良い例
prompt_template:
  - role: system
    text: |
      あなたは専門家です。
      以下の質問に答えてください：
      {{#1731228343114.user_query#}}

# ❌ 悪い例
prompt_template:
  - role: system
    text: "答えて"  # 不十分な指示
```

### 3. エラーハンドリング

```yaml
# Parameter Extractorの成功チェック
- id: "if_check"
  data:
    type: if-else
    cases:
      - case_id: 'true'
        conditions:
          - varType: number
            variable_selector:
              - "1731237000000"
              - "__is_success"
            comparison_operator: '='
            value: '1'
```

### 4. モデル設定

```yaml
# 用途に応じた温度設定
model:
  completion_params:
    temperature: 0.0   # 事実ベース、決定的
    # temperature: 0.5  # バランス型
    # temperature: 1.0  # 創造的
```

---

## 検証チェックリスト

デプロイ前に確認：

```
✅ version: "0.5.0"
✅ kind: app
✅ app.mode が有効（chat/workflow/advanced-chat/agent-chat）
✅ すべてのノードIDがユニーク
✅ すべての変数参照が有効
✅ エッジの source/target が存在するノードを指す
✅ YAMLの構文が正しい（インデント、引用符）
✅ 必須フィールドがすべて設定されている
```

**検証コマンド：**
```bash
docker compose run --rm dify-creator validate --dsl app.dsl.yml
```

---

## よくあるエラーと解決

### エラー：ノードが見つかりません

```
Error: Reference to undefined node 'process_step'
```

**解決：** エッジのsource/targetが正しいノードIDを指しているか確認

### エラー：無効な変数参照

```
Error: Invalid variable reference '{{#node.var#}}'
```

**解決：** ノードIDと変数名を確認。大文字小文字を区別します。

### エラー：YAMLの構文エラー

```
Error: Unexpected indent at line 42
```

**解決：** インデントを確認（2スペース推奨）

---

## 実用例

### 質問分類 + 知識検索 + LLM応答

```yaml
workflow:
  graph:
    edges:
      - source: "start"
        target: "classifier"
        data: {sourceType: start, targetType: question-classifier}
      - source: "classifier"
        sourceHandle: '1'
        target: "knowledge1"
        data: {sourceType: question-classifier, targetType: knowledge-retrieval}
      - source: "knowledge1"
        target: "llm"
        data: {sourceType: knowledge-retrieval, targetType: llm}
      - source: "llm"
        target: "end"
        data: {sourceType: llm, targetType: end}

    nodes:
      - id: "start"
        data: {type: start, ...}
      - id: "classifier"
        data: {type: question-classifier, classes: [...]}
      - id: "knowledge1"
        data: {type: knowledge-retrieval, ...}
      - id: "llm"
        data: {type: llm, ...}
      - id: "end"
        data: {type: end, ...}
```

---

## 詳細情報

- [テンプレート例](templates.md)
- [ワークフローガイド](../core/workflows.md)
- [完全なDSL仕様](../../../../docs/DSL_SPECIFICATION.md)

**推奨：** [templates.md](templates.md)の実際のテンプレートから始めて、必要に応じてカスタマイズしてください。
