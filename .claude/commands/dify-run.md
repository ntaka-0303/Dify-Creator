# dify-run（テスト実行のみ）

**（主にエージェント内部で使用。通常は `/dify-sync` を使用してください）**

指定した app_id のアプリをテスト実行します。

## 事前確認（エージェント向け）

1. app_id（テスト対象のアプリID）
2. 入力JSONのパス（通常: `examples/inputs.json`）

## 実行コマンド

```bash
docker compose run --rm dify-creator run \
  --app-id "YOUR_APP_ID" \
  --inputs-json examples/inputs.json \
  --out artifacts/run_result.json
```

## 実行結果

- `artifacts/run_result.json` に実行結果が保存される


