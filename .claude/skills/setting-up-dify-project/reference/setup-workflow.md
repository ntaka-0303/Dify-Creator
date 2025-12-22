# セットアップワークフローガイド

Dify-Creatorをセットアップするための完全なステップバイステップガイドです。

## 目次
- セットアップ前のチェックリスト
- セットアップステップ
- 検証
- トラブルシューティング
- 高度な設定

---

## セットアップ前のチェックリスト

セットアップを開始する前に、以下があることを確認してください：

```
セットアップ要件：
- [ ] Difyアカウントが作成されている（cloud.dify.aiまたは自己ホスト）
- [ ] Difyログインメールとパスワード
- [ ] Dockerがインストールされている（docker --versionでバージョンが表示される）
- [ ] Gitリポジトリがローカルにクローンされている
- [ ] ターミナル/CLIアクセス
- [ ] 安定したインターネット接続
```

### クイック検証

```bash
# Dockerがインストールされているか確認
docker --version
# 出力例：Docker version 20.x.x or higher

# Gitを確認
git --version
# 出力例：git version 2.x.x or higher
```

---

## セットアッププロセス

### ステップ1：情報を収集

**Dify Cloud（推奨）**：
```
URL: https://cloud.dify.ai
メール：your-email@example.com
パスワード：your-dify-password
SSL検証：はい（デフォルトのまま）
```

**自己ホスト型Dify**：
```
URL: http://your-server-ip:5001
メール：your-email@example.com
パスワード：your-password
SSL検証：証明書による
```

### ステップ2：セットアップを実行

```bash
# Claudeにプロジェクトをセットアップするよう依頼：
/setting-up-dify-project
```

または手動で：

```bash
# テンプレートから.envを作成（存在しない場合）
test -f .env || cp .env.example .env

# .envを認証情報で編集
# （下記の値を参照）
```

### ステップ3：設定を提供

Claudeが以下を求めます：

1. **Dify URL**
   - クラウド：`https://cloud.dify.ai`（デフォルト）
   - 自己ホスト型：`http://your-server:5001`

2. **メール**
   - Difyアカウントメール
   - 例：`user@example.com`

3. **パスワード**
   - Difyアカウントパスワード
   - `.env`で安全に保管

4. **SSL検証**（自己ホスト型の場合）
   - `true`有効なSSL証明書用（推奨）
   - `false`自己署名証明書用

### ステップ4：自動設定

Claudeがセットアップ：

```bash
# 1. .envファイルを作成/更新
DIFY_BASE_URL=https://cloud.dify.ai
DIFY_EMAIL=your-email@example.com
DIFY_PASSWORD=your-password
DIFY_VERIFY_SSL=true

# 2. Dockerイメージをビルド
docker compose build

# 3. 接続をテスト
docker compose run --rm dify-creator login

# 4. 成功メッセージを表示
# セットアップ完了！アプリを作成する準備ができました。
```

### ステップ5：セットアップを検証

成功は次のようになります：

```
✅ 設定が作成されました
✅ Dockerイメージがビルドされました
✅ 接続テストが成功しました
✅ アプリ作成の準備ができました
```

---

## セットアップ成功後

### すべてが機能するかテスト

```bash
# ログインをテスト（静かに成功するはず）
docker compose run --rm dify-creator login

# 成功した場合、エラーメッセージは表示されません
# 失敗した場合、エラーが表示されます。報告してください
```

### 作成されたもの

```
.env                          # 認証情報（Gitにコミットしないこと）
（dockerイメージ）            # ビルドされ使用準備完了
.docker/                      # Dockerファイル（必要に応じて作成）
```

### 使用準備完了

これでできるようになります：
- 新しいDifyアプリを作成：`/managing-dify-apps`
- 既存のアプリを編集：`/managing-dify-apps`
- プロジェクトを管理

---

## 詳細設定オプション

### `.env`ファイル

セットアップはこれらの変数を持つ`.env`を作成します：

| 変数 | 意味 | 例 |
|----------|---------|---------|
| `DIFY_BASE_URL` | Difyサーバーアドレス | `https://cloud.dify.ai` |
| `DIFY_EMAIL` | Difyアカウントメール | `user@example.com` |
| `DIFY_PASSWORD` | Difyパスワード | `your-secure-password` |
| `DIFY_VERIFY_SSL` | SSL証明書を検証 | `true`または`false` |

