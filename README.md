# Dify-Creator

このリポジトリは **DifyのConsole API（`/console/api`）** を使って、Dify Studioの画面を触らずに

- **DSL（Workflow/Advanced ChatのYAML）をインポート（新規作成）**
- **DSLを上書きインポート（既存 `app_id` に反映）**
- **ドラフトWorkflowのテスト実行（`workflows/draft/run`）**
- **DSLのエクスポート（`/export`）**

をスクリプトで回すための最小環境です。

## セットアップ

### 依存関係（ローカルPython）

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### 依存関係（Docker）

このCLIはDocker/Composeでも実行できます（推奨）。

```bash
docker compose build
```

### 環境変数

`env.example` をコピーして `.env` を作り、値を入れてください。

- `DIFY_BASE_URL`: DifyのURL（例: `http://localhost` / `https://your-dify.example.com`）
- `DIFY_EMAIL`, `DIFY_PASSWORD`: Consoleログイン用（アプリAPIキーではありません）
- `DIFY_VERIFY_SSL`: 自己署名証明書などで検証を切る場合 `false`

## 使い方（代表）

以降の例は **Docker実行** を前提に書きます（ローカルPythonの場合は `docker compose run --rm dify-creator` を `python -m dify_creator` に置き換えてください）。

Docker実行時は、`.env` を使うために `DIFY_ENV_FILE=.env` を付けて実行してください（`compose.yml` はデフォルトで `env.example` を読みます）。

## Cursor Project Commands（/コマンド）から実行する（おすすめ）

Cursor公式の「コマンド」機能を使って、チャットで `/` を打つだけで実行できます。  
このリポジトリでは `.cursor/commands/` にコマンドを用意しています。

### 使い方

1. `env.example` を `.env` にコピーして値を入れる
2. Cursorのチャット入力で `/` を入力
3. 以下のどれかを選ぶ（ファイル名がコマンド名になります）
   - `/dify-setup`（初回：`.env` 作成 + build）
   - `/dify-sync`（インポート→ドラフト実行：開発ループはこれ）
   - `/dify-import`
   - `/dify-run`
   - `/dify-export`

### 各コマンドで「何ができるか」

非エンジニアの方は、基本は **Cursorの `/dify-*`（Project Commands）を選ぶだけ**でOKです。  
下の説明は「そのコマンドが何をするか」を理解するためのものです。

- **ログイン確認**（`/dify-setup` の次に、接続トラブルの切り分けに使う）
  - **できること**: `.env` の `DIFY_BASE_URL / DIFY_EMAIL / DIFY_PASSWORD` でDifyにログインできるか確認します。
  - **うまくいくと**: `ok` と表示されます。
  - **うまくいかないと**: URL・メール/パスワード・SSL設定（`DIFY_VERIFY_SSL`）を見直します。

- **DSLインポート（新規 / 上書き）**（`/dify-import`）
  - **できること**: DSL（YAML）をDifyに反映します。
  - **新規作成**: `app_id` を指定しない → 新しいDifyアプリが作られます。
  - **上書き**: `app_id` を指定する → **既存アプリの中身を差し替え**ます（開発は基本これ）。
  - **うまくいくと**: 結果JSONに `app_id` が出ます（このIDを控えて以後ずっと使います）。

- **テスト実行（ドラフトWorkflow）**（`/dify-run`）
  - **できること**: いまのドラフト状態のWorkflowを、入力JSONで実行して結果を取ります。
  - **入力**: `examples/inputs.json` をあなたのWorkflowの入力に合わせて編集します。
  - **うまくいくと**: `artifacts/run_result.json`（または指定先）に実行ログが保存されます。

- **import → テスト実行を一気に**（`/dify-sync`）
  - **できること**: **DSLを上書きインポート→すぐテスト実行**までを1回で行います。
  - **開発ループは基本これ**: 「修正 → sync → 結果確認」を繰り返すだけで進められます。
  - **うまくいくと**: `artifacts/import_result.json` と `artifacts/run_result.json` が保存されます。

- **DSLエクスポート**（`/dify-export`）
  - **できること**: 現在のDifyアプリ設定をDSL（YAML）として書き出します。
  - **使いどころ**: バックアップ、共有、いまの状態をファイル化してレビューする時。

### Difyアプリ開発の「基本フロー」（おすすめ）

1. **最初の1回だけ**: `/dify-setup` を実行し、`.env` にDifyのURLとログイン情報を入れる
2. **ベースになるアプリを用意**（どちらでもOK）
   - 既存のDifyアプリを使う（おすすめ）→ その `app_id` を控える
   - もしくはDSLから新規作成し、結果に出た `app_id` を控える
3. **DSL（YAML）を編集してアプリを作る**
   - 例: 変数名、プロンプト、ノード、分岐、ツール設定などをDSL側で更新
4. **入力JSON（`examples/inputs.json`）を用意**して、テストで使う入力を決める
5. **/dify-sync を実行**（上書きインポート→テスト実行）
6. **`artifacts/run_result.json` を確認**して、想定通りかチェック
7. **直して 5〜6 を繰り返す**

> ポイント: Difyの画面を触る作業は「最初の app_id を知る」以外は極力減らし、以降は **DSLと入力JSONを更新して /dify-sync** で回します。

## 補足（このCLIが叩いているConsole API）

OSS実装上、Console APIは `base_url + /console/api` 配下です。代表的に使っているエンドポイントは以下です。

- `POST /console/api/login`（Cookieで `access_token`/`csrf_token` を受け取る）
- `POST /console/api/apps/imports`（`app_id` を入れると上書き。`status=pending` の場合あり）
- `POST /console/api/apps/imports/{import_id}/confirm`（`pending` の確定）
- `GET /console/api/apps/{app_id}/export`（DSL文字列を返す）
- `POST /console/api/apps/{app_id}/workflows/draft/run`（ドラフトのWorkflow実行。ストリーミング）
