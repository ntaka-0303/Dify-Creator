# トラブルシューティングガイド

Difyアプリ管理ツール使用時の一般的な問題と解決方法です。

## 目次
- 接続と認証の問題
- 検証エラー
- テスト実行の問題
- ワークフローエラー
- モデル設定の問題
- 問題を防ぐためのベストプラクティス

---

## 接続と認証の問題

### 「接続が拒否されました」または「Difyに接続できません」

**症状：**
```
Error: Could not connect to https://cloud.dify.ai
Connection refused
```

**解決方法：**

1. **インターネット接続を確認**
   ```bash
   ping cloud.dify.ai
   ```

2. **`.env`のDify認証情報を確認**：
   ```bash
   cat .env | grep DIFY
   ```

3. **ログイン手動テスト**（ローカルDifyインスタンスの場合）：
   ```bash
   docker compose run --rm dify-creator login
   ```

4. **URLフォーマットを確認**：
   - クラウド：`https://cloud.dify.ai` ✅
   - ローカル：`http://localhost:5001`（HTTPS不要） ✅
   - カスタム：URLが完全かつアクセス可能であることを確認

5. **自己ホスト型DifyでSSLの問題がある場合**：
   - 自己署名証明書を使用している場合は、`.env`を更新：
     ```
     DIFY_VERIFY_SSL=false
     ```

---

### 「無効な認証情報」または「認証失敗」

**症状：**
```
Error: Invalid email or password
```

**解決方法：**

1. **認証情報が正しいか確認**：
   - Difyアカウントメールアドレスを使用していますか？（APIキーではなく）
   - パスワードは正しいですか？
   - パスワードは最近変更されていませんか？

2. **`.env`を正しい認証情報で更新**：
   ```bash
   # .env を編集
   DIFY_EMAIL=your-actual-email@example.com
   DIFY_PASSWORD=your-actual-password
   ```

3. **セットアップを再実行**：
   ```bash
   /dify-setup
   ```

4. **接続をテスト**：
   ```bash
   docker compose run --rm dify-creator login
   ```

---

## 検証エラー

### 「検証失敗：必須フィールドが見つかりません」

**症状：**
```
❌ Validation failed (2 errors):
  - Required field 'workflow' not found
  - 'app.mode' is invalid
```

**原因：** YAML構造が不完全であるか、モードが誤っています。

**解決方法：**

1. **app.modeが設定と一致するか確認**：
   ```yaml
   app:
     mode: "chat"      # または "workflow" または "agent"
   ```

2. **必須セクションが存在することを確認**：
   - `mode: chat`の場合 → `model_config`セクションが必要
   - `mode: workflow`の場合 → `workflow`セクションが必要
   - `mode: agent`の場合 → `model_config`セクションが必要

3. **テンプレートを参考に使用**：[templates.md](templates.md)を参照

---

### 「無効なフィールド値」または「型の不一致」

**症状：**
```
Error: 'temperature' must be a number between 0.0 and 1.0
Error: 'max_tokens' must be a positive integer
```

**解決方法：**

1. **フィールドの型を確認**：
   ```yaml
   # ✅ 正しい
   temperature: 0.7          # 数字
   max_tokens: 2048          # 整数
   system_prompt: "text"     # 文字列

   # ❌ 間違い
   temperature: "0.7"        # 文字列（数字である必要がある）
   max_tokens: "2048"        # 文字列（整数である必要がある）
   ```

2. **温度**：0.0～1.0の間である必要があります
3. **最大トークン**：正の整数である必要があります（通常：512-4096）

---

### 「YAMLの構文エラー」

**症状：**
```
Error: Failed to parse YAML at line 25: unexpected indent
```

**解決方法：**

1. **インデントを確認**（YAMLは厳密です）：
   ```yaml
   # ✅ 正しい - 一貫した2スペースインデント
   model:
     provider: "anthropic"
     name: "claude-3-5-sonnet-20241022"

   # ❌ 間違い - 一貫性のないインデント
   model:
    provider: "anthropic"
     name: "claude-3-5-sonnet-20241022"
   ```

2. **タブなし** - スペースのみを使用：
   ```bash
   # タブをチェック
   grep -P '\t' app.dsl.yml
   # （何も返されないはず）
   ```

