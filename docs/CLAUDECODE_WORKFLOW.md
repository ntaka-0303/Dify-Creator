# ClaudeCode で Dify アプリを開発するワークフロー

このドキュメントは、ClaudeCodeを使ってDifyアプリケーション（Workflow、ChatBot）を効率的に開発するためのステップバイステップガイドです。

> **✨ 推奨：新しい Skill ベースのアプローチを使用してください**
>
> このプロジェクトは、Agent-Skillsベストプラクティスに基づいた新しいSkill構造に移行しました。
>
> - **`setting-up-dify-project`（Difyプロジェクトをセットアップする）Skill**: 初期セットアップ
> - **`managing-dify-apps`（Difyアプリを管理・作成する）Skill**: アプリの作成・編集・管理
>
> 新しい Skills を使用すると、ClaudeCode が自動で YAML 生成・検証・テストを行います。
> 詳細は [.claude/skills/](../.claude/skills/) を参照してください。
>
> 以下は従来のコマンドベースの開発フロー（参考用）です。

## 概要

このプロジェクトの狙いは、**Dify Studio（ブラウザUI）を触らずに、ClaudeCodeのみでDifyアプリを開発・管理する**ことです。

開発フロー（従来のコマンドベース）：
```
ClaudeCode で DSL 編集
          ↓
    ローカルで検証
          ↓
  Dify にインポート
          ↓
   テスト実行
          ↓
結果確認・修正
```

開発フロー（新しい Skill ベース - 推奨）：
```
managing-dify-apps Skill を選択
          ↓
「新規作成」または「編集」を選択
          ↓
ClaudeCode が自動で全処理
  - YAML 生成・修正
  - 検証
  - テスト実行
          ↓
結果確認・修正（自動ループ）
```

## 前提条件

1. **Difyサーバーがアクセス可能**（クラウド版 `https://cloud.dify.ai` またはセルフホスト版）
2. **ログイン可能**（Consoleメール/パスワード）
3. **このプロジェクトが環境構築済み**（`.env` が存在）

## セットアップ（初回のみ）

### 推奨：新しい Skill ベースのセットアップ

`setting-up-dify-project` Skill を使用してください。この Skill が以下を自動で行います：

```
1. 環境情報を収集（Dify URL、メール、パスワード）
2. .env ファイルを自動作成
3. Docker イメージをビルド
4. 接続をテスト
```

詳細は [.claude/skills/setting-up-dify-project/SKILL.md](../.claude/skills/setting-up-dify-project/SKILL.md) を参照してください。

### 参考：従来のコマンドベースのセットアップ

#### ステップ1：環境設定

```bash
# .env.example をコピー
cp .env.example .env

# .env を編集
DIFY_BASE_URL="https://cloud.dify.ai"  # または自社ホスト版
DIFY_EMAIL="your-email@example.com"
DIFY_PASSWORD="your-password"
DIFY_VERIFY_SSL=true
```

#### ステップ2：ログイン確認

```bash
docker compose run --rm dify-creator login
# または
python -m dify_creator login
```

成功すると `ok` が表示されます。

## 開発フロー

### **パターン A：既存のDifyアプリから開発を始める**

既にDify Studio で作ったアプリがある場合、それをDSLでエクスポートして、ClaudeCodeで編集します。

#### A1. 既存アプリをエクスポート

Difyのアプリ一覧から、対象アプリを探して `app_id` を確認します。

```bash
# app_id の確認方法：
# - Dify Studio でアプリを開く
# - URL から "apps/[app_id]/..." の部分をコピー

docker compose run --rm dify-creator export \
  --app-id "your-app-id" \
  --out app.dsl.yml
```

または、プロジェクトディレクトリで `app.dsl.yml` というファイルが生成されます。

#### A2. ClaudeCode で app.dsl.yml を編集

1. `app.dsl.yml` をエディタで開く
2. ノード、プロンプト、変数などを修正
3. ファイルを保存

参考：
- [DSL仕様書](./DSL_SPECIFICATION.md)
- [テンプレート例](../examples/templates/)

#### A3. DSL を検証（ローカルでエラーチェック）

Difyにアップロードする前に、基本的な構文をチェック：

```bash
docker compose run --rm dify-creator validate --dsl app.dsl.yml
```

