# Difyアプリテンプレート

このガイドは、異なるアプリタイプ用の5つの利用可能なDSLテンプレートを選択し理解するのに役立ちます。

## 目次
- テンプレート概要と選択ガイド
- 各テンプレートの使用時期
- テンプレート構造とキーセクション
- カスタマイズガイダンス
- 実際の使用例

---

## クイック選択ガイド

| テンプレート | アプリタイプ | 使用例 | 最適な用途 |
|----------|----------|-----------|----------|
| **1_simple_chatbot** | Q&Aチャット | サポートボット、FAQ回答、対話型AI | 初心者、シンプルな対話 |
| **2_echo_workflow** | ワークフロー | テキストエコー、シンプルパススルー | 学習、最小限の処理 |
| **3_llm_workflow** | ワークフロー + LLM | テキスト分析、要約、変換 | 標準的な複数ステップ操作 |
| **4_conditional_workflow** | 分岐ロジック | ルーティング、判定木、条件付き出力 | 複雑な意思決定 |
| **5_http_api_workflow** | API統合 | 外部データ取得、サービス呼び出し | サードパーティ統合 |

---

## テンプレート 1：シンプルチャットボット（`1_simple_chatbot.dsl.yml`）

### 機能
Claudeを搭載したシンプルなQ&Aチャットボット。ユーザーが質問し、AIが対話的に応答します。

### 最適な用途
- カスタマーサポートチャットボット
- FAQ回答サービス
- 一般知識Q&A
- 初めてDifyを使用するユーザー

### 主な特徴
- **モード：** `chat`（対話型）
- **モデル：** Claude（最新バージョン）
- **入力：** ユーザーメッセージ
- **出力：** AI応答
- **複雑度：** ⭐ 低
- **ステップ数：** 1（単一LLM呼び出し）

### 構造概要

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

### カスタマイズのヒント

**トーンを変更する：**
```yaml
system_prompt: |
  あなたはプロフェッショナルなカスタマーサポートエージェントです。
  フォーマルで簡潔、ソリューション重視であること。
  常に次のステップを提供する。
```

**コンテキストまたは知識を追加：**
```yaml
system_prompt: |
  あなたはEコマースプラットフォームのサポートエージェントです。
  当社のポリシー：[主要ポリシーをリスト]
  一般的な問題と解決策：[問題を文書化]
```

**応答制限を設定：**
```yaml
model:
  max_tokens: 512  # より短い応答
  temperature: 0.3 # より決定的
```

### 変数（必要な場合）

動的な動作のため、プロンプト変数を追加：
```yaml
prompt_variables:
  - variable_name: "customer_tier"
    type: "string"
  - variable_name: "language_preference"
    type: "string"
```

その後、system_promptで参照：`{customer_tier}`、`{language_preference}`

---

## テンプレート 2：エコーワークフロー（`2_echo_workflow.dsl.yml`）

### 機能
入力テキストをそのまま返す最小限のワークフロー。ワークフロー構造を理解するのに役立ちます。

### 最適な用途
- Difyワークフローの基礎を学ぶ
- 接続をテスト
- 非常にシンプルなパススルー操作のテンプレート
- 正常性チェック

### 主な特徴
- **モード：** `workflow`（プロセスベース）
- **ステップ：** 1（エコー/パススルー）
- **入力：** テキスト
- **出力：** 同じテキスト（エコー）
- **複雑度：** ⭐ 非常に低い
- **使用例：** プロダクション使用は推奨されません。主に教育目的

### 構造概要

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

### 実際の使用時期
- Dify接続が機能していることを確認
- アプリデプロイメカニズムをテスト
- より複雑なワークフローのベースライン

---

## テンプレート 3：LLMワークフロー（`3_llm_workflow.dsl.yml`）

### 機能
データ入力、処理、LLM分析を組み合わせた複数ステップのワークフロー。ほとんどのアプリケーションの標準的な選択肢です。

### 最適な用途
- テキスト要約
- コンテンツ分析と分類
- データ変換と強化
- ほとんどのプロダクションアプリケーション

