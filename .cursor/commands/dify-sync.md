# dify-sync（インポート→ドラフト実行）

DSLをDifyに **インポート（必要なら上書き）→ドラフトWorkflowを実行**し、結果を `artifacts/` に保存します。

## 事前確認（ユーザーに質問）

1. DSL YAMLのパスは？（例: `path/to/app.dsl.yml`）
2. 上書き対象の `app_id` は？（新規作成なら空でOK）
3. 入力JSONのパスは？（例: `examples/inputs.json`）
4. 出力先ディレクトリは？（デフォルト: `artifacts`）

## 実行内容

- `.env` を使ってDockerコンテナから `dify_creator sync` を実行します。

## 実行コマンド（例）

```bash
DIFY_ENV_FILE=.env docker compose run --rm dify-creator sync \
  --dsl "path/to/app.dsl.yml" \
  --app-id "YOUR_APP_ID" \
  --inputs-json "examples/inputs.json" \
  --out-dir "artifacts"
```

## 注意

- `--app-id` を省略すると **新規作成**になります。
- `examples/inputs.json` はあなたのWorkflow入力スキーマに合わせて編集してください。


