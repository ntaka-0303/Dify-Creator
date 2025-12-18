# Dify-Creator：Difyアプリを簡単に作成・編集するツール

**ClaudeCode のコマンド（Commands）を選ぶだけで、ブラウザを開かずにDifyアプリを作ったり修正したりできます。**

> **✨ 最新版の特徴：** ターミナルコマンド不要。ClaudeCode に「どんなアプリを作りたいか」説明するだけで、ClaudeCode が YAML 生成・Dify 登録・テスト実行をすべて自動で行います。

---

## 🎯 使い方は簡単：2パターン

### 1️⃣ **新しいアプリを作る**
```
チャットで `/dify-new-app` を選ぶ
    ↓
「どんなアプリを作りたいか」説明
    ↓
ClaudeCode が自動で作成・テスト
    ↓
完成！
```

### 2️⃣ **既存のアプリを修正する**
```
チャットで `/dify-edit-app` を選ぶ
    ↓
アプリのIDと「どう修正したいか」を説明
    ↓
ClaudeCode が自動で修正・テスト
    ↓
完成！
```

**つまり、ブラウザは一度も開きません。説明するだけです。**

---

## 🚀 最初の1回だけ：初期化

### ステップ1：ClaudeCode で `/dify-setup` を実行

チャット画面で `/` を入力して、`dify-setup` を選んでください。

または直接：
```
/dify-setup
```

### ステップ2：情報を入力（ClaudeCode が聞いてきます）

以下を答えるだけです：

- **Dify のURL** - `https://cloud.dify.ai` を選ぶ（推奨）
- **メールアドレス** - Dify にログインするメール
- **パスワード** - Dify にログインするパスワード

> **ヒント：** Dify のアプリ APIキーではなく、アカウントそのもののログイン情報です。

### ステップ3：完了！

ClaudeCode が以下を自動でやってくれます：
- 設定ファイル（.env）の作成
- Docker のビルド
- 接続テスト

成功メッセージが出たら、準備完了です。

---

## ✨ 使用開始：新規アプリ作成

### `/dify-new-app` を実行

チャット画面で：
```
/dify-new-app
```

### ClaudeCode が質問してきます

1. **どんなアプリを作りたいですか？**
   - 例：「顧客からの質問に自動で答えるチャットボット」
   - 例：「テキストを要約するアプリ」
   - できるだけ詳しく説明してください

2. **アプリの種類は？**（ClaudeCode が提案する場合があります）
   - Q&Aチャットボット
   - ワークフロー
   - 複雑な判定
   - API連携

### ClaudeCode が自動で実行

以下をすべて自動で行います：

1. テンプレートを選択
2. YAML ファイル（アプリの設定）を生成
3. Dify に登録
4. テスト実行
5. 結果を表示

### 完成！

アプリが完成しました。

- 修正が必要な場合は、その説明を ClaudeCode に伝える
- ClaudeCode が修正して、テスト実行
- 何度でも繰り返し可能

---

## ✏️ 既存アプリを修正

### `/dify-edit-app` を実行

チャット画面で：
```
/dify-edit-app
```

### ClaudeCode が質問してきます

1. **アプリの ID は？**
   - Dify のウェブサイトで、アプリの URL から ID をコピー
   - 例：`https://cloud.dify.ai/app/abc123def456/overview`
   - → `abc123def456` がID です

2. **何を修正したいですか？**
   - 例：「プロンプトをもっと丁寧な回答にする」
   - 例：「テキストの言語を英語から日本語に変える」
   - できるだけ詳しく説明してください

### ClaudeCode が自動で実行

1. Dify からアプリをダウンロード
2. 修正を反映
3. 修正内容をプレビュー（OK かどうか確認）
4. Dify に上書き保存
5. テスト実行
6. 結果を表示

### 修正が完成するまで繰り返し

結果がおかしい場合：
- 「何が違うか」ClaudeCode に説明
- ClaudeCode が再度修正・テスト
- OK になるまで繰り返し

---

## 📋 実務流：何度も修正する場合

完成まで、ClaudeCode とやり取りするだけです。

```
1. 「プロンプトを変更したい」と説明
            ↓
2. ClaudeCode が自動修正・テスト実行
            ↓
3. 結果を確認
            ↓
4. OK なら完成、ダメなら「こう変更して」と説明
```

**ターミナルコマンドは一度も不要です。**

---

## 🆘 よくある質問

### Q: エラーが出た