### 主な特徴
- **モード：** `workflow`（プロセスベース）
- **ステップ：** 2-4（通常：入力 → 処理 → LLM → 出力）
- **柔軟性：** 高い—ステップの追加/削除が容易
- **複雑度：** ⭐⭐ 中
- **LLM統合：** 完全なコントロール

### 構造概要

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

### カスタマイズ例

**例1：テキスト要約器**
```yaml
llm_node:
  system_prompt: |
    あなたはテキスト要約器です。
    提供されたテキストを3～5つの箇条書きで要約してください。
    主要な洞察と実行可能なポイントに焦点を当てる。
  input:
    text: "${start.article_text}"
```

**例2：感情分析器**
```yaml
llm_node:
  system_prompt: |
    提供された顧客フィードバックの感情を分析してください。
    回答：感情（ポジティブ/ネガティブ/ニュートラル）と2つの裏付け詳細。
  input:
    feedback: "${start.customer_feedback}"
```

**例3：コードレビュアー**
```yaml
llm_node:
  system_prompt: |
    あなたはコードレビュアーです。提供されたコードをレビュー：
    - 正確性とロジックエラー
    - パフォーマンスの問題
    - セキュリティ脆弱性
    - ベストプラクティス
  input:
    code: "${start.code_snippet}"
```

### 複数ステップの追加

LLMノードをチェーンしてワークフローを拡張：

```yaml
workflow:
  nodes:
    - id: "step1_analyze"
      type: "llm"
      # 最初の分析...

    - id: "step2_refine"
      type: "llm"
      input:
        previous_result: "${step1_analyze.output}"
      # 最初の結果に基づいて改善...

    - id: "output"
      type: "end"
      output:
        final_result: "${step2_refine.output}"
```

---

## テンプレート 4：条件付きワークフロー（`4_conditional_workflow.dsl.yml`）

### 機能
分岐ロジックを持つワークフロー。条件に基づいてデータを異なるパスに送信します。

### 最適な用途
- コンテンツに基づいて異なるハンドラへルーティング
- 判定木と分類
- 複雑なマルチパスプロセス
- 動的応答選択

### 主な特徴
- **モード：** `workflow`（プロセスベース）
- **ステップ：** 3+（条件分岐を含む）
- **分岐：** はい—条件ごとに異なるパス
- **複雑度：** ⭐⭐⭐ より高い
- **典型的な構造：** 入力 → 分類 → 分岐 → 処理 → 出力

### 構造概要

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

### 使用例

**例1：カスタマーサポートルーティング**
```yaml
# 分類 → 異なるチームへルーティング
# COMPLAINT → 謝罪 + 解決策
# QUESTION → 役立つ回答
# COMPLIMENT → 感謝 + エンゲージメント
```

**例2：コンテンツモデレーション**
```yaml
# 分類 → リスクレベルに基づいてルーティング
# HIGH_RISK → 人間によるレビュー
# MEDIUM_RISK → フィルター + 許可
# LOW_RISK → 即座に承認
```

**例3：動的応答選択**
```yaml
# 入力を分析 → 応答テンプレートを選択
# FORMAL_TONE → プロフェッショナルな応答
# CASUAL_TONE → フレンドリーな応答
# URGENT → 迅速な対応
```

### 条件付きノード構文

```yaml
- id: "router"
  type: "if"
  condition: "${classifier.output.contains('urgent')}"
  branches:
    - id: "urgent_path"
      # 緊急対応用のノード...
    - id: "standard_path"
      # 通常対応用のノード...
```

---

## テンプレート 5：HTTP APIワークフロー（`5_http_api_workflow.dsl.yml`）

### 機能
外部APIからデータを取得して処理するワークフロー。

### 最適な用途
- リアルタイムデータ取得（天気、ニュース、価格）
- サードパーティサービス統合
- API経由のデータベースクエリ
- 外部エンリッチメント

### 主な特徴
- **モード：** `workflow`（プロセスベース）
- **ステップ：** 3+（API呼び出しを含む）
- **外部呼び出し：** はい—外部サービスへのHTTPリクエスト
- **複雑度：** ⭐⭐⭐ より高い
- **典型的な構造：** 入力 → リクエスト準備 → API呼び出し → 処理 → 出力

### 構造概要

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

### 使用例

