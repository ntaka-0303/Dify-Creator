# dify-export（Difyからアプリをダウンロード）

**（主にエージェント内部で使用。ユーザーは `/dify-edit-app` を使ってください）**

Dify から既存アプリの設定（DSL）をダウンロードして、ローカルの `app.dsl.yml` に保存します。

## 事前確認（エージェント向け）

1. app_id（ダウンロード対象のアプリID）

## エージェントの実行内容

```bash
docker compose run --rm dify-creator export \
  --app-id "YOUR_APP_ID" \
  --out "app.dsl.yml"
```

## 実行結果

- `app.dsl.yml` が作成される（現在のアプリ設定）


