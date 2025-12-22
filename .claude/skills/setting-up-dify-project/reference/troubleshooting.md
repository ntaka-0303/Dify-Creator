# セットアップのトラブルシューティング

一般的なセットアップの問題と解決方法です。

## 目次
- 認証情報の問題
- Dockerと環境の問題
- 接続の問題
- ファイル権限の問題
- プラットフォーム固有の問題

---

## 認証情報の問題

### 「無効な認証情報」または「認証失敗」

**症状：**
```
Error: Invalid email or password
Error: Unauthorized
```

**根本的な原因と解決方法：**

1. **間違ったメール形式**：
   - **アカウントメール**を使用していることを確認（APIキーではなく）
   - タイプミスと余分なスペースを確認
   - メールがDifyアカウントに関連付けられていることを確認

2. **パスワード間違い**：
   - 最初にweb UIで<bログインを試す（https://cloud.dify.ai）
   - パスワードがそこで機能することを確認
   - 最近変更されていないか確認

3. **間違ったDifyインスタンス**：
   - クラウドユーザー：`https://cloud.dify.ai`であることを確認
   - 自己ホスト型：正しいURLとポートを使用
   - 例：`http://localhost:5001`または`https://dify.company.com`

**修正手順：**

```bash
# 1. 最初にDify web UIで認証情報を確認
# https://cloud.dify.ai にアクセスして手動でログイン

# 2. 正しい値で.envを更新
nano .env
# 正しい：
# DIFY_EMAIL=your-actual-email@example.com
# DIFY_PASSWORD=your-actual-password
# DIFY_BASE_URL=https://cloud.dify.ai

# 3. ログインを再度テスト
docker compose run --rm dify-creator login
```

---

### 「アカウントがロック」または「ログイン試行が多すぎます」

**症状：**
```
Error: Account locked. Too many failed attempts.
```

**解決方法：**

1. **15～30分待機**してから再試行
2. **認証情報が正しいことを確認**
3. **パスワードをリセット**（Dify web UIで可能な場合）
4. **長時間ロックされている場合はDifyサポートに連絡**

---

## Dockerと環境の問題

### 「Dockerがインストールされていません」または「dockerコマンドが見つかりません」

**症状：**
```
Command 'docker' not found
```

**解決方法：**

1. **Dockerをインストール**：
   - Mac: https://docs.docker.com/desktop/install/mac-install/
   - Windows: https://docs.docker.com/desktop/install/windows-install/
   - Linux: https://docs.docker.com/engine/install/

2. **インストールを確認**：
   ```bash
   docker --version
   # 出力例：Docker version 20.x or higher
   ```

3. **Dockerデーモンを開始**（インストール済みだが実行されていない場合）：
   - **Mac**：Docker Desktopアプリ
   - **Windows**：Docker Desktopアプリ
   - **Linux**：`sudo systemctl start docker`

---

### 「Dockerデーモンが実行されていません」

**症状：**
```
Error: Cannot connect to Docker daemon at unix:///var/run/docker.sock
```

**解決方法：**

1. **Mac/Windowsの場合**：Docker Desktopアプリケーションを開く
2. **Linuxの場合**：
   ```bash
   sudo systemctl start docker
   # または：
   sudo service docker start
   ```

3. **実行していることを確認**：
   ```bash
   docker ps
   # 実行中のコンテナをリストアップ（空の場合がある）
   ```

---

### 「Dockerビルド失敗」

**症状：**
```
Error during build: ...
Failed to build image
```

**解決方法：**

1. **クリーンリビルド**（キャッシュを削除）：
   ```bash
   docker compose build --no-cache
   ```

2. **ディスク容量を確認**：
   ```bash
   df -h /
   # 最低5GB空いている必要があります
   # 少ない場合：未使用のDockerイメージ/コンテナを削除
   ```

3. **インターネット接続を確認**：
   - ビルドはインターネットから依存関係をダウンロード
   - 接続が安定していることを確認

4. **詳細出力で再試行**：
   ```bash
   docker compose build --verbose
   # 失敗の詳細を表示
   ```

---

### 「.envファイルが見つかりません」または「.envが見つかりません」