出力例：
```
DSL Validation: app.dsl.yml

✅ 検証成功：DSLは基本的に有効です
```

エラーがある場合は、修正してから再度実行します。

#### A4. 上書きインポート＆テスト実行

修正したDSLをDifyに上書きインポートし、すぐにテスト実行：

```bash
docker compose run --rm dify-creator sync \
  --dsl app.dsl.yml \
  --app-id "your-app-id" \
  --inputs-json examples/inputs.json
```

結果は `artifacts/` に保存されます：
- `artifacts/import_result.json` - インポート結果
- `artifacts/run_result.json` - 実行結果

#### A5. 結果確認＆修正ループ

`artifacts/run_result.json` を確認して、期待通りの結果が得られているか確認。

修正が必要なら、A2 に戻ります。

---

### **パターン B：ClaudeCode で最初から新規作成**

既存アプリがない場合、テンプレートから始めます。

#### B1. テンプレートを選択・コピー

`examples/templates/` から、目的に合ったテンプレートを選びます：

| テンプレート | 説明 | 推奨用途 |
|-----------|------|--------|
| `1_simple_chatbot.dsl.yml` | Chatモード | Q&A、チャットボット |
| `2_echo_workflow.dsl.yml` | 最小限のWorkflow | 学習用 |
| `3_llm_workflow.dsl.yml` | LLMを含むWorkflow | 標準的なワークフロー |
| `4_conditional_workflow.dsl.yml` | 条件分岐あり | 複雑なフロー |
| `5_http_api_workflow.dsl.yml` | 外部API連携 | API統合 |

例：
```bash
cp examples/templates/3_llm_workflow.dsl.yml app.dsl.yml
```

#### B2. app.dsl.yml を ClaudeCode で編集

1. エディタで `app.dsl.yml` を開く
2. 以下を編集：
   - `app.name`, `app.description`
   - LLMノードのプロンプト（`prompt_template`）
   - 変数定義（`variable_pool`）
   - ノード接続（`connections`）
3. 保存

[DSL仕様書](./DSL_SPECIFICATION.md) を参照しながら編集してください。

#### B3. 検証

```bash
docker compose run --rm dify-creator validate --dsl app.dsl.yml
```

#### B4. 新規作成インポート

`app_id` を指定しない場合は、新しいDifyアプリとして作成されます：

```bash
docker compose run --rm dify-creator import --dsl app.dsl.yml
```

出力に含まれる `"app_id": "..."` をメモしておきます。

#### B5. テスト実行

```bash
# B4 で取得した app_id を使用
docker compose run --rm dify-creator sync \
  --dsl app.dsl.yml \
  --app-id "新しいapp_id" \
  --inputs-json examples/inputs.json
```

#### B6. 修正ループ

結果を確認し、修正が必要ならB2に戻ります。

---

## 実践例：シンプルなチャットボット開発

### シナリオ

「Claude API を使った簡単なQ&Aチャットボットを作りたい」

### 実装手順

**ステップ1：テンプレートをコピー**

```bash
cp examples/templates/1_simple_chatbot.dsl.yml my-chatbot.dsl.yml
```

**ステップ2：ClaudeCode で編集**

```yaml
# my-chatbot.dsl.yml
app:
  name: "Customer Support ChatBot"  # 名前を変更
  description: "顧客サポート用AI"

model_config:
  opening_statement: "こんにちは、カスタマーサポートです。ご質問をお聞きします。"

  system_prompt: |
    You are a customer support specialist for TechCorp.

    Rules:
    1. Always be polite and professional
    2. If you don't know the answer, say so and offer to connect with a human
    3. Keep responses concise (under 200 words)
```

**ステップ3：検証**

```bash
docker compose run --rm dify-creator validate --dsl my-chatbot.dsl.yml
```

**ステップ4：新規作成**

```bash
docker compose run --rm dify-creator import --dsl my-chatbot.dsl.yml
```

出力から `app_id` を確認（例：`abc123def456`）

**ステップ5：テスト入力を作成**

```json
// examples/inputs.json
{}
```

Chatモードの場合は、入力JSONは空でもOK。

**ステップ6：実行**

