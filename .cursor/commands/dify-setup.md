# dify-setup（初回セットアップ：.env作成 + Docker build）

このプロジェクトの `dify-creator`（Docker版）を実行できるように初期化します。

## 事前確認（ユーザーに質問）

1. `DIFY_BASE_URL` はどこですか？（例: `http://localhost` / `https://your-dify.example.com`）
2. Consoleログイン用の `DIFY_EMAIL` と `DIFY_PASSWORD` は準備できていますか？

## 実行内容（エージェントがやること）

1. ルートに `.env` が無ければ `env.example` から作成する（中身はユーザーに編集してもらう）
2. Dockerイメージをビルドする

### 実行コマンド

```bash
test -f .env || cp env.example .env
docker compose build
```

## 次にやること

`.env` を編集して値を入れたあと、`/dify-sync` で **インポート→テスト実行**まで回せます。


