# dify-import（Difyにアプリをアップロード）

**（主にエージェント内部で使用。ユーザーは `/dify-new-app` または `/dify-edit-app` を使ってください）**

`app.dsl.yml` を Dify にアップロードします（app_id 指定で上書き）。

## 事前確認（エージェント向け）

1. DSL YAMLのパス（通常: `app.dsl.yml`）
2. app_id（上書き時。新規作成時は不要）

## エージェントの実行内容

### 新規作成

```bash
docker compose run --rm dify-creator import --dsl app.dsl.yml
```

### 上書き

```bash
docker compose run --rm dify-creator import --dsl app.dsl.yml --app-id "YOUR_APP_ID"
```

## 実行結果

- `app_id` とアプリ情報が返される