**A:** ClaudeCode に「エラーが出た」と伝えてください。ClaudeCode が原因を特定して修正します。

### Q: テンプレートを見たい

**A:** 以下に 5 つのテンプレート例があります：

| テンプレート | 用途 |
|-----------|------|
| 1_simple_chatbot.dsl.yml | Q&A チャットボット |
| 2_echo_workflow.dsl.yml | シンプルなワークフロー |
| 3_llm_workflow.dsl.yml | 標準的なワークフロー |
| 4_conditional_workflow.dsl.yml | 複雑な判定処理 |
| 5_http_api_workflow.dsl.yml | 外部 API 連携 |

```bash
cat examples/templates/3_llm_workflow.dsl.yml
```

で見ることができます。

### Q: 複雑なアプリを作りたい

**A:** 最初は簡単な版を作ってから、少しずつ修正してください。

1. 簡単な版を `/dify-new-app` で作成
2. `/dify-edit-app` で少しずつ機能追加

### Q: 複数人で開発したい

**A:** Git を使用してください。

1. このリポジトリをチーム全員で共有
2. 各メンバーが `/dify-edit-app` で修正
3. Git で変更管理

### Q: アプリを公開したい

**A:** 修正が完成したら、Dify のウェブサイトで「公開」ボタンを押すだけです。

修正は常に「ドラフト」状態で行われているので、公開ボタンで本番環境に出ます。

### Q: YAML（アプリの設定ファイル）を直接編集したい

**A:** `app.dsl.yml` をテキストエディタで直接編集してから、以下を実行：

```bash
/dify-sync
```

ClaudeCode が修正を Dify に反映してテストします。

---

## 📚 詳しく学ぶ

### ドキュメント

| ドキュメント | 説明 |
|-----------|------|
| [DSL仕様書](./docs/DSL_SPECIFICATION.md) | YAML ファイルの詳細仕様 |
| [開発ワークフロー](./docs/CLAUDECODE_WORKFLOW.md) | より詳しい使い方 |
| [テンプレート例](./examples/templates/) | 実装例 5 つ |

### Commands

| Command | 説明 |
|---------|------|
| `/dify-setup` | 初回セットアップ |
| `/dify-new-app` | 新規アプリ作成（メイン） |
| `/dify-edit-app` | 既存アプリ編集（メイン） |
| `/dify-export` | Dify からダウンロード |
| `/dify-sync` | YAML を修正してアップロード |

> **ほとんどの場合、`/dify-new-app` と `/dify-edit-app` だけで十分です。**

---

## 💻 ターミナルコマンド（参考）

**通常は不要ですが、参考までに：**

```bash
# ログイン確認
docker compose run --rm dify-creator login

# DSL 検証
docker compose run --rm dify-creator validate --dsl app.dsl.yml

# ダウンロード
docker compose run --rm dify-creator export --app-id YOUR_APP_ID --out app.dsl.yml

# アップロード＋テスト
docker compose run --rm dify-creator sync \
  --dsl app.dsl.yml \
  --app-id YOUR_APP_ID \
  --inputs-json examples/inputs.json
```

---

## ✨ このツールの利点

✅ ブラウザ（Dify Studio）を開かない
✅ ClaudeCode だけで完結
✅ ファイルベース（Git で管理可能）
✅ 修正が素早い（説明 → 自動実行）
✅ チーム開発が容易

---

## 🎓 用語解説

| 用語 | 説明 |
|------|------|
| **DSL** | ファイルベースのアプリ設定（YAML 形式） |
| **app_id** | Dify アプリの ID（編集時に使用） |
| **Dify** | AI ワークフロー構築プラットフォーム |
| **ドラフト** | 公開前の編集状態 |
| **YAML** | テキストベースの設定ファイル形式 |

---

## 📖 参考資料