**症状：**
```
Error: .env file not found
Error: Cannot read .env
```

**解決方法：**

```bash
# .envが存在するか確認
ls -la .env

# 見つからない場合、作成：
cp .env.example .env

# 作成されたことを確認
cat .env

# 認証情報で編集
nano .env  # または好みのエディタ
```

---

### 「.envが空または無効です」

**症状：**
```
Configuration empty
Variables not loaded
```

**解決方法：**

```bash
# ファイルサイズを確認
wc -l .env
# 4行以上が表示されるはず

# 空またはが破損している場合、テンプレートから復元
cat .env.example > .env

# 値で編集
nano .env
```

---

## 接続の問題

### 「Difyに接続できません」

**症状：**
```
Error: Connection refused
Error: Failed to connect to https://cloud.dify.ai
```

**解決方法：**

1. **インターネット接続を確認**：
   ```bash
   ping google.com
   # レスポンスを受け取るべき
   ```

2. **Difyへの接続をテスト**：
   ```bash
   # クラウドの場合：
   ping cloud.dify.ai

   # 自己ホスト型の場合：
   ping your-server-ip
   ```

3. **.envのURLを確認**：
   ```bash
   grep DIFY_BASE_URL .env
   # 表示例：DIFY_BASE_URL=https://cloud.dify.ai
   # （または自己ホスト型のURL）
   ```

4. **DNS解決を確認**：
   ```bash
   nslookup cloud.dify.ai
   # IPアドレスが表示されるべき
   ```

---

### 「接続タイムアウト」

**症状：**
```
Error: Connection timed out
Error: Timed out connecting to server
```

**解決方法：**

1. **`.env`でタイムアウトを増加**：
   ```bash
   # 追加または変更
   CONNECTION_TIMEOUT=30
   REQUEST_TIMEOUT=60
   ```

2. **ファイアウォールを確認**：
   - ポート443（HTTPS）をブロックしている可能性
   - 自己ホスト型：ポート5001を確認

3. **ネットワーク/プロキシを確認**：
   - 企業ファイアウォール？
   - プロキシが必要？
   - 異なるネットワークから接続を試す

4. **サーバーが実行されていることを確認**：
   - 自己ホスト型：Difyが実行されているか？
   - 確認：`curl http://your-server:5001`

---

### 「SSL証明書エラー」

**症状：**
```
Error: Certificate verification failed
Error: SSL: CERTIFICATE_VERIFY_FAILED
```

**解決方法：**

1. **自己署名証明書用**（開発のみ）：
   ```bash
   # .envを編集
   DIFY_VERIFY_SSL=false
   ```

2. **実際の証明書の場合**：
   - 証明書が有効で有効期限が切れていないことを確認
   - 証明書チェーンを確認
   - システム証明書を更新

3. **SSLを無視して接続をテスト**：
   ```bash
   # デバッグのみ
   curl -k https://your-server:5001
   # -k はSSLエラーを無視
   ```

---

### 「プロキシまたはファイアウォールがブロック」

**症状：**
```
Error: Cannot reach Dify
Works on different network
```

**解決方法：**

1. **`.env`でプロキシを設定**：
   ```bash
   HTTP_PROXY=http://proxy-server:8080
   HTTPS_PROXY=http://proxy-server:8080
   NO_PROXY=localhost,127.0.0.1
   ```

2. **プロキシ設定でテスト**：
   ```bash
   docker compose run --rm dify-creator login
   # これでプロキシ経由で接続すべき
   ```

3. **ネットワーク管理者に確認**：
   - Difyドメインをホワイトリスト登録する必要があるかもしれません
   - VPNが必要かもしれません
   - 企業プロキシ証明書が必要かもしれません

---

## ファイルと権限の問題

### 「アクセス許可が拒否されました」または「.envに書き込めません」

**症状：**
```
Error: Permission denied while trying to open '.env'
```

**解決方法：**

```bash
# 現在の権限を確認
ls -la .env

# 読み取り/書き込み可能にする
chmod 600 .env

# 確認
ls -la .env
# 表示：-rw------- （または書き込み権限付き）
```

---

### 「docker composeを実行できません」