### Dify Cloudの場合

```env
DIFY_BASE_URL=https://cloud.dify.ai
DIFY_EMAIL=your-email@example.com
DIFY_PASSWORD=your-password
DIFY_VERIFY_SSL=true
```

### 有効なSSL付きの自己ホスト型

```env
DIFY_BASE_URL=https://your-domain.com:5001
DIFY_EMAIL=your-email@example.com
DIFY_PASSWORD=your-password
DIFY_VERIFY_SSL=true
```

### 自己署名証明書を持つ自己ホスト型

```env
DIFY_BASE_URL=https://your-domain.com:5001
DIFY_EMAIL=your-email@example.com
DIFY_PASSWORD=your-password
DIFY_VERIFY_SSL=false
```

### ローカル開発の場合

```env
DIFY_BASE_URL=http://localhost:5001
DIFY_EMAIL=your-email@example.com
DIFY_PASSWORD=your-password
DIFY_VERIFY_SSL=false
```

---

## 検証ステップ

### ステップ1：.envが存在するか確認

```bash
# ファイルが存在し、空でない必要があります
test -f .env && wc -l .env
# 出力例：4 .env（または同様）
```

### ステップ2：接続を確認

```bash
# これはエラーなしで成功するはず
docker compose run --rm dify-creator login

# 成功：出力なしまたは「ログイン成功」
# 失敗：認証情報または接続に関するエラーメッセージ
```

### ステップ3：Dockerイメージを確認

```bash
# Dockerイメージが利用可能である必要があります
docker images | grep dify-creator
# イメージがリストされているはず
```

### ステップ4：テストを実行

その他のセットアップステップを完了した後：

```bash
# セットアップ全体を検証
docker compose run --rm dify-creator validate --dsl examples/templates/1_simple_chatbot.dsl.yml
# 出力：✅ 検証成功
```

---

## セットアップのトラブルシューティング

### 「.envが見つかりません」または「.envが空です」

**問題**：設定ファイルが見つかりません。

**解決方法**：
```bash
# テンプレートから作成
cp .env.example .env

# 認証情報で編集
nano .env  # （または好みのエディタ）

# 確認
cat .env
```

### 「Dockerがインストールされていません」

**問題**：Dockerコマンドが見つかりません。

**解決方法**：
1. Docker DesktopまたはDocker Engineをインストール
   - Mac: https://docs.docker.com/desktop/install/mac-install/
   - Windows: https://docs.docker.com/desktop/install/windows-install/
   - Linux: https://docs.docker.com/engine/install/

2. インストールを確認：
   ```bash
   docker --version
   ```

### 「認証失敗」または「ログインエラー」

**問題**：認証情報が誤っているか、アカウントが存在しません。

**解決方法**：

1. **認証情報を確認**：
   - メールは正しいですか？（アカウントログインメールである必要があります）
   - パスワードは正しいですか？（キャップスロック、特殊文字を確認）
   - パスワードは最近変更されていますか？

2. **認証情報を手動でテスト**：
   - Dify web UIにログイン（https://cloud.dify.ai）
   - メール/パスワードがそこで機能することを確認

3. **.envを更新**：
   ```bash
   nano .env
   # DIFY_EMAIL と DIFY_PASSWORD を修正
   ```

4. **ログインを再試行**：
   ```bash
   docker compose run --rm dify-creator login
   ```

### 「接続タイムアウト」または「サーバーに到達できません」

**問題**：Difyサーバーに接続できません。

**解決方法**：

1. **インターネット接続を確認**：
   ```bash
   ping cloud.dify.ai  # クラウド版の場合
   # レスポンスを返す必要があります
   ```

2. **.envのURLを確認**：
   ```bash
   grep DIFY_BASE_URL .env
   # 正しいURLが表示されるはず
   ```

3. **自己ホスト型Difyの場合**：
   - サーバーは実行されていますか？
   - URLは正しく、アクセス可能ですか？
   - ブラウザでテスト：`http://your-server:5001`

4. **ファイアウォール/プロキシの問題**：
   - ファイアウォールが接続をブロックしているか確認
   - 企業プロキシの設定が必要か確認

