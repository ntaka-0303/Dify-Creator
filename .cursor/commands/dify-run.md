# dify-run（ドラフトWorkflow実行）

指定した `app_id` の **ドラフトWorkflow** を入力JSONで実行します。

## 事前確認（ユーザーに質問）

1. `app_id` は？
2. 入力JSONのパスは？（例: `examples/inputs.json`）

## 実行コマンド（例）

```bash
DIFY_ENV_FILE=.env docker compose run --rm dify-creator run \
  --app-id "YOUR_APP_ID" \
  --inputs-json "examples/inputs.json" \
  --out "artifacts/run_result.json"
```


