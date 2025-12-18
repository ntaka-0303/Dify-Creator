# dify-validate（DSL検証：形式チェック）

**（主にエージェント内部で使用）**

`app.dsl.yml` の形式が正しいか、Dify にアップロードする前にチェックします。

## エージェントの実行内容

以下をチェック：

- ✅ YAML 形式が正しいか
- ✅ 必須フィールド（`version`, `kind`, `app`など）が存在するか
- ✅ `app.mode` が有効か（`workflow`, `chat`, `agent`）
- ✅ ノード定義の基本形式

## 実行コマンド

```bash
docker compose run --rm dify-creator validate --dsl app.dsl.yml
```

## 出力例

### 成功時
```
✅ 検証成功：DSLは基本的に有効です
```

### エラーがある場合
```
❌ エラー (2):
  - 必須フィールド 'workflow' が見つかりません
  - 'app.mode' は {'workflow', 'chat', 'agent'} のいずれかである必要があります
```

## 次のステップ

- **エラーあり** → 修正内容を修正
- **エラーなし** → アップロード準備完了
