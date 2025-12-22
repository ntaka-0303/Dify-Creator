# dify-sync（修正を反映＋テスト実行）

⚠️ **[重要] このコマンドは以下のSkillに統合されました：**

> **新しいSkill: [`managing-dify-apps`](./../skills/managing-dify-apps/SKILL.md)**
>
> このコマンドはエージェント内部で自動的に使用されます。

---

**（主にエージェント内部で使用。ユーザーは `/dify-new-app` または `/dify-edit-app` を使ってください）**

`app.dsl.yml` の修正を Dify に反映させて、すぐにテスト実行します。

## 事前確認（エージェント向け）

1. DSL YAMLのパス（通常: `app.dsl.yml`）
2. app_id（必須：どのアプリを上書きするか）
3. 入力JSONのパス（通常: `examples/inputs.json`）

## エージェントの実行内容

- `app.dsl.yml` を Dify にインポート（上書き）
- テスト入力で実行
- 結果を `artifacts/` に保存

## 実行コマンド（例）

```bash
docker compose run --rm dify-creator sync \
  --dsl app.dsl.yml \
  --app-id "YOUR_APP_ID" \
  --inputs-json examples/inputs.json \
  --out-dir artifacts
```

## 実行結果

以下が自動生成されます：

- `artifacts/import_result.json` - インポート結果
- `artifacts/run_result.json` - テスト実行結果