3. **YAMLバリデーターを使用**：
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('app.dsl.yml'))"
   ```

4. **YAMLの一般的な問題**：
   - キーの後にコロンが見当たらない
   - 引用符が正しく閉じられていない
   - `-`で始まるリストが適切にインデントされていない

---

## テスト実行の問題

### 「テストが予期しないフォーマットを返した」

**症状：**
```
Test ran successfully but output format is wrong
```

**解決方法：**

1. **system_prompt**が出力フォーマットを指定しているか確認：
   ```yaml
   system_prompt: |
     Return responses in JSON format:
     {
       "answer": "...",
       "confidence": "high|medium|low"
     }
   ```

2. **最初にシンプルな入力でテスト**：
   - 複雑なケースの前に、基本的な入力でテスト
   - アプリが基本的なリクエストを理解していることを確認

3. **prompt_variables**が正しく渡されているか確認：
   ```yaml
   prompt_variables:
     - variable_name: "output_format"
       type: "string"
   ```

---

### 「テストから出力がない」または「空の応答」

**症状：**
```
Test execution completed but result is empty
```

**解決方法：**

1. **APIキーが有効か確認**：
   ```bash
   docker compose run --rm dify-creator login
   ```

2. **モデルが利用可能か確認**：
   - モデル名を確認：`claude-3-5-sonnet-20241022`または最新
   - アカウントがこのモデルへのアクセス権を持っていることを確認

3. **`examples/inputs.json`内の入力パラメーターを確認**：
   ```json
   {
     "input_text": "your test input here"
   }
   ```

4. **完全なエラーログを確認**：
   ```bash
   cat artifacts/run_result.json
   ```

---

### 「テスト中にアプリがタイムアウトした」

**症状：**
```
Error: Test execution timed out after 30 seconds
```

**解決方法：**

1. **最大トークンを削減**：
   ```yaml
   model:
     max_tokens: 1024  # 2048から削減
   ```

2. **プロンプトをシンプル化**：
   - 不必要な指示を削除
   - system_promptをよりコンパクトに

3. **ワークフロー内の無限ループをチェック**：
   - 条件分岐に終了条件があることを確認
   - 循環ノード参照がないこと

4. **遅いAPI統合の場合**：
   - 設定でタイムアウトを増やす（利用可能な場合）
   - より高速なエンドポイントでテスト

---

## ワークフロー固有の問題

### 「ノードが見つかりません」エラー

**症状：**
```
Error: Reference to undefined node 'process_step'
```

**解決方法：**

1. **ノードID表記を確認**（大文字小文字を区別）：
   ```yaml
   nodes:
     - id: "process_step"    # Define first
       type: "llm"

     - id: "next_step"
       input:
         data: "${process_step.output}"  # Correct reference
   ```

2. **すべてのノードIDがユニークであることを確認**：
   ```bash
   grep "id:" app.dsl.yml | sort | uniq -d
   # （すべてがユニークな場合は何も返されない）
   ```

---

### 「変数参照が無効です」

**症状：**
```
Error: Undefined variable reference: ${unknown_var.output}
```

**解決方法：**

1. **変数プール**が変数を定義しているか確認：
   ```yaml
   workflow:
     variable_pool:
       - variable_name: "user_input"
         type: "string"
   ```

2. **ノード出力変数を確認**：
   ```yaml
   nodes:
     - id: "my_step"
       type: "llm"
       # 出力を持つ...

   # 後の参照：
   input: "${my_step.output}"  # 正しい
   ```

3. **一般的なミス**：
   ```yaml
   # ❌ 間違い - 定義されていないノード
   value: "${undefined_node.output}"

   # ❌ 間違い - ノードは存在するが出力に誤字
   value: "${my_node.result}"  # .outputであるべき

   # ✅ 正しい
   value: "${my_node.output}"
   ```

---

## モデル設定の問題

### 「モデルが利用不可」または「クォータを超過」

**症状：**
```
Error: Model claude-3-5-sonnet-20241022 not available
Error: Rate limit exceeded
```

**解決方法：**

1. **利用可能なモデルを確認**：
   - Difyコンソールにアクセスして、アカウントがどのモデルにアクセスできるか確認
   - `model.name`を利用可能なモデルに更新

2. **クォータを超過した場合**：
   - 再試行する前に待つ
   - `max_tokens`を削減してリソース使用量を減らす
   - アカウント使用制限を確認

---

### 「応答が矛盾している」または「品質が変動する」

**解決方法：**

1. **一貫性を高めるため温度を下げる**：
   ```yaml
   model:
     temperature: 0.3  # More consistent than 0.7
   ```

2. **system_promptに具体的な制約を追加**：
   ```yaml
   system_prompt: |
     これらのルールに常に従う：
     1. 正確なフォーマットを提供：[A]、[B]、[C]
     2. 余分な説明なし
     3. 不確実な場合は「不明」と言う
   ```

3. **動的コンテンツに prompt_variables を使用**：
   ```yaml
   prompt_variables:
     - variable_name: "tone"
       type: "string"

   system_prompt: "Respond with {tone} tone: ..."
   ```

---

## アップロード問題

### 「アップロード失敗：app_idが見つかりません」

**症状：**
```
Error: App with ID 'abc123' not found
```

**解決方法：**

1. **app_idを確認**：
   - Dify web：`https://cloud.dify.ai/app/YOUR_APP_ID/...`
   - 正しいですか？