**症状：**
```
Error: docker-compose: command not found
Or: docker: 'compose' is not a command
```

**解決方法：**

1. **Docker Composeがインストールされているか確認**：
   ```bash
   docker compose version
   # 最新：動作するはず
   # 古い：代わりに`docker-compose`を試す
   ```

2. **Docker Composeをインストール**（必要に応じて）：
   - 通常Docker Desktopに付属
   - Linux：https://docs.docker.com/compose/install/

---

### 「docker-compose.ymlを読み込めません」

**症状：**
```
Error: Cannot locate docker-compose.yml
```

**解決方法：**

```bash
# 正しいディレクトリにいることを確認
pwd
# 表示：/path/to/Dify-Creator

# ファイルが存在するか確認
ls docker-compose.yml
# 現在のディレクトリに存在するはず
```

---

## プラットフォーム固有の問題

### macOS問題

**Docker Desktopが起動しない**：
```bash
# 再起動を試す
pkill Docker
open /Applications/Docker.app

# ログを確認
cat ~/Library/Containers/com.docker.docker/data/log/vm/docker.log
```

**権限の問題**：
```bash
# sudoが必要かもしれません
sudo docker compose run --rm dify-creator login

# または権限を修正
sudo chown -R $(whoami) .
```

---

### Windows問題

**Docker Desktopが起動しない**：
1. Hyper-Vが有効になっているか確認
2. WSL 2がインストールされているか確認
3. 設定からDocker Desktopを再起動

**パスの問題**：
- パスでフォワードスラッシュを使用：`C:/Users/Name/project`
- バックスラッシュではなく：`C:\Users\Name\project`

**ターミナルの問題**：
- PowerShellを使用、コマンドプロンプトではなく
- またはWindows Terminal（推奨）を使用

---

### Linux問題

**Dockerデーモン権限**：
```bash
# ユーザーをdockerグループに追加
sudo usermod -aG docker $USER

# グループ変更を適用
newgrp docker

# 確認
docker ps
# これでsudoなしで動作するべき
```

**ファイアウォールの問題**：
```bash
# Dockerを許可
sudo ufw allow 5001
# （ufwを使用している場合）
```

---

## 検証チェックリスト

セットアップが完了したと宣言する前に、確認：

```
✅ Dockerがインストールされ実行中
   docker --version

✅ Docker Composeが利用可能
   docker compose version

✅ .envファイルが存在し認証情報がある
   cat .env | grep DIFY

✅ 接続テストが成功
   docker compose run --rm dify-creator login

✅ サンプルテンプレートが検証済み
   docker compose run --rm dify-creator validate --dsl examples/templates/1_simple_chatbot.dsl.yml

✅ .envがgitにない
   git status | grep .env
   （何も表示されないはず）
```

---

## ヘルプを得る

まだ動かない場合：

1. **診断情報を収集**：
   ```bash
   # システム情報
   uname -a                    # Mac/Linux
   systeminfo                  # Windows

   # Docker情報
   docker --version
   docker compose version
   docker ps

   # セットアップ情報
   cat .env | grep -v PASSWORD
   docker compose run --rm dify-creator login
   ```

2. **出力を保存**：
   ```bash
   # 共有しやすいようにファイルにリダイレクト
   docker compose run --rm dify-creator login 2>&1 | tee setup-error.log
   cat setup-error.log
   ```

3. **Claudeと共有**：
   - しようとしていたことを説明
   - エラーメッセージを含める
   - システム情報を含める
   - 実行したセットアップステップを含める

---

## クイック修正チェックリスト

**「動作しません、どうするんですか？」**

次の順序で試してください：

1. ✅ **Dockerを再起動**：Docker Desktopを閉じる / `sudo systemctl restart docker`
2. ✅ **.envを更新**：認証情報が正しいことを確認
3. ✅ **クリーンリビルド**：`docker compose build --no-cache`
4. ✅ **接続を確認**：`ping cloud.dify.ai`（またはサーバー）
5. ✅ **ディスク容量を確認**：`df -h /`（5GB必要）
6. ✅ **古いコンテナを削除**：`docker compose down`その後`docker compose up`

それでも動かない → 診断情報を収集してClaudeに助けを求めてください。
