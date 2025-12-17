# dify-import（DSLインポート/上書き）

DSLをDifyにインポートします（`app_id` を指定すると上書き）。

## 事前確認（ユーザーに質問）

1. DSL YAMLのパスは？（例: `path/to/app.dsl.yml`）
2. 上書きするなら `app_id` は？（新規なら空でOK）

## 実行コマンド（例）

### 新規作成

```bash
DIFY_ENV_FILE=.env docker compose run --rm dify-creator import --dsl "path/to/app.dsl.yml"
```

### 上書き

```bash
DIFY_ENV_FILE=.env docker compose run --rm dify-creator import --dsl "path/to/app.dsl.yml" --app-id "YOUR_APP_ID"
```