2. **アプリがまだ存在するか確認**：
   - Difyウェブコンソールにログイン
   - アプリリストでアプリを探す
   - 誤って削除された可能性があります

3. **正しいフォーマットを使用**：
   - app_idは英数字である必要があります
   - 余分なスペースや文字がない

---

### 「アップロード失敗：アクセス許可が拒否されました」

**症状：**
```
Error: Permission denied. You don't have access to this app.
```

**解決方法：**

1. **アプリを所有していることを確認**：
   - 正しいユーザーとしてログインしていますか？
   - Difyコンソールをチェックしてアプリを所有していることを確認

2. **アカウントステータスを確認**：
   - Difyアカウントはアクティブですか？
   - ロックアウトされていませんか？

3. **`.env`の認証情報**がアプリを所有するアカウントと一致することを確認

---

## 一般的なトラブルシューティングチェックリスト

**問題を報告する前に確認：**

```
接続と認証：
- [ ] インターネット接続が機能している
- [ ] .envが正しい認証情報を持っている
- [ ] ログインテストが成功：docker compose run --rm dify-creator login
- [ ] cloud.dify.aiまたは自己ホスト版の正しいURLを使用

設定：
- [ ] YAMLが検証済み：docker compose run --rm dify-creator validate --dsl app.dsl.yml
- [ ] 必須フィールドが存在（version、kind、app、mode）
- [ ] YAMLにインデント/構文エラーがない
- [ ] すべてのノードIDがユニーク
- [ ] すべての変数参照が存在

実行：
- [ ] examples/inputs.json内のテスト入力が有効
- [ ] モデルがアカウントで利用可能
- [ ] APIキー/認証情報が期限切れでない
- [ ] タイムアウト問題がない（max_tokensとプロンプトを確認）
```

---

## さらにヘルプを得る

**問題が解決しない場合：**

1. **診断情報を収集**：
   ```bash
   # 検証エラーを表示
   docker compose run --rm dify-creator validate --dsl app.dsl.yml

   # テスト結果の詳細を表示
   cat artifacts/run_result.json | python3 -m json.tool
   ```

2. **最近の変更を確認**：
   - 最後の正常な実行以降に何が変更されましたか？
   - 動作するバージョンに戻すことができますか？

3. **最小限の例を試す**：
   - 最もシンプルなテンプレート（テンプレート1または2）で開始
   - 動作しますか？
   - 徐々に複雑さを追加

4. **Claudeに助けを求める**：
   - エラーメッセージと関連するYAMLセクションを共有
   - 何をしようとしているのかを説明
   - 再現手順を含める

---

## 予防のヒント

✅ **すべきこと：**
- 変更後毎回検証
- 最初にシンプルな入力でテスト
- プロンプトは簡潔明確に
- テンプレートを出発点として使用
- 動作するバージョンをgitにコミット
- ライブアプリを更新する前にローカルでテスト

❌ **してはいけないこと：**
- 検証せずに複数の変更を行う
- アップロード前に検証をスキップ
- 構文を確認せずにYAMLをコピー&ペースト
- 一貫性のないインデントを使用
- エッジケースでのみテスト
- ローカルでのテストなしにアップロード