### 「Dockerビルド失敗」

**問題**：Dockerイメージビルドがエラーに遭遇しました。

**解決方法**：

1. **Dockerデーモンを確認**：
   ```bash
   docker ps
   # エラーが出た場合、Dockerデーモンが実行されていません
   ```

2. **ビルドを再試行**：
   ```bash
   docker compose build --no-cache
   ```

3. **ディスク容量を確認**：
   ```bash
   df -h /
   # 最低5GB空いている必要があります
   ```

### 「ポートが既に使用中」

**問題**：Dockerが必要なポートにバインドできません。

**解決方法**：

1. **ポートを使用しているプロセスを検出**：
   ```bash
   # Mac/Linuxの場合：
   lsof -i :5001

   # Windowsの場合：
   netstat -ano | findstr :5001
   ```

2. **`docker-compose.yml`のポートを変更**：
   ```yaml
   services:
     dify-creator:
       ports:
         - "5002:5001"  # 5001から5002に変更
   ```

---

## 高度な設定

### 複数の環境

複数のDifyインスタンスを管理する必要がある場合：

```bash
# 別々の.envファイルを作成
.env.cloud          # クラウドインスタンス
.env.local          # ローカル開発
.env.staging        # ステージングサーバー

# 特定の環境をロード
DIFY_ENV_FILE=.env.staging docker compose run --rm dify-creator login
```

### .envの代わりに環境変数を使用

```bash
# 変数を直接設定（.envより優先）
export DIFY_BASE_URL=https://cloud.dify.ai
export DIFY_EMAIL=user@example.com
export DIFY_PASSWORD=password

docker compose run --rm dify-creator login
```

### プロキシ設定

企業プロキシの背後にある場合：

```bash
# .envに追加
HTTP_PROXY=http://proxy-server:port
HTTPS_PROXY=http://proxy-server:port
NO_PROXY=localhost,127.0.0.1
```

---

## セキュリティベストプラクティス

✅ **すべきこと：**
- `.env`ファイルを安全に保管（Gitにコミットしない）
- 強力なパスワードを使用
- パスワードを定期的にローテーション
- `.env`を`.gitignore`に追加（すでに実行されているはず）
- 可能な場合Dify URLにHTTPSを使用
- SSL証明書を検証

❌ **してはいけないこと：**
- `.env`ファイルを他人と共有
- `.env`をバージョン管理にコミット
- 簡単に推測できるパスワードを使用
- プロダクション環境でデフォルト認証情報を残す
- SSL検証を無効にする（必要な場合のみ：自己署名証明書）

---

## セキュリティの確認

```bash
# .envが.gitignoreにあるか確認
grep .env .gitignore
# 出力：.env

# .envがコミットされないか確認
git status
# 変更内容に.envが表示されない必要があります
```

---

## セットアップをリセット

最初からやり直す必要がある場合：

```bash
# オプション1：認証情報を更新
nano .env
# DIFY_EMAIL と DIFY_PASSWORD を編集

# オプション2：Dockerイメージを再ビルド
docker compose down
docker compose build --no-cache

# オプション3：完全にリセット
rm .env
rm -rf .docker
# その後セットアップを再実行
```

---

## ヘルプを得る

セットアップがまだ失敗する場合：

1. **エラーメッセージを収集**：
   ```bash
   docker compose run --rm dify-creator login 2>&1 | tee setup-error.log
   ```

2. **ログをチェック**：
   ```bash
   cat setup-error.log
   ```

3. **エラーをClaudeと共有**：
   - エラーメッセージ
   - しようとしていたこと
   - システム（Mac/Windows/Linux）
   - Difyバージョン（自己ホスト型の場合）

---

## セットアップ後の次のステップ

セットアップが完了したら：

1. **最初のアプリを作成**：
   - `/managing-dify-apps`を使用
   - テンプレートを選択
   - アプリを作成してテスト

2. **テストアプリを作成して接続が機能することを確認**

3. **テンプレートについて学ぶ**：
   - [../managing-dify-apps/reference/templates.md](../managing-dify-apps/reference/templates.md)を参照

4. **ワークフローを調査**：
   - [../managing-dify-apps/reference/workflows.md](../managing-dify-apps/reference/workflows.md)を参照