```bash
docker compose run --rm dify-creator sync \
  --dsl my-chatbot.dsl.yml \
  --app-id "abc123def456" \
  --inputs-json examples/inputs.json
```

**ステップ7：結果確認**

`artifacts/run_result.json` を確認して、期待通りの応答が返ってきたか確認。

---

## 実践例：複数ステップのワークフロー開発

### シナリオ

「テキストの感情を判定して、ポジティブ/ネガティブで異なる応答をする」

### 実装手順

**ステップ1：条件分岐テンプレートをコピー**

```bash
cp examples/templates/4_conditional_workflow.dsl.yml sentiment-workflow.dsl.yml
```

**ステップ2：必要に応じて編集**

プロンプト、モデル選択、変数名などを調整。

**ステップ3：検証**

```bash
docker compose run --rm dify-creator validate --dsl sentiment-workflow.dsl.yml
```

**ステップ4：インポート＆実行**

```bash
docker compose run --rm dify-creator sync \
  --dsl sentiment-workflow.dsl.yml \
  --inputs-json examples/inputs.json
```

**ステップ5：テスト入力を作成**

```json
// examples/inputs.json
{
  "input_text": "This product is amazing! I love it."
}
```

**ステップ6：実行結果を確認**

`artifacts/run_result.json` で各ノードの出力をチェック。

---

## コマンド一覧

| コマンド | 説明 | ネットワークアクセス |
|--------|------|-----------|
| `validate` | DSL を検証 | ❌ なし |
| `login` | Dify ログイン確認 | ✅ 必要 |
| `export` | アプリをエクスポート | ✅ 必要 |
| `import` | DSL をインポート | ✅ 必要 |
| `run` | テスト実行 | ✅ 必要 |
| `sync` | インポート → テスト実行 | ✅ 必要 |

---

## トラブルシューティング

### `docker compose: command not found`

Docker Compose v1 をお使いの場合：
```bash
# docker-compose（ハイフン）を使用
docker-compose run --rm dify-creator validate --dsl app.dsl.yml
```

### `DIFY_BASE_URL が未設定です`

```bash
# .env が存在するか確認
cat .env

# なければコピー
cp .env.example .env

# Docker での実行時は、--env-file を明示
docker compose --env-file .env run --rm dify-creator login
```

### インポート後も `status: "pending"` で止まる

Difyが依存関係をチェック中の可能性があります。少し待ってから再実行してください：

```bash
docker compose run --rm dify-creator import --dsl app.dsl.yml --app-id "your-app-id"
```

（`--app-id` を指定すると自動的に `confirm` が実行されます）

### 検証時に警告が出る（エラーではない）

```
⚠️  警告:
  - 'start' ノードが見つかりません
```

Workflowモード の場合、`start` と `end` ノードが必須です。追加してください。

Chat/Agentモードではこの警告は無視してOKです。

---

## 参考資料

- [DSL 仕様書](./DSL_SPECIFICATION.md) - 詳細な形式仕様
- [テンプレート例](../examples/templates/) - 実装例
- [Dify 公式ドキュメント](https://docs.dify.ai)

---

## よくある質問（FAQ）

**Q: Dify Studio で作ったアプリと DSL の内容が異なる。どちらが正？**

A: Dify Studio 側が正です。DSL は Dify Studio の表現のサブセットです。Studio で追加した細部は DSL で再現できていない可能性があります。その場合は、Studio で確認→修正→エクスポート してください。

**Q: DSL で設定したプロンプトが反映されない**

A: Dify にインポート後、Draft（ドラフト）モードで確認してください。公開版とドラフト版が異なる場合があります。

**Q: LLM の API キーはどこに設定？**

A: Dify の設定画面で事前に API キーを登録しておく必要があります。DSL では「どのプロバイダーを使うか」だけを指定し、認証情報はDify側で管理します。

**Q: 複数のメンバーで同じアプリを開発したい**

A: リポジトリで `.dsl.yml` ファイルをバージョン管理して、Git でコラボレーション。各メンバーが修正→コミット→プルリクエスト で進める流れが推奨です。

---

## 次のステップ

1. テンプレートをコピーしてカスタマイズ
2. `validate` で検証
3. `sync` でDifyに反映
4. 結果を確認して修正ループ
5. 完成したら Dify Studio で公開

Happy coding! 🚀
