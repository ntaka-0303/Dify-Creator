# dify-export（DSLエクスポート）

指定した `app_id` のDSLをエクスポートしてファイルに保存します。

## 事前確認（ユーザーに質問）

1. `app_id` は？
2. 出力先パスは？（例: `artifacts/app.dsl.yml`）

## 実行コマンド（例）

```bash
mkdir -p artifacts
DIFY_ENV_FILE=.env docker compose run --rm dify-creator export \
  --app-id "YOUR_APP_ID" \
  --out "artifacts/app.dsl.yml"
```


