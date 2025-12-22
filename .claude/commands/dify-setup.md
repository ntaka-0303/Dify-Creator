# dify-setup（初回セットアップ：自動設定 + Docker build）

⚠️ **[重要] このコマンドは以下のSkillに統合されました：**

> **新しいSkill: [`setting-up-dify-project`](./../skills/setting-up-dify-project/SKILL.md)**
>
> Agent-Skillsベストプラクティスに準拠した新構造です。
> より詳細なドキュメント: [setup-workflow.md](./../skills/setting-up-dify-project/reference/setup-workflow.md)
>
> **推奨**: 新しいSkillの使用をお勧めします。このコマンドは後方互換性のため保持されます。

---

このプロジェクトを使い始めるための完全な初期化を行います。ユーザーは情報を答えるだけで、後はすべて自動です。

## ユーザーに確認すること

以下の情報をユーザーに聞いてください。**複数選択肢がある場合は、推奨をマークしてください。**

### 1. Dify のホスト先

```
- https://cloud.dify.ai（推奨：クラウド版）
- http://localhost:5001（自分のサーバー）
- その他のURL
```

### 2. ログイン情報

- Dify コンソールにログインするときのメールアドレス
- パスワード

### 3. SSL証明書確認（自分のサーバーを使う場合）

```
- はい（推奨：SSL証明書を検証）
- いいえ（自己署名証明書など）
```

## エージェントの実行内容

以下をすべて自動実行します：

1. `.env.example` から `.env` ファイルを作成
2. ユーザーが入力した値を `.env` に書き込み
3. 接続テストを実行（ログイン確認）
4. Docker イメージをビルド
5. セットアップ完了メッセージを表示

## 実行内容の詳細

```bash
# 1. .env ファイルが無ければコピー
test -f .env || cp .env.example .env

# 2. .env に値を設定（ユーザー入力から自動生成）
# DIFY_BASE_URL=...
# DIFY_EMAIL=...
# DIFY_PASSWORD=...

# 3. Docker build
docker compose build

# 4. ログイン確認
docker compose run --rm dify-creator login

# 5. 完了メッセージ
```

## セットアップ完了後

以下のコマンドが使えるようになります。

- `/dify-new-app` - 新しいアプリを作成
- `/dify-edit-app` - 既存アプリを編集
- `/dify-export` - アプリをダウンロード
- `/dify-sync` - 修正を Dify に反映＋テスト