- [Dify 公式ドキュメント](https://docs.dify.ai/)
- [DSL 詳細仕様](./docs/DSL_SPECIFICATION.md)
- [開発ワークフロー詳細ガイド](./docs/CLAUDECODE_WORKFLOW.md)

---

## 🚀 最初のステップ

1. チャットで `/dify-setup` を実行
2. 設定を入力
3. `/dify-new-app` または `/dify-edit-app` を実行
4. 説明を入力
5. ClaudeCode が自動で完成させる

**それだけです！**

---

## 📝 プロジェクト改善履歴

### ✨ 最新版での改善（v0.2.0）

このバージョンでは、**非エンジニア向けの UX を大幅に改善**しました。

#### 🎯 主な改善点

| 改善 | Before | After |
|------|--------|-------|
| **セットアップ** | `.env` を手動編集 | `/dify-setup` で全自動 |
| **アプリ作成** | CLI コマンド + YAML 手動作成 | `/dify-new-app` で全自動 |
| **アプリ編集** | CLI コマンド + YAML 手動編集 | `/dify-edit-app` で全自動 |
| **必要なスキル** | ターミナル操作、YAML編集知識 | ClaudeCode に説明するだけ |
| **所要時間** | 15分以上 | 2-3分 |

#### 🔧 技術的な改善

1. **新しい Commands を追加**
   - `/dify-new-app` - 新規アプリ作成の完全自動化
   - `/dify-edit-app` - 既存アプリ編集の完全自動化

2. **既存 Commands を改善**
   - `/dify-setup` - .env 設定を完全自動化
   - 他の Commands をエージェント向けに最適化

3. **ClaudeCode 統合の強化**
   - ClaudeCode がユーザーに質問を投げかけ、情報を収集
   - ClaudeCode が YAML を自動生成・修正
   - ClaudeCode がテスト実行と結果分析を自動化

4. **ドキュメント刷新**
   - README を Command 中心のガイドに改版
   - 非エンジニア向けの説明に統一
   - ターミナルコマンドは「参考」欄に移動

#### 📚 ドキュメント充実

新しく追加：
- [ClaudeCode 開発ワークフロー](./docs/CLAUDECODE_WORKFLOW.md) - 詳細ガイド
- [DSL 仕様書](./docs/DSL_SPECIFICATION.md) - 技術仕様
- [Command ドキュメント](./claude/commands/) - 各 Command の説明
- **5 つの DSL テンプレート例** - 実装リファレンス

### 利用者からのフィードバック

このバージョンは以下の課題を解決しました：

✅ **「ターミナルコマンドが複雑で難しい」**
→ ClaudeCode で説明するだけに変更

✅ **「YAML ファイルを手動で編集するのは難しい」**
→ ClaudeCode が自動生成・修正に変更

✅ **「セットアップが複雑」**
→ `/dify-setup` で全自動に変更

✅ **「どのテンプレートを使えばいいか分からない」**
→ ClaudeCode が質問してテンプレートを選択

---

## 🎓 旧バージョン（v0.1.0）から v0.2.0 への移行

旧バージョンをお使いの場合、以下の方法で最新版に更新できます：

### コマンド（推奨）

最新版のコマンドを使用してください：

```bash
/dify-setup      # 旧版：手動での .env 編集が必要
                 # 新版：質問に答えるだけで自動化

/dify-new-app    # 新しいコマンド：ワンコマンドで新規作成

/dify-edit-app   # 新しいコマンド：ワンコマンドで編集
```

### テンプレート

新しい 5 つのテンプレートが利用可能：

```
examples/templates/
├── 1_simple_chatbot.dsl.yml
├── 2_echo_workflow.dsl.yml
├── 3_llm_workflow.dsl.yml
├── 4_conditional_workflow.dsl.yml
└── 5_http_api_workflow.dsl.yml
```

---

## 💡 このツールが生まれた背景

Dify Studio（ブラウザUI）は使いやすいですが：

- 🖥️ **ブラウザを開く手間がある**
- 📝 **複雑な修正は手探りで時間がかかる**
- 🤝 **チーム開発でバージョン管理が難しい**
- 🔄 **同じアプリを複数環境に展開しにくい**

このツールは**ファイル + ClaudeCode ベース**で、これらの課題を解決します：

✅ ClaudeCode だけで完結
✅ 説明するだけで自動実行
✅ Git でバージョン管理可能
✅ CI/CD パイプラインに組み込み可能

---

## 🚀 今後のロードマップ

- [ ] Skill を追加（YAML 検証・デバッグのビジュアル化）
- [ ] 複数アプリの一括管理機能
- [ ] テスト入力の自動生成
- [ ] API 連携の簡潔なサポート
- [ ] Web UI での実行結果ビジュアライズ

---

## 📧 フィードバック・貢献

このプロジェクトは **改善提案を大歓迎**です。

- 🐛 バグ報告
- 💡 機能提案
- 📚 ドキュメント改善
- 🎨 UX/UX 改善

→ GitHub Issues または Pull Request でお知らせください。