**例1：天気ボット**
```yaml
# ユーザーから都市を取得 → 天気APIを呼び出し → 結果をフォーマット
# 入力：city_name
# API：天気サービス
# 出力：「[都市]の今日：[気温]、[状態]」
```

**例2：株価チェッカー**
```yaml
# ユーザーからシンボルを取得 → 金融APIを呼び出し → トレンドを分析
# 入力：stock_symbol
# API：金融データプロバイダー
# 出力：「現在の価格、変化、1年間のパフォーマンス」
```

**例3：ドキュメント検索**
```yaml
# ユーザーから質問を取得 → ドキュメントAPIを検索 → 検索結果を使用して回答
# 入力：technical_question
# API：ドキュメント検索サービス
# 出力：関連ドキュメント + Claudeの説明
```

### API設定

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

### エラーハンドリングパターン

```yaml
- id: "api_call"
  type: "http_request"
  # ... api設定 ...
  on_error:
    - id: "error_handler"
      type: "llm"
      system_prompt: "データ取得が失敗したことを丁寧に説明し、代替案を提供"
```

---

## テンプレート選択の判定木

```
開始：「Difyアプリを構築したい」
  │
  ├─ 「単なるQ&A会話ですか？」
  │  └─ はい → テンプレート1を使用：シンプルチャットボット
  │
  ├─ 「複数の処理ステップを含みますか？」
  │  ├─ はい（分岐あり？）
  │  │  ├─ はい → テンプレート4を使用：条件付きワークフロー
  │  │  └─ いいえ → テンプレート3を使用：LLMワークフロー
  │  └─ いいえ（テスト/学習？）
  │     └─ テンプレート2を使用：エコーワークフロー
  │
  └─ 「外部APIまたはサービスを呼び出しますか？」
     └─ はい → テンプレート5を使用：HTTP APIワークフロー
```

---

## カスタマイズワークフロー

### すべてのテンプレートの一般的なプロセス

1. **ベーステンプレートをコピー** `app.dsl.yml`としてプロジェクトへ
2. **メタデータを更新**（name、description、icon）
3. **モデル設定をカスタマイズ**（system_prompt、temperature、max_tokens）
4. **入出力スキーマを定義**（ユーザーが提供するもの、受け取るもの）
5. **プロンプト変数を追加**（アプリが動的な動作を必要とする場合）
6. **検証** `docker compose run --rm dify-creator validate --dsl app.dsl.yml`で
7. **代表的な入力でテスト**
8. **結果に基づいて反復**

### 一般的なカスタマイズパターン

**パターン1：システムプロンプトを変更**
```yaml
system_prompt: |
  ここにカスタム指示。
  AIの役割、制約、出力形式を定義。
```

**パターン2：入力変数を追加**
```yaml
prompt_variables:
  - variable_name: "user_tier"
  - variable_name: "language"
```

その後、プロンプトで使用：`「{language}で{user_tier}ユーザー向けに応答」`

**パターン3：複数のLLM呼び出しをチェーン**
```yaml
nodes:
  - id: "step1"
    type: "llm"
    # 最初の操作...
  - id: "step2"
    type: "llm"
    input:
      context: "${step1.output}"
    # step1に基づいて改善...
```

---

## テンプレートのベストプラクティス

✅ **すべきこと：**
- 最も近いマッチングテンプレートで開始
- プロンプトを明確かつ具体的に保つ
- 多様な入力でテスト
- 各ステップが何をするかを文書化
- 変更後毎回検証
- 意味のあるノードIDを使用

❌ **してはいけないこと：**
- テンプレートを設計を超えて曲げようとする（より良いテンプレートで最初からやり直す）
- 汎用プロンプトを未変更のまま残す
- 最初から不必要な複雑さを追加
- テストなしでテンプレートが機能すると仮定
- 検証エラーを無視
- 一度に複数の無関係な変更を行う

---

## 次のステップ

1. **テンプレートを選択** 上記のガイドから
2. **テンプレートファイルを表示** `examples/templates/`で
3. **カスタマイズ** 特定のニーズに合わせて
4. **設定を検証**
5. **実際の入力でテスト**
6. **デプロイして結果に基づいて反復**

完全なアプリ作成と反復ワークフローについては[workflows.md](workflows.md)を参照してください。
